from setuptools import setup



with open("README.md", "r") as fh:
    long_desc= fh.read()


setup(
        name="helloworld-marndr",
        version="0.0.1",
        description="say hello",
        py_modules=["helloworld"],
        package_dir={"":"src"},
        classifiers=[
            "Programming Language :: Python :: 3"
            ],
        long_description=long_desc,
        long_description_content_type="text/markdown",
        # install_requires = [],
        url="https://github.com/marndr/helloworld.git",
        author="Maryam NAderi",
        author_email="maryam.naderi@idiap.ch",
)
