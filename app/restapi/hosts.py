# from flask.ext.restful import Resource
from flask_restful import Resource
from flask import request, jsonify
from app import common


class HostsAPI(Resource):
    def get(self):
        print "test get"
        result = common.getAllHosts()
        if result:
            #data = {"hosts": [host for host in result]}
            data = [host for host in result]
        else:
            data = {"hosts": ""}
        #resp = jsonify(data)
        resp = jsonify(hosts=data)
        resp.status_code = 200
        return resp

    def post(self):
        data = request.json
        print "data"
        hostname = data['hostname']
        ansiblevars = data['vars']
        groups = data['groups']
        exists = [str(item) for item in common.getSearchHosts(hostname)]
        if exists:
            return 'Host already exists', 400
        if type(groups).__name__ != 'list':
            return 'hosts is not of type list', 400
        else:
            common.add_host(hostname, ansiblevars)
            common.add_host_togroups(hostname, groups)
        return 'host added', 201

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
