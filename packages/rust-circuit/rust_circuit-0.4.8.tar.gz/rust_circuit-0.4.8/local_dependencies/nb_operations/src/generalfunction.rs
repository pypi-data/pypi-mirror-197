use anyhow::{anyhow, bail, Context, Result};
use circuit_base::{generalfunction::*, Array, GeneralFunctionSpec};
use pyo3::{prelude::*, types::PyTuple};
use rand::{self, Rng};
use rr_util::{
    py_types::{assert_tensors_close, ExtraPySelfOps, Tensor},
    shape::{shape_is_known, shape_join_eq, Shape, Size},
};
use smallvec::ToSmallVec;

/// I now think this maybe should have been written in python.
/// Not to bad to port I guess...
#[pyclass]
pub struct GeneralFunctionSpecTester {
    #[pyo3(set, get)]
    pub samples_per_batch_dims: usize,
    #[pyo3(set, get)]
    pub base_shapes_samples: usize,
    #[pyo3(set, get)]
    pub min_frac_successful: f64,
    #[pyo3(set, get)]
    pub min_frac_checked_batch: f64,
    #[pyo3(set, get)]
    pub start_num_inputs: usize,
    #[pyo3(set, get)]
    pub end_num_inputs: usize,
    #[pyo3(set, get)]
    pub start_ndim: usize,
    #[pyo3(set, get)]
    pub end_ndim: usize,
    #[pyo3(set, get)]
    pub start_shape_num: usize,
    #[pyo3(set, get)]
    pub end_shape_num: usize,
    #[pyo3(set, get)]
    pub test_with_rand: bool,
    #[pyo3(set, get)]
    pub randn_size_cap: usize,
}

impl Default for GeneralFunctionSpecTester {
    fn default() -> Self {
        Self {
            samples_per_batch_dims: 3,
            base_shapes_samples: 100,
            min_frac_successful: 0.1,
            min_frac_checked_batch: 0.1,
            start_num_inputs: 0,
            end_num_inputs: 5,
            start_ndim: 0,
            end_ndim: 10,
            start_shape_num: 0,
            end_shape_num: 10,
            test_with_rand: true,
            randn_size_cap: 1024 * 16,
        }
    }
}

fn gen_size_in(rng: &mut impl Rng, start: usize, end: usize) -> Size {
    if rng.gen_bool(0.01) {
        Size::NONE
    } else {
        Size::known(rng.gen_range(start..end))
    }
}

#[pymethods]
impl GeneralFunctionSpecTester {
    #[new]
    #[pyo3(signature=(
        samples_per_batch_dims = GeneralFunctionSpecTester::default().samples_per_batch_dims,
        base_shapes_samples = GeneralFunctionSpecTester::default().base_shapes_samples,
        min_frac_successful = GeneralFunctionSpecTester::default().min_frac_successful,
        min_frac_checked_batch = GeneralFunctionSpecTester::default().min_frac_checked_batch,
        start_num_inputs = GeneralFunctionSpecTester::default().start_num_inputs,
        end_num_inputs = GeneralFunctionSpecTester::default().end_num_inputs,
        start_ndim = GeneralFunctionSpecTester::default().start_ndim,
        end_ndim = GeneralFunctionSpecTester::default().end_ndim,
        start_shape_num = GeneralFunctionSpecTester::default().start_shape_num,
        end_shape_num = GeneralFunctionSpecTester::default().end_shape_num,
        test_with_rand = GeneralFunctionSpecTester::default().test_with_rand,
        randn_size_cap = GeneralFunctionSpecTester::default().randn_size_cap
    ))]
    fn new(
        samples_per_batch_dims: usize,
        base_shapes_samples: usize,
        min_frac_successful: f64,
        min_frac_checked_batch: f64,
        start_num_inputs: usize,
        end_num_inputs: usize,
        start_ndim: usize,
        end_ndim: usize,
        start_shape_num: usize,
        end_shape_num: usize,
        test_with_rand: bool,
        randn_size_cap: usize,
    ) -> Self {
        Self {
            samples_per_batch_dims,
            base_shapes_samples,
            min_frac_successful,
            min_frac_checked_batch,
            start_num_inputs,
            end_num_inputs,
            start_ndim,
            end_ndim,
            start_shape_num,
            end_shape_num,
            test_with_rand,
            randn_size_cap,
        }
    }

    #[pyo3(signature=(spec, shapes, shapes_must_be_valid = false))]
    pub fn test_from_shapes(
        &self,
        spec: GeneralFunctionSpec,
        shapes: Vec<Shape>,
        shapes_must_be_valid: bool,
    ) -> Result<(bool, bool)> {
        let GeneralFunctionShapeInfo {
            shape,
            num_non_batchable_output_dims,
            input_batchability,
        } = match spec.get_shape_info(&shapes) {
            Ok(info) => info,
            Err(e) => {
                if shapes_must_be_valid {
                    bail!(e.context("was supposed to be valid, but actually wasn't!"))
                }
                return Ok((false, false)); // No tests in case where this is invalid list of shapes
            }
        };

        if num_non_batchable_output_dims as usize > shape.len() {
            bail!(
            "too many non batchable output dims! num_non_batchable_output_dims={} shape.len()={}",
            num_non_batchable_output_dims,
            shape.len()
        );
        }
        if input_batchability.len() != shapes.len() {
            bail!(
                "input batchability len doesn't match! input_batchability.len()={} shapes.len()={}",
                input_batchability.len(),
                shapes.len()
            );
        }

        if input_batchability.iter().all(|x| !*x) {
            // if none batchable, we don't have any tests to run
            return Ok((true, false));
        }
        let current_num_batch_dims = shape.len() - num_non_batchable_output_dims as usize;

        for (shape, &is_batch) in
            std::iter::once((&shape, &true)).chain(shapes.iter().zip(&input_batchability))
        {
            if is_batch && shape.len() < current_num_batch_dims {
                bail!(
                "some batchable shape too short for batch, shape.len()={} current_num_batch_dims={}",
                shape.len(),
                current_num_batch_dims
            );
            }
        }

        shapes.iter().zip(&input_batchability).filter_map(|(s, is_batch)| is_batch.then(|| &s[..current_num_batch_dims]))
            .try_fold(shape[..current_num_batch_dims].to_smallvec(), |a, b| {
                shape_join_eq(&a, b, ||
                anyhow!("inputs and output have non-matching 'batch' shapes, a={a:?} b={b:?} input_shapes={shapes:?} output_shape={shape:?}"))
            })?;

        let mut rng = rand::thread_rng();

        let mut run_sample = |num_batch_dims, random_inputs: bool| {
            let batch_shape: Shape = (0..num_batch_dims)
                .map(|_| gen_size_in(&mut rng, self.start_shape_num, self.end_shape_num))
                .collect();

            let new_shapes: Vec<Shape> = shapes
                .iter()
                .zip(&input_batchability)
                .map(|(s, &is_batch)| {
                    if is_batch {
                        batch_shape
                            .iter()
                            .chain(&s[current_num_batch_dims..])
                            .cloned()
                            .collect()
                    } else {
                        s.clone()
                    }
                })
                .collect();

            let general_info = || {
                format!(
                    "shapes={:?} shape={:?} new_shapes={:?} current_num_batch_dims={}",
                    shapes, shape, new_shapes, current_num_batch_dims
                )
            };

            let new_info = spec.get_shape_info(&new_shapes).with_context(|| {
                format!(
                    "spec isn't consistent, error on valid shapes\n{}",
                    general_info()
                )
            })?;

            let prefix = "spec isn't consistent, ";

            if new_info.num_non_batchable_output_dims != num_non_batchable_output_dims {
                bail!(
                "{}changed num_non_batchable_output_dims when only batching was changed\n{}\n{}",
                prefix,
                format!(
                    "new_info.num_non_batchable_output_dims={} != num_non_batchable_output_dims={}",
                    new_info.num_non_batchable_output_dims, num_non_batchable_output_dims
                ),
                general_info()
            );
            }

            if new_info.input_batchability != input_batchability {
                bail!(
                    "{}changed input_batchability when only batching was changed\n{}\n{}",
                    prefix,
                    format!(
                        "new_info.input_batchability={:?} != input_batchability={:?}",
                        new_info.input_batchability, input_batchability
                    ),
                    general_info()
                );
            }

            let non_batch_shape = &shape[current_num_batch_dims..];
            let expected_shape = batch_shape
                .into_iter()
                .chain(non_batch_shape.iter().cloned())
                .collect::<Shape>();
            if new_info.shape != expected_shape {
                bail!(
                    "{}unexpected shape\n{}\n{}",
                    prefix,
                    format!(
                        "new_info.shape={:?} != expected_shape={:?}",
                        new_info.shape, expected_shape
                    ),
                    general_info()
                );
            }

            let get_count_find = |shapes: &[Shape], shape| {
                shapes
                    .iter()
                    .chain(std::iter::once(shape))
                    .map(|x| x.iter().map(|x| x.t().unwrap_or(1)).product::<usize>())
                    .sum::<usize>()
                    < self.randn_size_cap
            };

            if random_inputs
                && get_count_find(&shapes, &shape)
                && get_count_find(&new_shapes, &new_info.shape)
                && num_batch_dims < current_num_batch_dims
                && shapes.iter().all(|x| shape_is_known(x))
            // only run random on < orig
            {
                // TODO: swap to f64 as needed!
                let tensors: Vec<_> = shapes
                    .iter()
                    .map(|shape| Array::randn(shape.clone()).unwrap().value)
                    .collect();

                let out_tensor = spec
                    .function(&tensors)
                    .context("failed to evaluate for test")?;
                if out_tensor.shape() != &shape {
                    bail!(
                        "{}: unexpected tensor shape\n{}\n{}",
                        spec.name(),
                        format!(
                            "out_tensor.shape={:?} != shape={:?}",
                            out_tensor.shape(),
                            shape
                        ),
                        general_info()
                    );
                }
                let dims_to_remove = current_num_batch_dims - num_batch_dims;
                if shape[..dims_to_remove].iter().any(|x| x.is(0)) {
                    return Ok(());
                }
                let idxs: Py<PyTuple> = Python::with_gil(|py| {
                    PyTuple::new(
                        py,
                        shape[..dims_to_remove]
                            .iter()
                            .map(|s| s.map(|x| rng.gen_range(0..x)).into_py(py)),
                    )
                    .into()
                });
                let run_idx = |tensor: Tensor| tensor.py_getitem_acquire(idxs.clone()).unwrap();

                let new_tensor = spec
                    .function(
                        &tensors
                            .iter()
                            .zip(&input_batchability)
                            .map(|(x, &b)| if b { run_idx(x.clone()) } else { x.clone() })
                            .collect::<Vec<_>>(),
                    )
                    .context("failed to evaluate for test")?;

                let new_tensor_expected_shape: Shape =
                    shape[dims_to_remove..].iter().cloned().collect();
                if new_tensor.shape() != &new_tensor_expected_shape {
                    bail!(
                        "{}: unexpected tensor shape\n{}\n{}",
                        spec.name(),
                        format!(
                            "new_tensor.shape={:?} != expected_shape={:?}",
                            new_tensor.shape(),
                            expected_shape
                        ),
                        general_info()
                    );
                }

                assert_tensors_close(new_tensor, run_idx(out_tensor))
                    .context("tensors not close! (TODO: error)")?
            }

            Ok(())
        };

        for num_batch_dims in 0..current_num_batch_dims + 5 {
            for _ in 0..self.samples_per_batch_dims {
                run_sample(num_batch_dims, false)?;
            }
            run_sample(num_batch_dims, self.test_with_rand)?;
        }

        Ok((true, true))
    }

    pub fn test_many_shapes(&self, spec: GeneralFunctionSpec) -> Result<()> {
        let mut rng = rand::thread_rng();
        let mut any_frac_successful = false;
        let mut any_frac_checked_batch = false;
        let num_inputs_range = self.start_num_inputs..self.end_num_inputs;
        for num_inputs in num_inputs_range.clone() {
            let mut total_successful = 0.;
            let mut total_checked_batch = 0.;
            for _ in 0..self.base_shapes_samples {
                let shapes = (0..num_inputs)
                    .map(|_| {
                        let ndim = rng.gen_range(self.start_ndim..self.end_ndim);
                        (0..ndim)
                            .map(|_| {
                                gen_size_in(&mut rng, self.start_shape_num, self.end_shape_num)
                            })
                            .collect()
                    })
                    .collect();

                let (was_successful, and_checked_batch) =
                    self.test_from_shapes(spec.clone(), shapes, false)?;
                total_successful += if was_successful { 1. } else { 0. };
                total_checked_batch += if and_checked_batch { 1. } else { 0. };
            }

            let frac_successful = total_successful / self.base_shapes_samples as f64;
            let frac_checked_batch = total_checked_batch / self.base_shapes_samples as f64;

            any_frac_successful =
                any_frac_successful || frac_successful >= self.min_frac_successful;
            any_frac_checked_batch =
                any_frac_checked_batch || frac_checked_batch >= self.min_frac_checked_batch;
        }

        if !num_inputs_range.is_empty() {
            if !any_frac_successful {
                bail!(
                    "frac successful too low\n{}\n{}",
                    "perhaps your function is too hard to automatically generate shapes for?",
                    "You can lower self.min_frac_successful to get this too pass, but you might not be testing very well"
                );
            }
            if !any_frac_checked_batch {
                bail!(
                    "frac check batch too low\n{}\n{}{}",
                    "perhaps your function is too hard to automatically generate batchable shapes for?",
                    "You can lower self.min_frac_checked_batch to get this too pass",
                    " (and you should set it to 0. if the function never supports batching)"
                );
            }
        }

        Ok(())
    }
}

#[test]
fn test_simple_general_function() -> Result<()> {
    pyo3::prepare_freethreaded_python();

    let tester = GeneralFunctionSpecTester {
        samples_per_batch_dims: 5,
        base_shapes_samples: 800,
        start_num_inputs: 0,
        end_num_inputs: 3,
        start_ndim: 0,
        end_ndim: 5,
        test_with_rand: false,
        ..Default::default()
    };

    for num_non_batchable_output_dims in 0..2 {
        for removed_from_end in 0..2 {
            let spec = GeneralFunctionSimpleSpec {
                name: "".into(),
                num_non_batchable_output_dims,
                removed_from_end,
            }
            .into();
            tester.test_many_shapes(spec)?;
        }
    }
    // // TODO: this segfaults in pytorch and I can't seem to fix :/
    // // Note that tests work in python, so it must be something with
    // // prepare_freethreaded_python.
    // let tester_rand = GeneralFunctionSpecTester {
    //     test_with_rand: true,
    //     start_shape_num: 1,
    //     ..tester
    // };

    // for spec in SPECS.values() {
    //     tester_rand.test_many_shapes(spec.clone())?;
    // }

    Ok(())
}

#[test]
fn test_index_general_function() -> Result<()> {
    let tester = GeneralFunctionSpecTester {
        samples_per_batch_dims: 5,
        base_shapes_samples: 800,
        start_num_inputs: 1,
        end_num_inputs: 4,
        start_ndim: 0,
        end_ndim: 5,
        test_with_rand: false,
        ..Default::default()
    };

    let mut rng = rand::thread_rng();
    for index_dim in -2..2 {
        for batch_x in [false, true] {
            for batch_index in [false, true] {
                let spec = GeneralFunctionIndexSpec {
                    index_dim,
                    batch_x,
                    batch_index,
                    check_index_ints: true,
                }
                .into();
                if !batch_index && index_dim >= 0 {
                    continue;
                }
                if !batch_x && !batch_index {
                    continue;
                }
                tester.test_many_shapes(spec)?;
            }
        }

        let spec: GeneralFunctionSpec = GeneralFunctionIndexSpec {
            index_dim,
            batch_x: true,
            batch_index: true,
            check_index_ints: true,
        }
        .into();
        for _ in 0..800 {
            let min_suffix_ndim = if index_dim < 0 {
                index_dim.abs()
            } else {
                index_dim + 1
            } as usize;
            let [prefix_shape, suffix_shape]: [Shape; 2] = [0, min_suffix_ndim]
                .into_iter()
                .map(|min_dims| {
                    let ndim = rng.gen_range(tester.start_ndim.max(min_dims)..tester.end_ndim);
                    (0..ndim)
                        .map(|_| {
                            gen_size_in(&mut rng, tester.start_shape_num, tester.end_shape_num)
                        })
                        .collect()
                })
                .collect::<Vec<_>>()
                .try_into()
                .unwrap();
            assert!(suffix_shape.len() >= min_suffix_ndim);

            let x_shape: Shape = prefix_shape
                .iter()
                .cloned()
                .chain(suffix_shape.iter().cloned())
                .collect();
            let index_shape = prefix_shape.clone();

            tester
                .test_from_shapes(
                    spec.clone(),
                    vec![x_shape.clone(), index_shape.clone()],
                    true,
                )
                .with_context(|| {
                    format!(
                        "fail with x_shape={:?} index_shape={:?} suffix_shape={:?} index_dim={}",
                        x_shape, index_shape, suffix_shape, index_dim
                    )
                })?;
        }
    }

    Ok(())
}
