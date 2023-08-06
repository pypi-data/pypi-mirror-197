use pyo3::{
    exceptions::PyException, pyclass, pymethods, types::PyModule, Py, PyErr, PyObject, PyResult,
    Python,
};

// TODO: remove when/if we drop 3.11 support
#[pyclass(extends=PyException)]
pub struct ExceptionWithRustContext {
    #[pyo3(get)]
    exc: PyObject,
    context: anyhow::Error,
}

#[pymethods]
impl ExceptionWithRustContext {
    fn __str__(&self) -> PyResult<String> {
        Python::with_gil(|_py| {
            let ctx = &self.context;
            Ok(format!("{ctx:?}\n(this is an ExceptionWithRustContext, access e.exc or upgrade to 3.11 to get the underlying exception)\n"))
        })
    }
}

pub struct ErrorInfo {
    pub try_to_py_err: fn(&(dyn std::error::Error + 'static), s: &str) -> Option<PyErr>,
    pub register: fn(Python<'_>, &PyModule) -> PyResult<()>,
    pub print_stub: fn(Python<'_>) -> PyResult<String>,
}
inventory::collect!(ErrorInfo);

pub fn register_exceptions(py: Python<'_>, m: &PyModule) -> PyResult<()> {
    for x in inventory::iter::<ErrorInfo> {
        (x.register)(py, m)?;
    }
    Ok(())
}

pub fn anyhow_to_py_err(err: anyhow::Error) -> PyErr {
    let root_cause = err.root_cause();
    let s = format!("{:?}", err);
    for x in inventory::iter::<ErrorInfo> {
        if let Some(r) = (x.try_to_py_err)(root_cause, &s) {
            return r;
        }
    }

    pyo3::anyhow::anyhow_to_py_err(err, |py, e, ctx| {
        PyErr::from_value(
            Py::new(
                py,
                ExceptionWithRustContext {
                    exc: e.into_value(py).into(),
                    context: ctx,
                },
            )
            .unwrap()
            .as_ref(py),
        )
    })
}

pub fn print_exception_stubs(py: Python<'_>) -> PyResult<String> {
    itertools::process_results(
        (inventory::iter::<ErrorInfo>)
            .into_iter()
            .map(|x| (x.print_stub)(py)),
        |it| it.intersperse("\n".to_string()).collect(),
    )
}

#[macro_export]
macro_rules! python_error_exception {
    (
        #[base_error_name($e_name:ident)]
        #[base_exception($base_ty:ty)]
        // #[error_py_description($desc:literal)]
        $( #[$($meta_tt:tt)*] )*
        $vis:vis enum $name:ident {
            $(
                #[error($($error_tt:tt)*)]
                $(#[$($meta_tt_item:tt)*])*
                $err_name:ident {
                    $(
                        $arg:ident : $arg_ty:ty
                    ),*
                    $(,)?
                },
            )*
        }
    ) => {
        $( #[$($meta_tt)*] )*
        $vis enum $name {
            $(
                #[error($($error_tt)*, e_name = format!("{}{}Error", stringify!($e_name), stringify!($err_name)))]
                $(#[$($meta_tt_item)*])*
                $err_name {
                    $(
                        $arg : $arg_ty,
                    )*
                },
            )*
        }

        paste::paste! {
            type [<__ $name BaseExcept>] = $base_ty;


            $(
                #[pyo3::prelude::pyclass]
                struct [<$e_name $err_name Info>] {
                    #[pyo3(get)]
                    err_msg_string : String,
                    $(
                        #[pyo3(get)]
                        $arg : $arg_ty,
                    )*
                }

                #[pyo3::prelude::pymethods]
                impl [<$e_name $err_name Info>] {
                    fn __repr__(&self) -> &str {
                        &self.err_msg_string
                    }

                    fn items(&self) -> pyo3::Py<pyo3::types::PyDict> {
                        Python::with_gil(|py| {
                            let dict = pyo3::types::PyDict::new(py);
                            $(
                                dict.set_item::<&str, PyObject>(stringify!($arg), self.$arg.clone().into_py(py)).unwrap();
                            )*
                            dict.into()
                        })
                    }
                }
            )*


            mod [< __ $name:snake _python_exception_stuff>] {
                $(
                use super::[<$e_name $err_name Info>];
                )*
                $crate::python_error_exception! {
                    @in_mod $vis $name {
                        $(
                            $err_name [[<$e_name $err_name Error>]] [[<$e_name $err_name Info>]] {
                                $(
                                    $arg : $arg_ty,
                                )*
                            },
                        )*
                    }
                    ([<$e_name Error>] super::[<__ $name BaseExcept>]
                     // $desc
                     )
                }
            }

            #[allow(dead_code)]
            $vis type [<Py $e_name Error>] = [< __ $name:snake _python_exception_stuff>]::[<$e_name Error>];
            $(
            #[allow(dead_code)]
            $vis type  [<Py $e_name $err_name Error>] = [< __ $name:snake _python_exception_stuff>]::[<$e_name $err_name Error>];
            )*
        }
    };
    (@op_name [] $name:ident) => {
        $name
    };
    (@op_name [$e_name:ident] $name:ident) => {
        paste::paste! {
            [<$e_name Error>]
        }
    };
    (
        @in_mod $vis:vis $name:ident {
            $(
                $err_name:ident [$sub_excep_name:ident] [$sub_excep_info_name:ident] {
                    $(
                        $arg:ident : $arg_ty:ty,
                    )*
                },
            )*
        }
        ($excep_name:ident $base_ty:ty
         // $desc:literal
         )
    ) => {
        use pyo3::{
            create_exception, types::PyModule, PyErr, PyResult, PyTypeInfo, Python,
        };

        use $crate::errors_util::ErrorInfo;

        create_exception!(
            rust_circuit,
            $excep_name,
            $base_ty
            //, $desc
        );
        $(
            create_exception!(
                rust_circuit,
                $sub_excep_name,
                $excep_name
            );
        )*

        paste::paste!{
            fn [<register_ $name:snake>](py: Python<'_>, m: &PyModule) -> PyResult<()> {
                m.add(
                    stringify!($excep_name),
                    py.get_type::<$excep_name>(),
                )?;
                $(
                    m.add(
                        stringify!($sub_excep_name),
                        py.get_type::<$sub_excep_name>(),
                    )?;
                    m.add_class::<$sub_excep_info_name>()?;
                )*

                Ok(())
            }

            fn [<print_stub_ $name:snake>](py : Python<'_>) -> PyResult<String> {
                let out = [
                    format!("class {}({}): ...", $excep_name::NAME, <$base_ty>::type_object(py).name()?),
                    $(
                        format!("class {}({}): ...", $sub_excep_name::NAME, $excep_name::NAME),
                    )*
                ].join("\n");
                Ok(out)
            }

            fn [<get_py_err_ $name:snake>](x: &super::$name, err_msg_string: String) -> pyo3::PyErr {
                use super::$name::*;
                match x {
                    $(
                        $err_name { $($arg,)* } => {
                            PyErr::new::<$sub_excep_name, _>($sub_excep_info_name { err_msg_string, $($arg : $arg.clone(),)* })
                        },
                    )*
                }
            }

            inventory::submit! {
                ErrorInfo {
                    try_to_py_err: |err, s| {
                        err.downcast_ref::<super::$name>().map(|x| [<get_py_err_ $name:snake>](x, s.to_owned()))
                    },
                    register: [<register_ $name:snake>],
                    print_stub: [<print_stub_ $name:snake>],
                }
            }
        }
    }
}
