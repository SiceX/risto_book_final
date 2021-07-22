from crispy_forms.layout import Submit, Layout, Field
from django import forms
from django.forms import DateInput, TextInput
from crispy_forms.helper import FormHelper


class DateNavForm(forms.Form):
	data = forms.DateField(widget=DateInput(), required=True)

	helper = FormHelper()
	helper.form_id = 'date_nav'
	helper.form_method = 'POST'
	helper.layout = Layout(
		Field('data', readonly="readonly")
	)
	helper.add_input(Submit('submit', 'Visualizza'))
