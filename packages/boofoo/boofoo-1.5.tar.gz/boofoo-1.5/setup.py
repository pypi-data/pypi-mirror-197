#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='boofoo',
    version='1.5',
    description='',
    author='Naif Alshaye',
    author_email='naif@naif.io',
    url='',
    packages=['boofoo'],
    install_requires=[
        'docopt','openai','pyperclip','configparser',
    ],
    entry_points={
            'console_scripts' : [
                'boofoo = boofoo.boofoo:main'
            ]
        }
    )