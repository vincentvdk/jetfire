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
import ldap
import ldap.modlist as modlist
import os
import re
from functools import wraps
from app import app
# establish connection with LDAP server

try:
    #l = ldap.initialize(os.getenv("LDAPHOST", "ldap://infra-08.prod.btr.local"))
    l = ldap.initialize(os.getenv("LDAPHOST", app.config['LDAPHOST']))
    username = os.getenv("LDAPBINDDN", app.config['LDAPBINDDN'])
    password = os.getenv("LDAPBINDPW", app.config['LDAPBINDPW'])
    l.set_option(ldap.OPT_PROTOCOL_VERSION,ldap.VERSION3)
    l.bind_s(username, password, ldap.AUTH_SIMPLE)

except ldap.LDAPError, e:
    print e

baseDN = os.getenv("LDAPBASEDN", app.config['LDAPBASEDN'])
searchScope = ldap.SCOPE_SUBTREE
attrs = None

class GetGroup(flask.views.MethodView):

    def get(self):
        return flask.render_template('getgroup.html')

    def post(self):
        groupname = str(flask.request.form['get_group'])
        filter = '(&(objectclass=ansibleGroup)(cn=' + groupname + '))'
        result = l.search_s(baseDN, searchScope, filter)
        #self.get_allgroups()
        if not result:
            flask.flash('Group ' + groupname + ' not found')
            return flask.redirect(flask.url_for('getgroup'))
        else:
            groupmembers = self.get_groupmembers(groupname)
            groupvars = self.get_groupvars(groupname)
            return flask.render_template('getgroup.html', groupname=groupname, members=groupmembers, groupvars=groupvars)

    def get_groupmembers(self,groupname):
        filter = '(&(objectclass=ansibleGroup)(cn=' + groupname + '))'
        result = l.search_s(baseDN, searchScope, filter)
        # return notfound when group does not exists
        if not result:
            members = None
        else:
            memberlist = result[0][1]['member']
            members = []
            for item in memberlist:
                member = item.split(",")
                members.append(member[0][3:])
        return members

    def get_groupvars(self,groupname):
        filter = '(&(objectclass=ansibleGroup)(cn=' + groupname + '))'
        result = l.search_s(baseDN, searchScope, filter)
        # return none when no vars found
        if not result:
            groupvars = None
        elif 'ansibleGroupVar' in result[0][1]:
            groupvars = result[0][1]['ansibleGroupVar']
            #print groupvars
        else:
            groupvars = None
        return groupvars

class GetAllGroups(flask.views.MethodView):

    def post(self):
        allgroups = self.get_allgroups()
        return flask.render_template('getgroup.html', allgroups=allgroups)

    def get_allgroups(self):
        filter = '(objectclass=ansibleGroup)'
        result = l.search_s(baseDN, searchScope, filter)
        allgroups = []
        for item in result:
            group = ''.join(map(str, item[1]['cn']))
            #print group
            allgroups.append(group)
        return allgroups

