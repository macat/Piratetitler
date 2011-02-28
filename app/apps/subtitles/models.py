# -*- coding: utf-8 -*-
from google.appengine.ext import db
from apps.users.models import User
from apps.films.models import Film, FilmVersion
from rwproperty import getproperty, setproperty

import logging

class Language(db.Model):
    name = db.StringProperty()
    native_name = db.StringProperty()
    iso_code = db.StringProperty()
    right_to_left = db.BooleanProperty(default=False)

    def __str__(self):
        return '%s language' % self.name

def subtitles_encode(lines):
    out = []
    for line in lines:
        try:
            out.append(u'%d#%d#%s' % tuple(line))
        except TypeError, e:
            logging.error(e)
            logging.error(line)
    return out

def subtitles_decode(text):
    ret_lines = []
    for raw_line in text:
        line = raw_line.split('#', 4)
        line[0] = int(line[0])
        line[1] = int(line[1])
        ret_lines.append(line)

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

    
    def set_changeset(self, lines):
        import logging
        changedLines = []
        for line in lines:
            # TODO: optimize it (it's max. line*N iteration, should be max. N)
            logging.debug(line)
            if line['o'] == False:
                if self.insertNewLine(line):
                    changedLines.append(line)
            else:
                if self.changeLine(line):
                    changedLines.append(line)
        if changedLines:
            return changedLines
        else:
            return None

    def inserNewLine(self, line):
        # cache lines
        self_lines = self.lines
        c_line = line['n']
        counter = 0
        for self_line in self_lines:
            if c_line[0] > self_line[0]:
                self_lines.insert(counter, c_line)
                self.lines = self_lines
                return line
            counter += 1
        return None

    def changeLine(self, line):
        import logging
        # cache lines
        self_lines = self.lines

        counter = len(self_lines)
        while counter:
            counter -= 1
            if line['o'][0] == self_lines[counter][0]:
                logging.debug(self_lines[counter][0])
            if line['o'][0] == self_lines[counter][0] and line['o'][1] == self_lines[counter][1]:
                logging.debug('-----')
                logging.debug(counter)
                logging.debug(line['n'])
                self_lines[counter] = line['n']
                self.lines = self_lines
                return line
        return None

                



    def get_times(self):
        lines = self.lines
        return [[x[0], x[1]] for x in lines]

    def __unicode__(self):
        return self.key().id()


            


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

