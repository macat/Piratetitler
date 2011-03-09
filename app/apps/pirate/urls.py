from tipfy import Rule

def get_rules(app):
    rules = [
        Rule('/films/<int:film_id>', endpoint='film-page', handler='apps.pirate.handlers.FilmPageHandler'),
        Rule('/', endpoint='film-list', handler='apps.pirate.handlers.FrontPageHandler'),
    ]
    return rules

