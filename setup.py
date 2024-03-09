from setuptools import setup
with open("README.md","r",encoding="utf-8") as fh:
    long_description=fh.read()

AUTHOR_NAME='SANKET JAMADAR'
SRC_REPO='src'  
LIST_OF_REQ=['streamlit']  

setup(
    name=SRC_REPO,
    version='0.0.1',
    author=AUTHOR_NAME,
    author_email='sankyjamadar@gmail.com',
    description='a python package to make a web app',
    long_description=long_description,
    long_description_content_type='text/markdown',
    package=[SRC_REPO],
    install_requires=LIST_OF_REQ,
    python_requires='>=3.7',


)