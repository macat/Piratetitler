from tipfy import Rule

def get_rules(app):
    rules = [
        Rule('/', endpoint='film-list', handler='apps.films.handlers.FilmListHandler'),
        Rule('/films/new', endpoint='film/add', handler='apps.films.handlers.NewFilmHandler'),
        Rule('/films/<int:film_id>', endpoint='film-page', handler='apps.films.handlers.FilmPageHandler'),
        Rule('/films/<int:film_id>/versions/new', endpoint='filmversion-add', handler='apps.films.handlers.NewFilmVersionHandler'),
        Rule('/films/<int:film_id>/versions/<int:version_id>', endpoint='filmversion-list', handler='apps.films.handlers.FilmVersionPageHandler'),
        Rule('/i/<resource>', endpoint='images/serve', handler='apps.films.handlers.ImageServeHandler'),
    ]

    return rules
