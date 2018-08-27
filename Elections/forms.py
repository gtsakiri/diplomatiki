from django.forms import ModelForm, forms
from .models import Edres, Eklogestbl
from django.utils.translation import gettext_lazy as _

class EdresForm(ModelForm):
    class Meta:
        model=Edres
        fields = '__all__'
        help_texts = {
            'sinoloedrwn': _('Το σύνολο εδρών πρέπει να ισούται με το άθροισμα των δύο επόμενων πεδίων'),
        }

    def clean(self):
        cleaned_data = super(EdresForm, self).clean()
        descr = cleaned_data.get('descr')
        sinoloedrwn = cleaned_data.get('sinoloedrwn')
        edresprwtou = cleaned_data.get('edresprwtou')
        edresypoloipwn = cleaned_data.get('edresypoloipwn')
        # if not name and not email and not message:
        if sinoloedrwn != (edresprwtou + edresypoloipwn):
            raise forms.ValidationError('Το σύνολο των εδρών πρέπει να ισούται με το άθροισμα των δύο άλλων σχετικών πεδίων!')

