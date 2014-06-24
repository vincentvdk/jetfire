from flask.ext.restful import reqparse, abort, Resource, Api
from flask import json
from flask import jsonify
import yaml
from app import common

parser = reqparse.RequestParser()
parser.add_argument('hostname', type=str, location='json')
parser.add_argument('vars', type=dict, location='json')
parser.add_argument('groups', type=list, location='json')


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
    for group in selectgroups:
        common.db.groups.update({'groupname': group}, {'$push': {'hosts': hostname}}, upsert=False, multi=False)


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
        args = parser.parse_args()
        hostname = args['hostname']
        ansiblevars = args['vars']
        groups = args['groups']
        exists = [str(item) for item in common.getSearchHosts(hostname)]
        if exists:
            return 'Host already exists', 201

        add_host(hostname, ansiblevars)
        add_host_togroups(hostname, groups)

        return '', 200

    def put(self):
        args = parser.parse_args()
        hostname = args['hostname']
        ansiblevars = args['vars']
        groups = args['groups']
        delete_host(hostname)
        add_host(hostname, ansiblevars)
        add_host_togroups(hostname, groups)
        return '', 200

    def delete(self):
        args = parser.parse_args()
        hostname = args['hostname']
        delete_host(hostname)
        return '', 200


class GetHostVarsAPI(Resource):
    def get(self, hostname):
        result = common.getHostnameInfo(hostname)
        if result:
            ansiblevars = [host["vars"] for host in result]
            data = {"vars": ansiblevars}
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
