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
#
import flask
import flask.views
import os
import pymongo

from app import app
from get_host import GetAllHosts
from get_group import GetAllGroups

# establish connection with mongodb server
dbserver = os.getenv("MONGOSRV", app.config['MONGOSRV'])
database = os.getenv("DATABASE", app.config['DATABASE'])
dbserverport = os.getenv("MONGOPORT", app.config['MONGOPORT'])

conn = pymongo.Connection(dbserver, dbserverport)
db = conn[database]


class Remove(flask.views.MethodView):

    def get(self):
        g = GetAllGroups()
        h = GetAllHosts()
        allgroups = [item["groupname"] for item in g.get_allgroups()]
        allhosts = h.get_allhosts()
        return flask.render_template('remove.html', allgroups=allgroups, allhosts=allhosts)

    def post(self):
        hremove = flask.request.form.getlist('selectedhostsremove')
        gremove = flask.request.form.getlist('selectedgroupsremove')
        if hremove:
            for item in hremove:
                self.host(item)
        if gremove:
            for item in gremove:
                self.group(item)
        return flask.render_template('remove.html')

    def host(self, hostname):
        db.hosts.remove({'hostname': hostname})
        groups =  db.groups.find({'hosts': hostname}).distinct('groupname')
        for item in groups:
             db.groups.update({"groupname": item}, {"$pull": {"hosts": hostname}})


    def group(self, groupname):
        db.groups.remove({'groupname': groupname})
        parentgroups = db.groups.find({'children': groupname}).distinct('groupname')
        for item in parentgroups:
            db.groups.update({"groupname": item}, {"$pull": {"children": groupname}})

