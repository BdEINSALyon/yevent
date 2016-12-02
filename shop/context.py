from django.conf import settings


def stripe_context(request):
    return {
        'stripe': settings.STRIPE_PUBLISHABLE
    }
