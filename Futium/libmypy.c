#include <Python.h>
#include "libmypy.h"

PyObject * hello(PyObject * self) {
	return PyUnicode_FromFormat("Hello C extension!");
}

PyObject * heyman(PyObject *self, PyObject *args) {
	int num;
	char *name;

	if(!PyArg_ParseTuple(args, "is", &num, &name))
		return NULL;

	return PyUnicode_FromFormat("Hay %s!  You gave me %d.", name, num);
}



// static *PyObject * Futium(PyObject *self) {
//     int x
//     char L[] = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'};

//     return L[x];
// }