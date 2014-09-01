#!/usr/bin/python
import pymongo
import json
import sys

# mongod connection
conn = pymongo.Connection('ansible06.demo.local', 27017, replicaSet='rS0')
db = conn['ansible']


# ------------------------------------------------------------------
# get all groups and their values
def getlist():
    inv = {}
    db.groups.ensure_index('groupname')
    grouplist = db.groups.find().distinct("groupname")
    # populate "all" group
    allhosts = [host for host in db.hosts.find().distinct("hostname")]
    inv["all"] = allhosts
    for item in grouplist:
        items = db.groups.find({"groupname": item}, {"_id": 0})
        for item in items:
            #groups = [ item["groupname"] for item in result]
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
        #varlist[host] = item["vars"]
        varlist = item["vars"]
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
