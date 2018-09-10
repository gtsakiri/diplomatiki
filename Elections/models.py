from django.db import models
from django.urls import reverse


class Edres(models.Model):
    edrid = models.AutoField(db_column='edrID', primary_key=True)  # Field name made lowercase.
    descr = models.CharField(max_length=45, verbose_name='Περιγραφή')
    sinoloedrwn = models.IntegerField(db_column='sinoloEdrwn', verbose_name='Σύνολο εδρών')  # Field name made lowercase.
    edresprwtou = models.IntegerField(db_column='edresPrwtou', verbose_name='Έδρες Πρώτου')  # Field name made lowercase.
    edresypoloipwn = models.IntegerField(db_column='edresYpoloipwn', verbose_name='Έδρες Υπολοίπων')  # Field name made lowercase.

    def __str__(self):
        return self.descr

    class Meta:
        managed = True
        db_table = 'EDRES'


class Edreskoin(models.Model):
    edrid = models.AutoField(db_column='edrID', primary_key=True)  # Field name made lowercase.
    descr = models.CharField(max_length=100)
    sinolo = models.IntegerField(default=0)

    def __str__(self):
        return self.descr + ' - ' + str(self.sinolo)

    class Meta:
        managed = True
        db_table = 'EDRESKOIN'

class Sistima(models.Model):
    sisid = models.AutoField(db_column='sisID', primary_key=True)  # Field name made lowercase.
    descr = models.CharField(max_length=100)

    def __str__(self):
        return str(self.sisid) + ' - ' + self.descr

    class Meta:
        managed = True
        db_table = 'SISTIMA'


class Typeofkoinotita(models.Model):
    tpkid = models.IntegerField(db_column='tpkID', primary_key=True)  # Field name made lowercase.
    descr = models.CharField(max_length=100)

    def __str__(self):
        return str(self.tpkid) + ' - ' + self.descr

    class Meta:
        managed = True
        db_table = 'TYPEOFKOINOTITA'

class Eklogestbl(models.Model):
    eklid = models.AutoField(db_column='eklID', primary_key=True)  # Field name made lowercase.
    descr = models.CharField(unique=True, max_length=100)
    dateofelection = models.DateField(db_column='dateOfElection', blank=True, null=True)  # Field name made lowercase.
    dimos = models.CharField(max_length=100, blank=True)
    sisid = models.ForeignKey('Sistima', models.DO_NOTHING, db_column='sisID')  # Field name made lowercase.
    edrid = models.ForeignKey(Edres, models.DO_NOTHING, db_column='edrID')  # Field name made lowercase.
    visible=models.IntegerField(db_column='visible', default=1)
    defaultelection=models.IntegerField(db_column='defaultElection', default=1)


    def __str__(self):
        return  self.descr

    class Meta:
        managed = True
        db_table = 'EKLOGESTBL'

class Perifereies(models.Model):
    perid = models.AutoField(db_column='perID', primary_key=True)  # Field name made lowercase.
    descr = models.CharField(max_length=100)

    def __str__(self):
        return str(self.perid) + ' - ' + self.descr

    class Meta:
        managed = True
        db_table = 'PERIFEREIES'

class Koinotites(models.Model):
    koinid = models.AutoField(db_column='koinID', primary_key=True)  # Field name made lowercase.
    descr = models.CharField(max_length=100)
    eidos = models.ForeignKey('Typeofkoinotita', models.DO_NOTHING, db_column='eidos')

    def __str__(self):
        return self.descr

    class Meta:
        managed = True
        db_table = 'KOINOTITES'


class Simbouloi(models.Model):
    simbid = models.AutoField(db_column='simbID', primary_key=True)  # Field name made lowercase.
    surname = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    fathername = models.CharField(max_length=100)
    comments = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.surname + ' - ' + self.firstname + ' - ' + self.fathername

    class Meta:
        managed = True
        db_table = 'SIMBOULOI'


class Sindiasmoi(models.Model):
    sindid = models.AutoField(db_column='sindID', primary_key=True)  # Field name made lowercase.
    descr = models.CharField(max_length=100)
    shortdescr = models.CharField(db_column='shortDescr', max_length=50)  # Field name made lowercase.
    photo = models.ImageField(db_column='photo',upload_to='sindiasmoi/',default='elections.jpg',null=True, blank=True)
    eidos = models.IntegerField(default=1)

    def __str__(self):
        return self.descr

    class Meta:
        managed = True
        db_table = 'SINDIASMOI'


class Eklper(models.Model):
    eklid = models.ForeignKey(Eklogestbl, models.DO_NOTHING, db_column='eklID')  # Field name made lowercase.
    perid = models.ForeignKey(Perifereies, models.CASCADE, db_column='perID')  # Field name made lowercase.

    def __str__(self):
        return str(self.eklid) + ' - '  + str(self.perid)

    class Meta:
        managed = True
        db_table = 'EKLPER'
        unique_together = (('eklid', 'perid'),)


class Eklperkoin(models.Model):
    eklid = models.ForeignKey(Eklogestbl, models.DO_NOTHING, db_column='eklID')  # Field name made lowercase.
    perid = models.ForeignKey(Perifereies, models.CASCADE, db_column='perID')  # Field name made lowercase.
    koinid = models.ForeignKey(Koinotites, models.CASCADE, db_column='koinID')  # Field name made lowercase.
    edrid = models.ForeignKey(Edreskoin, models.CASCADE, db_column='edrID', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return str(self.eklid) + ' - '  + str(self.perid) + ' - '  + str(self.koinid)

    class Meta:
        managed = True
        db_table = 'EKLPERKOIN'
        unique_together = (('eklid', 'koinid'),)


class Eklsimbkoin(models.Model):
    eklid = models.ForeignKey(Eklogestbl, models.DO_NOTHING, db_column='eklID')  # Field name made lowercase.
    simbid = models.ForeignKey(Simbouloi, models.DO_NOTHING, db_column='simbID')  # Field name made lowercase.
    koinid = models.ForeignKey(Koinotites, models.DO_NOTHING, db_column='koinID')  # Field name made lowercase.

    def __str__(self):
        return str(self.eklid) + ' - ' + str(self.simbid) + ' - ' + str(self.koinid)

    class Meta:
        managed = True
        db_table = 'EKLSIMBKOIN'
        unique_together = (('eklid', 'simbid'),)


class Eklsimbper(models.Model):
    eklid = models.ForeignKey(Eklogestbl, models.DO_NOTHING, db_column='eklID')  # Field name made lowercase.
    simbid = models.ForeignKey(Simbouloi, models.DO_NOTHING, db_column='simbID')  # Field name made lowercase.
    perid = models.ForeignKey(Perifereies, models.DO_NOTHING, db_column='perID')  # Field name made lowercase.

    def __str__(self):
        return str(self.eklid) + ' - ' + str(self.simbid) + ' - ' + str(self.perid)

    class Meta:
        managed = True
        db_table = 'EKLSIMBPER'
        unique_together = (('eklid', 'simbid'),)


class Eklsind(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    eklid = models.ForeignKey(Eklogestbl, models.DO_NOTHING, db_column='eklID')  # Field name made lowercase.
    sindid = models.ForeignKey(Sindiasmoi, models.CASCADE, db_column='sindID')  # Field name made lowercase.
    aa = models.CharField(max_length=45)
    edresa = models.IntegerField(db_column='edresA', default=0)  # Field name made lowercase.
    edresa_ypol = models.IntegerField(db_column='edresA_Ypol',default=0)  # Field name made lowercase.
    edresa_teliko = models.IntegerField(db_column='edresA_Teliko',default=0)  # Field name made lowercase.
    edresb = models.IntegerField(db_column='edresB',default=0)  # Field name made lowercase.
    ypol = models.IntegerField(default=0)

    def __str__(self):
        return str(self.eklid) + ' - ' + str(self.sindid) + ' - ' + str(self.edresa_teliko)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # obj is not None, so this is an edit
            return ['sindid', ]  # Return a list or tuple of readonly fields' names
        else:  # This is an addition
            return []

    class Meta:
        managed = True
        db_table = 'EKLSIND'
        unique_together = (('eklid', 'sindid'),)


class Eklsindkoin(models.Model):
    eklid = models.ForeignKey(Eklogestbl, models.DO_NOTHING, db_column='eklID')  # Field name made lowercase.
    sindid = models.ForeignKey(Sindiasmoi, models.DO_NOTHING, db_column='sindID')  # Field name made lowercase.
    koinid = models.ForeignKey(Koinotites, models.DO_NOTHING, db_column='koinID')  # Field name made lowercase.
    aa = models.CharField(max_length=45)
    proedros = models.CharField(max_length=100, blank=True)
    edresk = models.IntegerField(db_column='edresK', default=0)  # Field name made lowercase.
    edresk_ypol = models.IntegerField(db_column='edresK_Ypol', default=0 )  # Field name made lowercase.
    edresk_teliko = models.IntegerField(db_column='edresK_Teliko', default=0)  # Field name made lowercase.
    ypol = models.IntegerField(default=0)
    checkfordraw = models.IntegerField(db_column='checkForDraw', default=0)  # Field name made lowercase.

    def __str__(self):
        return str(self.eklid) + ' - ' + str(self.sindid) + ' - ' + str(self.koinid) + ' - ' + str(self.edresk_teliko)

    class Meta:
        managed = True
        db_table = 'EKLSINDKOIN'
        unique_together = (('eklid', 'sindid', 'koinid'),)


class Eklsindsimb(models.Model):
    eklid = models.ForeignKey(Eklogestbl, models.DO_NOTHING, db_column='eklID')  # Field name made lowercase.
    sindid = models.ForeignKey(Sindiasmoi, models.CASCADE, db_column='sindID', blank=True, null=True)  # Field name made lowercase.
    simbid = models.ForeignKey(Simbouloi, models.CASCADE, db_column='simbID')  # Field name made lowercase.
    aa = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return str(self.eklid) + ' - ' + str(self.sindid) + ' - ' + str(self.simbid)

    class Meta:
        managed = True
        db_table = 'EKLSINDSIMB'
        unique_together = (('eklid', 'simbid'),)


class Kentra(models.Model):
    kenid = models.AutoField(db_column='kenID', primary_key=True)  # Field name made lowercase.
    descr = models.CharField(max_length=45)
    eggegrammenoia = models.IntegerField(db_column='eggegrammenoiA', default=0)  # Field name made lowercase.
    psifisana = models.IntegerField(db_column='psifisanA', default=0)  # Field name made lowercase.
    egkiraa = models.IntegerField(db_column='egkiraA', default=0)  # Field name made lowercase.
    akiraa = models.IntegerField(db_column='akiraA', default=0)  # Field name made lowercase.
    lefkaa = models.IntegerField(db_column='lefkaA', default=0)  # Field name made lowercase.
    sinoloakiralefkaa = models.IntegerField(db_column='sinoloAkiraLefkaA', default=0)  # Field name made lowercase.
    comments = models.CharField(max_length=250, blank=True)
    eklid = models.ForeignKey(Eklogestbl, models.DO_NOTHING, db_column='eklID')  # Field name made lowercase.
    perid = models.ForeignKey(Perifereies, models.DO_NOTHING, db_column='perID')  # Field name made lowercase.
    koinid = models.ForeignKey(Koinotites, models.DO_NOTHING, db_column='koinID')  # Field name made lowercase.
    eggegrammenoib = models.IntegerField(db_column='eggegrammenoiB', default=0)  # Field name made lowercase.
    psifisanb = models.IntegerField(db_column='psifisanB', default=0)  # Field name made lowercase.
    egkirab = models.IntegerField(db_column='egkiraB', default=0)  # Field name made lowercase.
    akirab = models.IntegerField(db_column='akiraB', default=0)  # Field name made lowercase.
    lefkab = models.IntegerField(db_column='lefkaB', default=0)  # Field name made lowercase.
    sinoloakiralefkab = models.IntegerField(db_column='sinoloAkiraLefkaB', default=0)  # Field name made lowercase.
    eggegrammenoik = models.IntegerField(db_column='eggegrammenoiK', default=0)  # Field name made lowercase.
    psifisank = models.IntegerField(db_column='psifisanK', default=0)  # Field name made lowercase.
    egkirak = models.IntegerField(db_column='egkiraK', default=0)  # Field name made lowercase.
    akirak = models.IntegerField(db_column='akiraK', default=0)  # Field name made lowercase.
    lefkak = models.IntegerField(db_column='lefkaK', default=0)  # Field name made lowercase.
    sinoloakiralefkak = models.IntegerField(db_column='sinoloAkiraLefkaK', default=0)  # Field name made lowercase.


    def __str__(self):
        return self.descr + ' - ' + str(self.koinid)

    class Meta:
        managed = True
        db_table = 'KENTRA'
        unique_together = (('descr', 'eklid'),)


class Psifodeltia(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    sindid = models.ForeignKey(Sindiasmoi, models.CASCADE, db_column='sindID')  # Field name made lowercase.
    kenid = models.ForeignKey(Kentra, models.CASCADE, db_column='kenID')  # Field name made lowercase.
    votesa = models.IntegerField(db_column='votesA', default=0)  # Field name made lowercase.
    votesb = models.IntegerField(db_column='votesB', default=0)  # Field name made lowercase.
    votesk = models.IntegerField(db_column='votesK', default=0)  # Field name made lowercase.

    def __str__(self):
        return  str(self.sindid) +  ' - ' + str(self.kenid)

    class Meta:
        managed = True
        db_table = 'PSIFODELTIA'
        unique_together = (('sindid', 'kenid'),)


class Psifoi(models.Model):
    simbid = models.ForeignKey(Simbouloi, models.CASCADE, db_column='simbID')  # Field name made lowercase.
    kenid = models.ForeignKey(Kentra, models.CASCADE, db_column='kenID')  # Field name made lowercase.
    votes = models.IntegerField(default=0)

    def __str__(self):
        return  str(self.simbid) + ' - ' +  str(self.kenid) + ' - ' + str(self.votes)

    class Meta:
        managed = True
        db_table = 'PSIFOI'
        unique_together = (('simbid', 'kenid'),)

#DATABASE VIEWS

class EklKatametrimenaBVw(models.Model):
    id = models.IntegerField(primary_key=True)
    eklid = models.IntegerField(db_column='eklID')  # Field name made lowercase.
    katametrimenab = models.BigIntegerField(db_column='katametrimenaB')  # Field name made lowercase.

    def __str__(self):
        return str(self.eklid) + ' - ' + str(self.katametrimenab)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'EKL_KATAMETRIMENA_B_VW'


class EklKatametrimenaPsifoiVw(models.Model):
    id = models.IntegerField(primary_key=True)
    eklid = models.IntegerField(db_column='eklID')  # Field name made lowercase.
    katametrimena = models.BigIntegerField()

    def __str__(self):
        return str(self.eklid) + ' - ' + str(self.katametrimena)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'EKL_KATAMETRIMENA_PSIFOI_VW'


class EklKatametrimenaVw(models.Model):
    id = models.IntegerField(primary_key=True)
    eklid = models.IntegerField(db_column='eklID')  # Field name made lowercase.
    katametrimena = models.BigIntegerField()

    def __str__(self):
        return str(self.eklid) + ' - ' + str(self.katametrimena)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'EKL_KATAMETRIMENA_VW'


class EklPosostasindPerVw(models.Model):
    id = models.IntegerField(primary_key=True)
    eklid = models.IntegerField(db_column='eklID')  # Field name made lowercase.
    perid = models.IntegerField(db_column='perID')  # Field name made lowercase.
    perifereia = models.CharField(db_column='perifereia',max_length=100)
    sindiasmos = models.CharField(db_column='sindiasmos',max_length=100)
    shortdescr = models.CharField(db_column='shortDescr', max_length=50)
    sumper = models.DecimalField(db_column='sumPer', max_digits=32, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    sumvotes = models.DecimalField(db_column='sumVotes', max_digits=32, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    posostosindiasmou = models.DecimalField(max_digits=38, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.sindiasmos + ' - ' + self.perifereia

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'EKL_POSOSTASIND_PER_VW'


class EklPsifoisimbVw(models.Model):
    id = models.IntegerField(primary_key=True)
    eklid = models.IntegerField(db_column='eklID')  # Field name made lowercase.
    sindid = models.IntegerField(db_column='sindID', blank=True, null=True)  # Field name made lowercase.
    sindiasmos = models.CharField(max_length=100, blank=True, null=True)
    simbid = models.IntegerField(db_column='simbID')  # Field name made lowercase.
    surname = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    fathername = models.CharField(max_length=100)
    kenid = models.IntegerField(db_column='kenID')  # Field name made lowercase.
    kentro = models.CharField(max_length=45)
    votes = models.IntegerField()

    def __str__(self):
        return self.sindiasmos + ' - ' + self.surname

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'EKL_PSIFOISIMB_VW'


class EklSindedresKoinVw(models.Model):
    id = models.IntegerField(primary_key=True)
    eklid = models.IntegerField(db_column='eklID')  # Field name made lowercase.
    sindid = models.IntegerField(db_column='sindID')  # Field name made lowercase.
    koinid = models.IntegerField(db_column='koinID')  # Field name made lowercase.
    edresk = models.IntegerField(db_column='edresK')  # Field name made lowercase.
    edresk_ypol = models.IntegerField(db_column='edresK_Ypol')  # Field name made lowercase.
    edresk_teliko = models.IntegerField(db_column='edresK_Teliko')  # Field name made lowercase.
    ypol = models.IntegerField()
    sumedres = models.DecimalField(db_column='sumEdres', max_digits=32, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    sumedresypol = models.DecimalField(db_column='sumEdresYpol', max_digits=32, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    sumedresteliko = models.DecimalField(db_column='sumEdresTeliko', max_digits=32, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    sinolo = models.IntegerField()
    checkfordraw = models.IntegerField(db_column='checkForDraw')  # Field name made lowercase.

    def __str__(self):
        return str(self.eklid) + ' - ' + str(self.koinid) + ' - ' + str(self.sumedresteliko)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'EKL_SINDEDRES_KOIN_VW'


class EklSinolokentrwnAnaAnametrhsh(models.Model):
    id = models.IntegerField(primary_key=True)
    eklid = models.IntegerField()
    plithoskentrwn = models.BigIntegerField(db_column='plithosKentrwn')  # Field name made lowercase.

    def __str__(self):
        return str(self.eklid) + ' - ' + str(self.plithoskentrwn)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'EKL_SINOLOKENTRWN_ANA_ANAMETRHSH'


class EklSumpsifodeltiasindKenVw(models.Model):
    id = models.IntegerField(primary_key=True)
    eklid = models.IntegerField(db_column='eklID')  # Field name made lowercase.
    kenid = models.IntegerField(db_column='kenID')  # Field name made lowercase.
    kentro = models.CharField(max_length=45)
    votes = models.IntegerField()
    votesb = models.IntegerField(db_column='votesB')  # Field name made lowercase.
    sindid = models.IntegerField(db_column='sindID')  # Field name made lowercase.
    sindiasmos = models.CharField(max_length=100)

    def __str__(self):
        return str(self.kenid) + ' - ' + self.sindiasmos

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'EKL_SUMPSIFODELTIASIND_KEN_VW'


class EklSumpsifodeltiasindKoinVw(models.Model):
    id = models.IntegerField(primary_key=True)
    eklid = models.IntegerField(db_column='eklID')  # Field name made lowercase.
    sindid = models.IntegerField(db_column='sindID')  # Field name made lowercase.
    sindiasmos = models.CharField(max_length=100)
    koinid = models.IntegerField(db_column='koinID')  # Field name made lowercase.
    sumsindiasmou = models.DecimalField(db_column='sumSindiasmou', max_digits=32, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    sumkoinotitas = models.DecimalField(db_column='sumKoinotitas', max_digits=32, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.sindiasmos + ' - ' + str(self.sumsindiasmou)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'EKL_SUMPSIFODELTIASIND_KOIN_VW'


class EklSumpsifodeltiasindPerVw(models.Model):
    id = models.IntegerField(primary_key=True)
    eklid = models.IntegerField(db_column='eklID')  # Field name made lowercase.
    sindid = models.IntegerField(db_column='sindID')  # Field name made lowercase.
    sindiasmos = models.CharField(db_column='sindiasmos', max_length=100)
    shortdescr = models.CharField(db_column='shortDescr', max_length=50)
    perifereia = models.CharField(max_length=100)
    perid = models.IntegerField(db_column='perID')  # Field name made lowercase.
    sumvotes = models.DecimalField(db_column='sumVotes', max_digits=32, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.sindiasmos + ' - ' +str(self.sumvotes)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'EKL_SUMPSIFODELTIASIND_PER_VW'


class EklSumpsifodeltiasindVw(models.Model):
    id = models.IntegerField(primary_key=True)
    eklid = models.IntegerField(db_column='eklID')  # Field name made lowercase.
    sindid = models.IntegerField(db_column='sindID')  # Field name made lowercase.
    sindiasmos = models.CharField(max_length=100)
    shortdescr = models.CharField(db_column='shortDescr', max_length=50)  # Field name made lowercase.
    photo=models.ImageField(db_column='photo',null=True)
    sumvotes = models.DecimalField(db_column='sumVotes', max_digits=32, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    sinola = models.DecimalField(max_digits=32, decimal_places=0, blank=True, null=True)
    katametrimena = models.BigIntegerField(blank=True, null=True)
    plithoskentrwn = models.BigIntegerField(db_column='plithosKentrwn')  # Field name made lowercase.
    posostosindiasmou = models.DecimalField(db_column='posostoSindiasmou', max_digits=38, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    posostokatametrimenwnkentrwn = models.DecimalField(db_column='posostoKatametrimenwnKentrwn', max_digits=26, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    sumvotesb = models.DecimalField(db_column='sumVotesB', max_digits=32, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    sinolab = models.DecimalField(db_column='sinolaB', max_digits=32, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    posostosindiasmoub = models.DecimalField(db_column='posostoSindiasmouB', max_digits=38, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    katametrimenab = models.BigIntegerField(db_column='katametrimenaB', blank=True, null=True)  # Field name made lowercase.
    posostokatametrimenwnkentrwnb = models.DecimalField(db_column='posostoKatametrimenwnKentrwnB', max_digits=26, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.sindiasmos + ' - ' + str(self.posostosindiasmou)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'EKL_SUMPSIFODELTIASIND_VW'


class EklSumpsifodeltiaKenVw(models.Model):
    id = models.IntegerField(primary_key=True)
    eklid = models.IntegerField(db_column='eklID')  # Field name made lowercase.
    kentro = models.CharField(max_length=45)
    kenid = models.IntegerField(db_column='kenID')  # Field name made lowercase.
    sumvotes = models.DecimalField(db_column='sumVotes', max_digits=32, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    sumvotesb = models.DecimalField(db_column='sumVotesB', max_digits=32, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.kentro  + ' - ' +  str(self.sumvotes)


    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'EKL_SUMPSIFODELTIA_KEN_VW'


class EklSumpsifodeltiaPerVw(models.Model):
    id = models.IntegerField(primary_key=True)
    eklid = models.IntegerField(db_column='eklID')  # Field name made lowercase.
    perid = models.IntegerField(db_column='perID')  # Field name made lowercase.
    sumvotes = models.DecimalField(db_column='sumVotes', max_digits=32, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return str(self.perid)  + ' - ' + str(self.sumvotes)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'EKL_SUMPSIFODELTIA_PER_VW'


class EklSumpsifoisimbAnalytikoAnaperifereia(models.Model):
    id = models.IntegerField(primary_key=True)
    eklid = models.IntegerField(db_column='eklID')  # Field name made lowercase.
    eidos = models.CharField(max_length=20)
    simbid = models.IntegerField(db_column='simbID')  # Field name made lowercase.
    eklsimbkoin_simbid = models.IntegerField(db_column='EKLSIMBKOIN_simbID', blank=True, null=True)  # Field name made lowercase.
    surname = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    fathername = models.CharField(max_length=100)
    perid = models.IntegerField(db_column='perID')  # Field name made lowercase.
    perifereia = models.CharField(max_length=100)
    sumvotes = models.DecimalField(db_column='sumVotes', max_digits=32, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    sindid = models.IntegerField(db_column='sindID', blank=True, null=True)  # Field name made lowercase.
    sindiasmos = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.perifereia  + ' - ' +  self.surname  + ' - ' +  str(self.sumvotes)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'EKL_SUMPSIFOISIMB_ANALYTIKO_ANAPERIFEREIA'


class EklSumpsifoisimbKoinVw(models.Model):
    id = models.IntegerField(primary_key=True)
    eklid = models.IntegerField(db_column='eklID')  # Field name made lowercase.
    simbid = models.IntegerField(db_column='simbID')  # Field name made lowercase.
    surname = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    fathername = models.CharField(max_length=100)
    toposeklogisid = models.IntegerField(db_column='toposEklogisID')  # Field name made lowercase.
    toposeklogis = models.CharField(db_column='toposEklogis', max_length=100)  # Field name made lowercase.
    eidoskoinotitas = models.IntegerField(db_column='eidosKoinotitas')  # Field name made lowercase.
    sindid = models.IntegerField(db_column='sindID', blank=True, null=True)  # Field name made lowercase.
    sindiasmos = models.CharField(max_length=100, blank=True, null=True)
    sumvotes = models.DecimalField(db_column='sumVotes', max_digits=32, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.toposeklogis  + ' - ' +  self.surname  + ' - ' +  str(self.sumvotes)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'EKL_SUMPSIFOISIMB_KOIN_VW'


class EklSumpsifoisimbPerVw(models.Model):
    id = models.IntegerField(primary_key=True)
    eklid = models.IntegerField(db_column='eklID')  # Field name made lowercase.
    simbid = models.IntegerField(db_column='simbID')  # Field name made lowercase.
    surname = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    fathername = models.CharField(max_length=100)
    toposeklogisid = models.IntegerField(db_column='toposEklogisID')  # Field name made lowercase.
    toposeklogis = models.CharField(db_column='toposEklogis', max_length=100)  # Field name made lowercase.
    sindid = models.IntegerField(db_column='sindID', blank=True, null=True)  # Field name made lowercase.
    sindiasmos = models.CharField(max_length=100, blank=True, null=True)
    sumvotes = models.DecimalField(db_column='sumVotes', max_digits=32, decimal_places=0, blank=True, null=True)  # Field name made lowercase.


    def __str__(self):
        return self.toposeklogis  + ' - ' +  self.surname  + ' - ' +  str(self.sumvotes)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'EKL_SUMPSIFOISIMB_PER_VW'


class EklSumpsifoisimbVw(models.Model):
    eklid = models.IntegerField(db_column='eklID')  # Field name made lowercase.
    simbid = models.IntegerField(db_column='simbID')  # Field name made lowercase.
    surname = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    fathername = models.CharField(max_length=100)
    toposeklogisid = models.IntegerField(db_column='toposEklogisID')  # Field name made lowercase.
    toposeklogis = models.CharField(db_column='toposEklogis', max_length=100)  # Field name made lowercase.
    eidoskoinotitas = models.IntegerField(db_column='eidosKoinotitas', blank=True, null=True)  # Field name made lowercase.
    sindid = models.IntegerField(db_column='sindID', blank=True, null=True)  # Field name made lowercase.
    sindiasmos = models.CharField(max_length=100, blank=True, null=True)
    sumvotes = models.DecimalField(db_column='sumVotes', max_digits=32, decimal_places=0, blank=True, null=True)  # Field name made lowercase.


    def __str__(self):
        return self.toposeklogis  + ' - ' +  self.surname  + ' - ' +  str(self.sumvotes)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'EKL_SUMPSIFOISIMB_VW'

class EklSumpsifoisimbWithIdVw(models.Model):
    id = models.IntegerField(primary_key=True)
    eklid = models.IntegerField(db_column='eklID')  # Field name made lowercase.
    simbid = models.IntegerField(db_column='simbID')  # Field name made lowercase.
    surname = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    fathername = models.CharField(max_length=100)
    toposeklogisid = models.IntegerField(db_column='toposEklogisID')  # Field name made lowercase.
    toposeklogis = models.CharField(db_column='toposEklogis', max_length=100)  # Field name made lowercase.
    eidoskoinotitas = models.IntegerField(db_column='eidosKoinotitas', blank=True, null=True)  # Field name made lowercase.
    sindid = models.IntegerField(db_column='sindID', blank=True, null=True)  # Field name made lowercase.
    sindiasmos = models.CharField(max_length=100, blank=True, null=True)
    sumvotes = models.DecimalField(db_column='sumVotes', max_digits=32, decimal_places=0, blank=True, null=True)  # Field name made lowercase.


    def __str__(self):
        return self.toposeklogis  + ' - ' +  self.surname  + ' - ' +  str(self.sumvotes)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'EKL_SUMPSIFOISIMB_WITHID_VW'

class EklallsimbVw(models.Model):
    id = models.IntegerField(primary_key=True)
    eklid = models.IntegerField(db_column='eklID')  # Field name made lowercase.
    simbid = models.IntegerField(db_column='simbID')  # Field name made lowercase.
    surname = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    fathername = models.CharField(max_length=100)
    toposeklogisid = models.IntegerField(db_column='toposEklogisID')  # Field name made lowercase.
    toposeklogis = models.CharField(db_column='toposEklogis', max_length=100)  # Field name made lowercase.
    eidoskoinotitas = models.IntegerField(db_column='eidosKoinotitas', blank=True, null=True)  # Field name made lowercase.
    sindid = models.IntegerField(db_column='sindID', blank=True, null=True)  # Field name made lowercase.
    sindiasmos = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.toposeklogis  + ' - ' +  self.surname

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'EKL_ALLSIMB_VW'




class EklSumpsifoiKenVw(models.Model):
    id = models.IntegerField(primary_key=True)
    eklid = models.IntegerField(db_column='eklID')  # Field name made lowercase.
    kentro = models.CharField(max_length=45)
    kenid = models.IntegerField(db_column='kenID')  # Field name made lowercase.
    sumvotes = models.DecimalField(db_column='sumVotes', max_digits=32, decimal_places=0, blank=True, null=True)  # Field name made lowercase.


    def __str__(self):
        return self.kentro   + ' - ' +  str(self.sumvotes)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'EKL_SUMPSIFOI_KEN_VW'
