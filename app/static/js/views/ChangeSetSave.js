define(
function() {
  var saving = {
    url: '',
    type: '',
    _changeSetPool: [],
    _changeSetPoolAge: 0,
    //_savingPool: [],
    init: function() {
      this._changeSetPoolAge = new Date();
      $.subscribe(this.type +'/changed', $.proxy(this, 'handleChange'));
      $.subscribe('closave', $.proxy(this, 'save'));
      $.subscribe('save', $.proxy(this, 'save'));
    },

    handleChange: function(sender, el) {
      var key = $.inArray(el[0], this._changeSetPool);
      if (key >= 0) {
        this._changeSetPool[key] = el[0];
      }
      else {
        this._changeSetPool.push(el[0]);
      }
      if (this._changeSetPool.length > 3) { // || (new Date()) - this._changeSetPoolAge > 60000) {
        this.save();
      }
    },

    save: function() {
      var type = this.type;
      var changeset = $.map(this._changeSetPool, function(el) {
        var o = $(el).data(type +'-original'),
            n = $(el).data(type);
        return {
          'o': [o.start, o.end],
          'n': [n.start, n.end, n.text]
        };
      });
      $.ajax({
        url: this.url,
        type: 'post',
        data: {'changeset': $.toJSON(changeset)}
      });
      this._changeSetPool = [];
      this._changeSetPoolAge = new Date();
    }
  };

  return function(config) {
    var o = Object.create(saving);
    $.extend(o, config);
    o.init();    
  };
});
