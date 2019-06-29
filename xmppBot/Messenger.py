#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
import getpass
import time 
from optparse import OptionParser

import sleekxmpp

if sys.version_info < (3, 0):
	from sleekxmpp.util.misc_ops import setdefaultencoding
	setdefaultencoding('utf8')
else:
	raw_input = input

class Bot(sleekxmpp.ClientXMPP):
	def __init__(self, jid, password, recipient, msg_function, reply_function, freq=120, msg_t=True, rpl_t=True):
		self.recipient = recipient
		self.msg_function = msg_function
		self.reply_function = reply_function
		self.msg_t = msg_t
		self.rpl_t = rpl_t
		self.mm = []
		self.ntime = freq #seconds
		sleekxmpp.ClientXMPP.__init__(self, jid, password)
		self.add_event_handler("session_start", self.start)
		if rpl_t:
			self.add_event_handler("message", self.message)

	@classmethod        
	def receiveMessage(cls, jid, password, reply):
		logging.basicConfig(level=logging.ERROR,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		instance = cls(jid, password, None, None, reply, freq=-1, msg_t=False, rpl_t=True)
		instance.register_plugin('xep_0030') # Service Discovery
		instance.register_plugin('xep_0004') # Data Forms
		instance.register_plugin('xep_0060') # PubSub
		instance.register_plugin('xep_0199') # XMPP Ping
		if instance.connect():
			instance.process(block=True)
			print("Done")
		else:
			print("Unable to connect.")
		return instance 

	@classmethod        
	def sendMessage(cls, jid, password, recipient, message, freq=-1):
		logging.basicConfig(level=logging.ERROR,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		instance = cls(jid, password, recipient, message, None, freq, msg_t=True, rpl_t=False)
		instance.register_plugin('xep_0030') # Service Discovery
		instance.register_plugin('xep_0004') # Data Forms
		instance.register_plugin('xep_0060') # PubSub
		instance.register_plugin('xep_0199') # XMPP Ping
		if instance.connect():
			instance.process(block=True)
			print("Done")
		else:
			print("Unable to connect.")
		return instance    
        
	@classmethod        
	def initialize(cls, jid, password, recipient, message, reply, freq=120):
		logging.basicConfig(level=logging.ERROR,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		instance = cls(jid, password, recipient, message, reply, freq)
		instance.register_plugin('xep_0030') # Service Discovery
		instance.register_plugin('xep_0004') # Data Forms
		instance.register_plugin('xep_0060') # PubSub
		instance.register_plugin('xep_0199') # XMPP Ping
		if instance.connect():
			instance.process(block=True)
			print("Done")
		else:
			print("Unable to connect.")
		return instance         
            
	def start(self, event):
		self.send_presence()
		self.get_roster()
		if self.msg_t:
			self._start_thread("chat_send", self.monitor)
          
	def monitor(self):
		while True:
			time.sleep(1)
			if int(time.time())%self.ntime == 0 and self.ntime > 0:
				self.send_message(mto=self.recipient, mbody=self.msg_function(), mtype='chat')
			elif self.ntime < 0:
				self.send_message(mto=self.recipient, mbody=self.msg_function(), mtype='chat')
				self.disconnect(wait=True)
				break

 
	def message(self, msg):
		if msg['type'] in ('chat', 'normal'):
			msg.reply(self.reply_function(msg["body"])).send()
			print(str(msg["body"]))
			self.mm = msg
            
def monitor():
	return "func_moni test {}".format(time.time())
	
def reply(msg):
	return "Yout send {}".format(msg)

def main():
	optp = OptionParser()

	optp.add_option('-q', '--quiet', help='set logging to ERROR',
					action='store_const', dest='loglevel',
					const=logging.ERROR, default=logging.INFO)
	optp.add_option('-d', '--debug', help='set logging to DEBUG',
					action='store_const', dest='loglevel',
					const=logging.DEBUG, default=logging.INFO)
	optp.add_option('-v', '--verbose', help='set logging to COMM',
					action='store_const', dest='loglevel',
					const=5, default=logging.INFO)

    # JID and password options.
	optp.add_option("-j", "--jid", dest="jid",
					help="JID to use")
	optp.add_option("-p", "--password", dest="password",
					help="password to use")                
	optp.add_option("-t", "--to", dest="to",
					help="JID to send the message to")
	optp.add_option("-m", "--message", dest="message",
					help="message to send")                   

	opts, args = optp.parse_args()

	logging.basicConfig(level=opts.loglevel,format='%(levelname)-8s %(message)s')

	if opts.jid is None:
		opts.jid = raw_input("Username: ")
	if opts.password is None:
		opts.password = getpass.getpass("Password: ")
	xmpp = Bot.sendMessage(opts.jid, opts.password, opts.to, lambda: opts.message)

        

