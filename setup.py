#coding=utf8
from setuptools import setup

__author__ = 'alex'

setup(
    name='blogen',
    version='0.0.0.8 pre',
    packages=['blogen'],
    author='Alexander.Li',
    author_email='superpowerlee@gmail.com',
    license='LGPL',
    install_requires=["PyYAML>=3.10","Markdown>=2.1.1","jinja2>=2.6","bottle>=0.11"],
    description="A local static blog site generator and previewer,that help you deploy blog on github pages",
    entry_points ={
        'console_scripts':[
            'blogen=blogen.gen:main'
        ]
    },
    keywords ='github pages blog',
    url='https://github.com/ipconfiger/blogen'
)