define(
    
['text!/static/js/views/templates/SubtitleRow.html'],

function(tpl) {
  var list = {
    init: function(el) {
      this.el = el.eq(0);
      this.el.delegate('div.line', 'click', $.proxy(this, 'lineClick'));
      $.subscribe('subtitle/changed', $.proxy(this, 'reloadLine'));
      $.subscribe('subtitles/fetched', $.proxy(this, 'reloadLines'));
    },

    lineClick: function(e) {
      var target = $(e.currentTarget);
      $.publish('subtitle/click', [this, target]);
    },

    reloadLine: function(sender, el) {
      el.empty();
      $(Mustache.to_html(tpl, el.data('subtitle'))).appendTo(el);
    },

    reloadLines: function(sender, lines) {
      this.el.empty();
      for (var i = 0, l = lines.length; i < l; i++) {
        this.addLine(lines[i]);
      }
    },

    addLine: function(lineData) {
      var line = $('<div class="line"></div>').appendTo(this.el);
      $(Mustache.to_html(tpl, lineData)).appendTo(line);
      line.data('subtitle', lineData);
      line.data('subtitle-original', lineData);
    }
  };

  return function(el) {
    list.init(el);
  };

});
