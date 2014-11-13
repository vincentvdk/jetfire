#!/usr/bin/python
import subproces

class ansible():
	"""docstring for ansible"""
	def playbook(self, play, user, pwd):
		subproces.call(["ansible-playbook", "-i", "hosts", play, "-u", user, "-k", pwd])



p = ansible()

p.playbook()



