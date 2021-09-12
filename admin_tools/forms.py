from django import forms
from crispy_forms.layout import Submit, Layout, Field, Button, ButtonHolder, HTML, Fieldset
from crispy_forms.helper import FormHelper

from booking.models import Tavolo


class GestisciTavoliForm(forms.ModelForm):

	class Meta:
		model = Tavolo
		fields = ['nome', 'abilitato']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['nome'].required = True

		self.helper = FormHelper()
		self.helper.form_id = 'manage_tavoli_crispy_form'
		self.helper.form_method = 'POST'
