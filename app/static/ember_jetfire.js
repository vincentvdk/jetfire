var Jetfire = Ember.Application.create();

// Routes
Jetfire.Router.map(function() {
  this.resource("home", { path: "/"});
  this.resource("hosts");
  this.resource("groups", {path: "groups"});
});


// Controllers


// Routes
Jetfire.HostsRoute = Ember.Route.extend({
    model: function() {
      return this.store.find('host');
    }
});

//Jetfire.HostRoute = Ember.Route.extend({
//  model: function(params) {
//    return this.store.find('host', params.hostname);
//  }
//});

Jetfire.GroupsRoute = Ember.Route.extend({
  model: function() {
    return [{groupname: 'TESTGROUP1'},{groupname: 'TESTGROUP2'}]
  }
});

// Persitency
// Adapter
Jetfire.HostsAdapter = DS.RESTAdapter.extend ({
  revision: 14,
    host: 'http://localhost:5000'
});

DS.RESTAdapter.reopen({
  namespace: 'api/v1.0'
});

// Adjust response payload
//Jetfire.HostSerializer = DS.RESTSerializer.extend({
//  normalizePayload: function(payload) {
//    return payload;
//  }
//});


// Models

Jetfire.Hosts = DS.Model.extend({
  hosts: DS.attr('string')
});

Jetfire.Host = DS.Model.extend({
  hosts: DS.attr('string')
});
