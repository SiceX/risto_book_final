from django.forms import EmailField, EmailInput, CharField, TextInput, ImageField, IntegerField, FileField, ModelForm

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from foto_ricordo.models import FotoRicordo


class CreateFotoRicordoForm(ModelForm):
    foto_ricordo = ImageField(required=False)
    # data_ora = models.DateTimeField(null=False)

    class Meta:
        model = FotoRicordo
        fields = ("foto_ricordo",)

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     if commit:
    #         user.save()
    #     return user
