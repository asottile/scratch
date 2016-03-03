#include <Python.h>

static PyObject* _hello_world(PyObject* self) {
    return PyUnicode_FromString("hello world");
}

static struct PyMethodDef methods[] = {
    {"hello_world", (PyCFunction)_hello_world, METH_NOARGS},
    {NULL, NULL}
};

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "basic_c_module",
    NULL,
    -1,
    methods
};

PyMODINIT_FUNC PyInit_basic_c_module(void) {
    return PyModule_Create(&module);
}
#else
PyMODINIT_FUNC initbasic_c_module(void) {
    Py_InitModule3("basic_c_module", methods, NULL);
}
#endif
