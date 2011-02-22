define(

function() {
  var Service = {
    url: '',
    type: '',
    dataMapper: function(n){
      return {};
    },
    init: function() {
      $.subscribe(this.type+ '/get', $.proxy(this, 'fetchObject'));
    },
    fetchObject: function(id) {
      $.ajax({
        url: this.buildUrl(id), 
        success: $.proxy(this, 'handleData'),
        dataType: 'json'
      });
    },
    buildUrl: function(id) {
      if (typeof id == 'undefined') {
        return this.url;
      }
      return this.url.replace('<id>', id);
    },
    handleData: function(resp) {
      resp = $.map(resp, this.dataMapper);
      $.publish(this.type +'/fetched', [this, resp]);
    }
  };

  return function(config) {
    var o = Object.create(Service);
    $.extend(o, config);
    o.init();
    o.fetchObject();
  };
});
