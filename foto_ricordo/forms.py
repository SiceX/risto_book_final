from django.forms import ImageField, ModelForm
from django.utils import timezone
from foto_ricordo.models import FotoRicordo


class CreateFotoRicordoForm(ModelForm):
    foto_ricordo = ImageField(required=True)

    class Meta:
        model = FotoRicordo
        fields = ("foto_ricordo",)

    def save(self, commit=True):
        foto = super().save(commit=False)
        foto.data = timezone.now()
        if commit:
            foto.save()
        return foto
