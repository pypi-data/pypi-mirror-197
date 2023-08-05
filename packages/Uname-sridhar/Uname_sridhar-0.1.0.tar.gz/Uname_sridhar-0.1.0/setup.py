from setuptools import setup, find_packages
import os

requirements = os.popen("/usr/local/bin/pipreqs uname --print").read().splitlines()
# with open('README.md', 'r', encoding='utf-8') as fh:
#     long_description = fh.read()

setup(
    name='Uname_sridhar',
    version='0.1.0',
    author='Sridhar',
    author_email='dcsvsridhar@gmail.com',
    description='Uname_sridhar is a wrapper of uname Command',
    packages=find_packages(),
    url='https://git.selfmade.ninja/SRIDHARDSCV/package_uname',
    install_requires=requirements,
    # long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'Uname_sridhar=uname.uname:main',
        ],
    },
)