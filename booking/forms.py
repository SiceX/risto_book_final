from datetime import datetime, timedelta

from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit, Layout, Field, Button, ButtonHolder, HTML
from django import forms
from django.forms import DateInput, TextInput, HiddenInput
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

	class Meta:
		model = Prenotazione
		fields = ['tavolo', 'data_ora', 'queue_place']


class DateNavForm(forms.Form):
	data = forms.DateField(widget=DateInput(), required=True)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# year = kwargs['initial']['year']
		# month = kwargs['initial']['month']
		# day = kwargs['initial']['day']

		date = datetime.strptime(kwargs['initial']['datetime'], "%Y %m %d")
		self.data = forms.DateField(initial=date, widget=DateInput(), required=True)

		previous_date = date - timedelta(days=1)
		next_date = date + timedelta(days=1)

		previous_button = None
		if previous_date > datetime.now():
			previous_button = ButtonHolder(
				HTML("""<a href="{% url 'booking:dashboard-prenotazioni' """ + previous_date.strftime('%Y')
				+ """ """ + previous_date.strftime('%m')
				+ """ """ + previous_date.strftime('%d') + """ %}" > Giorno Precedente </a>"""),
			)

		next_button = ButtonHolder(
			HTML("""<a href="{% url 'booking:dashboard-prenotazioni' """ + next_date.strftime('%Y')
			+ """ """ + next_date.strftime('%m')
			+ """ """ + next_date.strftime('%d') + """ %}" > Giorno Successivo </a>"""),
		)

		find_button = ButtonHolder(
			HTML("""<a href="{% url 'booking:dashboard-prenotazioni-find' %}" > Trova primo giorno libero </a>"""),
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
	# helper.add_input(Submit('submit', 'Visualizza'))
