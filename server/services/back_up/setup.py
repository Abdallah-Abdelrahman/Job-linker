from setuptools import setup
from Cython.Build import cythonize

setup(
        ext_modules = cythonize("ai_job_creator.pyx")
)
