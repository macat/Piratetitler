from tipfy import Rule

def get_rules(app):
    rules = [
        Rule('/films', endpoint='film-list', handler='apps.films.handlers.FilmListHandler'),
        Rule('/films/new', endpoint='add-film', handler='apps.films.handlers.NewFilmHandler'),
        Rule('/films/versions', endpoint='filmversion-list', handler='apps.films.handlers.FilmVersionListHandler'),
        Rule('/films/versions/new', endpoint='filmversion-list', handler='apps.films.handlers.NewFilmVersionHandler'),
    ]

    return rules
