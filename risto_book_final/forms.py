from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import EmailField, EmailInput, CharField, TextInput


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
    username = CharField(widget=TextInput(attrs={'class': 'form-control'}))
    email = EmailField(widget=EmailInput(attrs={'class': 'form-control'}))
    password = None

    class Meta:
        model = User
        fields = ("username", "email")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
