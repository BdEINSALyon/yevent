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

from shop import views

urlpatterns = [
    url(r'^ongoing$', views.CartSelectionView.as_view(), name='shop.ongoing'),
    url(r'^questions$', views.CartQuestionView.as_view(), name='shop.questions'),
    url(r'^payment$', views.CartPaymentView.as_view(), name='shop.payment'),
    url(r'^paid', views.CartPaidView.as_view(), name='shop.paid'),
]
