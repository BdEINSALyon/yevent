from django.contrib import admin
from .models import Guest, Order, Type


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    pass
