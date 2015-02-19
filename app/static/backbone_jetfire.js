
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

var Groups = Backbone.Collection.extend({
  url: '/api/v1.0/groups'
});

// Views
var HostList = Backbone.View.extend ({
  el: '.page',
  render: function() {
    var that = this;
    var hosts = new Hosts();
    hosts.fetch({
      success: function(hosts) {
        var template = _.template($('#host-list-template').html());
        that.$el.html(template({hosts: hosts.models}));
        //console.log(hosts);
      }
    })
  }
});

var AddHost = Backbone.View.extend ({
  el: '.page',
  render: function() {
    var template = _.template($('#addhost-template').html());
    this.$el.html(template);
  },
  events: {
    'submit .add-host-form': 'saveHost'
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


var GroupList = Backbone.View.extend ({
  el: '.page',
  render: function() {
    var template = _.template($('#group-list-template').html());
    this.$el.html(template);
  }
});


// Instantiate view objects
var hostList = new HostList();
var groupList = new GroupList();
var addHost = new AddHost();

//# endviews


// Routes
var Router  = Backbone.Router.extend ({
  routes: {
    '': 'home',
    'hosts': 'hosts',
    'groups': 'groups',
    'addhost': 'addhost',
    'hosts/:id/vars': 'hostvars'
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
  groupList.render();
});
router.on('route:addhost', function(){
  console.log('we have loaded the addhost page');
  addHost.render();
});

//Start Backbone history a necessary step for bookmarkable URL's
Backbone.history.start();
