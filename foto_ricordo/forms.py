from django.forms import EmailField, EmailInput, CharField, TextInput, ImageField, IntegerField, FileField, ModelForm

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils import timezone

from foto_ricordo.models import FotoRicordo


class CreateFotoRicordoForm(ModelForm):
    foto_ricordo = ImageField(required=True)
    # data = models.DateTimeField(null=False)

    class Meta:
        model = FotoRicordo
        fields = ("foto_ricordo",)

    def save(self, commit=True):
        foto = super().save(commit=False)
        foto.data = timezone.now()
        if commit:
            foto.save()
        return foto
