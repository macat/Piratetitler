from tipfy import Rule

def get_rules(app):
    rules = [
        Rule('/', endpoint='home', handler='apps.pages.handlers.HomeHandler'),
    ]

    return rules

