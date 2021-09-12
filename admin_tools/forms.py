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

		# layout = None
		# if 'nome' in self.initial:
		# 	tavolo = self.initial['nome']
		#
		# 	layout = Layout(
		# 		HTML("""<tr>"""),
		# 		Fieldset(
		# 			HTML("""<td>"""),
		# 			'nome',
		# 			HTML("""</td>"""),
		# 			HTML("""<td>"""),
		# 			'abilitato',
		# 			HTML("""</td>"""),
		# 			HTML("""<td> <a href="{% url 'admin_tools:tavolo-detail' """ + tavolo + """ %}">Dettaglio</a> </td>"""),
		# 		),
		# 		HTML("""</tr>""")
		# 	)

		self.helper = FormHelper()
		self.helper.form_id = 'manage_tavoli_crispy_form'
		self.helper.form_method = 'POST'
		# self.helper.layout = layout
