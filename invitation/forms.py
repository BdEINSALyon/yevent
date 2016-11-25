from django import forms


class GuestForm(forms.Form):
    first_name = forms.CharField(label='Prénom', max_length=255)
    last_name = forms.CharField(label='Nom', max_length=255)
    email = forms.EmailField(label='Email', max_length=255)
    max_seats = forms.ChoiceField(label='Nombre de places', choices=[(i, i) for i in range(11)])
