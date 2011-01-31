# -*- coding: utf-8 -*-
"""
    config
    ~~~~~~

    Configuration settings.

    :copyright: 2009 by tipfy.org.
    :license: BSD, see LICENSE for more details.
"""
config = {}

# Configurations for the 'tipfy' module.
config['tipfy'] = {
    # Enable debugger. It will be loaded only in development.
    'middleware': [
        'tipfy.ext.debugger.DebuggerMiddleware',
    ],
    # Enable the Hello, World! app example.
    'apps_installed': [
        'apps.pages',
        'apps.users',
        'apps.films',
    ],
}

config['tipfy.ext.session'] = {
    'secret_key' : 'just_dev_testaf03jldksajfldskjfS',
}

config['tipfy.ext.auth.facebook'] = {
    'api_key':    'd5c36704dd4be59402db6f2f2b3a2275',
    'app_secret': 'c9a452a4dcad9a8548365a5a0cc4ee18',
}

config['tipfy.ext.auth.twitter'] = {
    'consumer_key':    'xedb3l2ON2Lqe5lPKcgtAA',
    'consumer_secret': '35tVdqF4iEdNH9kfUBVORxZZGacFzdhwddMpP3Ig',
}
