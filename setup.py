from setuptools import setup
import xmppBot

deps = ["sleekxmpp", "pythongnupg"]

setup(
    name="xmppBot",
    description="Python module for receiving and sending massage using XMPP protocol",
    version="v0.1",
    author="Albert Szadziński",
    author_email="albert.szadzinski@pm.me",
    license="MIT",
    requires=deps,
    install_requires=deps,
    packages=['xmppBot'],
    entry_points={
        'console_scripts': ['xmppBot = xmppBot.Messenger:main']
    }
)
