from tipfy import Rule

def get_rules(app):
    rules = [
        Rule('/films/<int:film_id>/versions/<int:version_id>/subtitles/import', endpoint='subtitles/import', handler='apps.subtitles.handlers.ImportHandler'),
        Rule('/subtitles/<int:subtitle_id>/edit', endpoint='subtitles/edit', handler='apps.subtitles.handlers.EditHandler'),
    ]

    return rules

