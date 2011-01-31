from google.appengine.ext import db
from tipfy.ext.auth.model import User as TipfyUser


class User(db.Model):
    created = db.DateTimeProperty(auto_now_add=True)

class AuthUser(TipfyUser):
    user = db.ReferenceProperty(User)

    def put(self, *args, **kwargs):
        if not self.user:
            u = User()
            u.put()
            self.user = u
        super(AuthUser, self).put(*args, **kwargs)
