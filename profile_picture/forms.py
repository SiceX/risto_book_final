from django.forms import EmailField, EmailInput, CharField, TextInput, ImageField, IntegerField, FileField, ModelForm

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from profile_picture.models import ImmagineProfilo


class EditPropicForm(ModelForm):
    # user_id = IntegerField(disabled=True)
    profile_picture = ImageField(required=False)

    class Meta:
        model = ImmagineProfilo
        fields = ("profile_picture",)

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user')
        super(EditPropicForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user