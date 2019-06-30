# XmppBot




![tag](https://img.shields.io/github/tag-date/aszadzinski/xmppBot.svg)
![commit](https://img.shields.io/github/last-commit/aszadzinski/xmppBot.svg)
![license](https://img.shields.io/github/license/aszadzinski/xmppBot.svg)

![status](https://img.shields.io/badge/build-passing-green.svg?style=flat&logo=Linux) ![status](https://img.shields.io/badge/build-falling-red.svg?style=flat&logo=Windows)

Python module for receiving and sending message using XMPP protocol.

Repos: [GitHub](https://github.com/aszadzinski/xmppBot.git) [GitLab](https://gitlab.com/aszadzinski/xmppbot)

---

## Table of Contents

- [Installation](#Installation)
- [Usage](#Usage)
	- [Module](#Module)
		- [Example 1](#example-1)
		- [Example 2](#example-2)
		- [Example 3](#example-3)
	- [Console script](#Console-script)
	- [Encryption](#Encryption)
		- [GPG](#GPG)
		- [OMEMO](#OMEMO)
- [Todo](#Todo)

---

## Installation


### From source

``` python3 setup.py install```

**Depedencies:**

- sleekxmpp
- python-gnupg

### Using pip (TODO)

`pip install xmppBot`

### AUR (TODO)

`makepkg xmppBot`

## Usage

### Module

#### example 1

(using classmethod)

```python
import xmppBot.Messenger as xb
import subprocess as sp

def monitor():
	return "Example message"

def reply(msg):
	return sp.check_output(msg, shell=True).decode()

#send monitor() every 60 seconds and keep receiving reply()
bot = xb.Bot.initialize("jabber_id@examp.le", "password",
				"send_to@examp.le", monitor, reply, freq=60)
 ```
![example 1](examples/obscura1561838699874.jpg)

#### example 2

(only sending messages)

 ```python
#send one message (for looping add freq param)
bot = xb.Bot.sendMessage("jabber_id@examp.le", "password",
 						"send_to@examp.le", monitor)
```

#### example 3

(only receiving messages)

  ```python
  bot = xb.Bot.receiveMessage("jabber_id@examp.le", "password", reply)
   ```

---

 ### Console script

`xmppBot -j <Jabber ID> -p <password> -t <recipient> -m <message>`

---

### Encryption

#### GPG

(in progress...)

```python
bot = xb.Bot.initialize("jabber_id@examp.le", "password",
				"send_to@examp.le", monitor, reply, freq=60, wait=True)
#temporarily doesn't support signing and receiving encrypted messages TODO!
bot.enableGPG("UID", "gnupghome_dir")

bot.run(wait=False)
```

#### OMEMO

TODO!
