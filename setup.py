#!/usr/bin/env python3

from setuptools import setup
import xmppBot

#with open('requirements.txt','r') as req:
#    deps = req.read().splitlines()

deps = ["sleekxmpp"]

setup(
        name = "xmppBot",
        description = "Python module for receiving and sending massage using XMPP protocol",
        version = "v0.1",
        author = "No Name",
        author_email = "no.name@pm.me",
        license = "MIT",
        requires = deps,
        install_requires = deps,
        packages = ['xmppBot'],
        entry_points = {
            'console_scripts': ['xmppBot = xmppBot.Messenger:main']
                        }
        )
