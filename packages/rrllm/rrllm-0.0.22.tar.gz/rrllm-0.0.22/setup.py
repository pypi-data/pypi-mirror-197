from setuptools import setup, find_packages
import os
import sys

if sys.version_info[0] != 3:
    raise RuntimeError('Unsupported python version "{0}"'.format(
        sys.version_info[0]))

def _get_file_content(file_name):
    with open(file_name, 'r') as file_handler:
        return str(file_handler.read())
      
def get_long_description():
    return _get_file_content('README.md')

INSTALL_REQUIRES = [
    'transformers',
    'simpletransformers==0.63.7',
    'pandas',
    'numpy'
    'torch',
    'tensorflow',
    'tensorflow_datasets',
    'sklearn',
    'matplotlib',
    'linearmodels',
    'scipy'
]

setup(
    name="rrllm",
    version='0.0.22 ',
    author="Muhammed Cifci",
    author_email="mkcifci@psu.edu",
    description="Rubin's rules to account for performance instability of LLMs",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    keywords='nlp transformers classification rubinsrules',
    url="https://github.com/mkcifci/RR_LLM.git",
    packages=['rrllm'],
    py_modules=['rrllm'],
    license="MIT",
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=INSTALL_REQUIRES
)
