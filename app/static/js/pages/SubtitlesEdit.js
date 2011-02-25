define(
[
  '../views/SubtitleList',
  '../views/SubtitleEdit',
  '../services/ObjectService',
  '../views/ChangeSetSave'
],

function(subtitleListSetup, subtitleEditSetup, objectServiceSetup, changeSetSaveSetup) {
  subtitleListSetup($('#subtitles'));
  subtitleEditSetup();
  objectServiceSetup({
    url: application.conf.objectServiceUrl,
    type: 'subtitles',
    dataMapper: function(n) {
      return {
        start: n[0],
        end: n[1],
        text: n[2] 
      };
    }
  });
  changeSetSaveSetup({
    url: application.conf.changeSetUrl,
    type: 'subtitle',
  });
});
