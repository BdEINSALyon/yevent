import os

from django.conf.urls import url
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.core.exceptions import ValidationError
from django.forms import forms
from django.shortcuts import render
from import_export.admin import ImportExportModelAdmin

from invitation import email
from .models import Guest, Order, Type
from xlrd import open_workbook


@admin.register(Guest)
class GuestAdmin(ModelAdmin):
    actions = ['send_email', 'send_email_force']
    list_filter = ('email_received',)
    list_display = ('first_name', 'last_name', 'email', 'email_received', 'max_seats')
    # Good but ugly : list_editable = ('email_received', 'max_seats')
    search_fields = ('first_name', 'last_name', 'email')
    change_list_template = 'invitation/admin/change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            url(r'^import/$',
                self.admin_site.admin_view(self.reset_products),
                name='invitation_guest_import'),
        ]
        return my_urls + urls

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

    def reset_products(self, request):
        """
        View
        """
        guests = Guest.objects.all()

        context = {
            'guests': guests
        }

        if request.method == 'POST' or request.method == 'DELETE':
            form = GuestImportForm(request.POST, request.FILES)

            if form.is_valid():
                with open_workbook(file_contents=request.FILES['file'].read()) as wb:
                    for sheet in wb.sheets():
                        number_of_rows = sheet.nrows
                        number_of_columns = sheet.ncols
                        headers = []

                        for row in range(number_of_rows):
                            if row == 0:
                                for col in range(number_of_columns):
                                    headers.append(sheet.cell(row, col).value)
                            else:
                                values = {}
                                for col in range(number_of_columns):
                                    value = sheet.cell(row, col).value
                                    values[headers[col]] = value
                                product = Guest(**values)
                                product.save()

                self.message_user(request, 'Produits importés')
            else:
                self.message_user(request, 'Formulaire invalide')

        else:
            form = GuestImportForm()

        context['form'] = form

        return render(request, 'invitation/admin/import.html', context)


def validate_import_extension(value):
    """
    Credits to http://stackoverflow.com/a/8826854/2758732
    """

    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.xls', '.xlsx']
    if ext not in valid_extensions:
        raise ValidationError('Type de fichier non autorisé !')


class GuestImportForm(forms.Form):
    file = forms.FileField(required=True, label='Fichier', validators=[validate_import_extension])

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    pass
