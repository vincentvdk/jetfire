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
import os
import pymongo

from app import app


# -----------------------------------------------------------------------------------
# establish connection with LDAP server
dbserver = os.getenv("MONGOSRV", app.config['MONGOSRV'])
database = os.getenv("DATABASE", app.config['DATABASE'])
dbserverport = os.getenv("MONGOPORT", app.config['MONGOPORT'])

conn = pymongo.Connection(dbserver, dbserverport)
db = conn[database]
# -----------------------------------------------------------------------------------
class GetGroup(flask.views.MethodView):

    def get(self):
        return flask.render_template('getgroup.html')

    def post(self):
        groupname = str(flask.request.form['get_group'])
        result = db.groups.find({"groupname": groupname}, {'groupname': 1, '_id': 0})
        group = [ item for item in result]
        if not group:
            flask.flash('Group ' + groupname + ' not found')
            return flask.redirect(flask.url_for('getgroup'))
        else:
            #groupmembers = self.get_groupmembers(groupname)
            groupmembers = self.get_groupchildren(groupname)
            groupvars = self.get_groupvars(groupname)
            grouphosts = self.get_grouphosts(groupname)
            return flask.render_template('getgroup.html', groupname=groupname, members=groupmembers, groupvars=groupvars, grouphosts=grouphosts)

#    def get_groupmembers(self,groupname):
    def get_groupchildren(self,groupname):
        result = db.groups.find({"groupname": groupname}, {'children': 1, '_id': 0})
        for item in result:
            childs = item
        children = []
        # return none if no group is entered in form
        #if len(groupname) == 0:
        #    members = None
        # return none if group has no children
        if not childs:
            #children = None
            children = []
        else:
            for item in childs["children"]:
                children.append(item)
        return children

    def get_grouphosts(self,groupname):
        result = db.groups.find({"groupname": groupname}, {'hosts': 1, '_id': 0})
        #hosts = [ item for item in result]
        for item in result:
            h = item
        members = []
        # return none if no group is entered in form
        #if len(groupname) == 0:
        #    members = None
        # return none if group has no children
        if not h:
            #members = None
            member = []
        else:
            #for item in hosts:
            for item in h["hosts"]:
                #members = item["hosts"]
                members.append(item)
        return members

    def get_groupvars(self,groupname):
        result = db.groups.find({"groupname": groupname}, {'vars': 1, '_id': 0})
        vars = [item for item in result]
        # return none when no vars found
        if len(groupname) == 0:
            groupvars = None
        elif not vars:
            groupvars = None
        else:
            for item in vars:
                groupvars = item["vars"]
        return groupvars

class GetAllGroups(flask.views.MethodView):

    def get(self):
        allgroups = self.get_allgroups()
        #allgroupmembers = GetGroup.get_groupmembers(group)
        return flask.render_template('getgroup.html', allgroups=allgroups)

    def get_allgroups(self):
        result = db.groups.find().distinct("groupname")
        allgroups = []
        #allgroups = {}
        group = GetGroup()
        for item in result:
            t = {}
            t["groupname"] = str(item)
            t["children"] = group.get_groupchildren(item)
            t["hosts"] = group.get_grouphosts(item)
            allgroups.append(t)
            #print type(t["children"])
            #print allgroups["groupname"]
            #print allgroups["children"]
        #print allgroups
        return allgroups

