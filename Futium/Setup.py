import cythonbuilder as cybuilder
import os
import shutil

cybuilder.cy_build()

myfile = "futium.html"
# If file exists, delete it.
if os.path.isfile(myfile):
    os.remove(myfile)


try:
    shutil.rmtree("build")
except OSError as e:
    # If it fails, inform the user.
    print("Error: %s - %s." % (e.filename, e.strerror))

# from distutils.core import setup, Extension

# setup(
# 	name = "futium",
# 	version = "1.1",
# 	ext_modules = [Extension("futium", ["bind.c", "futium.c"])]
# )