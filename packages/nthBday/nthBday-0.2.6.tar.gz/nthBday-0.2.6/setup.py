# from setuptools import setup, find_packages
# import codecs
# import os

# here = os.path.abspath(os.path.dirname(__file__))

# with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
#     long_description = "\n" + fh.read()

# VERSION = '0.2.5'
# DESCRIPTION = 'Find the "n-th" working day of a month.'
# LONG_DESCRIPTION = 'A package that allows to find n-th business day of a month (Currently only considers Indian Holidays).'

# # Setting up
# setup(
#     name="nthBday",
#     version=VERSION,
#     author="u77w41 (Ujjwal Chowdhury)",
#     author_email="<u77w41@gmail.com>",
#     description=DESCRIPTION,
#     long_description_content_type="text/markdown",
#     long_description=long_description,
#     packages=find_packages(),
#     install_requires=['pandas', 'datetime'],
#     keywords=['python', 'date', 'Business Day', 'Working Day', 'Holiday', 'calender'],
#     classifiers=[
#                 "Programming Language :: Python :: 3",
#                 "License :: OSI Approved :: MIT License",
#                 "Operating System :: OS Independent",
#     ]
# )


#####################################################################################################
"""setup"""
import pathlib
import os
import codecs
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (HERE / 'README.md').read_text(encoding='utf-8')
__version__ = '0.2.6'
__maintainer__ = 'Ujjwal Chowdhury'


# Setting up
setup(
    name='nthBday',
    version=__version__,
    description='An open-source python package to find business days of a month.',
    author=__maintainer__,
    author_email='<u77w41@gmail.com>',
    url='https://github.com/U77w41/nthBday',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['pandas','datetime'],
    tests_require=['pytest'],
    keywords= ['python', 'date', 'Business Day', 'Working Day', 'Holiday', 'calender']
)

#################################################################################################################
# python3 setup.py sdist bdist_wheel
# twine upload dist/*


