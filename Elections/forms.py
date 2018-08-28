from django.forms import ModelForm,  DateInput, CharField

from .models import Edres, Sistima, Eklogestbl, Sindiasmoi, Eklsind
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

class SistimaForm(ModelForm):
    class Meta:
        model=Sistima
        fields = '__all__'

    def clean(self):
        cleaned_data = super(SistimaForm, self).clean()
        descr = cleaned_data.get('descr')

class EklogestblForm(ModelForm):

    class Meta:
        model=Eklogestbl
        fields = '__all__'
        labels = {
            'descr': _('Περιγραφή'),
            'dateofelection': _('Ημερ. διεξαγωγής'),
            'dimos': _('Δήμος'),
            'sisid': _('Νομοθετικό πλαίσιο'),
            'edrid': _('Σύστημα κατανομής εδρών'),
            'visible': _('Ορατή'),
            'defaultelection': _('Προεπιλεγμένη'),
        }
        help_texts = {
            'dateofelection': _('η ημερομηνία στη μορφή Ετος-Μηνας-Μέρα παρακαλώ, π.χ. 2018-10-21'),
            'visible': _('Βάλε 1 αν πρέπει να είναι ορατή στην εφαρμογή, αλλιώς βάλε 0'),
        }



    def clean(self):
        cleaned_data = super(EklogestblForm, self).clean()
        descr = cleaned_data.get('descr')
        dateofelection = cleaned_data.get('dateofelection')
        dimos = cleaned_data.get('dimos')
        sisid = cleaned_data.get('sisid')
        edrid = cleaned_data.get('edrid')
        visible = cleaned_data.get('visible')
        defaultelection = cleaned_data.get('defaultElection')
        if visible != 1 and visible !=0:
            raise forms.ValidationError('Δεκτές τιμές για το πεδίο "Ορατή" μόνο 0 ή 1!')


class SindiasmoiForm(ModelForm):

    aa= CharField(label='ΑΑ συνδυασμού',max_length=45)

    class Meta:
        model=Sindiasmoi
        fields = ['descr', 'shortdescr', 'eidos', 'photo', 'aa']
        labels = {
            'descr': _('Περιγραφή'),
            'shortdescr': _('Σύντομος τίτλος'),
            'eidos': _('Κατηγορία'),
            'photo': _('Φωτογραφία'),
        }
        help_texts = {
            'shortdescr': _('Π.χ, το επίθετο του επικεφαλής μόνο'),
            'eidos': _('Αν είναι συνδυασμός που συμμετέχει σε όλο το Δήμο βάλε 1, αν συμμετέχει σε κοινότητα μόνο βάλε 0'),
        }




    def clean(self):
        cleaned_data = super(SindiasmoiForm, self).clean()
        descr = cleaned_data.get('descr')
        shortdescr = cleaned_data.get('shortdescr')
        eidos = cleaned_data.get('eidos')
        photo = cleaned_data.get('photo')
        if eidos != 1 and eidos !=0:
            raise forms.ValidationError('Δεκτές τιμές για το πεδίο "Κατηγορία" μόνο 0 ή 1!')

class EklsindForm(ModelForm):

    class Meta:
        model=Eklsind
        fields = '__all__'


    def clean(self):
        cleaned_data = super(EklsindForm, self).clean()
        eklid = cleaned_data.get('eklid')
        sindid = cleaned_data.get('sindid')
        edresa = cleaned_data.get('edresa')
        edresa_ypol = cleaned_data.get('edresa_ypol')
        edresa_teliko = cleaned_data.get('edresa_teliko')
        ypol = cleaned_data.get('ypol')
