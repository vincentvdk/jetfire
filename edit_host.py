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
        available_groups = self.get_availablegroups()
        groups = self.get_hostgroups(hostname)
        return flask.render_template('edithost.html', host=hostname, result=result, groups=groups, available_groups=available_groups)

    def get(self):
        return flask.render_template('edithost.html')

    def get_hostinfo(self, hostname):
        result = db.hosts.find({"hostname": hostname}).distinct("vars")
        if not result:
            return "notfound"
        else:
            j = json.dumps(result[0], sort_keys=True, indent=2)
            ansiblevar = yaml.dump(yaml.load(j), default_flow_style=False)
            return ansiblevar

    def get_hostgroups(self, hostname):
        result = db.groups.find({"hosts": hostname}, {'groupname': 1, '_id': 0})
        groups = [ item["groupname"] for item in result]
        return groups

    def get_availablegroups(self):
        allgroups = db.groups.find().distinct("groupname")
        # build compared list 
        hostname = str(flask.request.form['p_get'])
        groups = self.get_hostgroups(hostname)
        s = set(groups)
        availablegroups = [ x for x in allgroups if x not in s ]
        return availablegroups

class EditHostSubmit(flask.views.MethodView):

    def post(self):
        hostname = str(flask.request.form['p_get2'])
        #vars = yaml.load(flask.request.form['ehyaml'])
        self.update_host(hostname)
        self.update_groups(hostname)
        return flask.render_template('edithost.html')

    def update_host(self,hostname):
            yamlvars = flask.request.form['ehyaml']
            #groups = flask.request.form.getlist('groupselect')
            try:
                y = yaml.load(yamlvars)
            except yaml.YAMLError, exc:
                print "Yaml syntax error"
            #print y
            #post = {"hostname": hostname,
            #        "vars": y
            #}
            try:
                db.hosts.update({"hostname": hostname}, {"$set": {'vars': y}}, upsert=False,multi=False)
            except:
                pass
    def update_groups(self,hostname):
            g = EditHost()
            current_groups = g.get_hostgroups(hostname)
            updated_groups = flask.request.form.getlist('groupselect')
            ah = set(current_groups)
            rh = set(updated_groups)
            add_hosts_group = [ x for x in updated_groups if x not in ah ]
            remove_hosts_group = [ x for x in current_groups if x not in rh ]
            print remove_hosts_group
            #for item in add_hosts_group:
            #    db.groups.update({"groupname": item}, {"$push": {"hosts": hostname}})
            for item in remove_hosts_group:
                db.groups.update({"groupname": item}, {"$pull": {"hosts": hostname}})
            pass


    def get(self):
        return flask.render_template('edithost.html')
