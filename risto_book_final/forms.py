from django.forms import EmailField, EmailInput, CharField, TextInput, ImageField, IntegerField, FileField

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from profile_picture.models import ImmagineProfilo


class UserCreationWithEmailForm(UserCreationForm):
    email = EmailField(label="Email address", required=True, help_text="Required.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class EditProfileForm(UserChangeForm):
    profile_picture = ImageField(required=False)
    username = CharField(widget=TextInput(attrs={'class': 'form-control'}))
    email = EmailField(widget=EmailInput(attrs={'class': 'form-control'}))
    password = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_id = kwargs['initial']['user_id']
        if ImmagineProfilo.objects.filter(utente_id=user_id).exists():
            self.profile_picture.initial = ImmagineProfilo.objects.filter(utente_id=user_id).get()

    class Meta:
        model = User
        fields = ("username", "email", "profile_picture")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        ImmagineProfilo.objects.update_or_create(utente_id=user.id, immagine=self.cleaned_data["profile_picture"])
        if commit:
            user.save()
        return user
