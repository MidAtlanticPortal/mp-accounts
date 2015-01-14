# Some BS-friendly widgets

from django.forms.widgets import TextInput

class BSLeftIconTextInput(TextInput):
    """A text input with a bootstrap icon on the left side of the field.
    """
    
    TEMPLATE = """<div class="left-inner-addon">
    <i class="{icon_class}"></i>
    {default_input}
</div>
    """
    
    def __init__(self, attrs=None, icon_class=''):
        attrs = attrs or {}
        attrs.update({'class': 'form-control'})
        self.icon_class = icon_class
        super(BSLeftIconTextInput, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        default_input = super(BSLeftIconTextInput, self).render(name, value, 
                                                                attrs)
        
        return self.TEMPLATE.format(default_input=default_input, 
                                    icon_class=self.icon_class)

class BSLeftIconPasswordInput(BSLeftIconTextInput):
    input_type = 'password'

class BSLeftIconEmailInput(BSLeftIconTextInput):
    input_type = 'email'
