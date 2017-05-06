# -*- coding: utf-8 -*-
'''
Nord VPN API (unofficial)
=========================
Unofficial nordvpn api
'''

VERSION = "0.0.1"

from setuptools import setup, find_packages

setup(
    name='nordvpn',
    description='Unofficial nordvpn api',
    long_description='\n'.join(
        [
            open('README.md', 'rb').read().decode('utf-8')
        ]
    ),
    author='Sang Han',
    license='Apache License 2.0',
    url='https://github.com/jjangsangy/nordvpn',
    author_email='jjangsangy@gmail.com',
    include_package_data=True,
    packages=find_packages(),
    version=VERSION,
    install_requires=['requests', 'chardet', 'pandas'],
    platforms='any',
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'nord = nordvpn.__main__:main'
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Unix Shell',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
