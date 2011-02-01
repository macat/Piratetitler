from wtforms.form import Form
from wtforms import fields, validators
from tipfy.ext.i18n import gettext as _

class SrtImportForm(Form):
    srt_file = fields.FileField(_(u'Srt file'))
    language = fields.TextField(_(u'Language'))

    
    
