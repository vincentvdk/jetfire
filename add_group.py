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
import pymongo
import json
import yaml
from functools import wraps
from app import app

# establish connection with mongod
conn = pymongo.Connection('192.168.122.240', 27017)
db = conn['ansible']

class AddGroup(flask.views.MethodView):

    def get(self):
        '''logic to return a list of all available ansible hosts'''
        hosts = db.hosts.find().distinct("hostname")
        return flask.render_template('addgroup.html', hosts=hosts)

    def post(self):
        groupname = str(flask.request.form['add_group'])
        if len(groupname) == 0:
            flask.flash('empty groupname')
            return flask.render_template('addgroup.html')
        else:
            # insert logic to see if group already exists (get_groupname)
            self.add_group(groupname)
            flask.flash('Group added successfully')
            return flask.render_template('addgroup.html')


    def add_group(self, groupname):
        yamlvars = flask.request.form['gyaml']
        # return empty list in inventory output when no vars
        if not yamlvars:
            y = []
        else:
            y = yaml.load(yamlvars)
            #print y
        selectedhosts = flask.request.form.getlist('selectedhosts')
        # create a list with the DNs from the selected hostnames
        children = []
        members = []
        for host in selectedhosts:
            members.append(host)
        attrs = {}
        post = {"groupname": groupname,
                "hosts": members,
                "vars": y,
                "children": children
        }
        try:
            db.groups.insert(post)
        except:
            pass
