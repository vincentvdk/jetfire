# Jetfire is an Ansible inventory tool
# Copyright (c) 2013 by Vincent Van der Kussen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import os
import pymongo
from app import app

SECRET_KEY = os.getenv("SECRET_KEY", app.config['SECRET_KEY'])

# establish connection with mongodb
dbserver = os.getenv("MONGOSRV", app.config['MONGOSRV'])
database = os.getenv("DATABASE", app.config['DATABASE'])
dbserverport = os.getenv("MONGOPORT", app.config['MONGOPORT'])

conn = pymongo.Connection(dbserver, dbserverport)
db = conn[database]
db.groups.ensure_index('groupname')


def host_exists(hostname):
    if db.hosts.find({"hostname": hostname}).count() > 0:
        return True
    return False


def count_hosts(filter_hostname=None):
    if filter_hostname:
        return db.hosts.find({'hostname': {'$regex': filter_hostname}}).count()
    else:
        return db.hosts.find().count()


def count_groups(filter_groupname=None):
    if filter_groupname:
        return db.groups.find({'groupname': {'$regex': filter_groupname}}).count()
    else:
        return db.groups.find().count()


def get_all_groups_for_host(hostname):
    return db.groups.find({"hosts": hostname}, {'groupname': 1, '_id': 0})


def get_hostname_info(hostname):
    return db.hosts.find({"hostname": hostname}, {'hostname': 0, '_id': 0})


def get_search_hosts(search_term):
    return db.hosts.find({'hostname': {'$regex': search_term}})


def get_paged_hosts(skip, number_of_items, filter_hostname=None):
    if filter_hostname:
        return db.hosts.find({'hostname': {'$regex': filter_hostname}}).skip(skip).limit(number_of_items)
    else:
        return db.hosts.find().skip(skip).limit(number_of_items)


def get_all_hosts():
    return db.hosts.find().distinct("hostname")


def get_all_host_for_group(groupname):
    return db.groups.find({'groupname': groupname}, {'hosts': 1, '_id': 0})


def get_all_children_for_group(groupname):
    return db.groups.find({"groupname": groupname}, {'children': 1, '_id': 0})


def get_group_variables(groupname):
    return db.groups.find({"groupname": groupname}, {'vars': 1, '_id': 0})


def get_paged_groups(skip, number_of_items, filter_groupname=None):
    if filter_groupname:
        return db.groups.find({'groupname': {'$regex': filter_groupname}}).skip(skip).limit(number_of_items)
    else:
        return db.groups.find().skip(skip).limit(number_of_items)


def get_all_groups():
    return db.groups.find().distinct("groupname")


def get_group(groupname):
    return db.groups.find({"groupname": groupname}, {'groupname': 1, '_id': 0})


def get_group_info(groupname):
    return db.groups.find({"groupname": groupname}).distinct("vars")


def get_search_groups(search_term):
    return db.groups.find({'groupname': {'$regex': search_term}})

