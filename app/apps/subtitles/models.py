# -*- coding: utf-8 -*-
from google.appengine.ext import db
from apps.users.models import User
from apps.films.models import Film, FilmVersion
from rwproperty import getproperty, setproperty

class Language(db.Model):
    name = db.StringProperty(required=True)

def subtitles_encode(lines):
    out = []
    for line in lines:
        out.append(u'%d#%d#%s' % line)
    return out

def subtitles_decode(text):
    ret_lines = []
    for raw_line in text:
        ret_lines.append(raw_line.split('#', 4))
    return ret_lines

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
        if not self._lines: 
            self._lines = subtitles_decode(self.text)
        return self._lines


    @setproperty
    def lines(self, lines):
        self._lines = lines
        self.text = subtitles_encode(lines)

    
    def set_changeset(self, lines, user):
        cache_lines = {}
        for line in lines:
            cache_lines[line[0]] = line

        subtitles_set = SubtitlesChangeSet(text=subtitles_encode(lines),
                                           subtitles=self,
                                           user=user)
        subtitles_set.put()

        l = len(self.lines)
        while l:
            l -= 1
            if self._lines[l][0] in cache_lines:
                self._lines[l] = cache_lines[self._lines[l][0]]
                del cache_lines[self._lines[l][0]]
        #TODO : Handle new lines

            


class SubtitlesChangeSet(db.Model):
    text = db.StringListProperty(required=True)
    subtitles = db.ReferenceProperty(Subtitles, collection_name='revisions', required=True)
    user = db.ReferenceProperty(User, collection_name='subtitle_lines', required=True)
    created = db.DateTimeProperty(auto_now_add=True)


class SrtFile(db.Model):
    name = db.StringProperty(required=True)
    content = db.TextProperty()
    user = db.ReferenceProperty(collection_name='srtfiles', required=False)
    created = db.DateTimeProperty(auto_now_add=True)

