define(

/**
 * Sets up application-wide functionality, then figures out
 * which page we're on based on the body element's data-page
 * attribute, and loads the appropriate page functionality.
 *
 * @returns {Function} Application init function
 */
function() {
  return function() {
    // load per-page functionality
    require(['pages/SubtitlesEdit']);
  };
}

);

