from tipfy import Rule

def get_rules(app):
    rules = [
        Rule('/films/<int:film_id>', endpoint='film-page', handler='apps.pirate.handlers.FilmPageHandler'),
        Rule('/films/<int:film_id>/versions/<int:version_id>/subtitles-xml', endpoint='subtitles-xml', handler='apps.pirate.handlers.LanguagesXMLHandler'),
        Rule('/films/<int:film_id>/versions/<int:version_id>/subtitles-xml/<string(length=2):default_language>', endpoint='subtitles-xml', handler='apps.pirate.handlers.LanguagesXMLHandler'),
        Rule('/films/<int:film_id>/versions/<int:version_id>/watch', endpoint='watch', handler='apps.pirate.handlers.WatchHandler'),
        Rule('/films/<int:film_id>/versions/<int:version_id>/watch/<string(length=2):default_language>', endpoint='watch', handler='apps.pirate.handlers.WatchHandler'),
        Rule('/', endpoint='film-list', handler='apps.pirate.handlers.FrontPageHandler'),
    ]
    return rules

