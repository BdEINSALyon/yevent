from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Guest, Order, Type


@admin.register(Guest)
class GuestAdmin(ImportExportModelAdmin):
    actions = ['send_email']

    def send_email(self, request, queryset):
        pass

    send_email.short_description = "Envoyer le mail d'invitation"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    pass
