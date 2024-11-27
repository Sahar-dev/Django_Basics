from django import forms
from .models import Subscription
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super(SubscriptionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(
            Submit('submit', 'Save', css_class='btn btn-success'))
