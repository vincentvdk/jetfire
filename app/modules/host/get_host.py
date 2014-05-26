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
from app import common
from flask.ext.paginate import Pagination
from flask import request


class GetHost(flask.views.MethodView):

    def get(self):
        return flask.render_template('gethost.html')

    def post(self):
        hostname = str(flask.request.form['p_get'])
        result = self.get_hostinfo(hostname)
        groups = self.get_hostgroups(hostname)
        #print groups
        if result != 'notfound':
            hostinfo = result
            return flask.render_template('gethost.html', res=result, groupres=groups, hostname=hostname)
        else:
            flask.flash('Host ' + hostname + ' not found')
            return flask.redirect(flask.url_for('gethostinfo'))

    def get_hostinfo(self, hostname):
        result = common.getHostnameInfo(hostname)
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
        result = common.getAllGroupsForHost(hostname)
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

    def get(self):
        NUMBER_OF_ITEMS = 10

        search = False
        q = request.args.get('q')
        if q:
            search = True
        try:
            page = int(request.args.get('page', 1))
        except ValueError:
            page = 1

        skip = NUMBER_OF_ITEMS * (page - 1)
        allhosts = self.get_pagedhosts(skip, NUMBER_OF_ITEMS)

        pagination = Pagination(page=page, total=common.countHosts(), search=search, record_name='host')
        return flask.render_template('gethost.html', allhosts=allhosts, pagination=pagination)

    def get_pagedhosts(self, skip, numberOfItems):
        result = common.getPagedHosts(skip, numberOfItems)
        #allhosts = []
        allhosts = {}
        host = GetHost()
        for item in result:
            hostname = ""
            if (type(item) is dict):
                hostname = item["hostname"]
            else:
                hostname = item

            itemgroups = host.get_hostgroups(hostname)
            #allhosts.append(item)
            allhosts[hostname] = [str(x) for x in itemgroups]
        return allhosts

    def get_allhosts(self):
        result = common.getAllHosts()
        #allhosts = []
        allhosts = {}
        host = GetHost()
        for item in result:
            itemgroups = host.get_hostgroups(item)
            #allhosts.append(item)
            allhosts[item] = [str(x) for x in itemgroups]
        return allhosts
