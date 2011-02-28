from tipfy.ext.session import AllSessionMixins, SessionMiddleware
from tipfy.ext.auth import MultiAuthMixin
from tipfy import RequestHandler
from tipfy.ext.jinja2 import Jinja2Mixin

class BaseHandler(RequestHandler, MultiAuthMixin, AllSessionMixins, Jinja2Mixin):
    middleware = [SessionMiddleware]
    
