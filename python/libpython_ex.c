#include <Python.h>
#include <assert.h>

/*
 * Usage:
 * $ gcc -I/usr/include/python2.7 libpython_ex.c -o main -lpython2.7 && ./main
 * It works!
 */

static void add_empty_string_to_path() {
    /* Do this to import from the current directory */
    PyObject* sys = PyImport_ImportModule("sys");
    assert(sys);
    PyObject* sys_modules = PyObject_GetAttrString(sys, "modules");
    assert(sys_modules);
    PyObject* empty_string = PyUnicode_FromString("");
    assert(empty_string);
    PyList_Insert(sys_modules, 0, empty_string);

    Py_DECREF(empty_string);
    Py_DECREF(sys_modules);
    Py_DECREF(sys);
}

int main() {
    Py_Initialize();

    add_empty_string_to_path();

    printf("It works!\n");

    Py_Finalize();

    return 0;
}
