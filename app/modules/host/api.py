from flask.ext.restful import reqparse, abort, Resource, Api
from flask import jsonify
from flask import request
from app import common

# commented until API is stable. then we'll use API for webinterface
#
#
#def add_host_togroups(hostname, groups):
#    selectgroups = [str(group) for group in groups]
#    print selectgroups
#    for group in selectgroups:
#        common.db.groups.update({'groupname': group}, {'$push': {'hosts': hostname}}, upsert=False, multi=False)


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
            return 'host does not exist', 201


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
