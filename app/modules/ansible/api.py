from flask.ext.restful import Resource
from flask import request, jsonify
from app import app,common
from subprocess import Popen
from os import listdir
import json, os

playdir = os.getenv("PLAYBOOK_DIR", app.config['PLAYBOOK_DIR'])

class ansibleAPI(Resource):
	def get(self):
		playbooks = {"playbooks": [p for p in listdir(playdir) if p.endswith(".yml")]}
		resp = jsonify(playbooks)
		resp.status_code = 200
		return resp

	def post(self):
		data = request.json
		process = Popen("ansible-playbook -i /home/vincent/repositories/ansible_api/hosts " + data['play'] + " -u " + data['user'], shell=True)
		process.communicate()
		exitcode = process.wait()
		if exitcode == 0:
			return 'playbook %s successfully completed' % data['play'], 201
		elif exitcode == 1:
			return 'playbook %s failed' % data['play'], 201