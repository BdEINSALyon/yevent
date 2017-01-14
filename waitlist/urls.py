from django.conf.urls import url

from waitlist.views import ListWaitRegistrations, CreateWaitRegistration, DeleteWaitRegistration

urlpatterns = [
    url(r'^waitlist$', ListWaitRegistrations.as_view(), name='waitlist'),
    url(r'^waitlist/register$', CreateWaitRegistration.as_view(), name='register_waitlist'),
    url(r'^waitlist/leave$', DeleteWaitRegistration.as_view(), name='leave_waitlist')
]
