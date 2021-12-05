from django.forms.widgets import Widget, Input, ClearableFileInput
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper

class MultipleDatesWidget(Widget):
    template_name = 'components/widgets/multiple_dates_widget.html'

    class Media:
        js = ('js/forms.js',)

class QuillWidget(Widget):
    template_name = 'components/widgets/quill.html'

    class Media:
        js = ('js/forms.js',)

class ColorInput(Input):
    input_type = 'color'

class CropperWidget(ClearableFileInput):
    template_name = 'components/widgets/cropper_file_input.html'

    class Media:
        js = ('js/forms.js',)

class Select2(RelatedFieldWidgetWrapper):
    template_name = 'components/widgets/select2.html'