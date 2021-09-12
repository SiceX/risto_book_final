from django import forms
from crispy_forms.layout import Submit, Layout, Field, Button, ButtonHolder, HTML
from crispy_forms.helper import FormHelper

from booking.models import Tavolo


class GestisciTavoliForm(forms.ModelForm):

	helper = FormHelper()
	helper.form_id = 'manage_tavoli_crispy_form'
	helper.form_method = 'POST'
	helper.add_input(Submit('submit', 'Conferma'))
	helper.inputs[0].field_classes = 'btn btn-success'
	# helper.layout = Layout(
	# 	Field('tavolo', readonly="readonly"),
	# 	Field('data_ora', readonly="readonly"),
	# 	Field('queue_place', readonly="readonly")
	# )

	# def __init__(self, *args, **kwargs):
	# 	super(PrenotazioneForm, self).__init__(*args, **kwargs)
	# 	self.fields['tavolo'].disabled = True
	# 	self.fields['tavolo'].required = False
	# 	self.fields['queue_place'].required = False
	#
	# 	if 'tavolo' not in self.initial:
	# 		self.fields['tavolo'].widget = HiddenInput()
	# 	if 'queue_place' not in self.initial:
	# 		self.fields['queue_place'].widget = HiddenInput()

	class Meta:
		model = Tavolo
		fields = ['nome', 'abilitato']