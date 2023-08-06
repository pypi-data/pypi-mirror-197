use std::{fmt, fmt::Write, hash::Hash, ops::Deref};

use anyhow::{anyhow, Result};
use num_bigint::BigUint;
use once_cell::sync::Lazy;
use pyo3::prelude::*;
use rustc_hash::FxHashMap as HashMap;

// see also circuit_print::print
const BAR: &str = "│";
const TEE: &str = "├";
const ARROW: &str = "‣";
const UP_ELBOW: &str = "└";

pub fn color(string: &str, color_int: CliColor) -> String {
    if let Some(color_int) = color_int.0 {
        return format!(
            "\u{001b}[{}m{}\u{001b}[0m",
            COLOR_CODES[color_int % COLOR_CODES.len()],
            string
        );
    }
    string.to_owned()
}

// TODO: improve color scheme
const COLOR_CODES: [usize; 14] = [31, 32, 33, 34, 35, 36, 90, 91, 92, 93, 94, 95, 96, 97];
static NAME_TO_COLOR: Lazy<HashMap<String, usize>> = Lazy::new(|| {
    HashMap::from_iter(
        [
            ("Red", 0),
            ("Green", 1),
            ("Yellow", 2),
            ("Blue", 3),
            ("Magenta", 4),
            ("Cyan", 5),
            ("White", 6),
        ]
        .into_iter()
        .map(|(a, b)| (a.to_owned(), b)),
    )
});
static COLOR_TO_NAME: Lazy<HashMap<usize, String>> =
    Lazy::new(|| NAME_TO_COLOR.iter().map(|(a, b)| (*b, a.clone())).collect());

#[derive(Clone, Copy, Hash, PartialEq, Eq, PartialOrd, Ord)]
pub struct CliColor(pub Option<usize>);

impl CliColor {
    pub const NONE: Self = CliColor(None);
    pub fn from_string(string: String) -> Result<CliColor> {
        NAME_TO_COLOR
            .get(&string)
            .ok_or_else(|| anyhow!("unknown color name {}", string))
            .map(|x| CliColor(Some(*x)))
    }
    pub fn new(int: usize) -> Self {
        CliColor(Some(int % COLOR_CODES.len()))
    }
    pub fn start_str(&self) -> String {
        if let Some(c) = self.0 {
            format!("\u{001b}[{}m", COLOR_CODES[c % COLOR_CODES.len()])
        } else {
            "".to_owned()
        }
    }
    pub fn is_some(&self) -> bool {
        self.0.is_some()
    }
}
impl<'source> FromPyObject<'source> for CliColor {
    fn extract(circuit_obj: &'source PyAny) -> PyResult<Self> {
        {
            if circuit_obj.is_none() {
                return Ok(CliColor(None));
            }
            circuit_obj
                .extract::<Option<usize>>()
                .map(CliColor)
                .or_else(|_e| CliColor::from_string(circuit_obj.extract()?))
                .map_err(|e| e.into())
        }
    }
}

impl IntoPy<PyObject> for CliColor {
    fn into_py(self, py: Python<'_>) -> PyObject {
        {
            self.0.into_py(py)
        }
    }
}

impl From<Option<CliColor>> for CliColor {
    fn from(value: Option<CliColor>) -> Self {
        match value {
            None => CliColor::NONE,
            Some(x) => x,
        }
    }
}

impl Deref for CliColor {
    type Target = Option<usize>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl std::fmt::Display for CliColor {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        if let Some(s) = self.0 {
            if let Some(ctn) = COLOR_TO_NAME.get(&s) {
                write!(f, "{}", ctn)
            } else {
                write!(f, "{}", s)
            }
        } else {
            write!(f, "None")
        }
    }
}

pub fn last_child_arrows(last_child: &Vec<bool>, is_output: bool, arrows: bool) -> String {
    if !arrows {
        return "  ".repeat(last_child.len());
    }
    let depth = last_child.len();
    let mut result = "".to_owned();
    for i in 0..depth.saturating_sub(1) {
        result.push_str(if last_child[i] { " " } else { BAR });
        result.push(' ');
    }
    if depth > 0 {
        if is_output {
            result.push_str(if *last_child.last().unwrap() {
                UP_ELBOW
            } else {
                TEE
            });
            result.push_str(ARROW);
        } else {
            write!(
                result,
                "{} ",
                if !last_child[depth - 1] { BAR } else { " " }
            )
            .unwrap();
        }
    }
    result
}

#[macro_export]
macro_rules! clicolor {
    ($name:ident) => {
        CliColor::from_string(stringify!($name).to_owned()).unwrap()
    };
}

#[pyfunction]
#[pyo3(name = "oom_fmt")]
pub fn oom_fmt_py(t: BigUint) -> String {
    oom_fmt(t)
}

pub fn oom_fmt<T: Into<BigUint>>(num: T) -> String {
    let mut num: BigUint = num.into();
    let k = BigUint::from(1000usize);
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"].iter() {
        if num < k {
            return format!("{}{}", num, unit);
        }
        num /= &k;
    }
    format!("{}Y", num)
}
