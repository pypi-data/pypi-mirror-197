import setuptools

setuptools.setup(
    name="zca",
    version="0.1.1",
    url="https://github.com/davebulaval/zca",
    author="Maarten Versteegh, David Beauchemin",
    author_email="maartenversteegh@gmail.com",
    description="ZCA whitening",
    long_description=open("README.rst").read(),
    packages=setuptools.find_packages(),
    install_requires=["numpy", "scipy", "scikit-learn"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
