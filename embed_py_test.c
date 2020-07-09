#define PY_SSIZE_T_CLEAN
#include <Python.h>

int
main(int argc, char *argv[])
{
    PyObject *pModule, *pFunc, *pArgs;

    Py_Initialize();
    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append(\".\")");

   
    pModule = PyImport_ImportModule("py_emb");
    pFunc = PyObject_GetAttrString(pModule, "multiply");
    pArgs = PyTuple_New(1);
    PyTuple_SetItem(pArgs, 0, PyLong_FromLong(42L));
    PyObject* pResult = PyObject_CallObject(pFunc, pArgs);
    
    Py_DECREF(pModule);
    Py_XDECREF(pFunc);
    Py_DECREF(pModule);

    return 0;
}