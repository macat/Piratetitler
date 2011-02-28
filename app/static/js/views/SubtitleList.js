define(
    
['text!/static/js/views/templates/SubtitleRow.html'],

function(tpl) {
  var list = {
    init: function(el) {
      this.el = el.eq(0);
      this.el.delegate('div.line', 'click', $.proxy(this, 'lineClick'));
      $.subscribe('subtitle/changed', $.proxy(this, 'reloadLine'));
      $.subscribe('subtitles/fetched', $.proxy(this, 'reloadLines'));
      $.subscribe('subtitles-reference/fetched', $.proxy(this, 'handleFetchedReferences'));
    },

    lineClick: function(e) {
      var target = $(e.currentTarget);
      if (target.data('blocked') != true) {
        $.publish('subtitle/click', [this, target]);
      }
    },

    reloadLine: function(sender, el) {
      el.empty();
      $(Mustache.to_html(tpl, el.data('subtitle'))).appendTo(el);
      var text = el.find('.text');
      text.html(text.text().replace(/\n/, '<br/>'));
      var reference = el.data('subtitle-reference');
      if (reference) {
        el.find('.subtitle-reference').html(reference.text.replace(/\n/, '<br/>'));
      }
    },

    reloadLines: function(sender, lines) {
      this.el.empty();
      for (var i = 0, l = lines.length; i < l; i++) {
        this.addLine(lines[i]);
      }
    },

    handleFetchedReferences: function(sender, lines) {
      var el = null;
      for (var i = 0, l = lines.length; i < l; i++) {
        el = $('#subtitle-'+ lines[i].start +'-'+ lines[i].end);
        if (el) {
          el.find('.subtitle-reference').html(lines[i].text.replace(/\n/, '<br/>'));
          el.data('subtitle-reference', lines[i]);
        }
      }
    },

    addLine: function(lineData) {
      var line = $('<div class="line"></div>').appendTo(this.el);
      line.data('subtitle', lineData);
      line.data('subtitle-original', lineData);
      line.attr('id', 'subtitle-'+ lineData.start +'-'+ lineData.end);

      var context = {
        'start': this.ms2time(lineData.start),
        'end': this.ms2time(lineData.end),
        'text': lineData.text.replace(/\n/, '<br/>')
      };
      $(Mustache.to_html(tpl, context)).appendTo(line);
    },
    ms2time: function(ms) {
      it = ms / 1000
      ms = ms - it*1000
      ss = it % 60
      mm = ((it-ss)/60) % 60
      hh = ((it-(mm*60)-ss)/3600) % 60
      return sprintf("%02d:%02d:%02d,%03d", hh, mm, ss, ms);
    }
  };

  return function(el) {
    list.init(el);
  };

});
