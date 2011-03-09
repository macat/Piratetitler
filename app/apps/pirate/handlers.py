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
        return self.render_response('films/page.html', versions=versions, film=film, subtitles=subtitles_out, translate_form=translate_form)
