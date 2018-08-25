from django.forms import ModelForm
from .models import Edres, Eklogestbl

class EdresForm(ModelForm):
    class Meta:
        model=Edres
        fields = '__all__'