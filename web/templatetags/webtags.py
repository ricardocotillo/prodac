from django import template

register = template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})

@register.filter(name='input')
def input(f):
    attrs = {
        'placeholder': f.label,
    }
    if hasattr(f.field.widget, 'input_type') and f.field.widget.input_type == 'select':
        attrs['class'] = ''
    return f.as_widget(attrs=attrs)

@register.filter(name='hiddeninput')
def hiddeninput(f):
    attrs = {}
    if f.field.widget.input_type == 'file':
        attrs['class'] = 'hidden invisible'
    return f.as_widget(attrs=attrs)