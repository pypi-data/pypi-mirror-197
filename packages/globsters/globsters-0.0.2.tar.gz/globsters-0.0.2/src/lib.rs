use pyo3::prelude::*;
// use pyo3::types::{PyDict, PyTuple};
// use globset::Glob;
use globset::GlobBuilder;
// use globset::GlobMatcher;

#[pyclass]
pub struct Globster {
    globset: globset::GlobSet,
    negative: bool,
}

// Could be replaced by 2 Globster objects (one for positive, one for negative)
#[pyclass]
pub struct Globsters {
    globset: globset::GlobSet,
    nglobset: globset::GlobSet,
}

#[pymethods]
impl Globster {
    #[new]
    #[pyo3(signature = (pattern, case_insensitive=false))]
    fn __new__(pattern: String, case_insensitive: Option<bool>) -> Self {
        case_insensitive.unwrap_or(false);
        let mut builder = globset::GlobSetBuilder::new();
        let string_pattern = pattern.trim_start_matches('!');
        let mut glob_builder = GlobBuilder::new(string_pattern);
        if case_insensitive.unwrap_or(false) {
            glob_builder.case_insensitive(true);
        }
        let built_glob_result = glob_builder.build();
        match built_glob_result {
            Ok(glob) => {
                builder.add(glob);
            }
            Err(e) => panic!("Error building glob: {}", e),
        }
        let negative = pattern.starts_with('!');
        let globset = builder.build().unwrap();
        Self { globset, negative }
    }

    fn is_match(&self, string: String) -> bool {
        self.globset.is_match(string.as_str())
    }

    fn __call__(&self, string: String) -> PyResult<bool> {
        let is_match = self.globset.is_match(string.as_str());
        Ok(is_match ^ self.negative)
    }
}

#[pymethods]
impl Globsters {
    #[new]
    #[pyo3(signature = (patterns, case_insensitive=false))]
    fn __new__(patterns: Vec<String>, case_insensitive: Option<bool>) -> Self {
        case_insensitive.unwrap_or(false);
        let mut builder = globset::GlobSetBuilder::new();
        let mut nglob_builder = globset::GlobSetBuilder::new();
        for pattern in patterns {
            if pattern.starts_with('!') {
                let string_pattern = pattern.trim_start_matches('!');
                let mut glob_builder = GlobBuilder::new(string_pattern);
                if case_insensitive.unwrap_or(false) {
                    glob_builder.case_insensitive(true);
                }
                let built_glob_result = glob_builder.build();
                match built_glob_result {
                    Ok(glob) => {
                        nglob_builder.add(glob);
                    }
                    Err(e) => panic!("Error building glob: {}", e),
                }
            } else {
                let mut glob_builder = GlobBuilder::new(pattern.as_str());
                if case_insensitive.unwrap_or(false) {
                    glob_builder.case_insensitive(true);
                }
                let built_glob_result = glob_builder.build();
                match built_glob_result {
                    Ok(glob) => {
                        builder.add(glob);
                    }
                    Err(e) => panic!("Error building glob: {}", e),
                }
            }
        }
        let globset = builder.build().unwrap();
        let nglobset = nglob_builder.build().unwrap();
        Globsters { globset, nglobset }
    }

    fn is_match(&self, string: String) -> bool {
        if self.nglobset.is_match(string.as_str()) {
            return false;
        }
        self.globset.is_match(string.as_str())
    }

    fn is_not_match(&self, string: String) -> bool {
        if self.nglobset.is_empty() {
            return false;
        }
        self.nglobset.is_match(string.as_str())
    }

    fn __call__(&self, string: String) -> PyResult<bool> {
        let is_negative_match = self.nglobset.is_match(string.as_str());
        if is_negative_match {
            return Ok(false);
        }
        let is_match = self.globset.is_match(string.as_str());

        Ok(is_match)
    }
}

#[pyfunction]
fn bslash2fslash(string: String) -> String {
    string.replace("\\", "/")
}

#[pyfunction]
fn fslash2bslash(string: String) -> String {
    string.replace("/", "\\")
}

/// A Python module implemented in Rust.
#[pymodule]
fn globsters(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add("__version_lib__", env!("CARGO_PKG_VERSION"))?;
    m.add_function(wrap_pyfunction!(bslash2fslash, m)?)?;
    m.add_function(wrap_pyfunction!(fslash2bslash, m)?)?;
    m.add_class::<Globster>()?;
    m.add_class::<Globsters>()?;
    Ok(())
}
