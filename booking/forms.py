from datetime import datetime, timedelta

from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit, Layout, Field, Button, ButtonHolder, HTML
from django import forms
from django.core.exceptions import ValidationError
from django.forms import DateInput, TextInput, HiddenInput
from crispy_forms.helper import FormHelper
from django.urls import reverse_lazy
from django.utils import timezone

from booking.models import Prenotazione


class PrenotazioneForm(forms.ModelForm):

	helper = FormHelper()
	helper.form_id = 'prenotazione_crispy_form'
	helper.form_method = 'POST'
	helper.add_input(Submit('submit', 'Conferma'))
	helper.inputs[0].field_classes = 'btn btn-success'
	helper.layout = Layout(
		Field('tavolo', readonly="readonly"),
		Field('data_ora', readonly="readonly"),
		Field('queue_place', readonly="readonly")
	)

	def __init__(self, *args, **kwargs):
		super(PrenotazioneForm, self).__init__(*args, **kwargs)
		self.fields['tavolo'].disabled = True
		self.fields['tavolo'].required = False
		self.fields['queue_place'].required = False

		if 'tavolo' not in self.initial:
			self.fields['tavolo'].widget = HiddenInput()
		if 'queue_place' not in self.initial:
			self.fields['queue_place'].widget = HiddenInput()

	def clean(self):
		cleaned_data = super().clean()
		data = cleaned_data.get('data_ora')
		if data:
			if data.date() < (timezone.now().date() + timedelta(days=1)):
				raise ValidationError("Non è possibile prenotare pranzi o cene per oggi o nel passato")
		return cleaned_data

	class Meta:
		model = Prenotazione
		fields = ['tavolo', 'data_ora', 'queue_place']


class DateNavForm(forms.Form):
	data = forms.DateField(widget=DateInput(), required=True, )

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		date = datetime.strptime(kwargs['initial']['datetime'], "%Y %m %d")
		self.data.initial = date

		previous_date = date - timedelta(days=1)
		next_date = date + timedelta(days=1)

		previous_button = None
		if previous_date > datetime.now():
			previous_button = ButtonHolder(
				HTML("""<a href="{% url 'booking:dashboard-prenotazioni' """ + previous_date.strftime('%Y')
				+ """ """ + previous_date.strftime('%m')
				+ """ """ + previous_date.strftime('%d') + """ %}" 
				class="btn btn-success"> Giorno Precedente </a>"""),
			)

		next_button = ButtonHolder(
			HTML("""<a href="{% url 'booking:dashboard-prenotazioni' """ + next_date.strftime('%Y')
			+ """ """ + next_date.strftime('%m')
			+ """ """ + next_date.strftime('%d') + """ %}" 
				class="btn btn-success"> Giorno Successivo </a>"""),
		)

		find_button = ButtonHolder(
			HTML("""<a href="{% url 'booking:dashboard-prenotazioni-find' %}" 
				class="btn btn-success"> Trova primo giorno libero </a>"""),
		)

		self.helper = FormHelper()
		self.helper.form_id = 'date_nav'
		self.helper.form_method = 'POST'
		self.helper.layout = Layout(
			Field('data', readonly="readonly"),
			FormActions(
				previous_button,
				Submit('submit', 'Visualizza'),
				next_button,
				find_button
			)
		)

	# def clean(self):
	# 	cleaned_data = super().clean()
	# 	data = cleaned_data.get('data')
	# 	if data:
	# 		data = datetime.strptime(data, "%Y %m %d")
	# 		if data.date() < (timezone.now().date() + timedelta(days=1)):
	# 			raise ValidationError("Non è possibile prenotare pranzi o cene per oggi o nel passato")
	# 	return cleaned_data
