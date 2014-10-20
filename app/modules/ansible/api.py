from flask.ext.restful import Resource
from flask import request, jsonify
from app import app
from subprocess import Popen
from os import listdir
import os

playdir = os.getenv("PLAYBOOK_DIR", app.config['PLAYBOOK_DIR'])
inventory = os.getenv("ANSIBLE_INVENTORY", app.config['ANSIBLE_INVENTORY'])


class ansibleAPI(Resource):
    def get(self):
        playbooks = {"playbooks": [p for p in listdir(playdir) if
                     p.endswith(".yml")]}
        resp = jsonify(playbooks)
        resp.status_code = 200
        return resp

    def post(self):
        data = request.json
        process = Popen("ansible-playbook -i " + inventory + " "
                        + data['play'] + " -u " + data['user'], shell=True)
        process.communicate()
        exitcode = process.wait()
        if exitcode == 0:
            return 'playbook %s successfully completed' % data['play'], 201
        elif exitcode == 1:
            return 'playbook %s failed' % data['play'], 201
