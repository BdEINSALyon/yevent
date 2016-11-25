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
from django.views.generic import TemplateView

from invitation import views

urlpatterns = [
    url(r'^shop/(?P<code>[A-Za-z0-9\-]*)$', views.ShopView.as_view(), name='shop'),
    url(r'^shop/config/(?P<code>[A-Za-z0-9+/=]*)$', views.ConfigView.as_view(), name='config'),
    url(r'^shop/available/(?P<code>[A-Za-z0-9+/=]*)$', views.AvailableView.as_view(), name='available'),
    url(r'^shop/ping/(?P<code>[A-Za-z0-9+/=]*)$', views.PingView.as_view(), name='ping'),
    url(r'^shop/complete/(?P<code>[A-Za-z0-9+/=]*)$', views.CompleteView.as_view(), name='complete')
]
