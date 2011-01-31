# -*- coding: utf-8 -*-
import logging
from tipfy import RequestHandler, redirect, cached_property
from tipfy.ext.jinja2 import render_response
from tipfy.ext.auth import login_required, AppEngineAuthMixin
from tipfy.ext.session import AllSessionMixins, SessionMiddleware
from forms import FilmForm, FilmVersionForm
from models import Film, FilmVersion



class FilmListHandler(RequestHandler):
    def get(self):
        films = Film.all()
        return render_response('films/list.html', films=films)

class FilmPageHandler(RequestHandler):
    def get(self, film_id):
        film = Film.get_by_id(film_id)
        versions = FilmVersion.all().filter('film =', film)
        return render_response('films/page.html', versions=versions, film=film)

class NewFilmHandler(RequestHandler, AppEngineAuthMixin, AllSessionMixins):
    middleware = [SessionMiddleware]

    @login_required
    def get(self, **kwargs):
        return render_response('films/new.html', form=self.form)

    @login_required
    def post(self, **kwargs):
        if self.form.validate():
            film = Film(
                title = self.form.title.data,
                description = self.form.description.data,
                user = self.auth_session
            )
            film.put()
            return redirect('/films')
        return self.get(**kwargs)

    @cached_property
    def form(self):
        return FilmForm(self.request)



class FilmVersionPageHandler(RequestHandler):
    def get(self, film_id, version_id):
        version = FilmVersion().get_by_id(version_id)
        return render_response('versions/page.html', version=version)

class NewFilmVersionHandler(RequestHandler, AppEngineAuthMixin, AllSessionMixins):
    middleware = [SessionMiddleware]

    @login_required
    def get(self, **kwargs):
        return render_response('versions/new.html', form=self.form)

    @login_required
    def post(self, film_id, **kwargs):
        if self.form.validate():
            film = Film.get_by_id(film_id)
            version = FilmVersion(
                film=film,
                title=self.form.title.data,
                user=self.auth_session
            )
            version.put()
            return redirect('/films/%d' % film.key().id())
        return self.get(**kwargs)

    @cached_property
    def form(self):
        return FilmVersionForm(self.request)
