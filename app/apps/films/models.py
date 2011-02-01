from google.appengine.ext import db
from apps.users.models import User

class Film(db.Model):
    title = db.StringProperty(required=True)
    description = db.TextProperty(required=True)
    user = db.ReferenceProperty(User, required=True)
    created = db.DateTimeProperty(auto_now_add=True)


class FilmVersion(db.Model):
    film = db.ReferenceProperty(Film, required=True)
    title = db.StringProperty(required=True)
    user = db.ReferenceProperty(User, required=True)
    created = db.DateTimeProperty(auto_now_add=True)

