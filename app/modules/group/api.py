from flask.ext.restful import Resource, Api
from app import common


class GetGroupsAPI(Resource):

    def get(self):
        result = common.getAllGroups()
        if result:
            data = {"groups": [group for group in result]}
        else:
            data = {"groups": ""}
        return data


class GetGroupVarsAPI(Resource):

    def get(self, groupname):
        result = common.getGroupVariables(groupname)
        if result:
            data = {"vars": [group["vars"] for group in result]}
        else:
            data = {"vars": ""}
        return data


class GetGroupChildrenAPI(Resource):

    def get(self,groupname):
        result = common.getAllChilderenForGroup(groupname)
        if result:
            data = {"children": [group["children"] for group in result]}
        else:
            data = {"children": ""}
        return data


class GetGroupHostsAPI(Resource):

    def get(self,groupname):
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
