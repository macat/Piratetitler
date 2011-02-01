# -*- coding: utf-8 -*-
from google.appengine.ext import db
from apps.users.models import User
from apps.films.models import Film, FilmVersion

class Language(db.Model):
    name = db.StringProperty(required=True)


class Subtitle(db.Model):
    film = db.ReferenceProperty(Film, collection_name='subtitles', required=True)
    version = db.ReferenceProperty(FilmVersion, collection_name='subtitles', required=True)
    user = db.ReferenceProperty(User, collection_name='subtitles', required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
    language = db.ReferenceProperty(Language, collection_name='subtitles', required=True)
    translated_from_language = db.ReferenceProperty(Language, collection_name='subtitles_translated', required=False)
    reference = db.SelfReferenceProperty(collection_name='references', required=False)


class Line(db.Model):
    subtitle = db.ReferenceProperty(Subtitle, collection_name='lines', required=True)
    start = db.IntegerProperty(required=True)
    end = db.IntegerProperty(required=True)
    reference = db.SelfReferenceProperty(collection_name='ref', required=False)


class LineRevision(db.Model):
    line = db.ReferenceProperty(Line, collection_name='lines', required=True)
    user = db.ReferenceProperty(User, collection_name='subtitle_lines', required=True)
    text = db.StringProperty(required=True, multiline=True)
    created = db.DateTimeProperty(auto_now_add=True)


class SrtFile(db.Model):
    name = db.StringProperty(required=True)
    content = db.TextProperty()
    user = db.ReferenceProperty(collection_name='srtfiles', required=False)
    created = db.DateTimeProperty(auto_now_add=True)

