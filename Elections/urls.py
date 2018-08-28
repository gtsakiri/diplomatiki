from django.conf.urls import url
from django.urls import path, re_path
from . import views


urlpatterns = [
path('', views.Elections_list, name='Elections_list'),
path('edres/<int:eklid>/', views.edres_list, name='edres_list'),
path('edresedit/<int:eklid>/<int:edrid>/', views.edres_edit, name='edres_edit'),
path('edresadd/<int:eklid>/', views.edres_add, name='edres_add'),
path('edresdelete/<int:eklid>/<int:edrid>/', views.edres_delete, name='edres_delete'),

path('sistima/<int:eklid>/', views.sistima_list, name='sistima_list'),
path('sistimaedit/<int:eklid>/<int:sisid>/', views.sistima_edit, name='sistima_edit'),
path('sistimaadd/<int:eklid>/', views.sistima_add, name='sistima_add'),
path('sistimadelete/<int:eklid>/<int:sisid>/', views.sistima_delete, name='sistima_delete'),

path('sindiasmoi/<int:eklid>/', views.sindiasmoi_list, name='sindiasmoi_list'),
path('sindiasmoiedit/<int:eklid>/<int:sindid>/', views.sindiasmoi_edit, name='sindiasmoi_edit'),
path('sindiasmoiadd/<int:eklid>/', views.sindiasmoi_add, name='sindiasmoi_add'),
path('sindiasmoidelete/<int:eklid>/<int:sindid>/', views.sindiasmoi_delete, name='sindiasmoi_delete'),

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

