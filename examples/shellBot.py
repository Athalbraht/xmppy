import xmppBot.Messenger as xb
import subprocess as sp

def monitor():
	return "Example message"

def reply(msg):
	return sp.check_output(msg, shell=True).decode()

#send monitor() every 60 seconds and keep receiving reply()
bot = xb.Bot.initialize("jabber_id@examp.le", "password",
				"send_to@examp.le", monitor, reply, freq=60)
