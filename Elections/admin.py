from django.contrib import admin

from .models import Edres, Edreskoin, Eklogestbl, Eklper, Eklperkoin, Eklsimbkoin, Eklsimbper, Eklsind
from .models import Eklsindkoin, Eklsindsimb, Kentra, Koinotites, Perifereies, Psifodeltia, Psifoi, Simbouloi, Sindiasmoi
from .models import Sistima, Typeofkoinotita, EklSumpsifodeltiasindVw, EklSumpsifoiKenVw


class EdresAdmin(admin.ModelAdmin):
    list_display = ('edrid', 'descr','sinoloedrwn', 'edresprwtou', 'edresypoloipwn')

class EdresKoinAdmin(admin.ModelAdmin):
    list_display = ('edrid', 'descr','sinolo')

class EklogestblAdmin(admin.ModelAdmin):
    list_display = ('eklid', 'descr', 'dateofelection', 'dimos', 'sisid', 'edrid', 'visible', 'defaultelection')

class EklperAdmin(admin.ModelAdmin):
    list_display = ('id', 'eklid', 'perid')
    list_filter = ('eklid','perid',)

class EklperkoinAdmin(admin.ModelAdmin):
    list_display = ('id', 'eklid', 'perid', 'koinid', 'edrid')
    list_filter = ('eklid','perid','koinid',)

class EklsimbkoinAdmin(admin.ModelAdmin):
    list_display = ('id', 'eklid', 'simbid', 'koinid')
    list_filter = ('eklid', 'koinid',)

class EklsimbperAdmin(admin.ModelAdmin):
    list_display = ('id', 'eklid', 'simbid', 'perid')
    list_filter = ('eklid', 'perid',)

class EklsindAdmin(admin.ModelAdmin):
    list_display = ('id', 'eklid', 'sindid', 'aa', 'edresa', 'edresa_ypol', 'edresa_teliko', 'edresb', 'ypol')
    list_filter = ('eklid', 'sindid', )

class EklsindsimbAdmin(admin.ModelAdmin):
    list_display = ('id', 'eklid', 'sindid',  'simbid', 'aa')
    list_filter = ('eklid', 'sindid',)

class EklsindkoinAdmin(admin.ModelAdmin):
    list_display = ('id', 'eklid', 'sindid', 'koinid' ,'aa', 'proedros', 'edresk', 'edresk_ypol', 'edresk_teliko',  'ypol', 'checkfordraw')
    list_filter = ('eklid', 'sindid','koinid',)

class KentraAdmin(admin.ModelAdmin):
    list_display = ('kenid', 'descr', 'comments', 'eklid')
    list_filter = ( 'eklid','descr',)

class KoinotitesAdmin(admin.ModelAdmin):
    list_display = ('koinid', 'descr', 'eidos')
    list_filter = ('descr', 'eidos',)

class PerifereiesAdmin(admin.ModelAdmin):
    list_display = ('perid', 'descr')
    list_filter = ('descr',)

class PsifodeltiaAdmin(admin.ModelAdmin):
    list_display = ('id', 'sindid', 'kenid', 'votesa', 'votesb', 'votesk')
    list_filter = ('sindid', )


class PsifoiAdmin(admin.ModelAdmin):
    list_display = ('id', 'simbid', 'kenid', 'votes')
    list_filter = ('kenid', )


class SimbouloiAdmin(admin.ModelAdmin):
    list_display = ('simbid', 'surname', 'firstname', 'fathername', 'comments')
    list_filter = ('surname',)

class SindiasmoiAdmin(admin.ModelAdmin):
    list_display = ('sindid', 'descr', 'shortdescr', 'photofield', 'eidos')

class SistimaAdmin(admin.ModelAdmin):
    list_display = ('sisid', 'descr')

class TypeofkoinotitaAdmin(admin.ModelAdmin):
    list_display = ('tpkid', 'descr')



admin.site.register(Edres, EdresAdmin)
admin.site.register(Edreskoin, EdresKoinAdmin)
admin.site.register(Eklogestbl, EklogestblAdmin)
admin.site.register(Eklper, EklperAdmin)
admin.site.register(Eklperkoin, EklperkoinAdmin)
admin.site.register(Eklsimbkoin, EklsimbkoinAdmin)
admin.site.register(Eklsimbper, EklsimbperAdmin)
admin.site.register(Eklsind, EklsindAdmin)
admin.site.register(Eklsindkoin, EklsindkoinAdmin)
admin.site.register(Eklsindsimb, EklsindsimbAdmin)
admin.site.register(Kentra, KentraAdmin)
admin.site.register(Koinotites, KoinotitesAdmin)
admin.site.register(Perifereies, PerifereiesAdmin)
admin.site.register(Psifodeltia, PsifodeltiaAdmin)
admin.site.register(Psifoi, PsifoiAdmin)
admin.site.register(Simbouloi, SimbouloiAdmin)
admin.site.register(Sindiasmoi, SindiasmoiAdmin)
admin.site.register(Sistima, SistimaAdmin)
admin.site.register(Typeofkoinotita, TypeofkoinotitaAdmin)



#admin.site.register(EklSumpsifodeltiasindVw)
#admin.site.register(EklSumpsifoiKenVw)

