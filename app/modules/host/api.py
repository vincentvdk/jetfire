from flask.ext.restful import Resource, Api
from app import common


class GetHostsAPI(Resource):

    def get(self):
        result = common.getAllHosts()
        if result:
            data = {"hosts": [host for host in result]}
        else:
            data = {"hosts": ""}
        return data


class GetHostVarsAPI(Resource):

    def get(self, hostname):
        result = common.getHostnameInfo(hostname)
        if result:
            data = {"vars": [host["vars"] for host in result]}
        else:
            data = {"vars": ""}
        return data


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
