from django.contrib import admin

from shop.models import Payment, Order, PromoCode
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


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    pass
