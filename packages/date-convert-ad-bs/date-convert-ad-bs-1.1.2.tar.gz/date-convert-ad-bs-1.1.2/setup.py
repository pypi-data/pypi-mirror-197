from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.1.2'
DESCRIPTION = 'Convert AD to BS and vice versa'

# Setting up
setup(
    name="date-convert-ad-bs",
    version=VERSION,
    author="Ulleri Tech (Binij Shrestha)",
    author_email="<uller@ulleri.tech>",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Ulleri-Tech/date-convert-AD-BS',
    license='MIT',
    packages=find_packages(),
    package_data={
        'date-convert-ad-bs': ['dataconvert/constants.json']
    },
    keywords=['python', "Convert Date",
              "AD to BS",
              "BS to AD"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
