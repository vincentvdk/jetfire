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

import flask
import flask.views
import yaml
import json
from app import common
from app.common import db


class EditGroup(flask.views.MethodView):
    def post(self):
        groupname = str(flask.request.form['group_get'])
        childgroups = self.get_childgroups(groupname)
        if len(groupname) == 0:
            flask.flash('empty groupname given')
            return flask.render_template('editgroup.html')
        elif self.get_groupinfo(groupname) is None:
            flask.flash('Group does not exist')
            return flask.redirect(flask.url_for('editgroup'))
        else:
            result = self.get_groupinfo(groupname)
            hosts = self.get_grouphosts(groupname)
            available_hosts = self.get_availablehosts()
            availablechildgroups = self.get_availablechildren()
            return flask.render_template('editgroup.html', group=groupname, result=result, hosts=hosts,
                                         available_hosts=available_hosts, childgroups=childgroups,
                                         availablechildgroups=availablechildgroups)

    def get(self):
        return flask.render_template('editgroup.html')

    def get_groupinfo(self, groupname):
        result = common.getGroupInfo(groupname)
        if not result:
            ansiblevar = None
        else:
            j = json.dumps(result[0], sort_keys=True, indent=2)
            ansiblevar = yaml.dump(yaml.load(j), default_flow_style=False)
        return ansiblevar

    def get_grouphosts(self, groupname):
        '''retrieve all hosts from the group'''
        result = common.getAllHostForGroup(groupname)
        hosts = result[0]["hosts"]
        if not hosts:
            return None
        else:
            return hosts

    def get_availablehosts(self):
        ''' return all hosts not a member of this group'''
        allhosts = common.getAllHosts()
        # build compared list
        groupname = str(flask.request.form['group_get'])
        hosts = self.get_grouphosts(groupname)
        if hosts:
            s = set(hosts)
            avaiblable = [x for x in allhosts if x not in s]
            return avaiblable
        return allhosts

    def get_childgroups(self, groupname):
        result = db.groups.find({"groupname": groupname}, {'children': 1, '_id': 0})
        for item in result:
            childgroups = item["children"]
        return childgroups

    def get_availablechildren(self):
        allgroups = common.getAllGroups()
        # build compared list
        groupname = str(flask.request.form['group_get'])
        childgroups = self.get_childgroups(groupname)
        s = set(childgroups)
        availablechildgroups = [x for x in allgroups if x not in s]
        return availablechildgroups


class EditGroupSubmit(flask.views.MethodView):
    def post(self):
        groupname = str(flask.request.form['group_get2'])
        self.update_group(groupname)
        self.update_hosts(groupname)
        self.update_childgroups(groupname)
        return flask.redirect('getgroup')

    def get(self):
        return flask.render_template('editgroup.html')

    def update_group(self, groupname):
        yamlvars = flask.request.form['egyaml']
        try:
            y = yaml.load(yamlvars)
        except yaml.YAMLError, exc:
            print "Yaml syntax error"

        try:
            db.groups.update({"groupname": groupname}, {"$set": {'vars': y}}, upsert=False, multi=False)
        except:
            pass

    def update_hosts(self, groupname):
        global add_hosts, rem_hosts
        h = EditGroup()
        current_hosts = h.get_grouphosts(groupname)
        updated_hosts = flask.request.form.getlist('hostselect')
        if current_hosts is not None and len(updated_hosts) > 0:
            addh = set(current_hosts)
            remh = set(updated_hosts)
            add_hosts = [x for x in updated_hosts if x not in addh]
            rem_hosts = [x for x in current_hosts if x not in remh]
        else:
            if len(updated_hosts) > 0:
                add_hosts = [x for x in updated_hosts]

            if current_hosts:
                rem_hosts = [x for x in current_hosts]

        if add_hosts:
            for item in add_hosts:
                db.groups.update({"groupname": groupname}, {"$push": {"hosts": item}})
        if rem_hosts:
            for item in rem_hosts:
                db.groups.update({"groupname": groupname}, {"$pull": {"hosts": item}})
        pass

    def update_childgroups(self, groupname):
        c = EditGroup()
        current_children = c.get_childgroups(groupname)
        updated_children = flask.request.form.getlist('childrenselect')
        addchld = set(current_children)
        remchld = set(updated_children)
        add_chlds = [x for x in updated_children if x not in addchld]
        rem_chlds = [x for x in current_children if x not in remchld]
        for item in add_chlds:
            db.groups.update({"groupname": groupname}, {"$push": {"children": item}})
        for item in rem_chlds:
            db.groups.update({"groupname": groupname}, {"$pull": {"children": item}})

