from django.conf import settings

from invitation import models
from invitation import security


def user_code(request):
    return {
        'user_code': request.session.get('user_code', ''),
        'google_analytics': settings.GOOGLE_ANALYTICS
    }
