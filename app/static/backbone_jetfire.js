// Collection and models

var Hosts = Backbone.Collection.extend({
  url: '/api/v1.0/hosts'
});

/*var Host = Backbone.Model.extend({
  sync: function (method, model, options) {
    if (method === 'create' || method === 'update') {
      return $.ajax({
        dataType: 'json',
        url: '/api/v1.0/hosts',
        data: {
          hostname: (this.get('hostname') || ''),
          groups: (this.get('groups') || ''),
          hostvars: (this.get('hostvars') || '')
        },
        success: function (data) {
          var newhost = data;
          data.save();
        }
      });
    }
  }
});*/

var Host = Backbone.Model.extend({
  urlRoot: '/api/v1.0/hosts',
  dataType: 'json',
  defaults: {
    hostname: '',
    vars: '',
    groups: []
  }
});

var DeleteHost = Backbone.Model.extend({
  urlRoot: '/api/v1.0/hosts',
  //idAttribute: "id"
});

var Groups = Backbone.Collection.extend({
  url: '/api/v1.0/groups',
  //idAttribute: "groups"
});

var Group = Backbone.Model.extend({
  urlRoot: '/api/v1.0/groups',
  dataType: 'json',
  defaults: {
    groupname: '',
    vars: '',
    children: [],
    hosts: []
  }
});

var DeleteGroup = Backbone.Model.extend({
  urlRoot: '/api/v1.0/groups',
});

var ChildGroups = Backbone.Model.extend({
  urlroot: function(){
    return 'groups/'+this.options.group/+'children';
  }
})
//------------------------------------------------------------------------------

//------------------------------------------------------------------------------
// Views

var HostList = Backbone.View.extend ({
  el: '.page',
  render: function() {
    var self = this;
    var hosts = new Hosts();
    hosts.fetch({
      success: function(hosts) {
        var template = _.template($('#host-list-template').html());
        self.$el.html(template({hosts: hosts.models}));
      }
    })
  }
});

var AddHost = Backbone.View.extend ({
  el: '.page',
  render: function() {
    var self = this;
    var groups = new Groups();
    groups.fetch({
      success: function(groups) {
        var template = _.template($('#addhost-template').html());
        self.$el.html(template({groups: groups.models}));
        //console.log(groups.models);
      }
    });
  },
  events: {
    'click button#addhost-btn': 'saveHost'
  },
  saveHost: function(event) {
    var newhostmodel = new Host ({
      hostname: $('#hostname').val(),
      //groups: $('#groups').val(),
      vars: $('#hostvars').val()
    });
    //console.log(newhostmodel.get('hostvars'));
    newhostmodel.save();
    // stay on the form page
    return false;
  }
});

var AddGroup = Backbone.View.extend ({
  el: '.page',
  render: function() {
    var self = this;
    var hosts = new Hosts();
    var childgroups = new ChildGroups();
    childgroups.fetch({
      success: function(childgroups) {
        console.log('childgroups', childgroups.models)
      }
    });
    hosts.fetch({
      success: function(hosts) {
        var template = _.template($('#addgroup-template').html());
        self.$el.html(template({hosts: hosts.models}));
      }
    });
  },
  events: {
    'click button#addgroup-btn': 'saveGroup'
  },
  saveGroup: function(event) {
    var newgroupmodel = new Group ({
      groupname: $('#groupname').val(),
      //groups: $('#groups').val(),
      vars: $('#groupvars').val()
    });
    console.log(newgroupmodel.get('groupname'));
    newgroupmodel.save();
    // stay on the form page
    return false;
  }
});


/*var RemoveHost = Backbone.View.extend ({
  el: '.page',
  events: {
    'click .remove-host': 'removeHost'
  },
  removeHost: function(event) {
    console.log('entered delete view host' + id);
    //var hostremovemodel = new DeleteHost({id: 'test.philippe'});
    var hostremovemodel = new DeleteHost(id);
    console.log(hostremovemodel)
    hostremovemodel.destroy();
  }
});
*/
var GroupList = Backbone.View.extend ({
  el: '.page',
  //console.log('data from route to view' + groups)
  render: function() {
    var self = this;
    var groups = new Groups();
    groups.fetch({
      success: function(groups) {
        var template = _.template($('#group-list-template').html());
        self.$el.html(template({groups: groups.models}));
      }
    })
  }
});


// Instantiate view objects
var hostList = new HostList();
var groupList = new GroupList();
var addHost = new AddHost();
var addGroup = new AddGroup();
//var removeHost = new RemoveHost();

// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------
// Routes
var Router  = Backbone.Router.extend ({
  routes: {
    '': 'home',
    'hosts': 'hosts',
    'groups': 'groups',
    'addhost': 'addhost',
    'addgroup': 'addgroup',
    'hosts/:id/vars': 'hostvars',
    'hosts/:id': 'removehost',
    'groups/:id': 'removegroup',
    'groups/:id/children': 'childgroups'
  }
});

var router = new Router();
router.on('route:home', function() {
  console.log('we have loaded the home page');
  //hostList.render();
});
router.on('route:hosts', function(){
  console.log('we have loaded the hostslist page');
  hostList.render();
});
router.on('route:groups', function(){
  console.log('we have loaded the groupslist page');
  var groups = new Groups();
  groups.fetch({
    success: function(groups) {
      groups = {groups: groups.models.toJSON}
      console.log(groups)
    }
  })
  //console.log("return groups in route: " + groups.fetch())
  groupList.render();
});
router.on('route:addhost', function(){
  console.log('we have loaded the addhost page');
  addHost.render();
});
router.on('route:removehost', function(id){
  console.log('/api/v1.0/hosts/', id);
  var hostremovemodel = new DeleteHost({id: id});
  hostremovemodel.destroy();
});
router.on('route:addgroup', function(){
  console.log('we loaded the add group pasge');
  // get childgroups
  // var childgroupsmodel = new ChildGroups()
  // childgroups function(id){
    // console.log('trying to get childgroups', id);
    // var childgroupsmodel = new ChildGroups()
  // },
  // end childgroups
  addGroup.render();
});
router.on('route:removegroup', function(id){
  console.log('/api/v1.0/groups/', id);
  var groupremovemodel = new DeleteGroup({id: id});
  groupremovemodel.destroy();
});

// router.on('route:childgroups', function(id){
//   console.log('loaded childgroups', id);
// });

//Start Backbone history a necessary step for bookmarkable URL's
Backbone.history.start();
