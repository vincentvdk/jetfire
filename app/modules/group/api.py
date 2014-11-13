from flask.ext.restful import Resource
from flask import request
from app import common


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
            return 'Group already exists', 201

        common.add_group(groupname, ansiblevars, children, hosts)
        return 'group added', 200

    def put(self):
        '''for now we only allow update of vars. further logic needs to
        be in common'''
        data = request.json
        groupname = data['groupname']
        ansiblevars = data['vars']
        #children = data['children']
        #hosts = data['hosts']
        #common.delete_group(groupname)
        #common.add_group(groupname, ansiblevars, children, hosts)
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
