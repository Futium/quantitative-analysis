from distutils.core import setup, Extension

setup(
	name = "futium",
	version = "1.0",
	ext_modules = [Extension("futium", ["bind.c", "futium.c"])]
)