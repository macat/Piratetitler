# -*- coding: utf-8 -*-
import logging
from google.appengine.ext import blobstore
from tipfy import RequestHandler, redirect, cached_property, url_for
from tipfy.ext.jinja2 import Jinja2Mixin
from tipfy.ext.auth import user_required, MultiAuthMixin
from tipfy.ext.session import AllSessionMixins, SessionMiddleware
from tipfy.ext.blobstore import BlobstoreDownloadMixin, BlobstoreUploadMixin
from forms import FilmForm, FilmVersionForm
from models import Film, FilmVersion

from apps.subtitles.models import Subtitles



class FilmListHandler(RequestHandler, MultiAuthMixin, AllSessionMixins, Jinja2Mixin):
    middleware = [SessionMiddleware]

    def get(self):
        films = Film.all()
        return self.render_response('films/list.html', films=films)

class FilmPageHandler(RequestHandler, Jinja2Mixin):
    def get(self, film_id):
        film = Film.get_by_id(film_id)
        versions = list(FilmVersion.all().filter('film =', film))
        subtitles = list(Subtitles.all().filter('film =', film))
        subtitles_out = {}
        logging.debug(versions)
        for entry in subtitles:
            if entry.version.key().id() not in subtitles_out:
                subtitles_out[entry.version.key().id()] = []
            subtitles_out[entry.version.key().id()].append(entry)
        return self.render_response('films/page.html', versions=versions, film=film, subtitles=subtitles_out)


class NewFilmHandler(RequestHandler, MultiAuthMixin, AllSessionMixins, Jinja2Mixin):
    middleware = [SessionMiddleware]

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
                user = self.auth_current_user.user
            )
            film.put()
            response = redirect('/films/%d' % film.key().id())
            return response

        return self.get(**kwargs)

    @cached_property
    def form(self):
        return FilmForm(self.request)

class ImageServeHandler(RequestHandler, BlobstoreDownloadMixin, Jinja2Mixin):
    def get(self, **kwargs):
        blob_info = blobstore.BlobInfo.get(kwargs.get('resource'))
        return self.send_blob(blob_info)

class FilmVersionPageHandler(RequestHandler, Jinja2Mixin):
    def get(self, film_id, version_id):
        version = FilmVersion().get_by_id(version_id)
        return self.render_response('versions/page.html', version=version)


class NewFilmVersionHandler(RequestHandler, MultiAuthMixin, AllSessionMixins, Jinja2Mixin):
    middleware = [SessionMiddleware]

    @user_required
    def get(self, **kwargs):
        return self.render_response('versions/new.html', form=self.form)

    @user_required
    def post(self, film_id, **kwargs):
        if self.form.validate():
            film = Film.get_by_id(film_id)
            version = FilmVersion(
                film=film,
                title=self.form.title.data,
                user=self.auth_current_user.user
            )
            version.put()
            return redirect('/films/%d' % film.key().id())
        return self.get(**kwargs)

    @cached_property
    def form(self):
        return FilmVersionForm(self.request)
