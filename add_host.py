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
#import ldap
#import ldap.modlist as modlist
import os
import pymongo
import yaml
import json
from app import app


# establish connection
conn = pymongo.Connection('192.168.122.240', 27017)
db = conn['ansible']


class AddHost(flask.views.MethodView):

    def get(self):
        groups =  db.groups.find().distinct("groupname")
        # return everything to the template
        return flask.render_template('addhost.html', groups=groups)

    def post(self):
        hostname = str(flask.request.form['add_host'])
        # check if hostname already exists
        if len(hostname) == 0:
            flask.flash('Empty hostname given')
            return flask.redirect(flask.url_for('addhost'))
        elif hostname == self.get_hostname(hostname):
            flask.flash('Host already exists')
            return flask.redirect(flask.url_for('addhost'))
        else:
            # add the host
            self.add_host(hostname)
            # add the host to selected groups
            self.add_host_togroups(hostname)
            flask.flash('Host added successfully')
            return flask.redirect(flask.url_for('addhost'))

    def get_hostname(self,hostname):
        host = [str(item) for item in db.hosts.find({"hostname": hostname}).distinct("hostname")]
        if not host:
            host = None
        else:
            host = host[0]
        return host

    def add_host(self,hostname):
        # Get the ansible vars from the form
        yamlvars = flask.request.form['hyaml']
        y = yaml.load(yamlvars)
        post = {"hostname": hostname,
                "vars": y
        }
        try:
            db.hosts.insert(post)
        except:
            pass

    def add_host_togroups(self, hostname):
        selectgroups = flask.request.form.getlist('selectedgroups')
        #remove unicode tags
        selectgroups = [str(group) for group in selectgroups]
        # Add host as member to each selecred group
        for group in selectgroups:
            # get group ObjectId for insert
            objectid = db.groups.find({"groupname": group}).distinct("_id")
            db.groups.update({'groupname': group}, {'$push':{'hosts': hostname}},upsert=False,multi=False)

