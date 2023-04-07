#include <Python.h>
#include "futium.h"

PyObject * oneChar(PyObject *self, PyObject *args) {
	int x;
	
	// parses the arguments that have been passed from Python into local variables
	if(!PyArg_ParseTuple(args, "i", &x)) {
		return NULL;
	}
	
	char L[] = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'};

	char s[2] = {L[x], '\0'}; // Create a null-terminated string with a single character

	return Py_BuildValue("s", s);
}

PyObject * ewm(PyObject *self, PyObject *args) {
	// EMA(t) = Price(t) x k + EMA(y) x (1-k)
}