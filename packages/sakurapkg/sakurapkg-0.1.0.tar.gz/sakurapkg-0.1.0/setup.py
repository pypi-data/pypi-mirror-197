from setuptools import setup
import pypkg
import sys

DESCRIPTION = "sakurapkg: Python pyproject.toml Genelator"
NAME = 'sakurapkg'
AUTHOR = 'sonyakun'
AUTHOR_EMAIL = 'sonyakun217@gmail.com'
URL = 'https://github.com/sonyakun/sakurapkg'
LICENSE = 'MIT'
DOWNLOAD_URL = 'https://github.com/sonyakun/sakurapkg/releases'
PYTHON_REQUIRES = ">=3.10"

INSTALL_REQUIRES = [
    'toml',
    'cleo',
]

CLASSIFIERS = [
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3 :: Only',
]

long_description_content_type = "https://github.com/sonyakun/sakurapkg"

setup(
    name=NAME,
      version="0.1.0",
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      maintainer=AUTHOR,
      maintainer_email=AUTHOR_EMAIL,
      description=DESCRIPTION,
      long_description=long_description_content_type,
      license=LICENSE,
      url=URL,
      download_url=DOWNLOAD_URL,
      python_requires=PYTHON_REQUIRES,
      install_requires=INSTALL_REQUIRES,
      classifiers=CLASSIFIERS,
    entry_points={
        "console_scripts": [
            "sakura=pypkg.cli.main:main".format(sys.version_info[0]),
        ]
    },
)
