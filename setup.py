#!/usr/bin/env python
# -*- coding: utf8 -*-
import os
from setuptools import find_packages, setup

setup(
    name = 'TracUserfunk',
    version='1.0',
    packages = ['userfunk'],
    package_data = { 'userfunk': [] },

    author = 'Leif Högberg',
    author_email = 'leihog@gmail.com',
    description = 'Adds user related Wiki Macros',
    long_description = open(os.path.join(os.path.dirname(__file__), 'README')).read(),
    url = 'https://github.com/leihog/TracUserfunk',
    license = 'BSD',

    install_requires = ['Trac>=0.12'],
    entry_points = {
        'trac.plugins': [
            'userfunk.userlist = userfunk.userlist',
            'userfunk.username = userfunk.username'
        ],
    },
)
