from django import forms


class GuestForm(forms.Form):
    first_name = forms.CharField(label='prénom', max_length=255)
    last_name = forms.CharField(label='nom', max_length=255)
    email = forms.EmailField(label='email', max_length=255)
    max_seats = forms.IntegerField(label='nombre de places', min_value=0, max_seats=1600)
