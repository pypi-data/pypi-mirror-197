from setuptools import find_packages
from setuptools import setup

classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Intended Audience :: Education",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
]

setup(
    name="numeric_grad",
    version="0.0.3",
    description="Small library for computing gradients of functions that are commonly used in Machine Learning and Deep Learning.",
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    url="https://github.com/anil-gurbuz/Numeric-grad",
    author="Anil Gurbuz",
    author_email="anlgrbz91@gmail.com",
    license="MIT",
    classifiers=classifiers,
    keywords=[
        "Deep learning",
        "Machine Learning",
        "Gradient",
        "Backpropagation",
    ],
    packages=find_packages(),
    install_requires=["torch"],
)
