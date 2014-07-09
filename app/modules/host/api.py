from flask.ext.restful import reqparse, abort, Resource, Api
from flask import json
from flask import jsonify
from flask import request
import yaml
from app import common


def delete_host(hostname):
    common.db.hosts.remove({'hostname': hostname})
    groups = common.db.groups.find({'hosts': hostname}).distinct('groupname')
    for item in groups:
        common.db.groups.update({"groupname": item}, {"$pull": {"hosts": hostname}})


def add_host(hostname, ansiblevars):
    try:
        if ansiblevars:
            j = json.dumps(ansiblevars, sort_keys=True, indent=2)
            y = yaml.load(j)
        else:
            y = yaml.load('{}')
    except yaml.YAMLError, exc:
        print "Yaml syntax error"

    post = dict(hostname=hostname, vars=y)

    try:
        common.db.hosts.insert(post)
    except:
        print "insert error"
        pass


def add_host_togroups(hostname, groups):
    selectgroups = [str(group) for group in groups]
    print selectgroups
    for group in selectgroups:
        common.db.groups.update({'groupname': group}, {'$push': {'hosts': hostname}}, upsert=False, multi=False)


class HostsAPI(Resource):
    def get(self):
        result = common.get_all_hosts()
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

        exists = [str(item) for item in common.get_search_hosts(hostname)]
        if exists:
            return 'Host already exists', 201

        if type(groups) != list:
            return 'hosts is not of type list', 201
        if type(ansiblevars) != dict:
            return 'AnsibleVars is not of type dict', 201

        add_host(hostname, ansiblevars)
        add_host_togroups(hostname, groups)

        return 'host added', 200

    def put(self):
        data = request.json
        hostname = data['hostname']
        ansiblevars = data['vars']
        groups = data['groups']

        if type(groups) != list:
            return 'hosts is not of type list', 201
        if type(ansiblevars) != dict:
            return 'AnsibleVars is not of type dict', 201

        delete_host(hostname)
        add_host(hostname, ansiblevars)
        add_host_togroups(hostname, groups)
        return 'host updated', 200


class DeleteHostAPI(Resource):
    def delete(self, hostname):
        exists = [str(item) for item in common.get_search_hosts(hostname)]
        if exists:
            delete_host(hostname)
            return 'host deleted', 200
        else:
            return 'host does not exist', 201


class GetHostVarsAPI(Resource):
    def get(self, hostname):
        result = common.get_hostname_info(hostname)
        if result:
            ansiblevars = [host["vars"] for host in result]
            data = {"vars": ansiblevars}
        else:
            data = {"vars": ""}
        resp = jsonify(data)
        resp.status_code = 200
        return resp


class GetHostGroupsAPI(Resource):
    def get(self, hostname):
        result = common.get_all_groups_for_host(hostname)
        if result:
            data = {"groups": [host["groupname"] for host in result]}
        else:
            data = {"groups": ""}
        resp = jsonify(data)
        resp.status_code = 200
        return resp


class GetHostsSearchAPI(Resource):
    def get(self, search_term):
        result = common.get_search_hosts(search_term)
        if result:
            data = {"hosts": [host["hostname"] for host in result]}
        else:
            data = {"hosts": ""}
        resp = jsonify(data)
        resp.status_code = 200
        return resp
