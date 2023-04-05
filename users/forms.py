from django import forms
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, ButtonHolder, Submit
from django.utils.translation import gettext_lazy as _


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Email'}),)
    mobile_number = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Mobile Number'}),)
    first_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),)
    last_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),)
    username = forms.CharField( max_length=200, help_text=_( "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."), widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),)
    password1 = forms.CharField(label="Password", required = False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}), help_text=_( "Your password can’t be too similar to your other personal information."
     " Your password must contain at least 8 characters."
     " Your password can’t be a commonly used password."
     " Your password can’t be entirely numeric."),)
    password2 = forms.CharField(label="Password confirmation", required = False, help_text=_( "Enter the same password as before, for verification."), widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Your Password'}),)

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'first_name', 'last_name', 'email', 'mobile_number', 'password1', 'password2']:
            for key, value in self.fields[fieldname].error_messages.items():
                self.fields[fieldname].error_messages['required'] = ''
        self.fields['email'].required = False

        # self.helper = FormHelper(self)
        # # self.helper.form_method = 'POST'
        # self.helper.form_action = '/register/'
        # self.helper.form_class = 'form-horizontal'
        # self.helper.form_show_errors = True
        # self.helper.error_text_inline = False
        # # NEW:
        # self.helper.label_class = 'col-sm-4'
        # self.helper.field_class = 'col-sm-5'

        # self.helper.layout = Layout(
        #     Field('username', css_class="black-fields"),
        #     Field('first_name', css_class='input-sm'),
        #     Field('last_name', css_class='input-sm'),

        #     Field('email', css_class='input-sm'),
        #     Field('password1', css_class='input-sm'),
        #     Field('password2', css_class='input-sm'),
        #     # NEW:
        #     ButtonHolder(
        #         Submit('submit', 'Submit', css_class='btn btn-primary')
        #     )
        # )
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'mobile_number', 'password1', 'password2']
            # print(self.fields[fieldname].help_text)
            # self.fields[fieldname].help_text = None
            # self.fields[fieldname].error_messages = {}
            # print(self.fields[fieldname].error_messages)

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username')
