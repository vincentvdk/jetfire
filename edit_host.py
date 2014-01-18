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

conn = pymongo.Connection('192.168.122.240', 27017)
db = conn['ansible']


#class GetHost(flask.views.MethodView):
#
#    def get(self):
#        return flask.render_template('gethost.html')
#
#    def post(self):
#        hostname = str(flask.request.form['p_get'])
#        result = self.get_hostinfo(hostname)
#        groups = self.get_hostgroups(hostname)
#        if result != 'notfound':
#            hostinfo = result
#            return flask.render_template('gethost.html', res=result, groupres=groups, host=hostname)
#        else:
#            flask.flash('Host ' + hostname + ' not found')
#            return flask.redirect(flask.url_for('gethostinfo'))
#
#    def get_hostinfo(self, hostname):
#        result = db.hosts.find({"hostname": hostname}).distinct("vars")
#        #print result[0]
#        if not result:
#            return "notfound"
#        else:
#            j = json.dumps(result[0], sort_keys=True, indent=2)
#            ansiblevar = yaml.dump(yaml.load(j), default_flow_style=False)
#            return ansiblevar
#
#    def get_hostgroups(self, hostname):
#        pass
#        dn = self.get_dn(hostname)
#        # if host does not exists return None
#        if dn == None:
#            return None
#        else:
#            filter = '(&(objectClass=groupOfNames)(member=' + dn + '))'
#            result = l.search_s(baseDN, searchScope, filter)
#            groups = []
#            # if host does not exist return None
#            for item in result:
#                '''convert the lists(item) to a string'''
#                group_string = ''.join(map(str, item[1]['cn']))
#                ''' append to the group list '''
#                groups.append(group_string)
#            return groups

# import the above classes rather then put them above.
class EditHost(flask.views.MethodView):

    def post(self):
        hostname = str(flask.request.form['p_get'])
        #res = GetHost()
        #result = res.get_hostinfo(hostname)
        result = self.get_hostinfo(hostname)
        #groups = res.get_hostgroups(hostname)
        groups = self.get_hostgroups(hostname)
        return flask.render_template('edithost.html', host=hostname, result=result, groups=groups)

    def get(self):
        return flask.render_template('edithost.html')

    def get_hostinfo(self, hostname):
        result = db.hosts.find({"hostname": hostname}).distinct("vars")
        #print result[0]
        if not result:
            return "notfound"
        else:
            j = json.dumps(result[0], sort_keys=True, indent=2)
            ansiblevar = yaml.dump(yaml.load(j), default_flow_style=False)
            return ansiblevar

    def get_hostgroups(self, hostname):
        pass

class EditHostSubmit(flask.views.MethodView):

    def post(self):
        hostname = str(flask.request.form['p_get'])
        return flask.render_template('edithost.html')

    # new stuff added
        vars = flask.request.form.getlist('p_get')
        dn = str('cn=' + hostname + ',' + app.config['LDAPBASEDN'])
        atrrs = {}
        ldif = modlist.addModlist(attrs)

    def get(self):
         return flask.render_template('edithost.html')
