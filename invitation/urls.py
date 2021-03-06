"""yevent URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from invitation import ping
from invitation import views

urlpatterns = [
    url(r'^shop/(?P<code>[A-Za-z0-9\-]*)$', views.ShopView.as_view(), name='shop'),
    url(r'^shop/config/(?P<code>[A-Za-z0-9+/=]*)$', views.ConfigView.as_view(), name='config'),
    url(r'^shop/available/(?P<code>[A-Za-z0-9+/=]*)$', views.AvailableView.as_view(), name='available'),
    url(r'^shop/ping/(?P<code>[A-Za-z0-9+/=]*)$', views.PingView.as_view(), name='ping'),
    url(r'^shop/complete/(?P<code>[A-Za-z0-9+/=]*)$', views.CompleteView.as_view(), name='complete'),
    url(r'^invite/(?P<code>[A-Za-z0-9+/=\-]*)$', views.InviteView.as_view(), name='invite'),
    url(r'^email/(?P<code>[A-Za-z0-9+/=\-]*)$', views.EmailView.as_view(), name='email'),
    url(r'^yurplan_webhook$',  csrf_exempt(views.WebhookView.as_view()), name='webhook'),
    url(r'^shop/orders/(?P<id>YPTB[0-9]+)\.json$',  csrf_exempt(views.OrderApiView.as_view()), name='orders_api'),
    url(r'^ping$', ping.ping, name='ping'),
    url(r'^halt$', ping.halt, name='halt')
]
