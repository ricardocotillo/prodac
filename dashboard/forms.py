from django import forms
from card.models import Card
from dashboard.widgets import CropperWidget, Select2

class OrderForm(forms.Form):
    name = forms.CharField(label='Nombre')
    email = forms.EmailField()
    order = forms.CharField(widget=forms.Textarea, label='Pedido')

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = (
            'name',
            'email',
            'logo',
            'background',
            'description',
            'phone',
            'whatsapp',
            'facebook',
            'address',
            'products',
        )
        widgets = {
            'logo': CropperWidget(),
            'background': CropperWidget(attrs={'data-width': 1920, 'data-height': 1080}),
        }