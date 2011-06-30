from tipfy.ext.wtforms import Form
from wtforms.ext.appengine.db import model_form
from models import Film, FilmVersion
from tipfy.ext.i18n import gettext as _

_FilmForm = model_form(model=Film, 
                       base_class=Form, 
                       only=['title', 'description', 'imdb_link', 'release_year'])

class FilmForm(_FilmForm):
    """
    Form for Film model
    """
    descriptions = {
        'title': _('Title of film'), 
        'description': _('Short description about the film'),
        'imdb_link': _('Link to IMBd page'),
        'release_year': _('When was it released?'),
    }
    def __init__(self, *args, **kwargs):
        super(FilmForm, self).__init__(*args, **kwargs)
        for key in self.descriptions.keys():
            if key in self._fields:
                self._fields[key].description = self.descriptions[key]

        

FilmVersionForm = model_form(model=FilmVersion, 
                      base_class=Form, 
                      exclude=['film', 'created', 'user'])
