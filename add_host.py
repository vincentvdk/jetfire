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

class AddHost(flask.views.MethodView):

    def get(self):
        # logic to return list with all groups in the form
        filter = '(objectClass=ansibleGroup)'
        result = l.search_s(baseDN, searchScope, filter)
        groups = []
        for item in result:
            group = ''.join(map(str, item[1]['cn']))
            groups.append(group)
        # return everything to the template
        return flask.render_template('addhost.html', groups=groups)

    def post(self):
        hostname = str(flask.request.form['add_host'])
        #print hostname
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

    def add_host(self,hostname):
        # Get the ansible vars from the form
        ansivars = flask.request.form.getlist('pnew')
        # build ldif to add host + vars in LDAP
        dn = str('cn=' + hostname + ',' + app.config['LDAPBASEDN'])
        attrs = {}
        if ansivars == [u'']:
            attrs['objectclass'] = ['ansibleHost', 'top', 'device']
            attrs['cn'] = [hostname]
        else:
            attrs['ansibleVar'] = [str(var) for var in ansivars]
            attrs['objectclass'] = ['ansibleHost', 'top', 'device']
            attrs['cn'] = [hostname]
        ldif = modlist.addModlist(attrs)
        try:
            l.add_s(dn, ldif)
        except ldap.LDAPError, e:
            print e

    def get_hostname(self,hostname):
        filter = '(cn=' + hostname +')'
        result = l.search_s(baseDN, searchScope, filter)
        if result:
            hostname = ''.join(map(str, result[0][1]['cn']))
            return hostname

    def get_hostdn(self,hostname):
        # this will fail if hostname is not created previously
        filter = '(cn=' + hostname +')'
        result = l.search_s(baseDN, searchScope, filter)
        dn = result[0][0]
        return dn


    def add_host_togroups(self, hostname):
        selectgroups = flask.request.form.getlist('selectedgroups')
        #remove unicode tags
        selectgroups = [str(group) for group in selectgroups]
        # Add host as member to each selecred group
        for group in selectgroups:
            filter = '(cn=' + group +')'
            result = l.search_s(baseDN, searchScope, filter)
            groupdn = result[0][0]
            hostdn = self.get_hostdn(hostname)
            mod_attrs = [( ldap.MOD_ADD, 'member', hostdn )]
            try:
                l.modify_s(groupdn,mod_attrs)
            except ldap.LDAPError, e:
                print e

