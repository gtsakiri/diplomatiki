from django.forms import ModelForm, forms, DateInput, CharField, ModelChoiceField, IntegerField
from django import forms

from .models import Edres, Sistima, Eklogestbl, Sindiasmoi, Eklsind, Perifereies, Edreskoin, Typeofkoinotita, \
    Koinotites, Eklper, Eklsindkoin, Eklperkoin, Kentra, Psifodeltia, Simbouloi, Psifoi, Eklsindsimb
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

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

        if sinoloedrwn != (edresprwtou + edresypoloipwn):
            raise forms.ValidationError('Το σύνολο των εδρών πρέπει να ισούται με το άθροισμα των δύο άλλων σχετικών πεδίων!')

class EdresKoinForm(ModelForm):
    class Meta:
        model=Edreskoin
        fields = '__all__'
        labels = {
            'descr': _('Περιγραφή'),
            'sinolo': _('Σύνολο εδρών'),
        }


    def clean(self):
        cleaned_data = super(EdresKoinForm, self).clean()
        descr = cleaned_data.get('descr')
        sinolo = cleaned_data.get('sinolo')

class SistimaForm(ModelForm):

    class Meta:
        model=Sistima
        fields = '__all__'
        labels = {
            'descr': _('Περιγραφή'),
        }

    def clean(self):
        cleaned_data = super(SistimaForm, self).clean()
        descr = cleaned_data.get('descr')

class TypeofkoinotitaForm(ModelForm):

    class Meta:
        model=Typeofkoinotita
        fields = '__all__'
        labels = {
            'tpkid': _('Κωδικός'),
            'descr': _('Περιγραφή'),
        }

    def clean(self):
        cleaned_data = super(TypeofkoinotitaForm, self).clean()
        descr = cleaned_data.get('descr')
        tpkid = self.cleaned_data['tpkid']
'''
        if Typeofkoinotita.objects.filter(tpkid=tpkid).exists():
            raise forms.ValidationError(
                "This key has already been entered, try to update it"
            )
'''

class EklogestblForm(ModelForm):

    class Meta:
        model=Eklogestbl
        fields = '__all__'

        VISIBLE_CHOICES = (
            ('1', 'ΝΑΙ'),
            ('0', 'ΟΧΙ'),

        )

        DEFAULT_CHOICES = (
            ('1', 'ΝΑΙ'),
            ('0', 'ΟΧΙ'),

        )

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
            'dateofelection': _('η ημερομηνία στη μορφή dd/mm/yyyy παρακαλώ, π.χ. 21/10/2018'),
            'visible': _('Επιλέξτε ΝΑΙ αν πρέπει να είναι ορατή στην εφαρμογή, αλλιώς επιλέξτε ΟΧΙ'),
        }
        widgets = {
        'visible': forms.Select(choices=VISIBLE_CHOICES, attrs={'class': 'form-control'}),
        'defaultelection': forms.Select(choices=DEFAULT_CHOICES, attrs={'class': 'form-control'}),
        }



    def clean(self):
        cleaned_data = super(EklogestblForm, self).clean()
        descr = cleaned_data.get('descr')
        dateofelection = cleaned_data.get('dateofelection')
        dimos = cleaned_data.get('dimos')
        sisid = cleaned_data.get('sisid')
        edrid = cleaned_data.get('edrid')
        visible = cleaned_data.get('visible')
        defaultelection = cleaned_data.get('defaultelection')
        if visible != 1 and visible !=0:
            raise forms.ValidationError('Δεκτές τιμές για το πεδίο "Ορατή" μόνο 0 ή 1!')
        if visible == 0 and defaultelection == 1:
            raise forms.ValidationError('Δεν μπορεί να γίνει μη ορατή η προεπιλεγμένη εκλ. αναμέτρηση!')



class SindiasmoiForm(ModelForm):

    aa= CharField(label='ΑΑ συνδυασμού',max_length=45)
    #proedros=CharField(label='Πρόεδρος (σε περίπτωση Κοινότητας>300 κατ.',max_length=100)
    koinid=ModelChoiceField(queryset=Koinotites.objects.filter(eidos=4), label='Κοινότητα', required=False)
    proedros=CharField(label='Πρόεδρος',max_length=100, required=False)

    class Meta:
        model=Sindiasmoi
        fields = ['descr', 'shortdescr', 'eidos', 'koinid', 'proedros', 'photofield', 'aa']

        EIDOS_CHOICES = (
            (1, 'Δήμο'),
            (0, 'Κοινότητα'),
        )
        labels = {
            'descr': _('Περιγραφή'),
            'shortdescr': _('Σύντομος τίτλος'),
            'eidos': _('Υποψήφιος συνδυασμός για όλο το Δήμο ή σε Τοπική Κοινότητα μόνο?'),
            'koinid': _('Κοινότητα'),
            'proedros': _('Πρόεδρος'),
            'photofield': _('Φωτογραφία'),
        }
        help_texts = {
            'shortdescr': _('Π.χ, το επίθετο του επικεφαλής μόνο'),
            'koin': _('Κοινότητα στην οποία συμμέτεχει'),
            'aa': _('Με ποιο ΑΑ συμμετέχει o συνδυασμός στις εκλογές'),
        }
        widgets = {
            'eidos': forms.Select(choices=EIDOS_CHOICES, attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super(SindiasmoiForm, self).clean()
        descr = cleaned_data.get('descr')
        shortdescr = cleaned_data.get('shortdescr')
        koin = cleaned_data.get('koin')
        proedros=cleaned_data.get('proedros')
        eidos = cleaned_data.get('eidos')
        photofield = cleaned_data.get('photo')
        aa = cleaned_data.get('aa')

    def __init__(self, *args, **kwargs):
        super(SindiasmoiForm, self).__init__(*args, **kwargs)

        # SOS!!! κάνω override την μέθοδο Init και αρχικοποίηση των dropdown perid, edrid
        # Για το perid παίρνω μόνο τις περιφέρειες που έχουν καταχωρηθεί στην τρέχουσα εκλ. αναμέτρηση μόνο
        self.fields['koinid'].queryset = Koinotites.objects.filter(eidos=4)



class EklsindForm(ModelForm):

    class Meta:
        model=Eklsind
        fields = ['eklid','sindid','aa', 'edresa', 'edresa_ypol', 'edresa_teliko', 'edresb', 'ypol', 'lastupdate']
        labels = {
            'sindid': _('Συνδυασμός'),
            'aa': _('ΑΑ'),
            'edresa': _('Έδρες Α γύρου (αρχικές)'),
            'edresa_ypol': _('Υπόλοιπο Εδρών Α γύρου'),
            'edresa_teliko': _('Έδρες Α γύρου (τελικές)'),
            'edresb': _('Έδρες Β γύρου'),
            'ypol': _('Υπόλοιπο ψηφοδελτίων'),
            'lastupdate': _('Τελευταία ενημέρωση')
        }
        widgets = {
            #κρυφό πεδίο αφού θα παίρνει αυτόματα τιμή από το view χωρίς την παρέμβαση του χρήστη
            'eklid': forms.HiddenInput(),
        }

    def __init__(self, eklid, *args, **kwargs):
        super(EklsindForm, self).__init__(*args, **kwargs)

        #SOS!!! κάνω override την μέθοδο Init και αρχικοποίηση του dropdown sindid με τους συνδυασμούς που δεν έχουν εισαχθεί ακόμα στην τρέχουσα
        #εκλ. αναμέτρηση, ώστε να μην επαναεισάγει κατά λάθος ο χρήστης τον ίδιο συνδυασμό.

        self.fields['sindid'].queryset = Sindiasmoi.objects.filter(eidos=1).exclude(sindid__in=Eklsind.objects.filter(eklid=eklid).values_list('sindid'))

class EklsindkoinForm(ModelForm):

    class Meta:
        model = Eklsindkoin
        fields = ['eklid', 'koinid', 'sindid',  'aa', 'proedros', 'edresk', 'edresk_ypol', 'edresk_teliko', 'ypol', 'checkfordraw', 'lastupdate']
        labels = {
            'sindid': _('Συνδυασμός'),
            'koinid': _('Κοινότητα'),
            'aa': _('ΑΑ'),
            'proedros': _('Πρόεδρος'),
            'edresk': _('Έδρες Α γύρου (αρχικές)'),
            'edresk_ypol': _('Υπόλοιπο Εδρών Α γύρου'),
            'edresk_teliko': _('Έδρες Α γύρου (τελικές)'),
            'ypol': _('Υπόλοιπο ψηφοδελτίων'),
            'checkfordraw': _('Ένδειξη ισοπαλίας'),
            'lastupdate': _('Τελευταία ενημέρωση')

        }
        widgets = {
            # κρυφό πεδίο αφού θα παίρνει αυτόματα τιμή από το view χωρίς την παρέμβαση του χρήστη
            'eklid': forms.HiddenInput(),
        }

    def __init__(self, eklid, *args, **kwargs):
        super(EklsindkoinForm, self).__init__(*args, **kwargs)
        # δημιουργία φίλτρου με τη βοήθεια του Q object
        q = Q(sindid__in=Eklsindkoin.objects.filter(eklid=eklid).values_list('sindid')) | \
            Q(sindid__in=Eklsind.objects.filter(eklid=eklid).values_list('sindid'))

        self.fields['sindid'].queryset = Sindiasmoi.objects.filter(q)
        self.fields['koinid'].queryset = Koinotites.objects.filter(eidos=4).filter(koinid__in=Eklperkoin.objects.filter(eklid=eklid).values_list('koinid'))

    def clean(self):
        cleaned_data = super(EklsindkoinForm, self).clean()
        sindid = cleaned_data.get('sindid')
        koinid = cleaned_data.get('koinid')
        aa=cleaned_data.get('aa')
        proedros = cleaned_data.get('proedros')
        edresk = cleaned_data.get('edresk')
        edresk_ypol = cleaned_data.get('edresk_ypol')
        edresk_teliko = cleaned_data.get('edresk_teliko')
        ypol = cleaned_data.get('ypol')
        checkfordraw = cleaned_data.get('checkfordraw')


class PerifereiesForm(ModelForm):

    class Meta:
        model=Perifereies
        fields = '__all__'
        labels = {
            'descr': _('Περιγραφή'),
        }

    def clean(self):
        cleaned_data = super(PerifereiesForm, self).clean()
        descr = cleaned_data.get('descr')

class KoinotitesForm(ModelForm):

    perid= ModelChoiceField (queryset=Perifereies.objects.all(), label='Περιφέρεια')
    edrid = ModelChoiceField(queryset=Edreskoin.objects.all(), label='Κατηγορία κατανομής εδρών', required=False)

    class Meta:
        model=Koinotites
        fields = ['descr', 'eidos', 'perid', 'edrid']
        labels = {
            'descr': _('Περιγραφή'),
            'eidos': _('Είδος'),
        }

    def __init__(self, eklid, *args, **kwargs):
        super(KoinotitesForm, self).__init__(*args, **kwargs)

        # SOS!!! κάνω override την μέθοδο Init και αρχικοποίηση των dropdown perid, edrid
        # Για το perid παίρνω μόνο τις περιφέρειες που έχουν καταχωρηθεί στην τρέχουσα εκλ. αναμέτρηση μόνο
        self.fields['perid'].queryset = Perifereies.objects.filter(perid__in=Eklper.objects.filter(eklid=eklid).values_list('perid'))
        self.fields['edrid'].queryset = Edreskoin.objects.all()

    def clean(self):
        cleaned_data = super(KoinotitesForm, self).clean()
        descr = cleaned_data.get('descr')
        eidos = cleaned_data.get('eidos')
        perid = cleaned_data.get('perid')
        edrid = cleaned_data.get('edrid')

class KentraForm(ModelForm):

    class Meta:
        model=Kentra
        fields = ['descr', 'eggegrammenoia', 'psifisana', 'egkiraa', 'akiraa', 'lefkaa', 'sinoloakiralefkaa', 'comments', 'eklid', 'perid',
                  'koinid', 'eggegrammenoib', 'psifisanb', 'egkirab', 'akirab', 'lefkab', 'sinoloakiralefkab', 'eggegrammenoik', 'psifisank',
                  'egkirak', 'akirak', 'lefkak', 'sinoloakiralefkak']
        labels = {
            'descr': _('Περιγραφή'),'eggegrammenoia': _('Εγγεγραμμένοι (Α Κυριακή)'), 'psifisana': _('Ψήφισαν (Α Κυριακή)'), 'egkiraa': _('Έγκυρα (Α Κυριακή)'),
            'akiraa': _('Άκυρα (Α Κυριακή)'), 'lefkaa': _('Λευκά (Α Κυριακή)'), 'sinoloakiralefkaa': _('Σύνολο Άκυρα+Λευκά (Α Κυριακή)'),
            'comments': _('Επιπλέον περιγραφή'), 'eklid': _('Εκλ. Αναμέτρηση'),'perid': _('Εκλ. Περιφέρεια'), 'koinid': _('Κοινότητα'),
            'eggegrammenoib': _('Εγγεγραμμένοι (Β Κυριακή)'),'psifisanb': _('Ψήφισαν (Β Κυριακή)'), 'egkirab': _('Έγκυρα (Β Κυριακή)'), 'akirab': _('Άκυρα (Β Κυριακή)'),
            'lefkab': _('Λευκά (Β Κυριακή)'), 'sinoloakiralefkab': _('Σύνολο Άκυρα+Λευκά (Β Κυριακή)'),
            'eggegrammenoik': _('Εγγεγραμμένοι (Εκλογές Κοινότητας)'), 'psifisank': _('Ψήφισαν (Εκλογές Κοινότητας)'),
            'egkirak': _('Έγκυρα (Εκλογές Κοινότητας)'), 'akirak': _('Άκυρα (Εκλογές Κοινότητας)'),
            'lefkak': _('Λευκά (Εκλογές Κοινότητας)'), 'sinoloakiralefkak': _('Σύνολο Άκυρα+Λευκά (Εκλογές Κοινότητας)'),
        }
        widgets = {
            #κρυφό πεδίο αφού θα παίρνει αυτόματα τιμή από το view χωρίς την παρέμβαση του χρήστη
            'eklid': forms.HiddenInput(),
            #'perid': forms.HiddenInput(),
        }

    def __init__(self, eklid, *args, **kwargs):
        super(KentraForm, self).__init__(*args, **kwargs)

        # SOS!!! κάνω override την μέθοδο Init και αρχικοποίηση των dropdown perid, koinid
        self.fields['perid'].queryset = Perifereies.objects.filter(perid__in=Eklper.objects.filter(eklid=eklid).values_list('perid'))
        self.fields['koinid'].queryset = Koinotites.objects.filter(koinid__in=Eklperkoin.objects.filter(eklid=eklid).values_list('koinid'))

        # ορίζω ένα custom όνομα για το πεδίο perid για να το διαχειριστώ με javascript στο template
        self.fields['perid'].widget.attrs['id'] = 'perid_of_kentra'

    def clean(self):
        cleaned_data = super(KentraForm, self).clean()
        descr = cleaned_data.get('descr')
        eggegrammenoia = cleaned_data.get('eggegrammenoia')
        psifisana = cleaned_data.get('psifisana')
        egkiraa = cleaned_data.get('egkiraa')
        akiraa = cleaned_data.get('akiraa')
        lefkaa = cleaned_data.get('lefkaa')
        sinoloakiralefkaa = cleaned_data.get('sinoloakiralefkaa')
        comments = cleaned_data.get('comments')
        eklid = cleaned_data.get('eklid')
        perid = cleaned_data.get('perid')
        koinid = cleaned_data.get('koinid')
        eggegrammenoib = cleaned_data.get('eggegrammenoib')
        psifisanb = cleaned_data.get('psifisanb')
        egkirab = cleaned_data.get('egkirab')
        akirab = cleaned_data.get('akirab')
        lefkab = cleaned_data.get('lefkab')
        sinoloakiralefkab = cleaned_data.get('sinoloakiralefkab')
        eggegrammenoik= cleaned_data.get('eggegrammenoik')
        psifisank = cleaned_data.get('psifisank')
        egkirak = cleaned_data.get('egkirak')
        akirak = cleaned_data.get('akirak')
        lefkak = cleaned_data.get('lefkak')
        sinoloakiralefkak = cleaned_data.get('sinoloakiralefkak')

        if psifisana != (egkiraa + akiraa + lefkaa):
            raise forms.ValidationError('Το άθροισμα των πεδίων <<Έγκυρα>> + <<Άκυρα>> + <<Λευκά>> πρέπει να ισούται με το πεδίο <<Ψήφισαν>> για την Α Κυριακή!')
        if sinoloakiralefkaa != (akiraa + lefkaa):
            raise forms.ValidationError('Το άθροισμα των πεδίων <<Άκυρα>> + <<Λευκά>> πρέπει να ισούται με το πεδίο <<Σύνολο Άκυρα+Λευκά>> για την Α Κυριακή!')

        if psifisanb != (egkirab + akirab + lefkab):
            raise forms.ValidationError('Το άθροισμα των πεδίων <<Έγκυρα>> + <<Άκυρα>> + <<Λευκά>> πρέπει να ισούται με το πεδίο <<Ψήφισαν>> για την Β Κυριακή!')
        if sinoloakiralefkab != (akirab + lefkab):
            raise forms.ValidationError('Το άθροισμα των πεδίων <<Άκυρα>> + <<Λευκά>> πρέπει να ισούται με το πεδίο <<Σύνολο Άκυρα+Λευκά>> για την Β Κυριακή!')

        if psifisank != (egkirak + akirak + lefkak):
            raise forms.ValidationError('Το άθροισμα των πεδίων <<Έγκυρα>> + <<Άκυρα>> + <<Λευκά>> πρέπει να ισούται με το πεδίο <<Ψήφισαν>> για τις εκλογές της Κοινότητας!')
        if sinoloakiralefkak != (akirak + lefkak):
            raise forms.ValidationError('Το άθροισμα των πεδίων <<Άκυρα>> + <<Λευκά>> πρέπει να ισούται με το πεδίο <<Σύνολο Άκυρα+Λευκά>> για τις εκλογές της Κοινότητας!')

class PsifodeltiaForm(ModelForm):

    class Meta:
        model=Psifodeltia
        fields = ['sindid','kenid', 'votesa', 'votesb']
        labels = {
            'sindid': _('Συνδυασμός'),
            'kenid': _('Εκλ. Κέντρο'),
            'votesa': _('Ψηφοδέλτια (Α Κυριακής)'),
            'votesb': _('Ψηφοδέλτια (Β Κυριακής)'),

        }


    def __init__(self, eklid, *args, **kwargs):
        super(PsifodeltiaForm, self).__init__(*args, **kwargs)


        #SOS!!! κάνω override την μέθοδο Init και αρχικοποίηση του dropdown sindid με τους συνδυασμούς της επιλεγμένης εκλ. αναμέτρησης
        #self.fields['sindid'].queryset = Sindiasmoi.objects.filter(sindid__in=Eklsind.objects.filter(eklid=eklid).values_list('sindid'))
        # δημιουργία φίλτρου με τη βοήθεια του Q object
        #q = Q(sindid__in=Eklsindkoin.objects.filter(eklid=eklid).values_list('sindid')) | \
        #    Q(sindid__in=Eklsind.objects.filter(eklid=eklid).values_list('sindid'))

        q = Q(sindid__in=Eklsind.objects.filter(eklid=eklid).values_list('sindid'))

        self.fields['sindid'].queryset = Sindiasmoi.objects.filter(q)
        self.fields['kenid'].queryset = Kentra.objects.filter(kenid__in=Kentra.objects.filter(eklid=eklid).values_list('kenid'))

    def clean(self):
        cleaned_data = super(PsifodeltiaForm, self).clean()
        sindid = cleaned_data.get('sindid')
        kenid = cleaned_data.get('kenid')
        votesa = cleaned_data.get('votesa')
        votesb = cleaned_data.get('votesb')


class PsifodeltiaKoinForm(ModelForm):
    class Meta:
        model = Psifodeltia
        fields = ['sindid', 'kenid', 'votesk']
        labels = {
            'sindid': _('Συνδυασμός'),
            'kenid': _('Εκλ. Κέντρο'),
            'votesk': _('Ψηφοδέλτια Για Τοπικό Συμβούλιο'),

        }

    def __init__(self, eklid, *args, **kwargs):
        super(PsifodeltiaKoinForm, self).__init__(*args, **kwargs)

        # SOS!!! κάνω override την μέθοδο Init και αρχικοποίηση του dropdown sindid με τους συνδυασμούς της επιλεγμένης εκλ. αναμέτρησης
        # self.fields['sindid'].queryset = Sindiasmoi.objects.filter(sindid__in=Eklsind.objects.filter(eklid=eklid).values_list('sindid'))
        # δημιουργία φίλτρου με τη βοήθεια του Q object
        #q = Q(sindid__in=Eklsindkoin.objects.filter(eklid=eklid).values_list('sindid')) | \
        #    Q(sindid__in=Eklsind.objects.filter(eklid=eklid).values_list('sindid'))

        q = Q(sindid__in=Eklsindkoin.objects.filter(eklid=eklid).values_list('sindid'))

        self.fields['sindid'].queryset = Sindiasmoi.objects.filter(q)
        self.fields['kenid'].queryset = Kentra.objects.filter(
            kenid__in=Kentra.objects.filter(eklid=eklid).values_list('kenid'))

    def clean(self):
        cleaned_data = super(PsifodeltiaKoinForm, self).clean()
        sindid = cleaned_data.get('sindid')
        kenid = cleaned_data.get('kenid')
        votesk = cleaned_data.get('votesk')


class SimbouloiForm(ModelForm):

    EIDOS_CHOICES = (
        (1, 'Δήμο'),
        (0, 'Κοινότητα'),
    )

    hiddenid = IntegerField(label='ID Συμβούλου',required=False)

    eidos = forms.ChoiceField(choices = EIDOS_CHOICES, label="Σε Δήμο ή Κοινότητα ?", widget=forms.Select(), required=True)
    perid = ModelChoiceField(queryset=Perifereies.objects.none(), label='Εκλ. Περιφέρεια')
    koinid = ModelChoiceField(queryset=Koinotites.objects.none(), label='Κοινότητα', required=False)

    sindid = ModelChoiceField(queryset=Sindiasmoi.objects.none(), label='Συνδυασμός', required=False)
    aa = CharField(label='ΑΑ Συμβούλου', max_length=45)

    class Meta:
        model=Simbouloi
        fields = ['hiddenid', 'surname', 'firstname', 'fathername', 'eidos',  'perid',  'koinid',  'sindid', 'aa', 'comments']

        labels = {
            'surname': _('Επίθετο'),
            'firstname': _('Όνομα'),
            'fathername': _('Όν. Πατρός'),
            'comments': _('Παρατηρήσεις'),
            'perid': _('Εκλ. Περιφέρεια'),
            'koinid': _('Κοινότητα'),
            'sindid': _('Συνδυασμός'),
            'aa': _('ΑΑ'),
        }
        help_texts = {
            'aa': _('Με ποιο ΑΑ συμμετέχει o υποψήφιος στις εκλογές'),
        }

    def __init__(self, eklid,  *args, **kwargs):
        super(SimbouloiForm, self).__init__(*args, **kwargs)

        # SOS!!! κάνω override την μέθοδο Init και αρχικοποίηση των dropdown perid, sindid, koinid
        # Παίρνω μόνο perid, sindid, koinid που έχουν καταχωρηθεί στην τρέχουσα εκλ. αναμέτρηση μόνο
        self.fields['perid'].queryset = Perifereies.objects.filter(perid__in=Eklper.objects.filter(eklid=eklid).values_list('perid'))

        self.fields['koinid'].queryset = Koinotites.objects.filter(koinid__in=Eklperkoin.objects.filter(eklid=eklid).values_list('koinid'))

        self.fields['perid'].widget.attrs['id'] = 'perid_of_simbouloi'

        q = Q(sindid__in=Eklsind.objects.filter(eklid=eklid).values_list('sindid')) | Q(
           sindid__in=Eklsindkoin.objects.filter(eklid=eklid).values_list('sindid'))

        self.fields['sindid'].queryset = Sindiasmoi.objects.filter(q)

        self.fields['hiddenid'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super(SimbouloiForm, self).clean()
        surname = cleaned_data.get('surname')
        firstname = cleaned_data.get('firstname')
        fathername = cleaned_data.get('fathername')
        eidos = cleaned_data['eidos']
        comments = cleaned_data.get('comments')
        aa = cleaned_data.get('aa')
        sindid = cleaned_data.get('sindid')
        perid = cleaned_data.get('perid')
        koinid = cleaned_data.get('koinid')
        hiddenid = cleaned_data.get('hiddenid')


        #Έλεγχος αν ξέχασε να βάλει ο χρήστης Κοινότητα, αν πρόκειται για σύμβουλο Κοινότητας
        if eidos == '0' and koinid == None:
            raise forms.ValidationError("Το πεδίο Κοινότητα πρέπει να συμπληρωθεί αφού πρόκειται για υποψήφιο Κοινότητας!")
        if eidos == '1' and sindid == None:
            raise forms.ValidationError("Το πεδίο Συνδυασμός πρέπει να συμπληρωθεί αφού πρόκειται για υποψήφιο Δημοτικό Σύμβουλο!")

class PsifoiForm(ModelForm):

    class Meta:
        model=Psifoi
        fields = ['simbid', 'votes', 'kenid']
        labels = {
            'simbid': _('Υποψήφιος'),
            'votes': _('Ψηφοι'),
            'kenid': _('Εκλ. Κέντρο'),

        }

    def __init__(self, eklid, *args, **kwargs):
        super(PsifoiForm, self).__init__(*args, **kwargs)

        #SOS!!! κάνω override την μέθοδο Init και αρχικοποίηση των dropdown simbid, kenid με τα στοιχεία της επιλεγμένης εκλ. αναμέτρησης
        self.fields['simbid'].queryset = Simbouloi.objects.filter(simbid__in=Eklsindsimb.objects.filter(eklid=eklid).values_list('simbid')).order_by('surname', 'firstname', 'fathername')
        self.fields['kenid'].queryset = Kentra.objects.filter(eklid=eklid).order_by('descr')


    def clean(self):
        cleaned_data = super(PsifoiForm, self).clean()
        simbid = cleaned_data.get('simbid')
        votes = cleaned_data.get('votes')
        kenid = cleaned_data.get('kenid')
        if votes<0:
            raise forms.ValidationError('Δεν υπάρχει αρνητικό σύνολο ψήφων!')

