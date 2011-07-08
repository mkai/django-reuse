from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from registration.forms import RegistrationFormUniqueEmail

# Source: http://djangosnippets.org/snippets/686/
class EmailAddressTermsOfServiceRegistrationForm(RegistrationFormUniqueEmail):
    """
    A registration form that only requires the user to enter their e-mail 
    address and password. The username is automatically generated
    This class requires django-registration to extend the 
    RegistrationFormUniqueEmail
    """ 
    # add hidden username field
    username = forms.CharField(widget=forms.HiddenInput, required=False)

    # add TOS field
    tos = forms.BooleanField(widget=forms.CheckboxInput(),
                             label=_(u'I have read and agree to the Terms of Service.'),
                             error_messages={'required': _("You must agree to the terms to register.")})

    def clean_username(self):
        "This function is required to overwrite an inherited username clean"
        return self.cleaned_data['username']

    def clean(self):
        if not self.errors:
            self.cleaned_data['username'] = '%s%s' % (self.cleaned_data['email'].split('@',1)[0], User.objects.count())
        super(EmailAddressTermsOfServiceRegistrationForm, self).clean()
        return self.cleaned_data