from django.template.defaulttags import register

@register.filter
def amount(dict, key):
    """
    The amount of each dish is stored in a dictionary in request.session.
    To retrieve from a dictionary in a template, a tag like this is required.
    """
    return dict[key][0]
