# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='libABCD',
    version='0.3.0',
    description='the Autonomous Bariloche Central DAQ, a centralized DAQ system for scientific experiments',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://gitlab.com/bertou/libabcd',
    author='Nicolás Avalos and Xavier Bertou, Laboratorio Detección de Partículas y Radiación',
    author_email='bertou@cab.cnea.gov.ar',
    license='MIT',
    packages=['libABCD'],
    zip_safe=False)
