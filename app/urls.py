# -*- coding: utf-8 -*-
"""
    URL definitions.
"""
from tipfy import import_string


def get_rules(app):
    """Returns a list of URL rules for the application. The list can be
    defined entirely here or in separate ``urls.py`` files.

    :param app:
        The WSGI application instance.
    :return:
        A list of class:`tipfy.Rule` instances.
    """
    #  Here we show an example of joining all rules from the
    # ``apps_installed`` definition set in config.py.
    rules = []

    for app_module in app.get_config('tipfy', 'apps_installed'):
        try:
            # Load the urls module from the app and extend our rules.
            app_rules = import_string('%s.urls' % app_module)
            rules.extend(app_rules.get_rules(app))
        except ImportError, e:
            import logging
            logging.error('Importerror: %s' % e)
            pass

    
    return rules
