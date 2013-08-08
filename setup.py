from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
        Extension ("genevo.bitint",
                ["genevo/bitint.pyx"],
                 libraries = ["m"])
]

setup (
        name        = "genevo",
        cmdclass    = {"build_ext": build_ext},
        ext_modules = ext_modules
)
