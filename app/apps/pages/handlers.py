# -*- coding: utf-8 -*-
from tipfy import RequestHandler
from tipfy.ext.jinja2 import render_response


class HomeHandler(RequestHandler):
    """ Home page """
    def get(self):
        return render_response('pages/home.html')
