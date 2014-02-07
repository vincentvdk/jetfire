#!/usr/bin/python

import flask, flask.views
from app import app

#app = flask.Flask(__name__)
#app.config.from_pyfile('config.cfg')
app.secret_key = "ansible"
# read configuration file

class Main(flask.views.MethodView):
    def get(self):
        return flask.render_template('index.html')

    def post(self):
        pass

# external views
from add_host import AddHost
from get_host import GetHost, GetAllHosts
from get_group import GetGroup, GetAllGroups
from add_group import AddGroup
from edit_host import EditHost, EditHostSubmit
from edit_group import EditGroup, EditGroupSubmit
#from remove import RemoveGroup, RemoveHost
from remove import Remove
#class AddHost(flask.views.MethodView):
#    def get(self):
#        return flask.render_template('addhost.html')

#    def post(self):
#        hostname = str(flask.request.form['add_host'])
#        return hostname


app.add_url_rule('/',
                view_func=Main.as_view('index'),
                methods=['GET', 'POST'])

app.add_url_rule('/addhost',
                view_func=AddHost.as_view('addhost'),
                methods=['GET', 'POST'])

app.add_url_rule('/gethost',
                view_func=GetHost.as_view('gethostinfo'),
                methods=['GET', 'POST'])

app.add_url_rule('/gethosts',
                view_func=GetAllHosts.as_view('getallhosts'),
                methods=['POST'])

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

app.add_url_rule('/getgroups',
                view_func=GetAllGroups.as_view('getallgroups'),
                methods=['POST'])

app.add_url_rule('/addgroups',
                view_func=AddGroup.as_view('addgroup'),
                methods=['GET', 'POST'])

app.add_url_rule('/remove',
                view_func=Remove.as_view('remove'),
                methods=['GET', 'POST'])


#app.add_url_rule('/removehost',
#                view_func=RemoveHost.as_view('removehost'),
#                methods=['GET', 'POST'])


app.debug = True
app.run()
