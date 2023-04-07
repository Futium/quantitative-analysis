#include "futium.h"

// states what the f(x) does
char oneCharfunc_docs[] = "Converts number 0-35 into a character 0-9, a-z";
char ewmfunc_docs[] = "Finds exponential weighted moving average";

PyMethodDef futium_funcs[] = {
	{	"oneChar",
		(PyCFunction)oneChar,
		METH_VARARGS,
		oneCharfunc_docs},
	{
		"ewm",
		(PyCFunction)ewm,
		METH_VARARGS,
		ewmfunc_docs},
	{	NULL}
};

char futiummod_docs[] = "This is Futium module.";

PyModuleDef futium_mod = {
	PyModuleDef_HEAD_INIT,
	"futium",
	futiummod_docs,
	// -1 means doesnt support sub-interpreters, non-negative value would indicate memory requirement for module  
	-1,
	futium_funcs,
	NULL,
	NULL,
	NULL,
	NULL
};

PyMODINIT_FUNC PyInit_futium(void) {
	return PyModule_Create(&futium_mod);
}