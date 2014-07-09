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
from app import common, app
from flask.ext.paginate import Pagination
from flask import request


class GetHost(flask.views.MethodView):
    def get(self):
        query = request.args.get('q')
        if query:
            result = self.get_hostinfo(query)
            groups = self.get_hostgroups(query)
            if result is None:
                return self.get_search_hosts(query)
            else:
                return flask.render_template('gethost.html', res=result, groupres=groups, hostname=query)

        return flask.render_template('gethost.html')

    def post(self):
        hostname = str(flask.request.form['p_get'])
        result = self.get_hostinfo(hostname)
        groups = self.get_hostgroups(hostname)
        # print groups
        if result is None:
            return self.get_search_hosts(hostname)
        else:
            return flask.render_template('gethost.html', res=result, groupres=groups, hostname=hostname)

    def get_search_hosts(self, hostname):
        try:
            page = int(request.args.get('page', 1))
        except ValueError:
            page = 1

        skip = app.config['NUMBER_OF_ITEMS_PER_PAGE'] * (page - 1)

        all_hosts = GetAllHosts()
        search_hosts = all_hosts.get_pagedhosts(skip, app.config['NUMBER_OF_ITEMS_PER_PAGE'], hostname)

        pagination = Pagination(page=page, total=common.count_hosts(hostname), found=hostname, record_name='host',
                                per_page=app.config['NUMBER_OF_ITEMS_PER_PAGE'])
        return flask.render_template('gethost.html', allhosts=search_hosts, pagination=pagination)

    def get_hostinfo(self, hostname):
        result = common.get_hostname_info(hostname)
        host = [item for item in result]
        if len(hostname) == 0:
            return None
        elif not host:
            return None
        elif host[0]["vars"] is None:
            return None
        else:
            for item in host:
                print item
                ansiblevars = item["vars"]
            return ansiblevars

    def get_hostgroups(self, hostname):
        result = common.get_all_groups_for_host(hostname)
        groups = [item for item in result]
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
        try:
            page = int(request.args.get('page', 1))
        except ValueError:
            page = 1

        skip = app.config['NUMBER_OF_ITEMS_PER_PAGE'] * (page - 1)
        allhosts = self.get_pagedhosts(skip, app.config['NUMBER_OF_ITEMS_PER_PAGE'])

        pagination = Pagination(css_framework='bootstrap3', page=page, total=common.count_hosts(), record_name='host',
                                per_page=app.config['NUMBER_OF_ITEMS_PER_PAGE'])
        return flask.render_template('gethost.html', allhosts=allhosts, pagination=pagination)

    def get_pagedhosts(self, skip, number_of_items, filter_hostname=None):
        result = common.get_paged_hosts(skip, number_of_items, filter_hostname)
        allhosts = {}
        host = GetHost()
        for item in result:
            if type(item) is dict:
                hostname = item["hostname"]
            else:
                hostname = item

            itemgroups = host.get_hostgroups(hostname)
            allhosts[hostname] = [str(x) for x in itemgroups]
        return allhosts

    def get_allhosts(self):
        result = common.get_all_hosts()
        allhosts = {}
        host = GetHost()
        for item in result:
            itemgroups = host.get_hostgroups(item)
            allhosts[item] = [str(x) for x in itemgroups]
        return allhosts
