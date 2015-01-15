from django import forms
from widgets import BSLeftIconTextInput, BSLeftIconPasswordInput,\
    BSLeftIconEmailInput
from django.contrib.auth import get_user_model 

def l_icon(icon_class, placeholder=None, attrs=None):
    """Shortcut for a left icon text input
    """
    attrs = attrs or {}
    if placeholder: 
        attrs.update(placeholder=placeholder)
    return BSLeftIconTextInput(attrs, icon_class)


def l_icon_pw(icon_class, placeholder=None, attrs=None):
    attrs = attrs or {}
    if placeholder: 
        attrs.update(placeholder=placeholder)
    return BSLeftIconPasswordInput(attrs, icon_class)


def l_icon_email(icon_class, placeholder=None, attrs=None):
    attrs = attrs or {}
    if placeholder: 
        attrs.update(placeholder=placeholder)
    return BSLeftIconEmailInput(attrs, icon_class)


class DivForm(forms.Form):
    """A form that adds an 'as_div()' method which renders each form element
    inside <div></div> tags.
    """
    
    def as_div(self): 
        "Returns this form rendered as HTML <div>s."
        return self._html_output(
            normal_row='<div%(html_class_attr)s>%(errors)s%(label)s %(field)s%(help_text)s</div>',
            error_row='<div>%s</div>',
            row_ender='</div>',
            help_text_html=' <span class="helptext">%s</span>',
            errors_on_separate_row=False)


class SignUpForm(DivForm):
    username = forms.CharField(min_length=4, max_length=100,
                               widget=l_icon('fa fa-user', 'user name'))
    password = forms.CharField(min_length=6, max_length=100,
                               widget=l_icon_pw('fa fa-unlock-alt', 'password'))
    first_name = forms.CharField(min_length=3, max_length=100,
                                widget=l_icon('fa fa-info', 'first name'))
    last_name = forms.CharField(min_length=3, max_length=100,
                                widget=l_icon('fa fa-info', 'last name'))
    email = forms.EmailField(widget=l_icon('fa fa-envelope-o', 'email address'))
    
    def clean(self):
        """Raise a validation error if the username or email address provided
        are already in use. 
        """
        
        cleaned_data = super(SignUpForm, self).clean()
        
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        
        if get_user_model().objects.filter(username=username).exists(): 
            msg = u"This user name is already in use, please select another."
            self.add_error("username", msg)
        if get_user_model().objects.filter(email=email).exists():
            msg = u"This email address is already in use, please select another"
            self.add_error("email", msg)

        return cleaned_data
         
class LogInForm(DivForm):
    username = forms.CharField(min_length=4, max_length=100,
                               widget=l_icon('fa fa-user', 'user name'))
    password = forms.CharField(min_length=6, max_length=100,
                               widget=l_icon('fa fa-unlock-alt', 'password'))
    
