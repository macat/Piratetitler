from tipfy import Rule

def get_rules(app):
    rules = [
        Rule('/films/new', endpoint='film/add', handler='apps.films.handlers.NewFilmHandler'),
        Rule('/films/<int:film_id>/versions/new', endpoint='filmversion-add', handler='apps.films.handlers.NewFilmVersionHandler'),
        Rule('/i/<resource>', endpoint='images/serve', handler='apps.films.handlers.ImageServeHandler'),
    ]

    return rules
