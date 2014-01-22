#!/usr/bin/python
# Jetfire is an Ansible inventory tool
# # Copyright (c) 2013 by Vincent Van der Kussen
# #
# # This program is free software: you can redistribute it and/or modify
# # it under the terms of the GNU General Public License as published by
# # the Free Software Foundation, either version 3 of the License, or
# # (at your option) any later version.
# #
# # This program is distributed in the hope that it will be useful,
# # but WITHOUT ANY WARRANTY; without even the implied warranty of
# # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# # GNU General Public License for more details.
# #
# # You should have received a copy of the GNU General Public License
# # along with this program. If not, see <http://www.gnu.org/licenses/>.
# #

import flask, flask.views
import os
import yaml
import json
import pymongo
from functools import wraps
from app import app
from get_host import GetHost

conn = pymongo.Connection('192.168.122.240', 27017)
db = conn['ansible']

class EditGroup(flask.views.MethodView):

    def post(self):
        groupname = str(flask.request.form['group_get'])
        result = self.get_groupinfo(groupname)
        hosts = self.get_grouphosts(groupname)
        available_hosts = self.get_availablehosts()
        return flask.render_template('editgroup.html', group=groupname, result=result, hosts=hosts, available_hosts=available_hosts)

    def get(self):
        return flask.render_template('editgroup.html')

    def get_groupinfo(self, groupname):
        result = db.groups.find({"groupname": groupname}).distinct("vars")
        if not result:
            return "notfound"
        else:
            j = json.dumps(result[0], sort_keys=True, indent=2)
            ansiblevar = yaml.dump(yaml.load(j), default_flow_style=False)
            return ansiblevar

    def get_grouphosts(self, groupname):
        '''retrieve all hosts from the group'''
        result = db.groups.find({"groupname": groupname}, {'hosts': 1, '_id': 0})
        hosts = result[0]["hosts"]
        return hosts

    def get_availablehosts(self):
        ''' return all hosts not a member of this group'''
        allhosts = db.hosts.find().distinct("hostname")
        #print allhosts
        # build compared list
        groupname = str(flask.request.form['group_get'])
        hosts = self.get_grouphosts(groupname)
        #print hosts
        s = set(hosts)
        availablehosts = [ x for x in allhosts if x not in s ]
        #print availablehosts
        return availablehosts

class EditGroupSubmit(flask.views.MethodView):

    def post(self):
        groupname = str(flask.request.form['group_get2'])
        self.update_group(groupname)
        self.update_hosts(groupname)
        return flask.render_template('editgroup.html')

    def get(self):
        return flask.render_template('editgroup.html')

    def update_group(self,groupname):
        yamlvars = flask.request.form['egyaml']
        try:
            y = yaml.load(yamlvars)
        except yaml.YAMLError, exc:
            print "Yaml syntax error"
            #print y
            #post = {"hostname": hostname,
            #        "vars": y
            #}
        try:
            db.groups.update({"groupname": groupname}, {"$set": {'vars': y}}, upsert=False,multi=False)
        except:
            pass

    def update_hosts(self,groupname):
        h = EditGroup()
        current_hosts = h.get_grouphosts(groupname)
        updated_hosts = flask.request.form.getlist('hostselect')
        print current_hosts
        print updated_hosts
        addh = set(current_hosts)
        remh = set(updated_hosts)
        add_hosts = [x for x in updated_hosts if x not in addh]
        rem_hosts = [x for x in current_hosts if x not in remh]
        print "hosts to add: %s." % add_hosts
        print "hosts to remove: %s." % rem_hosts
        for item in add_hosts:
            db.groups.update({"groupname": groupname}, {"$push": {"hosts": item}})
        for item in rem_hosts:
            db.groups.update({"groupname": groupname}, {"$pull": {"hosts": item}})
        pass


