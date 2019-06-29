#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
import getpass
import time 
from xmppBot.gpg_holder import Gpg
from optparse import OptionParser

import sleekxmpp

if sys.version_info < (3, 0):
	from sleekxmpp.util.misc_ops import setdefaultencoding
	setdefaultencoding('utf8')
else:
	raw_input = input

class Bot(sleekxmpp.ClientXMPP):
	def __init__(self, jid, password, recipient, msg_function, reply_function, freq=120, msg_t=True, rpl_t=True, wait=False):
		self.j = jid
		self.p = password
		self.recipient = recipient
		self.msg_function = msg_function
		self.reply_function = reply_function
		self.msg_t = msg_t
		self.rpl_t = rpl_t
		self.mm = []
		self.gpg_encryption = False
		self.ntime = freq #seconds
		
		self.run(wait)
			
	def run(self, wait):
		if not wait:
			sleekxmpp.ClientXMPP.__init__(self, self.j, self.p)
			self.add_event_handler("session_start", self.start)
			if self.rpl_t:
				self.add_event_handler("message", self.message)	
			self.register_plugin('xep_0030') # Service Discovery
			self.register_plugin('xep_0004') # Data Forms
			self.register_plugin('xep_0060') # PubSub
			self.register_plugin('xep_0199') # XMPP Ping
			if self.connect():
				self.process(block=True)
				print("Done")
			else:
				print("Unable to connect.")
				
			
	@classmethod        
	def receiveMessage(cls, jid, password, reply):
		logging.basicConfig(level=logging.ERROR,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		instance = cls(jid, password, None, None, reply, freq=-1, msg_t=False, rpl_t=True)
		return instance 

	@classmethod        
	def sendMessage(cls, jid, password, recipient, message, freq=-1):
		logging.basicConfig(level=logging.ERROR,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		instance = cls(jid, password, recipient, message, None, freq, msg_t=True, rpl_t=False)
		return instance    
        
	@classmethod        
	def initialize(cls, jid, password, recipient, message, reply, freq=10,wait=False):
		logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		instance = cls(jid, password, recipient, message, reply, freq=freq, msg_t=True, rpl_t=True, wait=wait)
		return instance

         
            
	def start(self, event):
		self.send_presence()
		self.get_roster()
		if self.msg_t:
			print("start() --msg_t->True")
			self._start_thread("chat_send", self.monitor)
          
	def monitor(self):
		while True:
			time.sleep(1)
			if int(time.time())%self.ntime == 0 and self.ntime > 0:
				print("Sending...{}".format(self.MSG()))
				self.send_message(mto=self.recipient, mbody=self.MSG(), mtype='chat')
			elif self.ntime < 0:
				self.send_message(mto=self.recipient, mbody=self.MSG(), mtype='chat')
				self.disconnect(wait=True)
				break

 
	def message(self, msg):
		if msg['type'] in ('chat', 'normal'):
			msg.reply(self.RPL(msg["body"])).send()
			print(str(msg["body"]))
			self.mm = msg
	
	def enableGPG(self, uid, gpghome=''):
		self.gpg = Gpg(gpghome)
		self.uid = uid
		self.gpg_encryption = True
		return None

	def GPG(func):
		def wrap(self, *args, **kwargs):
			if self.gpg_encryption:
				message = self.gpg.encrypt(func(self, *args, **kwargs), uids=self.uid)
			else:
				message = func(self, *args, **kwargs)
			return message
		return wrap
	
	@GPG
	def MSG(self):
		return self.msg_function()
		
	@GPG
	def RPL(self, msg):
		return self.reply_function(msg)
            

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

        

