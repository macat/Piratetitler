define(
['text!/static/js/views/templates/SubtitleEditor.html'],
function(tpl) {
  var edit = {
    _editEl: null,
    init: function() {
      $.subscribe('subtitle/click', $.proxy(this, 'editLine'));
      $.subscribe('closing', $.proxy(this, 'closeEditLine'));
    },
    editLine: function(sender, target) {

      if (this._editEl) {
        if (target == this._editEl) {
          return;
        }
        this._editEl.data('blocked', false);
        this.saveText();
        $.publish('subtitle/changed', [this, this._editEl]);
      }
      this._editEl = target;
      target.data('blocked', true);
      target.html(Mustache.to_html(tpl, target.data('subtitle')));
    },

    closeEditLine: function(sender) {
      if (this._editEl) {
        this._editEl.data('blocked', false);
        this.saveText();
        $.publish('subtitle/changed', [this, this._editEl]);
      }
    },

    saveText: function() {
      var line = this._editEl.data('subtitle');
      line.text = this._editEl.find('textarea').val();
      this._editEl.data('subtitle', line);
    }
  };

  return function() {
    edit.init();
  }
}
)
