from tipfy.ext.session import AllSessionMixins, SessionMiddleware
from tipfy.ext.auth import MultiAuthMixin
from tipfy import RequestHandler

class BaseHandler(RequestHandler, MultiAuthMixin, AllSessionMixins):
    middleware = [SessionMiddleware]
    
