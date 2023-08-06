from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="simple-calulator-by-mk",
    version="0.1.2",
    author="Mohit Jha",
    author_email='mohitjha1511@gmail.com',
    description="A simple math library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/mohit-jha/simple-calculator',
    packages=["simple_calulator_by_mk"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
