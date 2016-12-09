from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from invitation import email
from .models import Guest, Order, Type


@admin.register(Guest)
class GuestAdmin(ImportExportModelAdmin):
    actions = ['send_email', 'send_email_force']
    list_filter = ('email_received',)
    list_display = ('first_name', 'last_name', 'email', 'email_received', 'max_seats')
    # Good but ugly : list_editable = ('email_received', 'max_seats')
    search_fields = ('first_name', 'last_name', 'email')

    def send_email(self, request, queryset):
        count = 0
        for guest in queryset.all():
            # noinspection PyBroadException
            try:
                if not guest.email_received:
                    email.send_email(guest)
                count += 1
            except:
                pass
        self.message_user(request, "{} email(s) envoyé à {} personne(s)".format(count, queryset.count()))

    def send_email_force(self, request, queryset):
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
    send_email_force.short_description = "Forcer l'envoie du mail d'invitation"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    pass
