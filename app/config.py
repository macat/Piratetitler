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
        'apps.admin',
    ],
}

config['tipfy.ext.session'] = {
    'secret_key' : '** secret **',
    'default_backend': 'memcache',
    'cookie_name': 'pirates.session',
}

config['tipfy.ext.auth'] = {
    'user_model': 'apps.users.models.AuthUser',
}

config['tipfy.ext.auth.facebook'] = {
    'api_key':    '** secret **',
    'app_secret': '** secret **',
}

config['tipfy.ext.auth.twitter'] = {
    'consumer_key':    '** secret **',
    'consumer_secret': '** secret **',
}

try:
    from config_local import config as config_ext
    config.update(config_ext)
except:
    pass

