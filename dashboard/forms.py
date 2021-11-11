from django import forms

class OrderForm(forms.Form):
    name = forms.CharField(label='Nombre')
    email = forms.EmailField()
    order = forms.CharField(widget=forms.Textarea, label='Pedido')