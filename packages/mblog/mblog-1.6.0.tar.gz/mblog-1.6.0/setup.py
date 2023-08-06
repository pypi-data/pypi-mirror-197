"""
mblog: a minimal markdown blog
"""
import os
from setuptools import setup, find_packages

from mblog import __VERSION__ as VERSION

def getRequirements():
    with open('requirements.txt') as requirements:
        for req in requirements:
            req = req.strip()
            if req and not req.startswith('#'):
                yield req

def getReadMe():
    with open('README.md') as readme:
            return readme.read()

def copyReadMe():
    inPackagePath = os.path.join('mblog', 'README.md')
    with open(inPackagePath, 'wt') as readmeWrite:
        readmeWrite.write(getReadMe())

copyReadMe()
setup(name='mblog',
      version=VERSION,
      description="mblog: a minimal markdown blog",
      long_description=getReadMe(),
      long_description_content_type='text/markdown',
      classifiers=['Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Content Management System'],
      keywords='blog markdown flask minimal mblog',
      author='Karthik Kumar Viswanathan',
      author_email='karthikkumar@gmail.com',
      url='https://github.com/guilt/mblog',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'examples.*', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=list(getRequirements()),
     )
