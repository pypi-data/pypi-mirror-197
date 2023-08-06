#!/usr/bin/env python

import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
  name='slmndr',
  version='1.1',
  install_requires=['PyOpenGL', 'PyOpenGL_accelerate', 'pygame', 'numpy'],
  description='Lightning fast python user interfaces created with opengl.',
  long_description = long_description,
  long_description_content_type = "text/markdown",
  author='BitPigeon',
  url='https://github.com/bitpigeon/salamander',
  packages_dir={"", "src"},
  packages=setuptools.find_packages(where="src"),
  classifiers=[
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
    "Natural Language :: English",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Developers",
    "Intended Audience :: Education",
    "Topic :: Software Development :: User Interfaces",
    "Topic :: Multimedia :: Graphics",
    "Topic :: Multimedia :: Graphics :: 3D Rendering",
  ],
  python_requires=">=2.7",
)
