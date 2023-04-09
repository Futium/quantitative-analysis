import cythonbuilder as cybuilder

cybuilder.cy_build()

# from distutils.core import setup, Extension

# setup(
# 	name = "futium",
# 	version = "1.1",
# 	ext_modules = [Extension("futium", ["bind.c", "futium.c"])]
# )