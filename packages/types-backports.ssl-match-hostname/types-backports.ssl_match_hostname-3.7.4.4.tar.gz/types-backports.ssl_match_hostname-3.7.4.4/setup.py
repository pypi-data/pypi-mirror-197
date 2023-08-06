from setuptools import setup

name = "types-backports.ssl_match_hostname"
description = "Typing stubs for backports.ssl_match_hostname"
long_description = '''
## Typing stubs for backports.ssl_match_hostname

This is a PEP 561 type stub package for the `backports.ssl_match_hostname` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`backports.ssl_match_hostname`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/backports.ssl_match_hostname. All fixes for
types and metadata should be contributed there.

*Note:* `types-backports.ssl_match_hostname` is unmaintained and won't be updated.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `7e0b9b44dea0b170081cafd596c2804089dc2125`.
'''.lstrip()

setup(name=name,
      version="3.7.4.4",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/backports.ssl_match_hostname.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['backports-stubs'],
      package_data={'backports-stubs': ['__init__.pyi', 'ssl_match_hostname/__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
