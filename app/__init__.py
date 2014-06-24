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

import flask
import flask.views

app = flask.Flask('app')
app.config.from_pyfile('../config.cfg')

from flask.ext.restful import Resource, Api
api = Api(app)

from app.modules.host.api import GetHostVarsAPI, HostsAPI, GetHostsSearchAPI, GetHostGroupsAPI
from app.modules.group.api import GroupsAPI, GetGroupsSearchAPI, GetGroupVarsAPI, GetGroupChildrenAPI, GetGroupHostsAPI
from app.modules.host.add_host import AddHost
from app.modules.host.get_host import GetHost, GetAllHosts
from app.modules.group.get_group import GetGroup, GetAllGroups
from app.modules.group.add_group import AddGroup
from app.modules.host.edit_host import EditHost, EditHostSubmit
from app.modules.group.edit_group import EditGroup, EditGroupSubmit
#from remove import RemoveGroup, RemoveHost
from remove import Remove

class Main(flask.views.MethodView):
    def get(self):
        return flask.render_template('index.html')

    def post(self):
        pass

api.add_resource(GetHostVarsAPI, '/api/v1.0/hosts/<string:hostname>/vars')
api.add_resource(GetHostGroupsAPI, '/api/v1.0/hosts/<string:hostname>/groups')
api.add_resource(GetHostsSearchAPI, '/api/v1.0/hosts/search/<string:search_term>')
api.add_resource(HostsAPI, '/api/v1.0/hosts')

api.add_resource(GetGroupChildrenAPI, '/api/v1.0/groups/<string:groupname>/children')
api.add_resource(GetGroupVarsAPI, '/api/v1.0/groups/<string:groupname>/vars')
api.add_resource(GetGroupHostsAPI, '/api/v1.0/groups/<string:groupname>/hosts')
api.add_resource(GetGroupsSearchAPI, '/api/v1.0/groups/search/<string:search_term>')
api.add_resource(GroupsAPI, '/api/v1.0/groups')

app.add_url_rule('/',
                view_func=Main.as_view('index'),
                methods=['GET', 'POST'])

app.add_url_rule('/addhost',
                view_func=AddHost.as_view('addhost'),
                methods=['GET', 'POST'])

app.add_url_rule('/gethostinfo',
                view_func=GetHost.as_view('gethostinfo'),
                methods=['GET', 'POST'])

app.add_url_rule('/getallhosts',
                view_func=GetAllHosts.as_view('getallhosts'),
                methods=['POST','GET'])

app.add_url_rule('/edithost',
                view_func=EditHost.as_view('edithost'),
                methods=['GET', 'POST'])

app.add_url_rule('/edithostsubmit',
                view_func=EditHostSubmit.as_view('edithostsubmit'),
                methods=['GET', 'POST'])

app.add_url_rule('/editgroup',
                view_func=EditGroup.as_view('editgroup'),
                methods=['GET', 'POST'])

app.add_url_rule('/editgroupsubmit',
                view_func=EditGroupSubmit.as_view('editgroupsubmit'),
                methods=['GET', 'POST'])

app.add_url_rule('/getgroup',
                view_func=GetGroup.as_view('getgroup'),
                methods=['GET', 'POST'])

app.add_url_rule('/getallgroups',
                view_func=GetAllGroups.as_view('getallgroups'),
                methods=['POST','GET'])

app.add_url_rule('/addgroups',
                view_func=AddGroup.as_view('addgroup'),
                methods=['GET', 'POST'])

app.add_url_rule('/remove',
                view_func=Remove.as_view('remove'),
                methods=['GET', 'POST'])

