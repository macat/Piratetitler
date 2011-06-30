from google.appengine.ext import db
from apps.users.models import User

class Film(db.Model):
    """
    This model represents a film.
    """
    title = db.StringProperty(required=True)
    description = db.TextProperty(required=True)
    imdb_link = db.LinkProperty(required=False)
    release_year = db.IntegerProperty(required=True)
    user = db.ReferenceProperty(User, required=True)
    created = db.DateTimeProperty(auto_now_add=True)


class FilmVersion(db.Model):
    """
    A film has one or more versions. (for example: 'Director's cut', 'Original cut')
    """
    film = db.ReferenceProperty(Film, required=True)
    title = db.StringProperty(required=True)
    user = db.ReferenceProperty(User, required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    vimeoid = db.StringProperty()

