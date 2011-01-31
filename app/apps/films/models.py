from google.appengine.ext import db

class Film(db.Model):
    title = db.StringProperty(required=True)
    description = db.TextProperty(required=True)
    user = db.UserProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)


class FilmVersion(db.Model):
    film = db.ReferenceProperty(Film, required=True)
    title = db.StringProperty(required=True)
    user = db.UserProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

