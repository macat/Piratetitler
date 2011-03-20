require(
[],
function() {
  $('.hidden-tool-button').click(function(e){
      e.preventDefault();
      $(this).hide();
      $($(this).attr('href')).show();
  });
});
