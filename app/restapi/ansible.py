from flask.ext.restful import Resource
from flask import request, jsonify
from subprocess import Popen
from os import listdir
from app import app
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
                        + playdir + "/" + data['play'] + " -u " + data['user'],
                        shell=True)
        process.communicate()
        exitcode = process.wait()
        #print exitcode
        if exitcode == 0:
            return 'playbook %s successfully completed' % data['play'], 201
        elif exitcode == 1:
            return 'playbook %s failed' % data['play'], 500
        elif exitcode == 3:
            return 'something went wrong. check logfile', 500
