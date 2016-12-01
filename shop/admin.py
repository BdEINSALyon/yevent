from django.contrib import admin

from ticketing.models import Price, Ticket, OptionPrice


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    pass


@admin.register(OptionPrice)
class OptionPriceAdmin(admin.ModelAdmin):
    pass