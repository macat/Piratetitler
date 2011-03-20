import logging
from apps.users.handlers import BaseHandler
from apps.films.models import Film, FilmVersion
from apps.subtitles.models import Subtitles
from apps.subtitles.forms import TranslateForm

class FrontPageHandler(BaseHandler):
    def get(self):
        films = Film.all()
        return self.render_response('films/list.html', films=films)

class FilmPageHandler(BaseHandler):
    def get(self, film_id):
        film = Film.get_by_id(film_id)
        versions = list(FilmVersion.all().filter('film =', film))
        subtitles = list(Subtitles.all().filter('film =', film))
        subtitles_out = {}
        translate_form = TranslateForm()
        logging.info(translate_form.language)
        for entry in subtitles:
            if entry.version.key().id() not in subtitles_out:
                subtitles_out[entry.version.key().id()] = []
            subtitles_out[entry.version.key().id()].append(entry)
        return self.render_response('films/page.html', 
                                    versions=versions, 
                                    film=film, 
                                    subtitles=subtitles_out, 
                                    translate_form=translate_form)


class LanguagesXMLHandler(BaseHandler):
    '''
    It serves an XML file for the Flash client.
    The XML contains all the languages for a Film version.
    '''
    def get(self, film_id, version_id, default_language=None):
        version = FilmVersion.get_by_id(version_id)
        subtitles = list(Subtitles.all().filter('version =', version))
        if len(subtitles) == 0:
            return self.abort(code=404)
        default = subtitles[0].language.iso_code
        if default_language:
            for entry in subtitles:
                if entry.language.iso_code == default_language:
                    default = default_language
                    break


        return self.render_response('subtitles/languages.xml', default=default, version=version, subtitles=subtitles)

class WatchHandler(BaseHandler):
    def get(self, film_id, version_id, default_language=None):
        version = FilmVersion.get_by_id(version_id)
        return self.render_response('films/watch.html', default_language=default_language, version=version)

