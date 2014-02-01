#!/usr/bin/python
# Jetfire is an Ansible inventory tool
# Copyright (c) 2013 by Vincent Van der Kussen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import flask, flask.views
import os
import yaml
import json
import pymongo
from functools import wraps
from app import app
from get_host import GetHost
# establish connection with mongodb server
dbserver = os.getenv("MONGOSRV", app.config['MONGOSRV'])
database = os.getenv("DATABASE", app.config['DATABASE'])
dbserverport = os.getenv("MONGOPORT", app.config['MONGOPORT'])

conn = pymongo.Connection(dbserver, dbserverport)
db = conn[database]


class EditHost(flask.views.MethodView):

    def post(self):
        hostname = str(flask.request.form['p_get'])
        #res = GetHost()
        #result = res.get_hostinfo(hostname)
        if len(hostname) == 0:
            flask.flash('empty hostname given')
            return flask.render_template('edithost.html')
        elif self.get_hostinfo(hostname) == "notfound":
            flask.flash('hostname not found')
            return flask.render_template('edithost.html')
        else:
            result = self.get_hostinfo(hostname)
            available_groups = self.get_availablegroups()
            groups = self.get_hostgroups(hostname)
            return flask.render_template('edithost.html', host=hostname, result=result, groups=groups, available_groups=available_groups)

    def get(self):
        return flask.render_template('edithost.html')

    def get_hostinfo(self, hostname):
        result = db.hosts.find({"hostname": hostname}).distinct("vars")
        if not result:
            return "notfound"
        else:
            j = json.dumps(result[0], sort_keys=True, indent=2)
            ansiblevar = yaml.dump(yaml.load(j), default_flow_style=False)
            return ansiblevar

    def get_hostgroups(self, hostname):
        '''retrieve all groups the host is a member of'''
        result = db.groups.find({"hosts": hostname}, {'groupname': 1, '_id': 0})
        groups = [ item["groupname"] for item in result]
        return groups

    def get_availablegroups(self):
        ''' return all groups this host is not a member of'''
        allgroups = db.groups.find().distinct("groupname")
        # build compared list
        hostname = str(flask.request.form['p_get'])
        groups = self.get_hostgroups(hostname)
        s = set(groups)
        availablegroups = [ x for x in allgroups if x not in s ]
        return availablegroups

class EditHostSubmit(flask.views.MethodView):

    def post(self):
        hostname = str(flask.request.form['p_get2'])
        #vars = yaml.load(flask.request.form['ehyaml'])
        self.update_host(hostname)
        self.update_groups(hostname)
        return flask.render_template('edithost.html')

    def update_host(self,hostname):
            yamlvars = flask.request.form['ehyaml']
            #groups = flask.request.form.getlist('groupselect')
            try:
                y = yaml.load(yamlvars)
            except yaml.YAMLError, exc:
                print "Yaml syntax error"
            #print y
            #post = {"hostname": hostname,
            #        "vars": y
            #}
            try:
                db.hosts.update({"hostname": hostname}, {"$set": {'vars': y}}, upsert=False,multi=False)
            except:
                pass
    def update_groups(self,hostname):
            g = EditHost()
            current_groups = g.get_hostgroups(hostname)
            #print current_groups
            updated_groups = flask.request.form.getlist('groupselect')
            #print updated_groups
            addh = set(current_groups)
            remh = set(updated_groups)
            add_hosts_group = [ x for x in updated_groups if x not in addh ]
            remove_hosts_group = [ x for x in current_groups if x not in remh ]
            #print remove_hosts_group
            for item in add_hosts_group:
                db.groups.update({"groupname": item}, {"$push": {"hosts": hostname}})
            for item in remove_hosts_group:
                db.groups.update({"groupname": item}, {"$pull": {"hosts": hostname}})
            pass


    def get(self):
        return flask.render_template('edithost.html')
