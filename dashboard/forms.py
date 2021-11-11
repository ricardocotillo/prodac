from django import forms

class OrderForm(forms.Form):
    name = forms.CharField(label='Nombre')
    email = forms.EmailField()
    order = forms.CharField(widget=forms.Textarea, label='Pedido')

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True