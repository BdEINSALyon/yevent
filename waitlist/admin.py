from django.contrib import admin
from . import models
from easy_select2 import select2_modelform

TicketForm = select2_modelform(models.WaitingTicket, attrs={'width': '250px'})


# Register your models here.
@admin.register(models.WaitingTicket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('owner', 'email', 'phone', 'amount', 'position', 'registered_at')
    ordering = ('registered_at',)
    list_filter = ('owner', 'phone', 'registered_at')
    form = TicketForm

    def email(self, obj):
        return obj.owner.email

admin.site.register(models.WaitingList)
