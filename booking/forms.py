from crispy_forms.layout import Submit, Layout, Field, Button
from django import forms
from django.forms import DateInput, TextInput
from crispy_forms.helper import FormHelper
from django.urls import reverse_lazy

from booking.models import Prenotazione


class PrenotazioneForm(forms.ModelForm):

	helper = FormHelper()
	helper.form_id = 'prenotazione_crispy_form'
	helper.form_method = 'POST'
	helper.add_input(Submit('submit', 'Conferma'))
	helper.inputs[0].field_classes = 'btn btn-success'
	helper.layout = Layout(
		Field('tavolo', readonly="readonly"),
		Field('data_ora', readonly="readonly")
	)

	def __init__(self, *args, **kwargs):
		super(PrenotazioneForm, self).__init__(*args, **kwargs)
		self.fields['tavolo'].disabled = True

	class Meta:
		model = Prenotazione
		fields = ['tavolo', 'data_ora']


class DateNavForm(forms.Form):
	data = forms.DateField(widget=DateInput(), required=True)

	helper = FormHelper()
	helper.form_id = 'date_nav'
	helper.form_method = 'POST'
	helper.layout = Layout(
		Field('data', readonly="readonly")
	)
	helper.add_input(Submit('submit', 'Visualizza'))
