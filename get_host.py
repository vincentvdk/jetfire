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
from functools import wraps
from app import app

# establish connection with Mongo server
conn = pymongo.Connection('192.168.122.240', 27017)
db = conn['ansible']

class GetHost(flask.views.MethodView):

    def get(self):
        return flask.render_template('gethost.html')

    def post(self):
        hostname = str(flask.request.form['p_get'])
        result = self.get_hostinfo(hostname)
        groups = self.get_hostgroups(hostname)
        print groups
        if result != 'notfound':
            hostinfo = result
            return flask.render_template('gethost.html', res=result, groupres=groups, host=hostname)
        else:
            flask.flash('Host ' + hostname + ' not found')
            return flask.redirect(flask.url_for('gethostinfo'))

    def get_hostinfo(self, hostname):
        result = db.hosts.find({"hostname": hostname}, {'hostname': 0, '_id': 0})
        host = [item for item in result]
        if len(hostname) == 0:
            return "notfound"
        elif not host:
            return "notfound"
        elif host[0]["vars"] == None:
            ansiblevars = None
            return ansiblevars
        else:
            for item in host:
                print item
                ansiblevars = item["vars"]
            return ansiblevars


    def get_hostgroups(self, hostname):
        result = db.groups.find({"hosts": hostname}, {'groupname': 1, '_id': 0})
        groups = [ item for item in result]
        grouplist = []
        # return empty list when host is not in a group
        if not groups:
            return grouplist
        else:
            for item in groups:
                grouplist.append(item["groupname"])
            return grouplist


class GetAllHosts(flask.views.MethodView):

    def post(self):
        allhosts = self.get_allhosts()
        return flask.render_template('gethost.html', allhosts=allhosts)

    def get_allhosts(self):
        result = db.hosts.find().distinct("hostname")
        allhosts = []
        for item in result:
            allhosts.append(item)
        return allhosts
