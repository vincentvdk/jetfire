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

import flask
import flask.views
import yaml
from app.common import db


class AddGroup(flask.views.MethodView):

    def get(self):
        '''logic to return a list of all available ansible hosts'''
        hosts = db.hosts.find().distinct("hostname")
        childgroups = db.groups.find().distinct("groupname")
        return flask.render_template('addgroup.html', hosts=hosts, childgroups=childgroups)

    def post(self):
        groupname = str(flask.request.form['add_group'])
        hosts = db.hosts.find().distinct("hostname")
        childgroups = db.groups.find().distinct("groupname")
        if len(groupname) == 0:
            flask.flash('empty groupname')
            return flask.render_template('addgroup.html', hosts=hosts, childgroups=childgroups)
        elif groupname == self.get_groupname(groupname):
            flask.flash('groupname already exists')
            return flask.render_template('addgroup.html', hosts=hosts, childgroups=childgroups)
        else:
            # insert logic to see if group already exists (get_groupname)
            self.add_group(groupname)
            flask.flash('Group added successfully')
            return flask.render_template('addgroup.html', hosts=hosts, childgroups=childgroups)

    # this checks if the groupname is already defined.
    # needt better implementation
    def get_groupname(self, groupname):
        group = [str(item) for item in db.groups.find({"groupname": groupname}).distinct("groupname")]
        if not group:
            group = None
        else:
            group = group[0]
        return group

    def add_group(self, groupname):
        yamlvars = flask.request.form['gyaml']
        # return empty list in inventory output when no vars
        if not yamlvars:
            y = {}
        else:
            y = yaml.load(yamlvars)
            #print y
        selectedhosts = flask.request.form.getlist('selectedhosts')
        selectedchildren = flask.request.form.getlist('selectedchildren')
        # create a list with the DNs from the selected hostnames
        children = []
        members = []
        for host in selectedhosts:
            members.append(host)
        for child in selectedchildren:
            print child
            children.append(child)
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
