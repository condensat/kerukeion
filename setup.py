from setuptools import setup, find_packages


setup(
    name='kerukeion',

    version='0.0.1',

    description='An open source exchange engine',

    author='condensat/banxit',

    author_email='thomas@condensat.com',

    packages=find_packages(exclude=['contrib', 'docs', 'test']),

    install_requires=['sortedcontainers', 'numpy'],

    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },

    entry_points={
        'console_scripts': [
            'start=kerukeion:main',
        ],
    },

    # List additional URLs that are relevant to your project as a dict.
    #
    # This field corresponds to the "Project-URL" metadata fields:
    # https://packaging.python.org/specifications/core-metadata/#project-url-multiple-use
    #
    # Examples listed include a pattern for specifying where the package tracks
    # issues, where the source is hosted, where to say thanks to the package
    # maintainers, and where to support the project financially. The key is
    # what's used to render the link text on PyPI.
    # project_urls={  # Optional
    #    'Bug Reports': '',
    #    'Funding': '',
    #    'Say Thanks!': '',
    #    'Source': '',
    # },
)
