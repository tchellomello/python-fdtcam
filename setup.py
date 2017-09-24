# coding=utf-8
"""FDT IP Camera setup script."""
from setuptools import setup

setup(
    name='fdtcam',
    packages=['fdtcam'],
    version='0.0.1',
    description='A Python library to communicate with FDT IP Cameras',
    author='Marcelo Moreira de Mello',
    author_email='tchello.mello@gmail.com',
    url='https://github.com/tchellomello/python-fdtcam',
    license='MIT',
    include_package_data=True,
    test_suite='tests',
    keywords=[
        'fdt',
        'ipcam',
        'iot',
    ],
)
