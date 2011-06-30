# -*- coding: utf-8 -*-

config = {}

config['tipfy'] = {
    'middleware': [
        'tipfy.ext.debugger.DebuggerMiddleware',
        'tipfy.ext.i18n.I18nMiddleware',
    ],
    'apps_installed': [
        'apps.pages',
        'apps.pirate',
        'apps.users',
        'apps.films',
        'apps.subtitles',
    ],
}

config['tipfy.ext.session'] = {
    'secret_key' : '695e67554e442869292e2c2f6648463d',
    'default_backend': 'memcache',
    'cookie_name': 'pirates.session',
}

config['tipfy.ext.auth'] = {
    'user_model': 'apps.users.models.AuthUser',
}

config['tipfy.ext.auth.facebook'] = {
    'api_key':    'f38cc231ef0067901faf127227aeb3f6',
    'app_secret': 'da76185a5286ffea07ed409982172fe1',
}

config['tipfy.ext.auth.twitter'] = {
    'consumer_key':    'mySMPIzpDdv4IRpkAjiaBA',
    'consumer_secret': 'fwE9v4xtF0aEjamR1zUSYtSytFpvezj7Tro9cDWXIM',
}

try:
    from config_local import config as config_ext
    config.update(config_ext)
except:
    pass

