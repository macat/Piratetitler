# -*- coding: utf-8 -*-
import re
from django.utils import simplejson
from tipfy import redirect, cached_property, render_json_response, Response
from tipfy.ext.jinja2 import render_response
from tipfy.ext.i18n import gettext as _
from tipfy.ext.auth import user_required, MultiAuthMixin

from apps.subtitles.models import Language, Subtitles, SubtitlesChangeSet
from apps.subtitles.forms import SrtImportForm
from apps.films.models import Film, FilmVersion
from apps.utils import BaseHandler

import logging

class ImportHandler(BaseHandler):
    @user_required
    def post(self, film_id, version_id):
        if self.form.validate():
            film = Film.get_by_id(film_id)
            film_version = FilmVersion.get_by_id(version_id)

            lan = Language.get(self.request.form.get('language'))

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
                
        return self.get(film_id, version_id)

    @user_required
    def get(self, film_id, version_id):
        return render_response('subtitles/import.html', form=self.form)

    @cached_property
    def form(self):
        return SrtImportForm(self.request.form)


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

def format_line(line):
    out = {
        'n': [int(line['n'][0]), int(line['n'][1]), unicode(line['n'][2])]
    }
    if line['o'] == False:
        out['o'] = False
    else:
        out['o'] = [int(line['o'][0]), int(line['o'][1])]

    return out
            

class EditHandler(BaseHandler):
    def get(self, subtitles_id):
        subtitles = Subtitles.get_by_id(subtitles_id)
        return render_response('subtitles/edit.html', subtitles=subtitles)

class SubtitleLines(BaseHandler):
    def get(self, subtitles_id):
        subtitles = Subtitles.get_by_id(subtitles_id)
        return render_json_response(subtitles.lines)

class ChangeSetHandler(BaseHandler):
    @user_required
    def get(self, subtitle_id):
        changeset = SubtitlesChangeSet.filter('subtitle =', subtitle_id)
        return render_json_response(changeset)

    @user_required
    def post(self, subtitle_id):
        subtitles = Subtitles.get_by_id(subtitle_id);
        if subtitles:
            changeset = map(format_line, simplejson.loads(self.request.form.get('changeset')))
            changedLines = subtitles.set_changeset(changeset)
            logging.debug(changedLines)
            if changedLines:
                changeset = SubtitlesChangeSet(
                    text=[simplejson.dumps(x) for x in changedLines],
                    subtitles=subtitles,
                    user=self.auth_current_user.user
                )
                changeset.put()
                subtitles.put()
                return render_json_response({'status': 'ok'})
            else: 
                return render_json_response({'status': 'error', 'message': _('Error happened during the saving process')})
        else:
            return render_json_response({'status': 'error', 'message': _('Not valid Subtitles ID')})

class TranslateHandler(BaseHandler):
    def post(self):
        subtitles = Subtitles.get_by_id(int(self.request.form.get('id')))
        if subtitles:
            times = subtitles.get_times()
            language = Language.get(self.request.form.get('language'));
            new_subtitles = Subtitles(
                film=subtitles.film,
                version=subtitles.version,
                user=self.auth_current_user.user,
                language=language,
                translated_from_language=subtitles.language,
                reference=subtitles,
            )
            empty_lines = [[x[0], x[1], ''] for x in times]
            new_subtitles.lines = empty_lines
            new_subtitles.put()
            return self.redirect_to('subtitles/edit', subtitles_id=new_subtitles.key().id())


class ExportHandler(BaseHandler):
    def get(self, subtitles_id):
        subtitles = Subtitles.get_by_id(int(subtitles_id))
        if subtitles:
            out = ""
            for line in subtitles.lines:
                out += ms2time(line[0]) + '\n'
                out += ms2time(line[1]) + '\n'
                out += line[2] + '\n\n'
            filename = subtitles.film.title + '-' + subtitles.version.title + '-' + subtitles.language.name + '.srt'
            response = Response(out,
                    headers=[('Content-Type', 'plain/text; charset=utf-8',),
                    ('Content-Disposition', 'Attachment; filename=%s' % filename,),
                    ('Pragma', 'no-cache',),]
            )
            return response
            

                
            
        
        

