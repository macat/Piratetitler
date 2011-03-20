define(
[
  '../views/SubtitleList',
  '../views/SubtitleEdit',
  '../services/ObjectService',
  '../views/ChangeSetSave'
],

function(subtitleListSetup, subtitleEditSetup, objectServiceSetup, changeSetSaveSetup) {
  var dataMapper = function(n){
      return {
        start: n[0],
        end: n[1],
        text: n[2] 
      };
  };
  subtitleListSetup($('#subtitles'));
  subtitleEditSetup();
  objectServiceSetup({
    url: application.conf.objectServiceUrl,
    type: 'subtitles',
    dataMapper: dataMapper
  });
  if (application.conf.objectReferenceServiceUrl) {
    $.subscribe('subtitles/fetched', function(sender, lines){
      objectServiceSetup({
        url: application.conf.objectReferenceServiceUrl,
        type: 'subtitles-reference',
        dataMapper: dataMapper
      });
    });
  }
  changeSetSaveSetup({
    url: application.conf.changeSetUrl,
    type: 'subtitle'
  });
  $(window).unload(function(e){
    $.publish('closing', [this]);
  });
  $('#save-button').click(function(e){
    e.preventDefault();
    $.publish('save', [this]);
  });
});
