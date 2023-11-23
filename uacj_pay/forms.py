from django import forms

class PayForm(forms.Form):
    card_number = forms.CharField(label="card_number", max_length=16)
    expiration_date = forms.DateField()
    cvv = forms.CharField(label="cvv", max_length=3)
    
    pass
