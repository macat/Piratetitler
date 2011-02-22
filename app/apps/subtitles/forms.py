from wtforms.form import Form
from wtforms import fields, validators
from tipfy.ext.i18n import gettext as _

from apps.subtitles.models import Language

class SrtImportForm(Form):
    srt_file = fields.FileField(_(u'Srt file'))
    language = fields.TextField(_(u'Language'))

    def validate_language(form, field):
        l = Language.get_by_id(field.data)
        if not l:
            raise validators.ValidationError(_(u'Not valid language'))
        

    
    
