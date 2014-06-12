from flask.ext.restful import reqparse, abort, Resource, Api
from flask import json
import yaml
from app import common

parser = reqparse.RequestParser()
parser.add_argument('hostname', type=str, location='json')
parser.add_argument('vars', type=str, location='json')
parser.add_argument('groups', type=str, location='json')


class HostsAPI(Resource):
    def get(self):
        result = common.getAllHosts()
        if result:
            data = {"hosts": [host for host in result]}
        else:
            data = {"hosts": ""}
        return data

    def post(self):
        args = parser.parse_args()
        hostname = args['hostname']
        vars = args['vars']
        groups = args['groups']
        exists = [str(item) for item in common.getSearchHosts(hostname)]
        if exists:
            return 'Host already exists', 201

        self.add_host(hostname, vars)
        #self.add_host_togroups(hostname, groups)

        return '', 200

    def add_host(self, hostname, vars):
        try:
            if not vars:
                y = yaml.load('{}')
            else:
                y = yaml.load(vars)
        except yaml.YAMLError, exc:
            print "Yaml syntax error"
        post = {"hostname": hostname,
                "vars": y
        }
        try:
            common.db.hosts.insert(post)
        except:
            pass


    def add_host_togroups(self, hostname, groups):
        selectgroups = [str(group) for group in groups]
        for group in selectgroups:
            common.db.groups.update({'groupname': group}, {'$push':{'hosts': hostname}},upsert=False,multi=False)


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