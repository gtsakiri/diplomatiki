from django.conf.urls import url
from django.urls import path, re_path
from . import views


urlpatterns = [
path('', views.Elections_list, name='Elections_list'),
#path('', views.simb_modal, name='simb_modal'),

path('edres/<int:eklid>/', views.edres_list, name='edres_list'),
path('edresedit/<int:eklid>/<int:edrid>/', views.edres_edit, name='edres_edit'),
path('edresadd/<int:eklid>/', views.edres_add, name='edres_add'),
path('edresdelete/<int:eklid>/<int:edrid>/', views.edres_delete, name='edres_delete'),

path('edreskoin/<int:eklid>/', views.edreskoin_list, name='edreskoin_list'),
path('edreskoinedit/<int:eklid>/<int:edrid>/', views.edreskoin_edit, name='edreskoin_edit'),
path('edreskoinadd/<int:eklid>/', views.edreskoin_add, name='edreskoin_add'),
path('edreskoindelete/<int:eklid>/<int:edrid>/', views.edreskoin_delete, name='edreskoin_delete'),

path('typeofkoinotita/<int:eklid>/', views.typeofkoinotita_list, name='typeofkoinotita_list'),
path('typeofkoinotitaedit/<int:eklid>/<int:tpkid>/', views.typeofkoinotita_edit, name='typeofkoinotita_edit'),
path('typeofkoinotitaadd/<int:eklid>/', views.typeofkoinotita_add, name='typeofkoinotita_add'),
path('typeofkoinotitadelete/<int:eklid>/<int:tpkid>/', views.typeofkoinotita_delete, name='typeofkoinotita_delete'),

path('sistima/<int:eklid>/', views.sistima_list, name='sistima_list'),
path('sistimaedit/<int:eklid>/<int:sisid>/', views.sistima_edit, name='sistima_edit'),
path('sistimaadd/<int:eklid>/', views.sistima_add, name='sistima_add'),
path('sistimadelete/<int:eklid>/<int:sisid>/', views.sistima_delete, name='sistima_delete'),

path('perifereia/<int:eklid>/', views.perifereia_list, name='perifereia_list'),
path('perifereiaedit/<int:eklid>/<int:perid>/', views.perifereia_edit, name='perifereia_edit'),
path('perifereiaadd/<int:eklid>/', views.perifereia_add, name='perifereia_add'),
path('perifereiadelete/<int:eklid>/<int:perid>/', views.perifereia_delete, name='perifereia_delete'),

path('koinotites/<int:eklid>/', views.koinotites_list, name='koinotites_list'),
path('koinotitesedit/<int:eklid>/<int:koinid>/', views.koinotites_edit, name='koinotites_edit'),
path('koinotitesdd/<int:eklid>/', views.koinotites_add, name='koinotites_add'),
path('koinotitesdelete/<int:eklid>/<int:koinid>/', views.koinotites_delete, name='koinotites_delete'),

path('kentra/<int:eklid>/', views.kentra_list, name='kentra_list'),
path('kentraedit/<int:eklid>/<int:kenid>/', views.kentra_edit, name='kentra_edit'),
path('kentradd/<int:eklid>/', views.kentra_add, name='kentra_add'),
path('kentradelete/<int:eklid>/<int:kenid>/', views.kentra_delete, name='kentra_delete'),

path('ajax/load-koinotites/<int:eklid>/', views.load_koinotites, name='ajax_load_koinotites'),
path('ajax/load-modal/', views.simb_modal, name='simb_modal'),

path('sindiasmoi/<int:eklid>/', views.sindiasmoi_list, name='sindiasmoi_list'),
path('sindiasmoiedit/<int:eklid>/<int:sindid>/', views.sindiasmoi_edit, name='sindiasmoi_edit'),
path('sindiasmoiadd/<int:eklid>/', views.sindiasmoi_add, name='sindiasmoi_add'),
path('sindiasmoidelete/<int:eklid>/<int:sindid>/', views.sindiasmoi_delete, name='sindiasmoi_delete'),

path('simbouloi/<int:eklid>/', views.simbouloi_list, name='simbouloi_list'),
path('simbouloiedit/<int:eklid>/<int:simbid>/', views.simbouloi_edit, name='simbouloi_edit'),
path('simbouloiadd/<int:eklid>/', views.simbouloi_add, name='simbouloi_add'),
#path('simbouloidelete/<int:eklid>/<int:simbid>/', views.simbouloi_delete, name='simbouloi_delete'),


path('psifodeltia/<int:eklid>/', views.psifodeltia_list, name='psifodeltia_list'),
path('psifodeltiaedit/<int:eklid>/<int:id>/', views.psifodeltia_edit, name='psifodeltia_edit'),
path('psifodeltiaadd/<int:eklid>/', views.psifodeltia_add, name='psifodeltia_add'),
path('psifodeltiadelete/<int:eklid>/<int:id>/', views.psifodeltia_delete, name='psifodeltia_delete'),

path('eklsind/<int:eklid>/', views.eklsind_list, name='eklsind_list'),
path('eklsindedit/<int:eklid>/<int:id>/', views.eklsind_edit, name='eklsind_edit'),
path('eklsindadd/<int:eklid>/', views.eklsind_add, name='eklsind_add'),
path('eklsinddelete/<int:eklid>/<int:id>/', views.eklsind_delete, name='eklsind_delete'),

path('eklsindkoin/<int:eklid>/', views.eklsindkoin_list, name='eklsindkoin_list'),
path('eklsindkoinedit/<int:eklid>/<int:id>/', views.eklsindkoin_edit, name='eklsindkoin_edit'),
path('eklsindkoinadd/<int:eklid>/', views.eklsindkoin_add, name='eklsindkoin_add'),
path('eklsindkoindelete/<int:eklid>/<int:id>/', views.eklsindkoin_delete, name='eklsindkoin_delete'),

path('ekloges/<int:eklid>/', views.ekloges_list, name='ekloges_list'),
path('eklogesedit/<int:eklid>/<int:cureklid>/', views.ekloges_edit, name='ekloges_edit'),
path('eklogesadd/<int:eklid>/', views.ekloges_add, name='ekloges_add'),
path('eklogesdelete/<int:eklid>/<int:cureklid>/', views.ekloges_delete, name='ekloges_delete'),

path('pososta/<int:eklid>/', views.pososta_telika, name='pososta_telika'),
path('posostaper/<int:eklid>/', views.pososta_perifereies, name='pososta_perifereies'),
path('psifoisimbperifereies/<int:eklid>/', views.psifoisimb_perifereies, name='psifoisimb_perifereies'),
path('psifoisimbkoinotites/<int:eklid>/<int:eidoskoinotitas>', views.psifoisimb_koinotites, name='psifoisimb_koinotites'),
path('psifodeltiasind_ken/<int:eklid>/', views.psifodeltiasind_ken, name='psifodeltiasind_ken'),
path('psifoisimb_ken/<int:eklid>/', views.psifoisimb_ken, name='psifoisimb_ken'),
path('export/per/<int:eklid>/<int:selected_order>/', views.export_psifoiper_xls, name='export_psifoiper_xls'),
path('export/koin/<int:eklid>/<int:selected_order>/', views.export_psifoikoin_xls, name='export_psifoikoin_xls'),
path('export/psifodeltiasindken/<int:eklid>/<int:selected_order>/', views.export_psifodeltiasind_ken, name='export_psifodeltiasind_ken'),
path('export/psifoisimbken/<int:eklid>/<int:selected_order>/', views.export_psifoisimb_ken, name='export_psifoisimbken'),

]

