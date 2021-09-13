from django.forms import EmailField, EmailInput, CharField, TextInput, ImageField, IntegerField, FileField, ModelForm

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from profile_picture.models import ImmagineProfilo


class EditPropicForm(ModelForm):
    profile_picture = ImageField(required=False)

    class Meta:
        model = ImmagineProfilo
        fields = ("profile_picture")

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.email = self.cleaned_data["email"]
    #     if commit:
    #         user.save()
    #     return user