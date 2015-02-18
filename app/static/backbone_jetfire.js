
var Hosts = Backbone.Collection.extend({
  url: '/api/v1.0/hosts'
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

// Routes
var Router  = Backbone.Router.extend ({
  routes: {
    '': 'home',
    'hosts': 'hosts',
    'groups': 'groups'
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


//Start Backbone history a necessary step for bookmarkable URL's
Backbone.history.start();
