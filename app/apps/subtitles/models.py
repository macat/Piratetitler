# -*- coding: utf-8 -*-
from google.appengine.ext import db
from apps.users.models import User
from apps.films.models import Film, FilmVersion
from rwproperty import getproperty, setproperty

class Language(db.Model):
    name = db.StringProperty(required=True)


class Subtitles(db.Model):
    film = db.ReferenceProperty(Film, collection_name='subtitles', required=True)
    version = db.ReferenceProperty(FilmVersion, collection_name='subtitles', required=True)
    user = db.ReferenceProperty(User, collection_name='subtitles', required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
    language = db.ReferenceProperty(Language, collection_name='subtitles', required=True)
    translated_from_language = db.ReferenceProperty(Language, collection_name='subtitles_translated', required=False)
    reference = db.SelfReferenceProperty(collection_name='references', required=False)
    text = db.StringListProperty(required=True)

    _lines = []

    @getproperty
    def lines(self):
        if self._lines: return self._lines

        ret_lines = []
        for raw_line in self.text:
            ret_lines.append(raw_line.split('#', 4))
        self._lines = ret_lines
        return ret_lines

    @setproperty
    def lines(self, lines):
        self._lines = lines
        self.text = []

        for line in lines:
                self.text.append(u'%d#%d#%s' % line)
    
    def set_changeset(self, lines):
        cache_lines = {}
        for line in lines:
            cache_lines[line[0]] = line

        changeset = []
        for line in self.lines:
            if line[0] in cache_lines:
                line = cache_lines[line[0]]
                del cache_lines[line[0]]
            if cache_lines.keys()[0][0] > line[0]:
                #TODO : finish it

            


class SubtitlesChangeSet(db.Model):
    text = db.StringListProperty(required=True)
    subtitle = db.ReferenceProperty(Subtitles, collection_name='revisions', required=True)
    user = db.ReferenceProperty(User, collection_name='subtitle_lines', required=True)
    created = db.DateTimeProperty(auto_now_add=True)


class SrtFile(db.Model):
    name = db.StringProperty(required=True)
    content = db.TextProperty()
    user = db.ReferenceProperty(collection_name='srtfiles', required=False)
    created = db.DateTimeProperty(auto_now_add=True)

