from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.17'
DESCRIPTION = 'Narrating Politics Using Python like a 🤖️.'

# Setting up
setup(
    name="politicsnlp",
    version=VERSION,
    author="Draco Deng",
    author_email="dracodeng6@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://cpanlp.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'politics', 'freedom', 'justice', 'power','democracy','party','intelligent politics', 'linguistic turn', 'linguistic',"intelligent party","natural language processing","machine learning","policy"],
    classifiers=[
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        'Natural Language :: English'
    ]
)