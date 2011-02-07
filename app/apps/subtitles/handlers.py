# -*- coding: utf-8 -*-
import re
from tipfy import RequestHandler, redirect, cached_property, render_json_response
from tipfy.ext.jinja2 import render_response
from tipfy.ext.auth import user_required, MultiAuthMixin
from tipfy.ext.session import AllSessionMixins, SessionMiddleware

from apps.subtitles.models import Language, Subtitles, SubtitlesChangeset
from apps.subtitles.forms import SrtImportForm
from apps.films.models import Film, FilmVersion

import logging

class ImportHandler(RequestHandler, MultiAuthMixin, AllSessionMixins):
    middleware = [SessionMiddleware]

    @user_required
    def post(self, film_id, version_id):
        if self.form.validate():
            film = Film.get_by_id(film_id)
            film_version = FilmVersion.get_by_id(version_id)

            lan = Language(name='hun')
            lan.put()

            srt_file = self.request.files.get('srt_file')

            if srt_file:
                logging.info('file')
                logging.info(srt_file.stream)
                logging.info(srt_file.stream.__doc__)
                srt_content = srt_file.read()
                try:
                    srt_content = unicode(srt_content)
                except:
                    import chardet
                    encoding = chardet.detect(srt_content)
                    srt_content = unicode(srt_content.decode(encoding['encoding']))
                    logging.info(encoding)

                srt_content.replace('\r', '')
                srt_lines = import_helper(srt_content)
                subtitle = Subtitles(film=film,
                                    version=film_version,
                                    user=self.auth_current_user.user,
                                    language=lan)
                subtitle.lines = srt_lines
                subtitle.put()


                
                return redirect('/subtitles/%d/edit' % subtitle.key().id())

    @user_required
    def get(self, film_id, version_id):
        return render_response('subtitles/import.html', form=self.form)

    @cached_property
    def form(self):
        return SrtImportForm()


def import_helper(content):
    _srt = re.sub(r'\r\n|\r|\n', '\n', content)
    lines = _srt.strip().split('\n\n')
    ret = []
    for line in lines:
        if line.strip():
            subtitle = line.lstrip().split('\n')
            if len(subtitle) >= 2:
                io = subtitle[1].split('-->')
                io[0] = io[0].strip().split(' ')[0]
                io[0] = re.sub('(\d{2}).(\d{2}).(\d{2}).(\d{3})', '\\1:\\2:\\3,\\4', io[0])
                io[1] = io[1].strip().split(' ')[0]
                io[1] = re.sub('(\d{2}).(\d{2}).(\d{2}).(\d{3})', '\\1:\\2:\\3,\\4', io[1])
                #sub_id ="%s" % int(subtitle[0])
                ret.append((
                    int(time2ms(io[0])), #start
                    int(time2ms(io[1])), #end
                    u'\n'.join(subtitle[2:]), #text
                ))
    return ret
    



def ms2time(ms):
  '''
  >>> ms2time(44592123)
  '12:23:12,123'
  '''
  it = int(ms / 1000)
  ms = ms - it*1000
  ss = it % 60
  mm = ((it-ss)/60) % 60
  hh = ((it-(mm*60)-ss)/3600) % 60
  return "%02d:%02d:%02d,%03d" % (hh, mm, ss, ms)

def time2ms(timeString):
  '''
  >>> time2ms('12:23:12,123')
  44592123
  '''
  ms = 0.0
  p = timeString.replace(',', '.').split(':')
  for i in range(len(p)):
    ms = ms * 60 + float(p[i])
  return int(ms * 1000)

            

class EditHandler(RequestHandler, MultiAuthMixin, AllSessionMixins):
    middleware = [SessionMiddleware]

    def get(self, subtitle_id):
        subtitle = Subtitles.get_by_id(subtitle_id)
        logging.info(subtitle.text)
        return render_response('subtitles/edit.html', subtitle=subtitle)

class ChangeSetHandler(RequestHandler, MultiAuthMixin, AllSessionMixins):
    middleware = [SessionMiddleware]

    def get(self, subtitle_id):
        changeset = SubtitlesChangeset.filter('subtitle =', subtitle_id)
        return render_json_response(changeset)

    def post(self, subtitle_id):
        changeset = SubtitlesChangeset(user=self.auth_current_user.user,
                                       subtitle=subtitle,
                                       text=self.POST.get(text))


        

