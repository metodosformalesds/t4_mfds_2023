from django import forms

class PayForm(forms.Form):
    card_number = forms.CharField(label="")
    expiration_date
    cvv
    pass
