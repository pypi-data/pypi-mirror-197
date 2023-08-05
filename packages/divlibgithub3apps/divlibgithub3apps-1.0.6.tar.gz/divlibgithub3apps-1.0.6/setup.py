# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open


version = '1.0.6'
setup(

    name='divlibgithub3apps',

    version=version,
    packages=find_packages(),

    description='Access the Github API as an Application',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    python_requires='>=3.10',

    author='OneDiversified',
    author_email='github@onediversified.com',
    url='https://github.com/onediversified/div.lib.github3apps',
    download_url="https://github.com/onediversified/div.lib.github3apps/archive/v%s.tar.gz" % version,
    keywords='automation github apps git',

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Version Control',

        'Programming Language :: Python :: 3',
    ],

    install_requires=[
        'cryptography>=39.0.2',
        'github3.py>=3.2.0',
        'pyjwt>=2.6.0',
        'requests>=2.28.2',
    ],

    extras_require={
        'dev': [
            'pypandoc',
            'twine',
            'wheel'
        ],
    }
)
