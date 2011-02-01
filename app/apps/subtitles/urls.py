from tipfy import Rule

def get_rules(app):
    rules = [
        Rule('/films/<int:film_id>/versions/<int:version_id>/subtitles/import', endpoint='subtitles/import', handler='apps.subtitles.handlers.ImportHandler'),
    ]

    return rules

