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
from functools import wraps
from app import app
# establish connection with LDAP server

try:
    l = ldap.initialize(os.getenv("LDAPHOST", app.config['LDAPHOST']))
    username = os.getenv("LDAPBINDDN", app.config['LDAPBINDDN'])
    password = os.getenv("LDAPBINDPW", app.config['LDAPBINDPW'])
    l.set_option(ldap.OPT_PROTOCOL_VERSION,ldap.VERSION3)
    l.bind_s(username, password, ldap.AUTH_SIMPLE)

except ldap.LDAPError, e:
    print e

# LDAP variables
#baseDN = os.getenv("LDAPBASEDN", 'ou=ansible-dev, dc=ansible, dc=local')
baseDN = os.getenv("LDAPBASEDN", app.config['LDAPBASEDN'])
searchScope = ldap.SCOPE_SUBTREE
attrs = None

class GetHost(flask.views.MethodView):

    def get(self):
        return flask.render_template('gethost.html')

    def post(self):
        hostname = str(flask.request.form['p_get'])
        result = self.get_hostinfo(hostname)
        groups = self.get_hostgroups(hostname)
        if result != 'notfound':
            hostinfo = result
            return flask.render_template('gethost.html', res=result, groupres=groups, host=hostname)
        else:
            flask.flash('Host ' + hostname + ' not found')
            return flask.redirect(flask.url_for('gethostinfo'))

    def get_hostinfo(self, hostname):
        filter = '(cn=' + hostname +')'
        result = l.search_s(baseDN, searchScope, filter)
        if not result:
            return "notfound"
        else:
            for item in result:
                # if ansiblevar is not available return None
                if 'ansibleVar' in item[1]:
                    ansiblevar = item[1]['ansibleVar']
                else:
                    ansiblevar = None
            return ansiblevar

    def get_dn(self,hostname):
        filter = '(cn=' + hostname +')'
        result = l.search_s(baseDN, searchScope, filter)
        if not result:
            return None
        else:
            dn = result[0][0]
            print dn
            return dn

    def get_hostgroups(self, hostname):
        dn = self.get_dn(hostname)
        # if host does not exists return None
        if dn == None:
            return None
        else:
            filter = '(&(objectClass=groupOfNames)(member=' + dn + '))'
            result = l.search_s(baseDN, searchScope, filter)
            groups = []
            # if host does not exist return None
            for item in result:
                '''convert the lists(item) to a string'''
                group_string = ''.join(map(str, item[1]['cn']))
                ''' append to the group list '''
                groups.append(group_string)
            return groups

# import the above classes rather then put them above.
class EditHost(flask.views.MethodView):

    def post(self):
        hostname = str(flask.request.form['p_get'])
        res = GetHost()
        result = res.get_hostinfo(hostname)
        groups = res.get_hostgroups(hostname)
        return flask.render_template('edithost.html', host=hostname, result=result, groups=groups)

    def get(self):
        return flask.render_template('edithost.html')

class EditHostSubmit(flask.views.MethodView):

    def post(self):
        return flask.render_template('edithost.html')

    def get(self):
         return flask.render_template('edithost.html')
