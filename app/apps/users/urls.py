# -*- coding: utf-8 -*-
"""
    urls
    ~~~~

    URL definitions.

    :copyright: 2009 by tipfy.org.
    :license: BSD, see LICENSE.txt for more details.
"""
from tipfy import Rule


def get_rules(app):
    """Returns a list of URL rules for the application. The list can be
    defined entirely here or in separate ``urls.py`` files.

    :param app:
        The WSGI application instance.
    :return:
        A list of class:`tipfy.Rule` instances.
    """
    rules = [
        Rule('/auth/login', endpoint='auth/login', handler='apps.users.handlers.LoginHandler'),
        Rule('/auth/logout', endpoint='auth/logout', handler='apps.users.handlers.LogoutHandler'),
        Rule('/auth/signup', endpoint='auth/signup', handler='apps.users.handlers.SignupHandler'),
        Rule('/auth/register', endpoint='auth/register', handler='apps.users.handlers.RegisterHandler'),

        Rule('/auth/facebook', endpoint='auth/facebook', handler='apps.users.handlers.FacebookAuthHandler'),
        Rule('/auth/google', endpoint='auth/google', handler='apps.users.handlers.GoogleAuthHandler'),
        Rule('/auth/twitter', endpoint='auth/twitter', handler='apps.users.handlers.TwitterAuthHandler'),
    ]

    return rules
