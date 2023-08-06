import setuptools

setuptools.setup(
    name="hofu",
    version="0.0.1",
    author="Arthurdw <dev@arthurdw.com>",
    description="A simple library which implements higher order functions in python using functional chaining.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Arthurdw/pyter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
