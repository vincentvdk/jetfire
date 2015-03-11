from flask_restful import Resource
from flask import request, jsonify
from app import app, common
from subprocess import Popen
from os import listdir
import os

playdir = os.getenv("PLAYBOOK_DIR", app.config['PLAYBOOK_DIR'])
inventory = os.getenv("ANSIBLE_INVENTORY", app.config['ANSIBLE_INVENTORY'])

# Group related API calls


class GroupsAPI(Resource):
    def get(self):
        result = common.getAllGroups()
        if result:
            data = {"groups": [group for group in result]}
        else:
            data = {"groups": ""}
        return data

    def post(self):
        data = request.json
        groupname = data['groupname']
        ansiblevars = data['vars']
        children = data['children']
        hosts = data['hosts']
        exists = [str(item) for item in common.getSearchGroups(groupname)]
        if exists:
            return 'Group already exists', 400

        common.add_group(groupname, ansiblevars, children, hosts)
        return 'group added', 200

    def put(self):
        '''for now we only allow update of vars. further logic needs to
        be in common'''
        data = request.json
        groupname = data['groupname']
        ansiblevars = data['vars']
        # children = data['children']
        # hosts = data['hosts']
        # common.delete_group(groupname)
        # common.add_group(groupname, ansiblevars, children, hosts)
        common.edit_group(groupname, ansiblevars)
        return 'group updated', 200


class DeleteGroupAPI(Resource):
    def delete(self, groupname):
        exists = [str(item) for item in common.getSearchGroups(groupname)]
        if exists:
            common.delete_group(groupname)
            return 'group deleted', 200
        else:
            return 'group does not exist', 201


class GetGroupVarsAPI(Resource):
    def get(self, groupname):
        result = common.getGroupVariables(groupname)
        if result:
            data = {"vars": [group["vars"] for group in result]}
        else:
            data = {"vars": ""}
        return data


class GetGroupChildrenAPI(Resource):
    def get(self, groupname):
        result = common.getAllChilderenForGroup(groupname)
        if result:
            data = {"children": [group["children"] for group in result]}
        else:
            data = {"children": ""}
        return data


class GetGroupHostsAPI(Resource):
    def get(self, groupname):
        result = common.getAllHostForGroup(groupname)
        if result:
            data = {"hosts": [group["hosts"] for group in result]}
        else:
            data = {"hosts": ""}
        return data


class GetGroupsSearchAPI(Resource):
    def get(self, search_term):
        result = common.getSearchGroups(search_term)
        if result:
            data = {"groups": [group["groupname"] for group in result]}
        else:
            data = {"groups": ""}
        return data


# Host related API calls
class HostsAPI(Resource):
    def get(self):
        result = common.getAllHosts()
        if result:
            data = {"hosts": [host for host in result]}
        else:
            data = {"hosts": ""}
        resp = jsonify(data)
        resp.status_code = 200
        return resp

    def post(self):
        data = request.json
        hostname = data['hostname']
        ansiblevars = data['vars']
        groups = data['groups']
        exists = [str(item) for item in common.getSearchHosts(hostname)]
        if exists:
            return 'Host already exists', 201
        if type(groups).__name__ != 'list':
            return 'hosts is not of type list', 201
        else:
            common.add_host(hostname, ansiblevars)
            common.add_host_togroups(hostname, groups)
        return 'host added', 200

    def put(self):
        # changing hostname results in 2 hosts. 1 new + 1 original. ->bug
        data = request.json
        hostname = data['hostname']
        ansiblevars = data['vars']
        groups = data['groups']
        common.delete_host(hostname)
        common.add_host(hostname, ansiblevars)
        common.add_host_togroups(hostname, groups)
        return 'host updated', 200


class DeleteHostAPI(Resource):
    def delete(self, hostname):
        exists = [str(item) for item in common.getSearchHosts(hostname)]
        if exists:
            common.delete_host(hostname)
            return 'host deleted', 200
        else:
            return 'host does not exist', 400


class GetHostVarsAPI(Resource):
    def get(self, hostname):
        result = common.getHostnameInfo(hostname)
        if result:
            ansiblevars = [host["vars"] for host in result]
            data = {"vars": ansiblevars}
        else:
            data = {"vars": ""}
        return data, 200


class GetHostGroupsAPI(Resource):
    def get(self, hostname):
        result = common.getAllGroupsForHost(hostname)
        if result:
            data = {"groups": [host["groupname"] for host in result]}
        else:
            data = {"groups": ""}
        return data


class GetHostsSearchAPI(Resource):
    def get(self, search_term):
        result = common.getSearchHosts(search_term)
        if result:
            data = {"hosts": [host["hostname"] for host in result]}
        else:
            data = {"hosts": ""}
        return data


class ansibleAPI(Resource):

    def get(self):
        playbooks = {"playbooks": [p for p in listdir(playdir) if
                     p.endswith(".yml")]}
        resp = jsonify(playbooks)
        resp.status_code = 200
        return resp

    def post(self):
        data = request.json
        process = Popen("ansible-playbook -i " + inventory + " "
                        + playdir + "/" + data['play'] + " -u " + data['user'],
                        shell=True)
        process.communicate()
        exitcode = process.wait()
        #print exitcode
        if exitcode == 0:
            return 'playbook %s successfully completed' % data['play'], 201
        elif exitcode == 1:
            return 'playbook %s failed' % data['play'], 500
        elif exitcode == 3:
            return 'something went wrong. check logfile', 500
