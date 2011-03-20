from wtforms.form import Form
from wtforms.ext.appengine.fields import ReferencePropertyField
from wtforms import fields, validators
from tipfy.ext.i18n import gettext as _

from apps.subtitles.models import Language

class SrtImportForm(Form):
    srt_file = fields.FileField(_(u'Srt file'))
    language = ReferencePropertyField(_(u'Language'), reference_class=Language, label_attr='name')

class TranslateForm(Form):
    language = ReferencePropertyField(_(u'Language'), reference_class=Language, label_attr='name')
    
    
