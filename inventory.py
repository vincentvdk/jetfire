#!/usr/bin/python
import pymongo
import json
import sys

# mongod connection
conn = pymongo.Connection('192.168.122.240', 27017)
db = conn['ansible']


# ------------------------------------------------------------------
# get all groups and their values
def getlist():
    inv = {}
    grouplist = db.groups.find().distinct("groupname")
    for item in grouplist:
        items = db.groups.find({"groupname": item}, {"_id": 0})
        for item in items:
            groupname = str(item["groupname"])
            groupitems = db.groups.find({"groupname": groupname}, {"_id": 0, "groupname": 0})
            for var in groupitems:
                inv[groupname] = var
    print json.dumps(inv, sort_keys=True, indent=2)

# ------------------------------------------------------------------
# get host variables
def getdetails(host):
    varlist = {}
    vars = db.hosts.find({"hostname": host}, {"_id": 0, "hostname": 0})
    for item in vars:
        varlist[host] = item["vars"]
    print json.dumps(varlist, sort_keys=True, indent=2)

# ------------------------------------------------------------------
# command line options
if len(sys.argv) == 2 and (sys.argv[1] == '--list'):
    getlist()

elif len(sys.argv) == 3 and (sys.argv[1] == '--host'):
    host = sys.argv[2]
    getdetails(host)

else:
    print "usage --list or --host <hostname>"
    sys.exit(1)
