from django.template.defaulttags import register

import datetime

@register.filter
def before30(future):
    """
    Check if the inputted date is less than 30 minutes away from now
    """
    nowplus30 = datetime.datetime.now() + datetime.timedelta(minutes=30)
    print(future, nowplus30, future <= nowplus30)
    return future <= nowplus30
