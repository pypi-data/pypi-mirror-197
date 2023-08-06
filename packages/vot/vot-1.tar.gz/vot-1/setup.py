# -*- coding: utf-8 -*-

from os.path import dirname, join
from setuptools import find_packages, setup

VERSION = "1"
__version__ = VERSION
__version_str__ = '.'.join(map(str, VERSION))

PATH = dirname(__file__)
f = open(join(PATH, 'README.md'))
# long_description = f.read().strip()
f.close()

install_requires = [

]


setup(
    name="vot",
    description="vot package",
    license="",
    # url="https://gitlab.zzjz.com/vot.git",
    # long_description=long_description,
    long_description="",
    version=__version_str__,
    author="wbx2023",
    author_email="974304805@qq.com",
    packages=find_packages(
        where='.',
        include=['vot']
    ),
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
    ],
    install_requires=install_requires,
    include_package_data=True,  # 启用清单文件MANIFEST.in
    # test_suite='nose.collector',
    entry_points={},
)
