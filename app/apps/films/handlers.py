# -*- coding: utf-8 -*-
import logging
from google.appengine.ext import blobstore
from tipfy import RequestHandler, redirect, cached_property, url_for
from tipfy.ext.jinja2 import Jinja2Mixin
from tipfy.ext.auth import user_required

from apps.users.handlers import BaseHandler
from forms import FilmForm, FilmVersionForm
from models import Film, FilmVersion

class NewFilmHandler(BaseHandler):
    """ Add new film page """
    @user_required
    def get(self, **kwargs):
        upload_url = blobstore.create_upload_url(url_for('film/add'))
        return self.render_response('films/new.html', form=self.form, form_action_url=upload_url)

    @user_required
    def post(self, **kwargs):
        if self.form.validate():
            film = Film(
                title = self.form.title.data,
                description = self.form.description.data,
                imdb_link=self.form.imdb_link.data,
                release_year=self.form.release_year.data,
                user = self.auth_current_user.user
            )
            film.put()
            return redirect('/films/%d' % film.key().id())
        return self.get(**kwargs)

    @cached_property
    def form(self):
        return FilmForm(self.request.form)

class NewFilmVersionHandler(BaseHandler):
    @user_required
    def post(self, film_id, **kwargs):
        if self.form.validate():
            film = Film.get_by_id(film_id)
            if film:
                version = FilmVersion(
                    film=film,
                    title=self.form.title.data,
                    user=self.auth_current_user.user
                )
            version.put()
        return redirect('films/%d' % film_id)

    @cached_property
    def form(self):
        return FilmVersionForm(self.request)
