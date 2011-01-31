from tipfy.ext.wtforms import Form
from wtforms.ext.appengine.db import model_form
from models import Film, FilmVersion

FilmForm = model_form(model=Film, 
                      base_class=Form, 
                      exclude=['created', 'user'])

FilmVersionForm = model_form(model=FilmVersion, 
                      base_class=Form, 
                      exclude=['film', 'created', 'user'])
