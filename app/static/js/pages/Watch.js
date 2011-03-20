require(
['https://ajax.googleapis.com/ajax/libs/swfobject/2.2/swfobject.js'],
function() {
  if (window.application.conf && window.application.conf.vimeoId) {
    // VimeoSrtPlayer options
    var flashVars = {
      swfId: 'VimeoSrtPlayer', // must match the id of the swf object!!!!
      vimeoId: window.application.conf.vimeoId, 
      srt: window.application.conf.srtUrl,
      localization: window.application.conf.srtXmlUrl,
      srtFontSize: 14
    }; 
    //  Default swf attributes
    var attributes = {
      bgcolor:"#000000" ,
      id:"VimeoSrtPlayer" ,
      name:"VimeoSrtPlayer" ,
      allowScriptAccess:"always",
      allowFullScreen:"true"
    };
     
    // Default swf params
    var params = {
      wmode: "window"
    };
     
    swfobject.embedSWF("/static/swf/VimeoSrtPlayer.swf?time="+new Date().getTime(), "watch-container", "400", "225", "10.0.0", "/static/swf/expressInstall.swf", flashVars, params, attributes);
  }
}
)
