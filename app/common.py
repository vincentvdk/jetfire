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

def hostExists(hostname):
    if db.hosts.find({"hostname": hostname}).count() > 0:
        return True
    return False

def countHosts(filterHostname = None):
    if filterHostname:
        return db.hosts.find({'hostname' : {'$regex' : filterHostname}}).count()
    else:
        return db.hosts.find().count()

def countGroups(filterGroupname = None):
    if filterGroupname:
        return db.groups.find({'groupname' : {'$regex' : filterGroupname}}).count()
    else:
        return db.groups.find().count()

def getAllGroupsForHost(hostname):
    return db.groups.find({"hosts": hostname}, {'groupname': 1, '_id': 0})

def getHostnameInfo(hostname):
    return db.hosts.find({"hostname": hostname}, {'hostname': 0, '_id': 0})

def getPagedHosts(skip, numberOfItems, filterHostname = None):
    if filterHostname:
        return db.hosts.find({'hostname' : {'$regex' : filterHostname}}).skip(skip).limit(numberOfItems)
    else:
        return db.hosts.find().skip(skip).limit(numberOfItems)

def getAllHosts():
    return db.hosts.find().distinct("hostname")

def getAllHostForGroup(groupname):
    return db.groups.find({'groupname': groupname}, {'hosts': 1, '_id': 0})

def getAllChilderenForGroup(groupname):
    return db.groups.find({"groupname": groupname}, {'children': 1, '_id': 0})

def getGroupVariables(groupname):
    return db.groups.find({"groupname": groupname}, {'vars': 1, '_id': 0})

def getPagedGroups(skip, numberOfItems, filterGroupname = None):
    if filterGroupname:
        return db.groups.find({'groupname' : {'$regex' : filterGroupname}}).skip(skip).limit(numberOfItems)
    else:
        return db.groups.find().skip(skip).limit(numberOfItems)

def getAllGroups():
    return db.groups.find().distinct("groupname")

def getGroup(groupname):
    return db.groups.find({"groupname": groupname}, {'groupname': 1, '_id': 0})

def getGroupInfo(groupname):
    return db.groups.find({"groupname": groupname}).distinct("vars")
