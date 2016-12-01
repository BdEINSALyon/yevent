from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from invitation import email
from .models import Guest, Type


@admin.register(Guest)
class GuestAdmin(ImportExportModelAdmin):
    actions = ['send_email']

    def send_email(self, request, queryset):
        count = 0
        for guest in queryset.all():
            # noinspection PyBroadException
            try:
                email.send_email(guest)
                count += 1
            except:
                pass
        self.message_user(request, "{} email(s) envoyé à {} personne(s)".format(count, queryset.count()))

    send_email.short_description = "Envoyer le mail d'invitation"


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    pass
