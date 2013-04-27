import htmltag

try:
    from distutils.core import setup
except ImportError:
    from setuptools import setup

from sphinx.setup_command import BuildDoc
cmdclass = {'build_sphinx': BuildDoc}

setup(
    name="htmltag",
    version=htmltag.__version__,
    description="Python HTML tag interface",
    author=htmltag.__author__,
    cmdclass=cmdclass,
    author_email="daniel.mcdougall@liftoffsoftware.com",
    url="https://github.com/liftoff/htmltag",
    license="Apache 2.0",
    py_modules=["htmltag"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
