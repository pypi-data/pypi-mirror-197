use pyo3::prelude::*;
use pyo3::types::PyList;
use num_cpus;
mod op;
use op::infer::RustInferenceEngine;
use op::reduce::reduce;
mod schema;
use schema::top::RustJsonSchema;
use schema::atomic::atomic::{Non, Str, Bool, Atomic};
use schema::atomic::num::{Float, Int};
use schema::record::{Record, FieldSet, UniformRecord};
use schema::array::{Array};
use schema::unions::{Union, Optional};
use schema::unknown::Unknown;
use schema::convert::py2rust;
//////////////////// Reduce Merge of Json Schemas ///////////////////////
#[pyclass]
struct InferenceEngine {
    rust_obj: RustInferenceEngine
}
// 
#[pymethods]
impl InferenceEngine {
    #[new]
    fn new(cpu_cnt: Option<i32>) -> PyResult<Self> {
        let set_cnt = match cpu_cnt {
            Some(val) => val as usize,
            _ => num_cpus::get()
        };
        println!("Thread Count: {}", set_cnt);
        Ok(InferenceEngine { rust_obj: RustInferenceEngine::new(set_cnt)})
    }
    fn run(&self, batch: &PyList) -> String {
        let vec: Vec<&str> = (0..batch.len())
            .map(|i| batch.get_item(i).unwrap().extract::<&str>().unwrap())
            .collect();
        self.rust_obj.infer(vec)
    }
    fn reduce(&self, batch: &PyList) -> String {
        let s_vec: Vec<RustJsonSchema> = (0..batch.len())
            .map(|i| batch.get_item(i).unwrap().extract::<&PyAny>().unwrap())
            .map(|s| py2rust(s))
            .collect();
        reduce(s_vec).repr()
    }
}
#[pymodule]
fn jskiner( _py: Python, m: &PyModule ) -> PyResult<()> {
    m.add_class::<InferenceEngine>()?;
    m.add_class::<Int>()?;
    m.add_class::<Float>()?;
    m.add_class::<Str>()?;
    m.add_class::<Non>()?;
    m.add_class::<Bool>()?;
    m.add_class::<Atomic>()?;
    m.add_class::<Array>()?;
    m.add_class::<Record>()?;
    m.add_class::<FieldSet>()?;
    m.add_class::<UniformRecord>()?;
    m.add_class::<Union>()?;
    m.add_class::<Optional>()?;
    m.add_class::<Unknown>()?;
    return Ok( () );
}