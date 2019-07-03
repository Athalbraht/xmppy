from setuptools import setup
import xmppy

deps = ["sleekxmpp", "python-gnupg"]

setup(
    name="xmppy",
    description="Python module for receiving and sending massage using XMPP protocol",
    version="v0.1",
    author="Albert Szadziński",
    author_email="albert.szadzinski@pm.me",
    license="MIT",
    install_requires=deps,
    packages=['xmppy'],
    entry_points={
        'console_scripts': ['xmppy = xmppy.Messenger:main']
    }
)
