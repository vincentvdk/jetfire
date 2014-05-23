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

from add_host import AddHost
from get_host import GetHost, GetAllHosts
from get_group import GetGroup, GetAllGroups
from add_group import AddGroup
from edit_host import EditHost, EditHostSubmit
from edit_group import EditGroup, EditGroupSubmit
#from remove import RemoveGroup, RemoveHost
from remove import Remove

class Main(flask.views.MethodView):
    def get(self):
        return flask.render_template('index.html')

    def post(self):
        pass

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
