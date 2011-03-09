from tipfy import Rule

def get_rules(app):
    rules = [
        Rule('/films/<int:film_id>/versions/<int:version_id>/subtitles/import', endpoint='subtitles/import', handler='apps.subtitles.handlers.ImportHandler'),
        Rule('/subtitles/<int:subtitles_id>/edit', endpoint='subtitles/edit', handler='apps.subtitles.handlers.EditHandler'),
        Rule('/subtitles/<int:subtitles_id>/export/srt', endpoint='subtitles/export', handler='apps.subtitles.handlers.ExportHandler'),
        Rule('/sc/<int:subtitle_id>', endpoint='subtitles_changeset/api', handler='apps.subtitles.handlers.ChangeSetHandler'),
        Rule('/sl/<int:subtitles_id>', endpoint='subtitle_lines/api', handler='apps.subtitles.handlers.SubtitleLines'),
        Rule('/translate', endpoint='subtitles/translate', handler='apps.subtitles.handlers.TranslateHandler'),
        Rule('/languages/import', endpoint='languages/import', handler='apps.subtitles.handlers.ImportLanguageHandler'),
        Rule('/languages/list', endpoint='languages/list', handler='apps.subtitles.handlers.ListLanguagesHandler'),
    ]

    return rules

