#include <pybind11/pybind11.h>
#include "aes.hpp"  // Include your AES header file

namespace py = pybind11;

PYBIND11_MODULE(aes_module, m) {
    py::class_<AES_128>(m, "AES_128")
        .def(py::init<>())
        .def("setKey", &AES_128::setKey)
        .def("setIV", &AES_128::setIV)
        .def("encrypt", &AES_128::encrypt)
        .def("decrypt", &AES_128::decrypt);
}
