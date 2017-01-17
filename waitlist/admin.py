from django.contrib import admin
from . import models


# Register your models here.
@admin.register(models.WaitingTicket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('owner', 'email', 'phone', 'amount', 'position', 'registered_at')
    ordering = ('registered_at',)
    list_filter = ('owner', 'phone', 'registered_at')

    def email(self, obj):
        return obj.owner.email

admin.site.register(models.WaitingList)
