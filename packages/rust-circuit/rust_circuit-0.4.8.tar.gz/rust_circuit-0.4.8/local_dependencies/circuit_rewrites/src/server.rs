use pyo3::prelude::*;
use rr_util::{lru_cache::TensorCacheRrfs, py_types::PY_UTILS, pycall, tensor_util::TorchDtype};
use tiny_http::{Response, Server};

use crate::scheduled_execution::Schedule;

#[pyfunction]
pub fn circuit_server_serve(my_url: String, tensor_cache: Option<TensorCacheRrfs>) {
    let server = Server::http(&my_url).unwrap();
    let mut tensor_cache = tensor_cache;
    println!("Starting circuit server on {}", &my_url);
    for mut request in server.incoming_requests() {
        let mut buf: Vec<u8> = vec![0; request.body_length().unwrap()];
        request.as_reader().read_exact(&mut buf).unwrap();
        let msg_string = String::from_utf8(buf).unwrap();
        println!("got {}", msg_string);
        let thingy = Schedule::deserialize(msg_string, &mut tensor_cache).unwrap();
        let result_tensors = thingy.evaluate_many(Default::default()).unwrap();
        let mut bytes: Vec<u8> = vec![];
        const _: () = assert!(std::mem::size_of::<TorchDtype>() == 1);
        for x in &result_tensors {
            let tensor_bytes: Vec<u8> = pycall!(PY_UTILS.tensor_to_bytes, (x,));
            bytes.extend(tensor_bytes.len().to_le_bytes());
            bytes.extend(
                &unsafe { std::mem::transmute::<TorchDtype, [u8; 1]>(x.device_dtype().dtype) }[..],
            );
            bytes.extend(tensor_bytes);
        }
        println!("bytes {:?} len {}", bytes.get(..1), bytes.len());
        // let result_key = save_tensor_rrfs(result_tensor).ok()?;
        // let response = Response::from_string(result_key);
        let response = Response::from_data(bytes);
        request.respond(response).unwrap();
    }
}
