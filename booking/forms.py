from crispy_forms.layout import Submit
from django import forms
from django.forms import DateInput
from crispy_forms.helper import FormHelper


class DateNavForm(forms.Form):
	data = forms.DateField(widget=DateInput())

	helper = FormHelper()
	helper.form_id = 'date_nav'
	helper.form_method = 'POST'
	helper.add_input(Submit('submit', 'Visualizza'))
