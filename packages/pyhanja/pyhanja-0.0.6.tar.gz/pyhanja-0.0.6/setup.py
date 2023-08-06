from setuptools import Extension, setup

if __name__ == "__main__":
    from pybind11.setup_helpers import Pybind11Extension

    setup(
        ext_modules=[
            Pybind11Extension(
                name="pyhanja._pyhanja",
                sources=["src/convert.cc", "src/types.cc", "src/dictionary.cc", "src/pyhanja.cc"],
                include_dirs=["include", "dependencies"],
                extra_compile_args=["-std=c++20"],
                language="c++"
            ),
        ]
    )
