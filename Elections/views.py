import xlwt
import mysql.connector
from django.contrib import  messages
from django.conf import settings
from django.contrib.auth import  authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from django.forms import DateInput, modelformset_factory
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
import datetime

from mysql.connector import Error
from mysql.connector import errorcode

from .models import Eklogestbl, EklSumpsifodeltiasindVw, EklPosostasindPerVw, Perifereies, \
    EklSumpsifoisimbPerVw, EklSumpsifoisimbKoinVw, Koinotites, EklSumpsifodeltiasindKenVw, \
    Kentra, EklPsifoisimbVw, Edres, Sistima, Sindiasmoi, Eklsind, Eklper, Edreskoin, Typeofkoinotita, Eklperkoin, \
    Eklsindkoin, Psifodeltia, Simbouloi, EklSumpsifoisimbWithIdVw, Eklsimbper, Eklsindsimb, Eklsimbkoin, EklallsimbVw, \
    Psifoi, EklSumpsifoisimbVw, EklSumpsifodeltiasindKoinVw, EklSumpsifodeltiasindKoinVw, \
    EklSumpsifodeltiasindKenTopikoiOnlyVw, EklSumpsifoisimbPerLightVw, EklKatametrimenaPsifoiVw, EklSumpsifoiKenVw, EklKatametrimenaPsifoiKoinotitesOnlyVw, EklSumpsifoiKoinVw
from .forms import EdresForm, SistimaForm, EklogestblForm, SindiasmoiForm, EklsindForm, PerifereiesForm, EdresKoinForm, \
    TypeofkoinotitaForm, KoinotitesForm, EklsindkoinForm, KentraForm, PsifodeltiaForm, SimbouloiForm, PsifoiForm, \
    PsifodeltiaKoinForm
from django.core.exceptions import PermissionDenied

from django.db import connection


def export_psifoiper_xls(request,eklid, selected_order):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="psifoiper.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('data')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.height = 280
    font_style.font.bold = True

    ws.write(row_num, 0, 'Κατάταξη υποψ. δημ. συμβούλων ανα Εκλ. Περιφέρεια', font_style)

    row_num += 2

    katametrimena_psifoi = EklKatametrimenaPsifoiVw.objects.get(eklid=eklid).katametrimena
    firstrow = EklSumpsifodeltiasindVw.objects.filter(eklid=eklid).values_list('katametrimena', 'plithoskentrwn','posostokatametrimenwnkentrwn').distinct()
    # for col_num in range(len(firstrow[0])):
    if firstrow:
        ws.write(row_num, 0,'Στα ' + str(katametrimena_psifoi) + ' από τα ' + str(firstrow[0][1]) + ' εκλ. κέντρα', font_style)
    else:
        #ws.write(row_num, 0, 'Δεν υπάρχουν καταχωρήσεις!', font_style)
        messages.error(request, 'Δεν υπάρχουν καταχωρήσεις!')
        return redirect('psifoisimb_perifereies', eklid)

    font_style = xlwt.XFStyle()
    font_style.font.height = 240
    font_style.font.bold = True

    row_num += 2

    columns = ['Συνδυασμός', 'Επίθετο', 'Όνομα', 'Ον. πατρός', 'Εκλ. Περιφέρεια', 'Ψήφοι']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    #rows = EklSumpsifoisimbPerVw.objects.filter(eklid=eklid).values_list('sindiasmos', 'surname', 'firstname', 'fathername', 'toposeklogis', 'sumvotes')
    if selected_order == 1:
        rows = EklSumpsifoisimbPerVw.objects.filter(eklid=eklid).values_list('sindiasmosnew', 'surname', 'firstname', 'fathername', 'toposeklogis', 'sumvotes').order_by('sindiasmosnew','-sumvotes')
    elif selected_order == 2:
        rows = EklSumpsifoisimbPerVw.objects.filter(eklid=eklid).values_list('sindiasmosnew', 'surname', 'firstname', 'fathername', 'toposeklogis', 'sumvotes').order_by('sindiasmosnew','surname', 'firstname')
    else:
        rows = EklSumpsifoisimbPerVw.objects.filter(eklid=eklid).values_list('sindiasmosnew', 'surname', 'firstname', 'fathername', 'toposeklogis', 'sumvotes').order_by('-sumvotes')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def export_psifoikoin_xls(request,eklid, selected_order, eidoskoinotitas):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="psifoikoin.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('data')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.height = 280
    font_style.font.bold = True

    ws.write(row_num, 0, 'Κατάταξη υποψ. συμβούλων Κοινοτήτων', font_style)

    row_num+=2

    katametrimena_koinotites = EklKatametrimenaPsifoiKoinotitesOnlyVw.objects.get(eklid=eklid).katametrimena_koinotites
    firstrow=EklSumpsifodeltiasindVw.objects.filter(eklid=eklid).values_list('katametrimena', 'plithoskentrwn','posostokatametrimenwnkentrwn').distinct()
    #for col_num in range(len(firstrow[0])):
    if firstrow:
        ws.write(row_num, 0, 'Στα ' + str(katametrimena_koinotites)+ ' από τα '+ str(firstrow[0][1]) + ' εκλ. κέντρα' , font_style)
    else:
        #ws.write(row_num, 0, 'Δεν υπάρχουν καταχωρήσεις!', font_style)
        messages.error(request, 'Δεν υπάρχουν καταχωρήσεις!')
        return redirect('psifoisimb_koinotites', eklid, eidoskoinotitas)

    font_style = xlwt.XFStyle()
    font_style.font.height = 240
    font_style.font.bold = True

    row_num += 2

    columns = ['Συνδυασμός', 'Επίθετο', 'Όνομα', 'Ον. πατρός', 'Κοινότητα', 'Ψήφοι']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    #rows = EklSumpsifoisimbPerVw.objects.filter(eklid=eklid).values_list('sindiasmos', 'surname', 'firstname', 'fathername', 'toposeklogis', 'sumvotes')
    if selected_order == 1:
        rows = EklSumpsifoisimbKoinVw.objects.filter(eklid=eklid).filter(eidoskoinotitas=eidoskoinotitas).values_list('sindiasmosnew', 'surname', 'firstname', 'fathername', 'toposeklogis', 'sumvotes').order_by('toposeklogis','sindiasmosnew','-sumvotes')
    elif selected_order == 2:
        rows = EklSumpsifoisimbKoinVw.objects.filter(eklid=eklid).filter(eidoskoinotitas=eidoskoinotitas).values_list('sindiasmosnew', 'surname', 'firstname', 'fathername', 'toposeklogis', 'sumvotes').order_by('toposeklogis','sindiasmosnew','surname',  'firstname')
    elif selected_order == 3:
        rows = EklSumpsifoisimbKoinVw.objects.filter(eklid=eklid).filter(eidoskoinotitas=eidoskoinotitas).values_list('sindiasmosnew', 'surname', 'firstname', 'fathername', 'toposeklogis', 'sumvotes').order_by('toposeklogis','-sumvotes')
    elif selected_order == 4:
        rows = EklSumpsifoisimbKoinVw.objects.filter(eklid=eklid).filter(eidoskoinotitas=eidoskoinotitas).values_list('sindiasmosnew', 'surname', 'firstname', 'fathername', 'toposeklogis','sumvotes').order_by('toposeklogis', 'surname', 'firstname')
    else:
        rows = EklSumpsifoisimbKoinVw.objects.filter(eklid=eklid).filter(eidoskoinotitas=eidoskoinotitas).values_list('sindiasmosnew', 'surname', 'firstname', 'fathername', 'toposeklogis', 'sumvotes').order_by('toposeklogis','-sumvotes')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def export_psifodeltiasind_ken(request, eklid, sunday, selected_order):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="psifodeltiasind_ken.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('data')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.height = 280
    font_style.font.bold = True

    if sunday == 1:
        ws.write(row_num, 0, 'Ψηφοδέλτια συνδυασμών για Δημ. Συμβούλιο ανά εκλ. κέντρο - Α Κυριακή', font_style)
    elif sunday == 2:
        ws.write(row_num, 0, 'Ψηφοδέλτια συνδυασμών για Δημ. Συμβούλιο ανά εκλ. κέντρο - Β Κυριακή', font_style)
    else:
        ws.write(row_num, 0, 'Ψηφοδέλτια συνδυασμών για Τοπικά Συμβούλια ανά εκλ. κέντρο ', font_style)

    row_num += 2

    if sunday == 1:
        firstrow = EklSumpsifodeltiasindVw.objects.filter(eklid=eklid).values_list('katametrimena', 'plithoskentrwn','posostokatametrimenwnkentrwn').distinct()
    elif sunday == 2:
        firstrow = EklSumpsifodeltiasindVw.objects.filter(eklid=eklid).values_list('katametrimenab', 'plithoskentrwn','posostokatametrimenwnkentrwnb').distinct()
    else:
        firstrow = EklSumpsifodeltiasindVw.objects.filter(eklid=eklid).values_list('katametrimenak', 'plithoskentrwn','posostokatametrimenwnkentrwnk').distinct()

    # for col_num in range(len(firstrow[0])):
    if firstrow:
        if firstrow[0][0] is not None:
            katametrimena = firstrow[0][0]
        else:
            katametrimena = 0

        if firstrow[0][1] is not None:
            sinoloKentrwn = firstrow[0][1]
        else:
            sinoloKentrwn = 0

        if firstrow[0][2] is not None:
            pososto_katametrimenwn = firstrow[0][2]
        else:
            pososto_katametrimenwn = 0


        if katametrimena==0:
            messages.error(request, 'Δεν υπάρχουν καταχωρήσεις!')
            return redirect('psifodeltiasind_ken', eklid, sunday)

        ws.write(row_num, 0,'Στα ' + str(katametrimena) + ' από τα ' + str(sinoloKentrwn) + ' εκλ. κέντρα (Ποσοστό ' + str(pososto_katametrimenwn) + '%)', font_style)
    else:
        #ws.write(row_num, 0,'Δεν υπάρχουν καταχωρήσεις!', font_style)
        messages.error(request, 'Δεν υπάρχουν καταχωρήσεις!')
        return redirect('psifodeltiasind_ken',eklid,sunday)



    font_style = xlwt.XFStyle()
    font_style.font.height = 240
    font_style.font.bold = True

    row_num += 2

    columns = ['Εκλ. Κέντρο', 'Συνδυασμός', 'Ψηφοδέλτια',]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    if sunday == 1:
        rows = EklSumpsifodeltiasindKenVw.objects.filter(eklid=eklid).filter(sindid__sindid__in=(Eklsind.objects.filter(eklid=eklid).values_list('sindid'))).values_list('kentro', 'sindiasmosnew', 'votes')
    elif sunday == 2:
        rows = EklSumpsifodeltiasindKenVw.objects.filter(eklid=eklid).filter(sindid__sindid__in=(Eklsind.objects.filter(eklid=eklid).values_list('sindid'))).values_list('kentro', 'sindiasmosnew', 'votesb')
    else: #sunday=3
        #ΠΡΟΣΟΧΗ!!!: Για Κοινότητες μόνο
        rows = EklSumpsifodeltiasindKenTopikoiOnlyVw.objects.filter(eklid=eklid).values_list('kentro', 'sindiasmosnew', 'votesk')


    #rows = EklSumpsifoisimbPerVw.objects.filter(eklid=eklid).values_list('sindiasmos', 'surname', 'firstname', 'fathername', 'toposeklogis', 'sumvotes')
    if selected_order == 1 or selected_order == 4:
        if sunday == 1:
            rows = rows.order_by('kentro','-votes')
        elif sunday == 2:
            rows = rows.order_by('kentro','-votesb')
        else:
            rows = rows.order_by('kentro','-votesk')


    elif selected_order == 2:
        rows = rows.order_by('kentro', 'sindiasmosnew')
    else:
        rows = rows.order_by('sindiasmosnew','kentro',)

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def export_psifodeltiasind_koin(request, eklid, selected_order, eidos, sunday):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="psifodeltiasind_koin.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('data')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.height = 280
    font_style.font.bold = True

    if eidos == 0:
        ws.write(row_num, 0, 'Ψηφοδέλτια συνδυασμών για την ανάδειξη Τοπικού Συμβουλίου ανά Κοινότητα', font_style)
    else:
        if sunday == 1:
            ws.write(row_num, 0, 'Ψηφοδέλτια συνδυασμών για την ανάδειξη Δημοτικής Αρχής ανά Κοινότητα (1η Κυριακή)', font_style)
        else:
            ws.write(row_num, 0, 'Ψηφοδέλτια συνδυασμών για την ανάδειξη Δημοτικής Αρχής ανά Κοινότητα (2η Κυριακή)', font_style)

    row_num += 2

    if eidos == 0:
        firstrow = EklSumpsifodeltiasindVw.objects.filter(eklid=eklid).values_list('katametrimenak', 'plithoskentrwn','posostokatametrimenwnkentrwnk').distinct()
    else:
        if sunday == 1:
            firstrow = EklSumpsifodeltiasindVw.objects.filter(eklid=eklid).values_list('katametrimena', 'plithoskentrwn','posostokatametrimenwnkentrwn').distinct()
        else:
            firstrow = EklSumpsifodeltiasindVw.objects.filter(eklid=eklid).values_list('katametrimenab','plithoskentrwn', 'posostokatametrimenwnkentrwnb').distinct()

    # for col_num in range(len(firstrow[0])):
    if firstrow:
        if firstrow[0][0] is not None:
            katametrimena = firstrow[0][0]
        else:
            katametrimena = 0

        if firstrow[0][1] is not None:
            sinoloKentrwn = firstrow[0][1]
        else:
            sinoloKentrwn = 0

        if firstrow[0][2] is not None:
            pososto_katametrimenwn = firstrow[0][2]
        else:
            pososto_katametrimenwn = 0

        if katametrimena==0:
            messages.error(request, 'Δεν υπάρχουν καταχωρήσεις!')
            return redirect('psifodeltiasind_koin', eklid, eidos,sunday)

        ws.write(row_num, 0, 'Στα ' + str(katametrimena) + ' από τα ' + str(sinoloKentrwn) + ' εκλ. κέντρα (Ποσοστό ' + str(pososto_katametrimenwn) + '%)', font_style)

    else:
        #ws.write(row_num, 0, 'Δεν υπάρχουν καταχωρήσεις!', font_style)
        messages.error(request, 'Δεν υπάρχουν καταχωρήσεις!')
        return redirect('psifodeltiasind_koin', eklid, eidos,sunday)

    font_style = xlwt.XFStyle()
    font_style.font.height = 240
    font_style.font.bold = True

    row_num += 2

    columns = ['Κοινότητα', 'Συνδυασμός', 'Ψηφοδέλτια',]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    if eidos == 0:
        rows = EklSumpsifodeltiasindKoinVw.objects.filter(eklid=eklid).values_list('descr', 'sindiasmosnew', 'sumksindiasmou')
    else:
        if sunday == 1:
            rows = EklSumpsifodeltiasindKoinVw.objects.filter(eklid=eklid).values_list('descr', 'sindiasmosnew', 'sumasindiasmou')
        else:
            rows = EklSumpsifodeltiasindKoinVw.objects.filter(eklid=eklid).values_list('descr', 'sindiasmosnew', 'sumbsindiasmou')

    #rows = EklSumpsifoisimbPerVw.objects.filter(eklid=eklid).values_list('sindiasmos', 'surname', 'firstname', 'fathername', 'toposeklogis', 'sumvotes')
    if selected_order == 1 or selected_order == 4:
        if eidos == 0:
            rows = rows.order_by('descr','-sumksindiasmou')
        else:
            if sunday == 1:
                rows = rows.order_by('descr', '-sumasindiasmou')
            else:
                rows = rows.order_by('descr', '-sumbsindiasmou')
    elif selected_order == 2:
        rows = rows.order_by('descr', 'sindiasmosnew')
    else:
        rows = rows.order_by('sindiasmosnew','descr',)

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def export_psifoisimb_ken(request,eklid, selected_order):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="psifoisimb_ken.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('data')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.height = 280
    font_style.font.bold = True

    ws.write(row_num, 0, 'Ψήφοι υποψηφίων συμβούλων ανά εκλ. κέντρο', font_style)

    row_num += 2

    katametrimena_psifoi = EklKatametrimenaPsifoiVw.objects.get(eklid=eklid).katametrimena
    firstrow = EklSumpsifodeltiasindVw.objects.filter(eklid=eklid).values_list('katametrimena', 'plithoskentrwn','posostokatametrimenwnkentrwn').distinct()

    # for col_num in range(len(firstrow[0])):

    if firstrow:
        ws.write(row_num, 0,'Στα ' + str(katametrimena_psifoi) + ' από τα ' + str(firstrow[0][1]) + ' εκλ. κέντρα', font_style)
    else:
        #ws.write(row_num, 0, 'Δεν υπάρχουν καταχωρήσεις!', font_style)
        messages.error(request, 'Δεν υπάρχουν καταχωρήσεις!')
        return redirect('psifoisimb_ken', eklid)

    font_style = xlwt.XFStyle()
    font_style.font.height = 240
    font_style.font.bold = True

    row_num += 2

    columns = ['Εκλ. Κέντρο', 'Κοινότητα', 'Επώνυμο', 'Όνομα', 'Όν. Πατρός', 'Είδος', 'Συνδυασμός', 'Ψήφοι']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    #rows = EklSumpsifoisimbPerVw.objects.filter(eklid=eklid).values_list('sindiasmos', 'surname', 'firstname', 'fathername', 'toposeklogis', 'sumvotes')
    if selected_order == 1 or selected_order == 6:
        rows = EklPsifoisimbVw.objects.filter(eklid=eklid).values_list('kentro','koinotita', 'surname', 'firstname', 'fathername', 'eidos', 'sindiasmosnew', 'votes').order_by('kenid','sindiasmosnew', '-votes')
    elif selected_order == 2:
        rows = EklPsifoisimbVw.objects.filter(eklid=eklid).values_list('kentro','koinotita', 'surname', 'firstname', 'fathername', 'eidos', 'sindiasmosnew', 'votes').order_by('kenid', 'sindiasmosnew','surname', 'firstname')
    elif selected_order == 3:
        rows = EklPsifoisimbVw.objects.filter(eklid=eklid).values_list('kentro','koinotita', 'surname', 'firstname', 'fathername','eidos', 'sindiasmosnew', 'votes').order_by('kenid','surname','firstname')
    elif selected_order == 4:
        rows = EklPsifoisimbVw.objects.filter(eklid=eklid).values_list('kentro','koinotita', 'surname', 'firstname', 'fathername','eidos', 'sindiasmosnew', 'votes').order_by('kenid','-votes')
    else:
        rows = EklPsifoisimbVw.objects.filter(eklid=eklid).values_list('kentro','koinotita', 'surname', 'firstname', 'fathername', 'eidos', 'sindiasmosnew', 'votes').order_by('kenid','eidos','-votes')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def Elections_list(request, eklid=0):

    if eklid == 0:
        eklid=Eklogestbl.objects.filter(defaultelection=1).values_list('eklid',flat=True)[0]

    paramekloges=request.GET.get('eklogesoption','')
    if request.method == 'POST':
        paramekloges=request.POST['eklid']

    paramkentro = request.GET.get('eklkentrooption', '')

    try:
        paramekloges = int(paramekloges)
    except:
        #paramekloges = Eklogestbl.objects.filter(defaultelection=1).values_list('eklid',flat=True)[0]
        paramekloges = Eklogestbl.objects.filter(eklid=eklid).values_list('eklid',flat=True)[0]
        if request.method=='POST':
            paramekloges=request.POST['eklid']
        #παίρνω το eklid της default εκλ. αναμέτρησης..ΠΡΟΣΟΧΗ!!! ΜΟΝΟ ΜΙΑ ΠΡΕΠΕΙ ΝΑ ΕΙΝΑΙ DEFAULT

    try:
        paramkentro = int(paramkentro)
    except:
        paramkentro = 0

    #φιλτράρισμα επιλεγμένης εκλ. αναμέτρησης και προαιρετικά κέντρου
    selected_ekloges = Eklogestbl.objects.prefetch_related('eklsimbkoin_set', 'eklperkoin_set').get(eklid=paramekloges)
    psifoi_kentrou = None

    try:
        selected_kentro = get_object_or_404(Kentra, eklid=paramekloges, descr=str(paramkentro))
        selected_koinotita = Koinotites.objects.get(kentra__kenid=selected_kentro.kenid)
        selected_simbouloi = Simbouloi.objects.filter(simbid__in=Psifoi.objects.filter(kenid=selected_kentro.kenid).values_list('simbid'))
        action_label = 'Εκλ. Κέντρο ' + selected_kentro.descr + ' - ' + selected_koinotita.descr
    except:
        selected_kentro = None
        selected_koinotita = None
        selected_simbouloi = None
        action_label = ''


        # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    #αν έχει δοθεί κέντρο προς αναζήτηση ή γίνεται αποθήκευση της φόρμας...
    if paramkentro!=0 or request.method == 'POST':

        #αν γίνεται αποθήκευση της φόρμας κάνω get το κέντρο..
        if request.method == 'POST':
            selected_kentro = get_object_or_404(Kentra, eklid=paramekloges, descr=request.POST['descr'])

        if selected_kentro is not  None:

            # παίρνω per_id, koin_id από τον Eklperkoin
            eklperkoin_item = selected_ekloges.eklperkoin_set.get(koinid=selected_kentro.koinid)
            per_id_item = eklperkoin_item.perid
            koin_id_item = eklperkoin_item.koinid

            if request.method == 'POST':

                form = KentraForm(paramekloges, request.POST or None, instance=selected_kentro)
                if form.is_valid():
                    item = form.save(commit=False)
                    item.save()

                    print(koin_id_item)
                    print(form.cleaned_data['koinid'])

                    # Αν αλλάξει η κοινότητα του κέντρου...
                    if koin_id_item != form.cleaned_data['koinid']:
                        # Διαγραφή ψήφων για τοπικούς συμβούλους της πρώην Κοινότητας
                        Psifoi.objects.filter(kenid=selected_kentro.kenid).filter(
                            simbid__in=selected_ekloges.eklsimbkoin_set.filter(koinid=koin_id_item).values_list('simbid')).delete()

                        # Δημιουργία εγγραφών στον πίνακα Psifoi για κάθε τοπικό σύμβουλο της Κοινότητας στην οποία ανήκει πλέον το εκλ. κέντρο
                        for rec in selected_ekloges.eklsimbkoin_set.filter(koinid=item.koinid):
                            Psifoi.objects.create(kenid=item,
                                                  simbid=rec.simbid,
                                                  votes=0
                                                  ).save()

                    messages.success(request, 'Η εγγραφή αποθηκεύτηκε!')
                    action_label = 'Εκλ. Κέντρο ' + selected_kentro.descr + ' - ' + item.koinid.descr
                    #return redirect('Elections_list')
            else:

                if not request.user.has_perm('Elections.change_kentra'):
                    raise PermissionDenied

                psifoi_kentrou = selected_kentro.psifoi_set.filter(kenid=selected_kentro.kenid)

                # αν δεν γίνει POST φέρνω τα πεδία του μοντέλου καθως και τα extra πεδία  manually
                form = KentraForm(paramekloges, request.POST or None, instance=selected_kentro,
                                  initial={'koinid': koin_id_item, 'perid': per_id_item})
        else:
            form = None
            action_label='Δεν βρέθηκαν στοιχεία!'
    else:
        form=None

    context = {'all_ekloges': all_ekloges,
               'selected_ekloges':selected_ekloges.eklid,
               'selected_kentro':selected_kentro,
               'selected_koinotita': selected_koinotita,
               'selected_simbouloi':selected_simbouloi,
               'psifoi_kentrou': psifoi_kentrou,
               'action_label' : action_label,
               'form':form}

    return render(request, 'Elections/Elections_list.html',context)


def pososta_telika(request, eklid, sunday):

#ΠΟΣΟΣΤΑ ΣΥΝΔΥΑΣΜΩΝ ΣΕ ΟΛΟ ΤΟ ΔΗΜΟ

    # φιλτράρισμα επιλεγμένης εκλ. αναμέτρησης
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)
    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    if sunday == 1:
        #ανάκτηση εγγραφών επιλεγμένης εκλ. αναμέτρησης από το σχετικό database view (μόνο καθολικοί συνδυασμοί επιλέγονται)
        all_pososta = EklSumpsifodeltiasindVw.objects.filter(eklid=eklid, eidos=1).order_by('-posostosindiasmou')
    else:
        #παίρνουμε μόνο τους συνδυασμούς της Β Κυριακής (ποσοστό>0)
        all_pososta = EklSumpsifodeltiasindVw.objects.filter(eklid=eklid, eidos=1).filter(posostosindiasmoub__gt=0).order_by('-posostosindiasmou')

    all_sind = Sindiasmoi.objects.filter(sindid__in=(all_pososta.values_list('sindid')))
    all_eklsind= Eklsind.objects.filter(eklid=eklid)

    oldeklid=-1
    #Βρίσκω το id Της ακριβώς προηγούμενης αναμέτρησης
    for item in Eklogestbl.objects.filter(eklid__lt=eklid).order_by('-eklid'):
        if item.eklid > 0:
            oldeklid = item.eklid
            break


    diafores_list = []
    all_pososta_prin_list = []
    if oldeklid>-1: # αν υπάρχει προηγούμενη εκλ. αναμέτρηση, φορτώνω τα αποτελέσματα
        all_pososta_prin = EklSumpsifodeltiasindVw.objects.filter(eklid=oldeklid, eidos=1)

        for itemNow in EklSumpsifodeltiasindVw.objects.filter(eklid=eklid):
            found = False
            for itemPrin in all_pososta_prin:
                if itemNow.sindid == itemPrin.sindid:
                    found = True   # αναζήτηση συνδυασμού στην προηγούμενη εκλ. αναμέτρηση...αν υπάρχει ενημερώνω δυο λίστες με τις διαφορές και τα ποσοστά αντίστοιχα
                    diafores_list.append([itemNow.sindid, itemNow.posostosindiasmou- itemPrin.posostosindiasmou])
                    all_pososta_prin_list.append([itemNow.sindid, itemPrin.posostosindiasmou, itemPrin.sumvotes])
            if not found:
                diafores_list.append([itemNow.sindid,'Δεν συμμετείχε ως υποψήφιος συνδυασμός'])  #αν δεν υπήρχε ο συνδυασμός στην προηγούμενη εκλ. αναμέτρηση, εισάγω κατάλληλες τιμές στις λίστες
                all_pososta_prin_list.append([itemNow.sindid, 'Δεν συμμετείχε ως υποψήφιος συνδυασμός'])
    else:#αν δεν υπάρχουν προηγούνες εκλ. αναμετρήσεις δεν επιστρέφω κάτι
        all_pososta_prin = []

    context = {'all_pososta':all_pososta,
               'all_pososta_prin': all_pososta_prin,
               'all_ekloges':all_ekloges,
               'selected_ekloges': selected_ekloges.eklid,
               'all_pososta_prin': all_pososta_prin,
               'all_pososta_prin_list': all_pososta_prin_list,
               'diafores_list': diafores_list,
               'all_sind': all_sind,
               'all_eklsind': all_eklsind,
               'sunday' : sunday,}

    return render(request, 'Elections/pososta_telika.html',context)


def pososta_perifereies(request, eklid):

# ΠΟΣΟΣΤΑ ΣΥΝΔΥΑΣΜΩΝ ΑΝΑ ΕΚΛΟΓΙΚΗ ΠΕΡΙΦΕΡΕΙΑ
    paramstr = request.GET.get('perifereiaoption','')

    try:
        paramstr = int(paramstr)
    except:
        paramstr = 1  # default perid  αν δεν δοθεί

    # φιλτράρισμα επιλεγμένης εκλ. αναμέτρησης
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)
    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    # φιλτράρισμα επιλεγμένης περιφέρειας
    selected_perifereia = Perifereies.objects.get(perid=paramstr)
    #ανάκτηση όλων των περιφερειών
    all_perifereies=Perifereies.objects.all()
    #ανάκτηση εγγραφών επιλεγμένης εκλ. αναμέτρησης από το σχετικό database view
    all_pososta = EklSumpsifodeltiasindVw.objects.filter(eklid=eklid).order_by('-posostosindiasmou')
    all_posostaper = EklPosostasindPerVw.objects.filter(eklid=eklid).filter(perid=paramstr)
    context = {'all_posostaper': all_posostaper,
                'all_pososta': all_pososta,
               'all_ekloges': all_ekloges,

               'selected_ekloges': selected_ekloges.eklid,
               'all_perifereies': all_perifereies,
               'selected_perifereia': selected_perifereia,
               }
    return render(request, 'Elections/pososta_perifereies.html',context)

def psifoisimb_perifereies(request, eklid):

# ΚΑΤΑΤΑΞΗ ΤΠΟΨΗΦΙΩΝ ΔΗΜ. ΣΥΜΒΟΥΛΩΝ

    paramstr = request.GET.get('perifereiaoption','')
    paramorder = request.GET.get('orderoption','')
    sigritika= request.GET.get('sigritika','')

    try:
        paramstr = int(paramstr)
    except:
        paramstr = 0 # default perid  αν δεν δοθεί


    try:
        paramorder = int(paramorder)
    except:
        paramorder = 4  # default ταξινόμηση

    if sigritika:
        sigritika=1
    else:
        sigritika = 0

    #φιλτράρισμα επιλεγμένης εκλ. αναμέτρησης
    #selected_ekloges = Eklogestbl.objects.get(eklid=eklid)
    selected_ekloges = Eklogestbl.objects.prefetch_related('eklsumpsifoisimbwithidvw_set', 'eklsumpsifoisimbpervw_set', 'eklsumpsifoisimbpervw_set').get(eklid=eklid)


    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    # φιλτράρισμα επιλεγμένης περιφέρειας
    if paramstr == 0: #επιλογή: "ΑΝΕΞΑΡΤΗΤΟΥ ΕΚΛ. ΠΕΡΙΦΕΡΕΙΑΣ"
        selected_perifereia = 0
        all_psifoi = selected_ekloges.eklsumpsifoisimbpervw_set.values_list('eklid', 'simbid',
            'surname', 'firstname', 'fathername', 'sindiasmosnew','toposeklogisid', 'sumvotes', 'toposeklogis' ).order_by('-sumvotes')
    else:
        selected_perifereia = Perifereies.objects.get(perid=paramstr).perid                      #retrieve Από το EklSumpsifoisimbPerVw
        all_psifoi = selected_ekloges.eklsumpsifoisimbpervw_set.filter(toposeklogisid=paramstr).values_list('eklid', 'simbid',
            'surname', 'firstname', 'fathername', 'sindiasmosnew','toposeklogisid', 'sumvotes', 'toposeklogis' )

    selected_order = paramorder

    katametrimena_psifoi = EklKatametrimenaPsifoiVw.objects.get(eklid=eklid).katametrimena

    #ανάκτηση όλων των περιφερειών
    all_perifereies=Perifereies.objects.all()
    #ανάκτηση εγγραφών επιλεγμένης εκλ. αναμέτρησης από το σχετικό database view
    all_pososta = EklSumpsifodeltiasindVw.objects.filter(eklid=eklid).order_by('-posostosindiasmou')

    akataxorita = EklSumpsifoiKenVw.objects.filter(eklid=eklid).filter(sumvotes=0)
    listakataxorita = []
    for item in akataxorita:
        listakataxorita.append(item.kentro)

    listaa = []
    if paramorder == 1:
        all_psifoi = all_psifoi.order_by('sindiasmosnew', '-sumvotes')
        cursind = 'aaa'
        counter = 0    #δημιουργία λίστας που θα έχει τα αα των συμβούλων για το template
        for item in all_psifoi:
            if cursind == item[5]:     #όποτε εμφανίζεται ο ιδιος συνδυασμός ο counter αυξάνεται...
                counter = counter + 1
                listaa.append(counter)
            else:                       # αλλιώς ξεκιναει απο την αρχη...
                counter = 1
                listaa.append(counter)
            cursind = item[5]
    elif paramorder == 2:
        all_psifoi = all_psifoi.order_by('sindiasmosnew', 'surname', 'firstname')
    else:
        all_psifoi = all_psifoi.order_by('-sumvotes')

    oldsimb_psifoi_list = []
    all_psifoi_prin = []
    ekloges_prin = []

    if sigritika == 1:
        # Για να βγάλω πιθανά συγκριτικά ψήφων...
        oldeklid = -1
        # Βρίσκω το id Της ακριβώς προηγούμενης αναμέτρησης
        for item in Eklogestbl.objects.filter(eklid__lt=eklid).order_by('-eklid'):
            if item.eklid > 0:
                oldeklid = item.eklid
                break


        if oldeklid > -1:  # αν υπάρχει προηγούμενη εκλ. αναμέτρηση, φορτώνω τα αποτελέσματα
            #ekloges_prin = Eklogestbl.objects.prefetch_related('eklsumpsifoisimbwithidvw_set','eklsumpsifoisimbpervw_set', 'eklsumpsifoisimbperlightvw_set').get(eklid=oldeklid)
            all_psifoi_prin = EklSumpsifoisimbPerLightVw.objects.filter(eklid=oldeklid).values_list('eklid', 'simbid',  'sumvotes' )
            ekloges_prin=Eklogestbl.objects.get(eklid=oldeklid)

            all_psifoi_now=EklSumpsifoisimbPerLightVw.objects.filter(eklid=eklid).values_list('eklid', 'simbid',  'sumvotes' )

            for itemNow in all_psifoi:
                for itemPrin in all_psifoi_prin:
                    if itemNow[1] == itemPrin[1]:
                        oldsimb_psifoi_list.append([itemNow[1], itemNow[7]- itemPrin[2]])
        else:  # αν δεν υπάρχουν προηγούνες εκλ. αναμετρήσεις δεν επιστρέφω κάτι
            all_psifoi_prin = []

    context = {'all_psifoi':all_psifoi,
                'all_pososta':all_pososta,
               'all_ekloges':all_ekloges,
               'ekloges_prin':ekloges_prin,
               'oldsimb_psifoi_list' : oldsimb_psifoi_list,
               'all_psifoi_prin' : all_psifoi_prin,
               'selected_ekloges':selected_ekloges.eklid,
               'all_perifereies':all_perifereies,
               'selected_perifereia': selected_perifereia,
               'selected_order':selected_order,
               'katametrimena_psifoi':katametrimena_psifoi,
               'listaa' : listaa,
               'listakataxorita': listakataxorita,
               'sigritika' : sigritika}

    return render(request, 'Elections/psifoisimb_perifereies.html',context)


def psifoisimb_koinotites(request, eklid, eidoskoinotitas):

# ΚΑΤΑΤΑΞΗ ΤΠΟΨΗΦΙΩΝ ΣΥΜΒΟΥΛΩΝ ΚΟΙΝΟΤΗΤΩΝ

    paramstr = request.GET.get('koinotitaoption','')
    paramorder = request.GET.get('orderoption','')

    try:
        paramstr = int(paramstr)
    except:
        p = EklSumpsifoisimbKoinVw.objects.filter(eklid=eklid).filter(eidoskoinotitas=eidoskoinotitas).order_by('toposeklogisid')
        if p:
            paramstr=p[0].toposeklogisid  # default toposeklogisid θα είναι ο πρώτος της λίστας αν δεν δοθεί κάτι
        else:
            paramstr=Kentra.objects.filter(eklid=eklid).order_by('kenid')
            paramstr=paramstr[0].kenid

    try:
        paramorder = int(paramorder)
    except:
        paramorder = 5  # default ταξινόμηση

    # φιλτράρισμα επιλεγμένης εκλ. αναμέτρησης
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)
    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    # φιλτράρισμα επιλεγμένης κοινότητας
    selected_koinotita = Koinotites.objects.filter(koinid=paramstr)

    if eidoskoinotitas == 1:
        selected_menu = ' > 2000 κάτοικοι'
    elif eidoskoinotitas == 2:
        selected_menu = ' έως 2000 κάτοικοι'
    elif eidoskoinotitas == 3:
        selected_menu = ' (έως 300 κάτοικοι)'
    else:
        selected_menu = ' (> 300 κάτοικοι)'

    selected_order = paramorder


    katametrimena_koinotites = EklKatametrimenaPsifoiKoinotitesOnlyVw.objects.get(eklid=eklid).katametrimena_koinotites

    akataxorita = EklSumpsifoiKoinVw.objects.filter(eklid=eklid).filter(sumvotes=0).order_by('kentro')
    listakataxorita = []
    for item in akataxorita:
        listakataxorita.append(item.kentro)

    #ανάκτηση όλων των κοινοτητων
    all_koinotites=Koinotites.objects.all().filter(eidos=eidoskoinotitas)
    #ανάκτηση εγγραφών επιλεγμένης εκλ. αναμέτρησης από το σχετικό database view
    all_pososta = EklSumpsifodeltiasindVw.objects.filter(eklid=eklid).order_by('-posostosindiasmou')

    if paramorder==1:
        all_psifoi = EklSumpsifoisimbKoinVw.objects.filter(toposeklogisid=paramstr).order_by('sindiasmosnew','-sumvotes')
    elif paramorder==2 :
        all_psifoi = EklSumpsifoisimbKoinVw.objects.filter(toposeklogisid=paramstr).order_by('sindiasmosnew','surname', 'firstname')
    elif paramorder==3:
        all_psifoi = EklSumpsifoisimbKoinVw.objects.filter(toposeklogisid=paramstr).order_by('-sumvotes')
    elif paramorder==4:
        all_psifoi = EklSumpsifoisimbKoinVw.objects.filter(toposeklogisid=paramstr).order_by('surname', 'firstname')
    else:
        all_psifoi = EklSumpsifoisimbKoinVw.objects.filter(toposeklogisid=paramstr).order_by('-sumvotes')

    context = {'all_psifoi':all_psifoi,
                'all_pososta':all_pososta,
               'all_ekloges':all_ekloges,
               'selected_ekloges':selected_ekloges.eklid,
               'all_koinotites':all_koinotites,
               'selected_koinotita': selected_koinotita,
               'selected_order':selected_order,
               'eidoskoinotitas': eidoskoinotitas,
               'katametrimena_koinotites' : katametrimena_koinotites,
               'listakataxorita' : listakataxorita,
               'selected_menu':selected_menu,}
    return render(request, 'Elections/psifoisimb_koinotites.html',context)

def psifodeltiasindken(request, eklid, sunday):

# ΨΗΦΟΟΔΕΛΤΙΑ ΣΥΝΔΥΑΣΜΩΝ ΑΝΑ ΕΚΛ. ΚΕΝΤΡΟ
    selected_ekloges = Eklogestbl.objects.prefetch_related('eklsumpsifodeltiasindkenvw_set').get(eklid=eklid)

    paramstr = request.GET.get('kentrooption','')
    paramorder = request.GET.get('orderoption','')

    try:
        paramstr = int(paramstr)
    except:
        p = selected_ekloges.eklsumpsifodeltiasindkenvw_set.all()
        paramstr=p[0].kenid.kenid  # default kenid θα είναι το πρώτο της λίστας αν δεν δοθεί κάτι

    try:
        paramorder = int(paramorder)
    except:
        paramorder = 4  # default ταξινόμηση

    # φιλτράρισμα επιλεγμένης εκλ. αναμέτρησης
    #selected_ekloges = Eklogestbl.objects.get(eklid=eklid)
    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    # φιλτράρισμα επιλεγμένου κέντρου
    selected_kentro = selected_ekloges.kentra_set.get(kenid=paramstr).kenid
    selected_kentro_details = selected_ekloges.kentra_set.get(kenid=paramstr)


    selected_order = paramorder

    #ανάκτηση όλων των κέντρων της εκλ. αναμέτρησης
    all_kentra= selected_ekloges.kentra_set.all()
    #ανάκτηση εγγραφών επιλεγμένης εκλ. αναμέτρησης από το σχετικό database view
    all_pososta = selected_ekloges.eklsumpsifodeltiasindvw_set.all().order_by('-posostosindiasmou')



    if paramorder == 1 or paramorder == 4:
        #Α Κυριακή sunday=1, Β Κυριακή sunday=2, Εκλογές Κοινότητας sunday=3,
        if sunday == 1:
            all_psifodeltia = selected_ekloges.eklsumpsifodeltiasindkenvw_set.filter(kenid=paramstr).filter(sindid__sindid__in=(Eklsind.objects.filter(eklid=eklid).values_list('sindid'))).order_by('-votes')
        elif sunday == 2:
            all_psifodeltia = selected_ekloges.eklsumpsifodeltiasindkenvw_set.filter(kenid=paramstr).filter(sindid__sindid__in=(Eklsind.objects.filter(eklid=eklid).values_list('sindid'))).order_by('-votesb')
        else: #sunday=3 άρα εκλογές κοινότητας
            #ΠΡΟΣΟΧΗ!!!: για τις εκλογές Κοινότητας φιλτράρω μόνο τους συμμετέχοντες συνδυασμούς στην Κοινότητα
            all_psifodeltia = selected_ekloges.eklsumpsifodeltiasindkenvw_set.filter(kenid=paramstr).filter(sindid__sindid__in=(Eklsindkoin.objects.filter(eklid=eklid, koinid__koinid__in=(Kentra.objects.filter(kenid=paramstr).values_list('koinid'))).values_list('sindid'))).order_by('-votesk')
    elif paramorder == 2:
        if sunday == 1:
            all_psifodeltia = selected_ekloges.eklsumpsifodeltiasindkenvw_set.filter(kenid=paramstr).filter(sindid__sindid__in=(Eklsind.objects.filter(eklid=eklid).values_list('sindid'))).order_by('sindiasmos')
        elif sunday == 2:
            all_psifodeltia = selected_ekloges.eklsumpsifodeltiasindkenvw_set.filter(kenid=paramstr).filter(sindid__sindid__in=(Eklsind.objects.filter(eklid=eklid).values_list('sindid'))).order_by('sindiasmos')
        else: #sunday=3 άρα εκλογές κοινότητας
            #ΠΡΟΣΟΧΗ!!!: για τις εκλογές Κοινότητας φιλτράρω μόνο τους συμμετέχοντες συνδυασμούς στην Κοινότητα
            all_psifodeltia = selected_ekloges.eklsumpsifodeltiasindkenvw_set.filter(kenid=paramstr).filter(sindid__sindid__in=(Eklsindkoin.objects.filter(eklid=eklid, koinid__koinid__in=(Kentra.objects.filter(kenid=paramstr).values_list('koinid'))).values_list('sindid'))).order_by('sindiasmos')
    else:
        if sunday == 1:
            all_psifodeltia = selected_ekloges.eklsumpsifodeltiasindkenvw_set.filter(kenid=paramstr).filter(sindid__sindid__in=(Eklsind.objects.filter(eklid=eklid).values_list('sindid'))).order_by('sindiasmos','kentro')
        elif sunday == 2:
            all_psifodeltia = selected_ekloges.eklsumpsifodeltiasindkenvw_set.filter(kenid=paramstr).filter(sindid__sindid__in=(Eklsind.objects.filter(eklid=eklid).values_list('sindid'))).order_by('sindiasmos','kentro')
        else: #sunday=3 άρα εκλογές κοινότητας
            #ΠΡΟΣΟΧΗ!!!: για τις εκλογές Κοινότητας φιλτράρω μόνο τους συμμετέχοντες συνδυασμούς στην Κοινότητα
            all_psifodeltia = selected_ekloges.eklsumpsifodeltiasindkenvw_set.filter(kenid=paramstr).filter(sindid__sindid__in=(Eklsindkoin.objects.filter(eklid=eklid, koinid__koinid__in=(Kentra.objects.filter(kenid=paramstr).values_list('koinid'))).values_list('sindid'))).order_by('sindiasmos','kentro')

    sumpsifodeltia = -1
    if sunday == 1:
        sumpsifodeltia = sum([i[0] for i in all_psifodeltia.values_list('votes')])
    elif sunday == 2:
        sumpsifodeltia = sum([i[0] for i in all_psifodeltia.values_list('votesb')])
    else:
        sumpsifodeltia = sum([i[0] for i in all_psifodeltia.values_list('votesk')])

    context = {'all_psifodeltia':all_psifodeltia,
                'all_pososta':all_pososta,
               'sunday': sunday,
               'all_ekloges':all_ekloges,
               'selected_ekloges':selected_ekloges.eklid,
               'all_kentra':all_kentra,
               'selected_kentro': selected_kentro,
               'selected_kentro_details' : selected_kentro_details,
               'selected_koinotita':selected_kentro_details.koinid.descr,
               'selected_order':selected_order,
               'sumpsifodeltia':sumpsifodeltia,
               }
    return render(request, 'Elections/psifodeltiasind_ken.html',context)

def psifodeltiasindkoin(request, eklid, eidos, sunday ):

# ΨΗΦΟΟΔΕΛΤΙΑ ΣΥΝΔΥΑΣΜΩΝ ΑΝΑ ΚΟΙΝΟΤΗΤΑ
    selected_ekloges = Eklogestbl.objects.prefetch_related('eklsumpsifodeltiasindkoinvw_set').get(eklid=eklid)

    paramstr = request.GET.get('koinotitaoption','')
    paramorder = request.GET.get('orderoption','')

    try:
        paramstr = int(paramstr)
    except:
        p = selected_ekloges.eklsumpsifodeltiasindkoinvw_set.all()
        paramstr=p[0].koinid  # default koinid θα είναι το πρώτο της λίστας αν δεν δοθεί κάτι

    try:
        paramorder = int(paramorder)
    except:
        paramorder = 4  # default ταξινόμηση

    # φιλτράρισμα επιλεγμένης εκλ. αναμέτρησης
    #selected_ekloges = Eklogestbl.objects.get(eklid=eklid)
    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    # φιλτράρισμα επιλεγμένου κέντρου
    selected_koinotita = Koinotites.objects.get(koinid=paramstr).koinid

    selected_order = paramorder

    #ανάκτηση όλων των κέντρων της εκλ. αναμέτρησης
    if selected_ekloges.sisid.sisid==1:
        all_koinotites= Koinotites.objects.filter(eidos__lte=2)
    else:
        all_koinotites = Koinotites.objects.filter(eidos=4)

    #ανάκτηση εγγραφών επιλεγμένης εκλ. αναμέτρησης από το σχετικό database view
    #all_pososta = selected_ekloges.eklsumpsifodeltiasindvw_set.all().order_by('-posostosindiasmou')


    if eidos == 0:
        # ΠΡΟΣΟΧΗ!!! : ΦΙΛΤΡΑΡΩ ΜΟΝΟ ΣΥΝΔΥΑΣΜΟΥΣ ΠΟΥ ΣΥΜΜΕΤΕΧΟΥΝ ΣΤΙΣ ΕΚΛΟΓΕΣ ΤΩΝ ΚΟΙΝΟΤΗΤΩΝ
        all_psifodeltia = selected_ekloges.eklsumpsifodeltiasindkoinvw_set.filter(koinid=paramstr).filter(
        sindid__sindid__in=(Eklsindkoin.objects.filter(eklid=eklid, koinid__koinid__in=(
            Kentra.objects.filter(koinid=paramstr).values_list('koinid'))).values_list('sindid'))).order_by(
        '-sumksindiasmou')
    else:
        # ΠΡΟΣΟΧΗ!!! : ΦΙΛΤΡΑΡΩ ΜΟΝΟ ΚΑΘΟΛΙΚΟΥΣ ΣΥΝΔΥΑΣΜΟΥΣ ΠΟΥ ΣΥΜΜΕΤΕΧΟΥΝ ΣΤΙΣ ΔΗΜΟΤΙΚΕΣ ΕΚΛΟΓΕΣ
        all_psifodeltia = selected_ekloges.eklsumpsifodeltiasindkoinvw_set.filter(koinid=paramstr).filter(
        sindid__sindid__in=(Eklsind.objects.filter(eklid=eklid).values_list('sindid')))


    sumpsifodeltia = -1
    if sunday == 1:
        sumpsifodeltia = sum([i[0] for i in all_psifodeltia.values_list('sumasindiasmou')])
    elif sunday == 2:
        sumpsifodeltia = sum([i[0] for i in all_psifodeltia.values_list('sumbsindiasmou')])
    else:
        sumpsifodeltia = sum([i[0] for i in all_psifodeltia.values_list('sumksindiasmou')])

    if paramorder == 1 or paramorder == 4:
        if eidos == 0:
            all_psifodeltia = all_psifodeltia.order_by('-sumksindiasmou')
        else:
            if sunday == 1:
                all_psifodeltia = all_psifodeltia.order_by('-sumasindiasmou')
            else:
                all_psifodeltia = all_psifodeltia.order_by('-sumbsindiasmou')
    elif paramorder == 2:
        all_psifodeltia = all_psifodeltia.order_by('sindiasmosnew')
    else:
        all_psifodeltia = all_psifodeltia.order_by('sindiasmosnew','descr')

    context = {'all_psifodeltia': all_psifodeltia,
               'all_ekloges': all_ekloges,
               'eidos' : eidos,
               'sunday' : sunday,
               'selected_ekloges': selected_ekloges.eklid,
               'all_koinotites': all_koinotites,
               'selected_koinotita': selected_koinotita,
               'selected_order':selected_order,
               'sumpsifodeltia' : sumpsifodeltia,
               }
    return render(request, 'Elections/psifodeltiasind_koin.html',context)


def psifoisimb_ken(request, eklid):

# ΨΗΦΟΙ ΣΥΜΒΟΥΛΩΝ ΑΝΑ ΕΚΛ. ΚΕΝΤΡΟ

    paramstr = request.GET.get('kentrooption','')
    paramorder = request.GET.get('orderoption','')


    # φιλτράρισμα επιλεγμένης εκλ. αναμέτρησης
    selected_ekloges = Eklogestbl.objects.prefetch_related('eklpsifoisimbvw_set').get(eklid=eklid)
    try:
        paramstr = int(paramstr)
    except:
        p = selected_ekloges.eklpsifoisimbvw_set.all().order_by('kentro')
        #EklPsifoisimbVw.objects.filter(eklid=eklid).order_by('kentro')
        if p:
            paramstr = p[0].kenid.kenid  # default kenid θα είναι το πρώτο της λίστας αν δεν δοθεί κάτι
        else:
            paramstr=Kentra.objects.filter(eklid=eklid).order_by('kenid')
            paramstr=paramstr[0].kenid
        #paramstr=p[0].kenid.kenid  # default kenid θα είναι το πρώτο της λίστας αν δεν δοθεί κάτι


    try:
        paramorder = int(paramorder)
    except:
        paramorder = 4  # default ταξινόμηση


    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    # φιλτράρισμα επιλεγμένου κέντρου
    selected_kentro = selected_ekloges.kentra_set.get(kenid=paramstr).kenid

    #Κέντρα όπου δεν περάστηκε σταυροδοσία (Δημ. Συμβουλοι)
    akataxoritaPer = EklSumpsifoiKenVw.objects.filter(eklid=eklid).filter(sumvotes=0)
    listakataxoritaPer = []
    for item in akataxoritaPer:
        listakataxoritaPer.append(item.kentro)

    #Κέντρα όπου δεν περάστηκε σταυροδοσία (Τοπ. Συμβουλοι)
    akataxoritaKoin = EklSumpsifoiKoinVw.objects.filter(eklid=eklid).filter(sumvotes=0).order_by('kentro')
    listakataxoritaKoin = []
    for item in akataxoritaKoin:
        listakataxoritaKoin.append(item.kentro)

    selected_order = paramorder

    #ανάκτηση όλων των κέντρων της εκλ. αναμέτρησης
    all_kentra=Kentra.objects.filter(eklid=eklid)
    #ανάκτηση εγγραφών επιλεγμένης εκλ. αναμέτρησης από το σχετικό database view
    all_pososta = EklSumpsifodeltiasindVw.objects.filter(eklid=eklid).order_by('-posostosindiasmou')

    if paramorder==1 or paramorder==6:
        all_psifoi = EklPsifoisimbVw.objects.filter(kenid=paramstr).order_by('sindiasmosnew','-votes')
    elif paramorder == 2:
        all_psifoi = EklPsifoisimbVw.objects.filter(kenid=paramstr).order_by('sindiasmosnew','surname', 'firstname')
    elif paramorder == 3:
        all_psifoi = EklPsifoisimbVw.objects.filter(kenid=paramstr).order_by('surname', 'firstname')
    elif paramorder == 4:
        all_psifoi = EklPsifoisimbVw.objects.filter(kenid=paramstr).order_by('-votes')
    else:
        all_psifoi = EklPsifoisimbVw.objects.filter(kenid=paramstr).order_by('eidos','-votes')


    context = {'all_psifoi':all_psifoi,
                'all_pososta':all_pososta,
               'all_ekloges':all_ekloges,
               'selected_ekloges':selected_ekloges.eklid,
               'all_kentra':all_kentra,
               'selected_kentro': selected_kentro,
               'listakataxoritaPer' : listakataxoritaPer,
               'listakataxoritaKoin' : listakataxoritaKoin,
               'selected_order':selected_order,
               }
    return render(request, 'Elections/psifoisimb_ken.html',context)

#ΠΑΡΑΜΕΤΡΙΚΑ

#@login_required
def edres_list(request, eklid):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.view_edres'):
        raise PermissionDenied

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    all_edres=Edres.objects.all()

    context = {'all_ekloges': all_ekloges,
               'selected_ekloges': selected_ekloges.eklid,
               'all_edres':all_edres
               }

    return render(request, 'Elections/edres_list.html' , context)

def edres_add(request, eklid):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.add_edres'):
        raise PermissionDenied

    action_label = 'Κατανομή εδρών - Νέα εγγραφή'

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    if request.method == 'POST':    #όταν γίνει POST των δεδομένων στη βάση
        form = EdresForm(request.POST)
        if form.is_valid():
            edres_item = form.save(commit=False)
            edres_item.save()
            messages.success(request, 'Η εγγραφή ολοκληρώθηκε!')
            form = EdresForm()
    else:
        form=EdresForm()  #όταν ανοίγει η φόρμα για καταχώριση δεδομένων

    context = {
                'selected_ekloges': selected_ekloges.eklid,
                'action_label' : action_label,
                'all_ekloges': all_ekloges,
                'form': form
               }

    return render(request, 'Elections/edres_form.html', context)

def edres_edit(request, eklid, edrid):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.change_edres'):
        raise PermissionDenied


    action_label = 'Κατανομή εδρών - Αλλαγή εγγραφής'

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    item=get_object_or_404(Edres, edrid=edrid)

    form = EdresForm(request.POST or None, instance=item)

    if form.is_valid():
        form.save()
        return redirect('edres_list', eklid)

    context = {
        'selected_ekloges': selected_ekloges.eklid,
        'action_label': action_label,
        'all_ekloges': all_ekloges,
        'form': form
    }

    return render(request, 'Elections/edres_form.html', context)

def edres_delete(request, eklid, edrid ):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.delete_edres'):
        raise PermissionDenied

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    obj=get_object_or_404(Edres, edrid=edrid)
    if request.method == 'POST':
        #parent_obj_url=obj.content_object.get_absolute_url()
        obj.delete()
        messages.success(request, "Η διαγραφή ολοκληρώθηκε")
        return redirect('edres_list', eklid)
    context={'selected_ekloges': selected_ekloges.eklid,
             'all_ekloges': all_ekloges,
             'object':obj
             }
    return render(request, 'Elections/confirm_delete.html', context)

def edreskoin_list(request, eklid):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.view_edreskoin'):
        raise PermissionDenied


    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    all_edreskoin=Edreskoin.objects.all()

    context = {'all_ekloges': all_ekloges,
               'selected_ekloges': selected_ekloges.eklid,
               'all_edreskoin':all_edreskoin
               }

    return render(request, 'Elections/edreskoin_list.html' , context)

def edreskoin_add(request, eklid):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.add_edreskoin'):
        raise PermissionDenied

    action_label = 'Κατανομή εδρών σε Κοινότητες - Νέα εγγραφή'

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    if request.method == 'POST':    #όταν γίνει POST των δεδομένων στη βάση
        form = EdresKoinForm(request.POST)
        if form.is_valid():
            edreskoin_item = form.save(commit=False)
            edreskoin_item.save()
            messages.success(request, 'Η εγγραφή ολοκληρώθηκε!')
            form = EdresKoinForm()
    else:
        form=EdresKoinForm()  #όταν ανοίγει η φόρμα για καταχώριση δεδομένων

    context = {
                'selected_ekloges': selected_ekloges.eklid,
                'action_label' : action_label,
                'all_ekloges': all_ekloges,
                'form': form
               }

    return render(request, 'Elections/edreskoin_form.html', context)

def edreskoin_edit(request, eklid, edrid):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.change_edreskoin'):
        raise PermissionDenied


    action_label = 'Κατανομή εδρών σε Κοινότητες - Αλλαγή εγγραφής'

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    item=get_object_or_404(Edreskoin, edrid=edrid)

    form = EdresKoinForm(request.POST or None, instance=item)

    if form.is_valid():
        form.save()
        return redirect('edreskoin_list', eklid)

    context = {
        'selected_ekloges': selected_ekloges.eklid,
        'action_label': action_label,
        'all_ekloges': all_ekloges,
        'form': form
    }

    return render(request, 'Elections/edreskoin_form.html', context)

def edreskoin_delete(request, eklid, edrid ):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.delete_edreskoin'):
        raise PermissionDenied

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    obj=get_object_or_404(Edreskoin, edrid=edrid)
    if request.method == 'POST':
        #parent_obj_url=obj.content_object.get_absolute_url()
        obj.delete()
        messages.success(request, "Η διαγραφή ολοκληρώθηκε")
        return redirect('edreskoin_list', eklid)
    context={'selected_ekloges': selected_ekloges.eklid,
             'all_ekloges': all_ekloges,
             'object':obj
             }
    return render(request, 'Elections/confirm_delete.html', context)

def sistima_list(request, eklid):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.view_sistima'):
        raise PermissionDenied

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    all_sistima=Sistima.objects.all()

    context = {'all_ekloges': all_ekloges,
               'selected_ekloges': selected_ekloges.eklid,
               'all_sistima':all_sistima
               }

    return render(request, 'Elections/sistima_list.html' , context)

def sistima_add(request, eklid):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.add_sistima'):
        raise PermissionDenied

    action_label = 'Εκλ. Συστήματα - Νέα εγγραφή'

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    if request.method == 'POST':    #όταν γίνει POST των δεδομένων στη βάση
        form = SistimaForm(request.POST)
        if form.is_valid():
            sistima_item = form.save(commit=False)
            sistima_item.save()
            messages.success(request, 'Η εγγραφή ολοκληρώθηκε!')
            form = SistimaForm()
            '''
            if "Save_and_add_another" in request.POST:
                return redirect('edres_add', eklid)
            else:
                return redirect('edres_list', eklid)'''
    else:
        form=SistimaForm()  #όταν ανοίγει η φόρμα για καταχώριση δεδομένων

    context = {
                'selected_ekloges': selected_ekloges.eklid,
                'action_label' : action_label,
                'all_ekloges': all_ekloges,
                'form': form
               }

    return render(request, 'Elections/sistima_form.html', context)

def sistima_edit(request, eklid, sisid):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.change_sistima'):
        raise PermissionDenied

    action_label = 'Εκλ. Συστήματα - Αλλαγή εγγραφής'

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    item=get_object_or_404(Sistima, sisid=sisid)

    form = SistimaForm(request.POST or None, instance=item)

    if form.is_valid():
        form.save()
        return redirect('sistima_list', eklid)

    context = {
        'selected_ekloges': selected_ekloges.eklid,
        'action_label': action_label,
        'all_ekloges': all_ekloges,
        'form': form
    }

    return render(request, 'Elections/sistima_form.html', context)

def sistima_delete(request, eklid, sisid ):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.delete_sistima'):
        raise PermissionDenied

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    obj=get_object_or_404(Sistima, sisid=sisid)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Η διαγραφή ολοκληρώθηκε")
        return redirect('sistima_list', eklid)
    context={'selected_ekloges': selected_ekloges.eklid,
             'all_ekloges': all_ekloges,
             'object':obj
             }

    return render(request, 'Elections/confirm_delete.html', context)


def typeofkoinotita_list(request, eklid):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.view_typeofkoinotita'):
        raise PermissionDenied

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    all_type=Typeofkoinotita.objects.all()

    context = {'all_ekloges': all_ekloges,
               'selected_ekloges': selected_ekloges.eklid,
               'all_type':all_type
               }

    return render(request, 'Elections/typeofkoinotita_list.html' , context)

def typeofkoinotita_add(request, eklid):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.add_typeofkoinotita'):
        raise PermissionDenied

    action_label = 'Τύποι κοινοτήτων - Νέα εγγραφή'

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    if request.method == 'POST':    #όταν γίνει POST των δεδομένων στη βάση
        form = TypeofkoinotitaForm(request.POST)
        if form.is_valid():
            type_item = form.save(commit=False)
            type_item.save()
            messages.success(request, 'Η εγγραφή ολοκληρώθηκε!')
            form = TypeofkoinotitaForm()
    else:
        form=TypeofkoinotitaForm()  #όταν ανοίγει η φόρμα για καταχώριση δεδομένων

    context = {
                'selected_ekloges': selected_ekloges.eklid,
                'action_label' : action_label,
                'all_ekloges': all_ekloges,
                'form': form,
               }

    return render(request, 'Elections/typeofkoinotita_form.html', context)

def typeofkoinotita_edit(request, eklid, tpkid):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.change_typeofkoinotita'):
        raise PermissionDenied

    action_label = 'Τύποι κοινοτήτων - Αλλαγή εγγραφής'

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    item=get_object_or_404(Typeofkoinotita, tpkid=tpkid)

    form = TypeofkoinotitaForm(request.POST or None, instance=item)

    if form.is_valid():
        form.save()
        return redirect('typeofkoinotita_list', eklid)

    context = {
        'selected_ekloges': selected_ekloges.eklid,
        'action_label': action_label,
        'all_ekloges': all_ekloges,
        'form': form
    }

    return render(request, 'Elections/typeofkoinotita_form.html', context)

def typeofkoinotita_delete(request, eklid, tpkid ):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.delete_typeofkoinotita'):
        raise PermissionDenied


    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    obj=get_object_or_404(Typeofkoinotita, tpkid=tpkid)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Η διαγραφή ολοκληρώθηκε")
        return redirect('typeofkoinotita_list', eklid)
    context={'selected_ekloges': selected_ekloges.eklid,
             'all_ekloges': all_ekloges,
             'object':obj
             }

    return render(request, 'Elections/confirm_delete.html', context)

def ekloges_list(request, eklid):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.view_eklogestbl'):
        raise PermissionDenied

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    #all_sistima=Sistima.objects.all()

    context = {'all_ekloges': all_ekloges,
               'selected_ekloges': selected_ekloges.eklid,
               }

    return render(request, 'Elections/ekloges_list.html' , context)

def ekloges_add(request, eklid):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.add_electionstbl'):
        raise PermissionDenied

    action_label = 'Εκλ. Συστήματα - Νέα εγγραφή'

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    if request.method == 'POST':    #όταν γίνει POST των δεδομένων στη βάση
        form = EklogestblForm(request.POST)
        if form.is_valid():
            ekl_item = form.save(commit=False)
            ekl_item.save()
            #Αν γίνει αυτή η προεπειλεγμένη αναμέτρηση, όλες τις άλλες τις κάνω μη προεπιλεγμένες
            if ekl_item.defaultelection == 1:
                Eklogestbl.objects.exclude(eklid=ekl_item.eklid).update(defaultelection=0)
            messages.success(request, 'Η εγγραφή ολοκληρώθηκε!')
            form = EklogestblForm()
            '''
            if "Save_and_add_another" in request.POST:
                return redirect('edres_add', eklid)
            else:
                return redirect('edres_list', eklid)'''
    else:
        form=EklogestblForm()  #όταν ανοίγει η φόρμα για καταχώριση δεδομένων

    context = {
                'selected_ekloges': selected_ekloges.eklid,
                'action_label' : action_label,
                'all_ekloges': all_ekloges,
                'form': form
               }

    return render(request, 'Elections/elections_form.html', context)

def ekloges_edit(request, eklid, cureklid):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.change_electionstbl'):
        raise PermissionDenied

    action_label = 'Εκλ. Συστήματα - Αλλαγή εγγραφής'

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    item=get_object_or_404(Eklogestbl, eklid=cureklid)

    form = EklogestblForm(request.POST or None, instance=item)

    if form.is_valid():
        form.save()
        # Αν γίνει αυτή η προεπειλεγμένη αναμέτρηση, όλες τις άλλες τις κάνω μη προεπιλεγμένες
        if item.defaultelection == 1:
            Eklogestbl.objects.exclude(eklid=item.eklid).update(defaultelection=0)
        return redirect('ekloges_list', eklid)

    context = {
        'selected_ekloges': selected_ekloges.eklid,
        'action_label': action_label,
        'all_ekloges': all_ekloges,
        'form': form
    }

    return render(request, 'Elections/elections_form.html', context)

def ekloges_delete(request, eklid, cureklid ):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.delete_eklogestbl'):
        raise PermissionDenied

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    obj=get_object_or_404(Eklogestbl, eklid=cureklid)
    if request.method == 'POST':
        #parent_obj_url=obj.content_object.get_absolute_url()
        obj.delete()
        #Σε περίπτωση διαγραφής προεπιλεγμένης αναμέτρησης, κάνω default την αμέσως προηγούμενη
        if obj.defaultelection == 1:
            Eklogestbl.objects.filter(eklid=Eklogestbl.objects.latest('eklid').eklid).update(defaultelection=1)

        messages.success(request, "Η διαγραφή ολοκληρώθηκε")
        return redirect('ekloges_list', eklid)
    context={'selected_ekloges': selected_ekloges.eklid,
             'all_ekloges': all_ekloges,
             'object':obj
             }

    return render(request, 'Elections/confirm_delete.html', context)


def sindiasmoi_list(request, eklid):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.view_sindiasmoi'):
        raise PermissionDenied

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    #eklsind_items=Sindiasmoi.objects.filter(sindid__in=Eklsind.objects.filter(eklid=eklid).values_list('sindid'))
    #eklsindkoin_items=Sindiasmoi.objects.filter(sindid__in=Eklsindkoin.objects.filter(eklid=eklid).values_list('sindid'))
    #all_sindiasmoi = eklsind_items.union(eklsindkoin_items).order_by('-eidos')
    all_sindiasmoi = Sindiasmoi.objects.all().order_by('-eidos','-sindid')

    context = {'all_ekloges': all_ekloges,
               'selected_ekloges': selected_ekloges.eklid,
               'all_sindiasmoi': all_sindiasmoi,
               }

    return render(request, 'Elections/sindiasmoi_list.html' , context)

def sindiasmoi_add(request, eklid):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.add_sindiasmoi'):
        raise PermissionDenied

    action_label = 'Υποψήφιοι Συνδυασμοί - Νέα εγγραφή'

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    if request.method == 'POST':    #όταν γίνει POST των δεδομένων στη βάση
        form = SindiasmoiForm(request.POST, request.FILES)
        #sub_form = EklsindFormPartial(request.POST)


        #if all([form.is_valid(), sub_form.is_valid()]):
        if form.is_valid():
            sind_item = form.save(commit=False)
            sind_item.save()

            pic = form.cleaned_data['photofield']
            if not pic:
                pic = 'sindiasmoi/elections.jpg'


            # Εισάγω και μια νέα εγγραφή στον πίνακα EKLSIND αν είναι καθολικός συνδυασμός
            if sind_item.eidos == 1:
                Eklsind.objects.create(eklid=Eklogestbl.objects.get(eklid=eklid),
                                       sindid=sind_item,
                                       aa = form.cleaned_data['aa'],
                                       edresa=0,
                                       edresa_ypol=0,
                                       edresa_teliko=0,
                                       edresb=0,
                                       descr=form.cleaned_data['descr'],
                                       shortdescr=form.cleaned_data['shortdescr'],
                                       photofield=pic,
                                       ypol=0).save()

                # Εισαγωγή εγγραφής συνδυασμού στον πίνακα Psifodeltia με votes=0 για κάθε κέντρο της
                # εκλ. αναμέτρησης, αφού ο καθολικός συνδυασμός ψηφίζεται σε ΟΛΟ ΤΟ ΔΗΜΟ
                for kentro in Kentra.objects.filter(eklid=Eklogestbl.objects.get(eklid=eklid)):
                    Psifodeltia.objects.create(
                        sindid=sind_item,
                        kenid=kentro,
                        votesa=0,
                        votesb=0,
                        votesk=0,
                    ).save()

            else:
                # αν όμως τοπικός συνδυασμός, Εισάγω και μια νέα εγγραφή στον πίνακα EKLSINDKOIN
                # Αν  είναι τοπικός, κρύβω στο template και το ΑΑ
                Eklsindkoin.objects.create(eklid=Eklogestbl.objects.get(eklid=eklid),
                                       sindid=sind_item,
                                       koinid=form.cleaned_data['koinid'],
                                       proedros=form.cleaned_data['proedros'],
                                       aa=form.cleaned_data['aa'],
                                       edresk=0,
                                       edresk_ypol=0,
                                       edresk_teliko=0,
                                       ypol=0,
                                       descr=form.cleaned_data['descr'],
                                       shortdescr=form.cleaned_data['shortdescr'],
                                        photofield=pic,
                                       checkfordraw=0).save()

                # Εισαγωγή εγγραφής  στον πίνακα Psifodeltia με votes=0 για κάθε κέντρο ΤΗΣ ΚΟΙΝΟΤΗΤΑΣ,
                # αφού ο ΤΟΠΙΚΟΣ συνδυασμός ψηφίζεται μόνο στην ΚΟΙΝΟΤΗΤΑ όπου είναι υποψήφιος
                for kentro in Kentra.objects.filter(koinid=form.cleaned_data['koinid']):
                    Psifodeltia.objects.create(
                        sindid=sind_item,
                        kenid=kentro,
                        votesa=0,
                        votesb=0,
                        votesk=0,
                    ).save()


            messages.success(request, 'Η εγγραφή ολοκληρώθηκε!' )
            return redirect('sindiasmoi_add', eklid)

    else:
        # όταν ανοίγει η φόρμα για καταχώριση δεδομένων
        form=SindiasmoiForm(initial={'aa': 0})
       # sub_form = EklsindFormPartial()

    context = {
                'selected_ekloges': selected_ekloges.eklid,
                'action_label' : action_label,
                'all_ekloges': all_ekloges,
                'form': form,
                #'sub_form': sub_form,
               }

    return render(request, 'Elections/sindiasmoi_form.html', context)

def sindiasmoi_edit(request, eklid, sindid):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.change_sindiasmoi'):
        raise PermissionDenied

    action_label = 'Υποψήφιοι Συνδυασμοί - Αλλαγή εγγραφής'

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    sind_item = get_object_or_404(Sindiasmoi, sindid=sindid)

    #ΠΡΟΣΟΧΗ!!! Τα extra πεδία aa, koinid, proedros τα φορτώνω manually
    try:
        aa_field = Eklsind.objects.get(sindid=sindid, eklid=eklid).aa
    except:
        aa_field=0

    try:
        koinid_field = Eklsindkoin.objects.get(sindid=sindid, eklid=eklid).koinid
    except:
        koinid_field= None

    try:
        proedros_field = Eklsindkoin.objects.get(sindid=sindid, eklid=eklid).proedros
    except:
        proedros_field= ''

    if Eklsind.objects.filter(sindid=sindid, eklid=eklid).exists():
        eidos_field = 1
    else:
        eidos_field = 0

    if request.method == 'POST':
        form = SindiasmoiForm(request.POST or None, request.FILES or None, instance=sind_item)
        #sub_form = EklsindFormPartial(request.POST or None, instance=eklsind_item)

        if form.is_valid():
            sind_item = form.save(commit=False)

            pic = form.cleaned_data['photofield']
            if not pic:
                pic = 'sindiasmoi/elections.jpg'
                sind_item.photofield=pic

            sind_item.save()

            test=form.cleaned_data['eidos']

            # Αν είναι  Καθολικός Συνδυασμός..
            if form.cleaned_data['eidos'] == 1:

                #Αν είναι ήδη Καθολικός Συνδυασμός, κάνω απλά Update το πεδίο aa
                if eidos_field == 1:
                    Eklsind.objects.filter(eklid=eklid, sindid=sindid).update(aa=form.cleaned_data['aa'])
                    #Eklsindkoin.objects.filter(eklid=eklid, sindid=sindid).delete()

                #αλλιώς αν έγινε από Τοπικός --> Καθολικός ..
                else:
                    #1) εισαγωγή εγγραφής στον Eklsind
                    Eklsind.objects.create(eklid=Eklogestbl.objects.get(eklid=eklid),
                                           sindid=sind_item,
                                           aa=form.cleaned_data['aa'],
                                           edresa=0,
                                           edresa_ypol=0,
                                           edresa_teliko=0,
                                           edresb=0,
                                           ypol=0).save()

                    # 2) Διαγραφή εγγραφής από τον  Eklsindkoin
                    Eklsindkoin.objects.filter(eklid=eklid, sindid=sindid).delete()

                    # 3) Διαγραφή ψήφων από πίνακα Psifodeltia και συγκεκριμένα όλες τις εγγραφές που έχουν τον συνδυασμό σε κέντρο της τρέχουσας εκλ. αναμέτρησης
                    Psifodeltia.objects.filter(sindid=sindid).filter(kenid__in=Kentra.objects.filter(eklid=eklid).values_list('kenid')).delete()

                    # 4) Εισαγωγή εγγραφής συνδυασμού στον πίνακα Psifodeltia με votes=0 για κάθε κέντρο της τρέχουσας
                    # εκλ. αναμέτρησης, αφού ο καθολικός συνδυασμός ψηφίζεται σε ΟΛΟ ΤΟ ΔΗΜΟ
                    for kentro in Kentra.objects.filter(eklid=eklid):
                        Psifodeltia.objects.create(
                            sindid=sind_item,
                            kenid=kentro,
                            votesa=0,
                            votesb=0,
                            votesk=0,
                        ).save()

            #αλλιώς αν είναι Τοπικός
            else:
                #1) Αν είναι ήδη Τοπικός Συνδυασμός, κάνω απλά Update τα πεδία aa, koinid, proedros στον Eklsindkoin
                if eidos_field == 0:
                    Eklsindkoin.objects.filter(eklid=eklid, sindid=sindid).update(aa=form.cleaned_data['aa'],
                                                                              koinid=form.cleaned_data['koinid'],
                                                                              proedros=form.cleaned_data['proedros'])
                    #2) Αν αλλάξει μόνο το koinid...
                    if koinid_field != form.cleaned_data['koinid']:
                        # α) Διαγραφή ψήφων από πίνακα Psifodeltia και συγκεκριμένα όλες τις εγγραφές που έχουν τον συνδυασμό σε κέντρο της τρέχουσας εκλ. αναμέτρησης
                        Psifodeltia.objects.filter(sindid=sindid).filter(kenid__in=Kentra.objects.filter(eklid=eklid).values_list('kenid')).delete()

                        # β) Εισαγωγή εγγραφής συνδυασμού στον πίνακα Psifodeltia με votes=0 για κάθε κέντρο ΤΗΣ ΚΟΙΝΟΤΗΤΑΣ,
                        # αφού ο ΤΟΠΙΚΟΣ συνδυασμός ψηφίζεται μόνο στην ΚΟΙΝΟΤΗΤΑ όπου είναι υποψήφιος
                        for kentro in Kentra.objects.filter(koinid=form.cleaned_data['koinid']):
                            Psifodeltia.objects.create(
                                sindid=sind_item,
                                kenid=kentro,
                                votesa=0,
                                votesb=0,
                                votesk=0,
                            ).save()

                #αν από Καθολικός --> Τοπικός..
                else:
                    #1) εισαγωγή εγγραφής στον Eklsindkoin
                    Eklsindkoin.objects.create(eklid=Eklogestbl.objects.get(eklid=eklid),
                                               sindid=sind_item,
                                               koinid=form.cleaned_data['koinid'],
                                               proedros=form.cleaned_data['proedros'],
                                               aa=form.cleaned_data['aa'],
                                               edresk=0,
                                               edresk_ypol=0,
                                               edresk_teliko=0,
                                               ypol=0,
                                               checkfordraw=0).save()

                    # 2) Διαγραφή εγγραφής από τον  Eklsind
                    Eklsind.objects.filter(eklid=eklid, sindid=sindid).delete()

                    # 3) Διαγραφή ψήφων από πίνακα Psifodeltia και συγκεκριμένα όλες τις εγγραφές που έχουν τον συνδυασμό σε κέντρο της τρέχουσας εκλ. αναμέτρησης
                    Psifodeltia.objects.filter(sindid=sindid).filter(kenid__in=Kentra.objects.filter(eklid=eklid).values_list('kenid')).delete()

                    # 4) Εισαγωγή εγγραφής συνδυασμού στον πίνακα Psifodeltia με votes=0 για κάθε κέντρο ΤΗΣ ΚΟΙΝΟΤΗΤΑΣ,
                    # αφού ο ΤΟΠΙΚΟΣ σύμβουλος ψηφίζεται μόνο στην ΚΟΙΝΟΤΗΤΑ όπου είναι υποψήφιος
                    for kentro in Kentra.objects.filter(koinid=form.cleaned_data['koinid']):
                        Psifodeltia.objects.create(
                            sindid=sind_item,
                            kenid=kentro,
                            votesa=0,
                            votesb=0,
                            votesk=0,
                        ).save()
            messages.success(request, 'Η αλλαγή αποθηκεύτηκε!')
            return redirect('sindiasmoi_list', eklid)
    else:
        #αν δεν γίνει POST φέρνω τα πεδία του μοντέλου καθως και το extra πεδίο aa manually
        form = SindiasmoiForm(request.POST or None, request.FILES or None, instance=sind_item, initial={'aa': aa_field, 'koinid': koinid_field, 'proedros':proedros_field})
        #sub_form = EklsindFormPartial(request.POST or None, instance=eklsind_item)

    context = {
        'selected_ekloges': selected_ekloges.eklid,
        'action_label': action_label,
        'all_ekloges': all_ekloges,
        'form': form,
    }

    return render(request, 'Elections/sindiasmoi_form.html', context)


def sindiasmoi_delete(request, eklid, sindid ):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.delete_sindiasmoi'):
        raise PermissionDenied

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    obj = get_object_or_404(Sindiasmoi, sindid=sindid)
    if request.method == 'POST':

        #####

        if request.method == 'POST':
            # parent_obj_url=obj.content_object.get_absolute_url()
            #if flag_found_palia == 1:
            Simbouloi.objects.filter(simbid__in=Eklsindsimb.objects.filter(sindid=obj).values_list('simbid')).delete()
        ####

        obj.delete()
        messages.success(request, "Η διαγραφή ολοκληρώθηκε")
        return redirect('sindiasmoi_list', eklid)
    context = {'selected_ekloges': selected_ekloges.eklid,
               'all_ekloges': all_ekloges,
               'object': obj
               }

    return render(request, 'Elections/confirm_sindiasmoi_delete.html', context)


def eklsind_list(request, eklid):
    selected_ekloges = Eklogestbl.objects.prefetch_related('eklsind_set').get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.view_eklsind'):
        raise PermissionDenied

    #selected_ekloges = Eklogestbl.objects.prefetch_related('eklsind_set').get(eklid=eklid)

    #all_simbouloi = selected_ekloges.eklallsimbvw_set.all().values_list('simbid', 'surname', 'firstname', 'fathername','toposeklogis', 'sindiasmos')

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    #all_eklsind = Eklsind.objects.filter(eklid=eklid).order_by( 'sindid__descr')
    all_eklsind = selected_ekloges.eklsind_set.all().order_by('-edresa_teliko')
    all_pososta = EklSumpsifodeltiasindVw.objects.filter(eklid=eklid, eidos=1).order_by('-posostosindiasmou')


    context = {'all_ekloges': all_ekloges,
               'selected_ekloges': selected_ekloges.eklid,
               'all_eklsind': all_eklsind,
               'all_pososta': all_pososta ,
               }

    return render(request, 'Elections/eklsind_list.html' , context)

def eklsind_add(request, eklid):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))


    if not request.user.has_perm('Elections.add_eklsind'):
        raise PermissionDenied


    action_label = 'Δημοτικοί Συνδυασμοί και Έδρες - Νέα εγγραφή'

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')



    if request.method == 'POST':    #όταν γίνει POST των δεδομένων στη βάση
        form = EklsindForm(eklid, request.POST, request.FILES ) #ΠΡΟΣΟΧΗ! περνάω σαν παράμετρο το eklid, γιατί στη φόρμα γίνεται αρχικοποίηση με αυτή την παράμετρο
        if form.is_valid():
            sind_item = form.save(commit=False)

            pic = form.cleaned_data['photofield']
            if not pic:
                pic = 'sindiasmoi/elections.jpg'

            sind_item.photofield=pic

            sind_item.save()

            ###

            # Εισαγωγή εγγραφής συνδυασμού στον πίνακα Psifodeltia με votes=0 για κάθε κέντρο της
            # εκλ. αναμέτρησης, αφού ο καθολικός συνδυασμός ψηφίζεται σε ΟΛΟ ΤΟ ΔΗΜΟ
            for kentro in Kentra.objects.filter(eklid=Eklogestbl.objects.get(eklid=eklid)):
                # μόνο αν δεν υπάρχει εγγραφή στον πίνακα Psifodeltia για το κέντρο, εισάγω εγγραφή για το συγκεκριμένο κέντρο
                if not Psifodeltia.objects.filter(sindid=sind_item.sindid).filter(kenid=kentro).exists():
                    Psifodeltia.objects.create(
                        sindid=sind_item.sindid,
                        kenid=kentro,
                        votesa=0,
                        votesb=0,
                        votesk=0,
                    ).save()

            ###

            messages.success(request, 'Η εγγραφή ολοκληρώθηκε!')
            #καλώ πάλι τη φόρμα με initial eklid την εκλ. αναμέτρηση στην οποία είμαστε συνδεδεμένο
            form = EklsindForm(eklid, initial={'eklid':Eklogestbl.objects.get(eklid=eklid)})

    else:
        #default eklid θέτω την εκλ. αναμέτρηση στην οποία είμαστε συνδεδεμένοι
        form=EklsindForm(eklid,initial={'eklid':Eklogestbl.objects.get(eklid=eklid)})  #όταν ανοίγει η φόρμα για καταχώριση δεδομένων

    context = {
                'selected_ekloges': selected_ekloges.eklid,
                'action_label' : action_label,
                'all_ekloges': all_ekloges,
                'form': form
               }

    return render(request, 'Elections/eklsind_form.html', context)

def eklsind_edit(request, eklid, id):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.change_eklsind'):
        raise PermissionDenied

    action_label = 'Δημοτικοί Συνδυασμοί και Έδρες - Αλλαγή εγγραφής'

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    item = get_object_or_404(Eklsind, id=id)

    #περνάω παράμετρο eklid=0, για να μπορεί να εμφανίσει στο dropdown sindid το συνδυασμό
    #γιατί διαφορετικά το αποκλείει σύμφωνα με την αρχικοποίηση που κάνω στη φόρμα EklsindForm
    form = EklsindForm(0, request.POST or None, request.FILES or None,  instance=item)
    #form = SindiasmoiForm(request.POST or None, request.FILES or None, instance=sind_item)
    if form.is_valid():

        pic = form.cleaned_data['photofield']
        if not pic:
            pic = 'sindiasmoi/elections.jpg'
            item.photofield = pic

        form.save()


        return redirect('eklsind_list', eklid)

    context = {
        'selected_ekloges': selected_ekloges.eklid,
        'action_label': action_label,
        'all_ekloges': all_ekloges,
        'form': form
    }

    return render(request, 'Elections/eklsind_form.html', context)


def eklsind_delete(request, eklid, id ):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))


    if not request.user.has_perm('Elections.delete_eklsind'):
        raise PermissionDenied

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    obj = get_object_or_404(Eklsind, id=id)
    if request.method == 'POST':

        #####
        #Βλέπω αν υπάρχει ο συνδυασμός και σε ΑΛΛΕΣ εκλ. αναμετρήσεις, και αν υπάρχει, σβήνω όλα τα σχετιζόμενα με αυτόν ΜΟΝΟ ΣΤΗΝ ΤΡΕΧΟΥΣΑ ΕΚΛ. ΑΝΑΜΕΤΡΗΣΗ

        if Eklsind.objects.filter(sindid=obj.sindid).exclude(eklid=eklid).exists():
            flag_found_palia = 1
            # Simbouloi.objects.filter(simbid=simb_item.simbid).delete()
        else:
            flag_found_palia = 0

        if flag_found_palia == 1:
            #ο συνδυασμός υπάρχει σε άλλες αναμετρήσεις...άρα σβήνω σχετικές εγγραφές μόνο της τρέχουσας εκλ. αναμέτρησης

            Eklsimbper.objects.filter(eklid=eklid).filter(simbid__in=Eklsindsimb.objects.filter(eklid=eklid).filter(sindid=obj.sindid).values_list('simbid')).delete()
            Eklsimbkoin.objects.filter(eklid=eklid).filter(simbid__in=Eklsindsimb.objects.filter(eklid=eklid).filter(sindid=obj.sindid).values_list('simbid')).delete()
            Psifoi.objects.filter(simbid__in=Eklsindsimb.objects.filter(eklid=eklid).filter(sindid=obj.sindid).values_list('simbid')).filter(kenid__in=Kentra.objects.filter(eklid=eklid).values_list('kenid')).delete()
            Psifodeltia.objects.filter(sindid=obj.sindid).filter(kenid__in=Kentra.objects.filter(eklid=eklid).values_list('kenid')).delete()
            Eklsindkoin.objects.filter(eklid=eklid).filter(sindid=obj.sindid).delete()
            Eklsindsimb.objects.filter(eklid=eklid).filter(sindid=obj.sindid).delete()

            #σβήνω εν τέλει και  "ορφανές" εγγραφές  από τον πίνακα simbouloi (που δεν έχουν δηλαδή αντίστοιχη εγγραφή στον πίνακα EKLSINDSIMB
            Simbouloi.objects.exclude(simbid__in=(Eklsindsimb.objects.all()).values_list('simbid')).delete()

            obj.delete()
        else:
            #αν ο συνδυασμός δεν υπάρχει σε προηγούμενες αναμετρήσεις...τότε σβήνω :

            # 1) τους σχετικούς συμβούλους και από πίνακα Simbouloi , ο οποίος λογω cascade θα σβήσει τις σχετικές εγγραφές και στους άλλους (EKLSIMBPER, EKLSIMBKOIN, EKLSINDSIMB, PSIFOI)
            Simbouloi.objects.filter(simbid__in=EklallsimbVw.objects.filter(sindid=obj.sindid.sindid).values_list('simbid')).delete()
            # 2) το συνδυασμό και από πίνακα Sindiasmoi, ο οποίος λογω cascade θα σβήσει τις σχετικές εγγραφές και στα PSIFODELTIA
            temp=obj   #προσωρινά αντιγραφή του obj στο temp επειδή το obj θα διαγραφεί.

            obj.delete() #SOS!!! : ειδικά σ' αυτήν την περίπτωση σβήνω πρώτα το obj και μετά από τους Sindiasmoi, γιατί αλλιώς θα έχω πρόβλημα με το ξένο κλειδί που υπάρχει στον Eklsind.

            Sindiasmoi.objects.filter(sindid=temp.sindid.sindid).delete()


        ####

        #obj.delete()
        messages.success(request, "Η διαγραφή ολοκληρώθηκε")
        return redirect('eklsind_list', eklid)
    context = {'selected_ekloges': selected_ekloges.eklid,
               'all_ekloges': all_ekloges,
               'object': obj
               }

    return render(request, 'Elections/confirm_sindiasmoi_delete.html', context)


def perifereia_list(request, eklid):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))


    if not request.user.has_perm('Elections.view_perifereies'):
        raise PermissionDenied


    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    all_perifereies=Perifereies.objects.filter(perid__in=Eklper.objects.filter(eklid=eklid).values_list('perid'))

    context = {'all_ekloges': all_ekloges,
               'selected_ekloges': selected_ekloges.eklid,
               'all_perifereies':all_perifereies
               }

    return render(request, 'Elections/perifereia_list.html' , context)

def perifereia_add(request, eklid):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.add_perifereies'):
        raise PermissionDenied


    action_label = 'Εκλ. Περιφέρειες - Νέα εγγραφή'

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    if request.method == 'POST':    #όταν γίνει POST των δεδομένων στη βάση
        form = PerifereiesForm(request.POST)
        if form.is_valid():
            perifereia_item = form.save(commit=False)
            perifereia_item.save()
            #Εισαγωγή εγγραφής και στον Eklper
            Eklper.objects.create(eklid=Eklogestbl.objects.get(eklid=eklid),
                                   perid=perifereia_item,
                                   ).save()
            messages.success(request, 'Η εγγραφή ολοκληρώθηκε!')
            form = PerifereiesForm()
    else:
        form=PerifereiesForm()  #όταν ανοίγει η φόρμα για καταχώριση δεδομένων

    context = {
                'selected_ekloges': selected_ekloges.eklid,
                'action_label' : action_label,
                'all_ekloges': all_ekloges,
                'form': form
               }

    return render(request, 'Elections/perifereia_form.html', context)

def perifereia_edit(request, eklid, perid):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.change_perifereies'):
        raise PermissionDenied

    action_label = 'Εκλ. Περιφέρειες - Αλλαγή εγγραφής'

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    item=get_object_or_404(Perifereies, perid=perid)

    form = PerifereiesForm(request.POST or None, instance=item)

    if form.is_valid():
        form.save()
        return redirect('perifereia_list', eklid)

    context = {
        'selected_ekloges': selected_ekloges.eklid,
        'action_label': action_label,
        'all_ekloges': all_ekloges,
        'form': form
    }

    return render(request, 'Elections/perifereia_form.html', context)

def perifereia_delete(request, eklid, perid ):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.delete_perifereies'):
        raise PermissionDenied

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    obj=get_object_or_404(Perifereies, perid=perid)

    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Η διαγραφή ολοκληρώθηκε")
        return redirect('perifereia_list', eklid)
    context={'selected_ekloges': selected_ekloges.eklid,
             'all_ekloges': all_ekloges,
             'object':obj
             }

    return render(request, 'Elections/confirm_delete.html', context)


def eklsindkoin_list(request, eklid):
    selected_ekloges = Eklogestbl.objects.prefetch_related('eklsindkoin_set').get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.view_eklsindkoin'):
        raise PermissionDenied


    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    all_eklsindkoin = selected_ekloges.eklsindkoin_set.all().order_by('koinid__descr', '-edresk_teliko')

    context = {'all_ekloges': all_ekloges,
               'selected_ekloges': selected_ekloges.eklid,
               'all_eklsindkoin': all_eklsindkoin,
               }

    return render(request, 'Elections/eklsindkoin_list.html' , context)

def eklsindkoin_add(request, eklid):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.add_eklsindkoin'):
        raise PermissionDenied

    action_label = 'Τοπικοί Συνδυασμοί και Έδρες - Νέα εγγραφή'

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    if request.method == 'POST':    #όταν γίνει POST των δεδομένων στη βάση
        form = EklsindkoinForm(eklid, request.POST, request.FILES ) #ΠΡΟΣΟΧΗ! περνάω σαν παράμετρο το eklid, γιατί στη φόρμα γίνεται αρχικοποίηση με αυτή την παράμετρο
        if form.is_valid():
            item = form.save(commit=False)

            pic = form.cleaned_data['photofield']
            if not pic:
                pic = 'sindiasmoi/elections.jpg'

            item.photofield = pic

            item.save()

            # Εισαγωγή εγγραφής  στον πίνακα Psifodeltia με votes=0 για κάθε κέντρο ΤΗΣ ΚΟΙΝΟΤΗΤΑΣ,
            # αφού ο ΤΟΠΙΚΟΣ συνδυασμός ψηφίζεται μόνο στην ΚΟΙΝΟΤΗΤΑ όπου είναι υποψήφιος
            for kentro in Kentra.objects.filter(koinid=form.cleaned_data['koinid']):
                # μόνο αν δεν υπάρχει εγγραφή στον πίνακα Psifodeltia για το κέντρο της συγκεκριμένης Κοινότητας, εισάγω εγγραφή για το συγκεκριμένο κέντρο
                if not Psifodeltia.objects.filter(sindid=item.sindid).filter(kenid=kentro).exists():
                    Psifodeltia.objects.create(
                        sindid=item.sindid,
                        kenid=kentro,
                        votesa=0,
                        votesb=0,
                        votesk=0,
                    ).save()

            messages.success(request, 'Η εγγραφή ολοκληρώθηκε!')
            #καλώ πάλι τη φόρμα με initial eklid την εκλ. αναμέτρηση στην οποία είμαστε συνδεδεμένο
            form = EklsindkoinForm(eklid, initial={'eklid':Eklogestbl.objects.get(eklid=eklid)})

    else:
        #default eklid θέτω την εκλ. αναμέτρηση στην οποία είμαστε συνδεδεμένοι
        form=EklsindkoinForm(eklid,initial={'eklid':Eklogestbl.objects.get(eklid=eklid)})  #όταν ανοίγει η φόρμα για καταχώριση δεδομένων

    context = {
                'selected_ekloges': selected_ekloges.eklid,
                'action_label' : action_label,
                'all_ekloges': all_ekloges,
                'form': form
               }

    return render(request, 'Elections/eklsindkoin_form.html', context)

def eklsindkoin_edit(request, eklid, id):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.edit_eklsindkoin'):
        raise PermissionDenied

    action_label = 'Τοπικοί Συνδυασμοί και Έδρες - Αλλαγή εγγραφής'

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    item = get_object_or_404(Eklsindkoin, id=id)
    oldeidosSind = item.sindid.eidos
    oldsindid = item.sindid
    oldkoinid = item.koinid

    #περνάω παράμετρο eklid=0, για να μπορεί να εμφανίσει στο dropdown sindid το συνδυασμό
    #γιατί διαφορετικά το αποκλείει σύμφωνα με την αρχικοποίηση που κάνω στη φόρμα EklsindForm
    form = EklsindkoinForm(eklid, request.POST or None,  instance=item)

    if form.is_valid():
        form.save()

        #1) αν αλλάξει συνδυασμός
        if form.cleaned_data['sindid'] != oldsindid: #and form.cleaned_data['koinid'] != oldkoinid:
            #α) Από Τοπικό συνδυασμό --> σε Καθολικό
            if form.cleaned_data['sindid'].eidos ==1 and oldeidosSind == 0:
                # i) Διαγραφή στον πίνακα Psifodeltia των εγγραφών των σχετικών με την πρώην Κοινότητα και τον πρώην Συνδυασμό
                #Psifodeltia.objects.filter(kenid__in=(Kentra.objects.filter(koinid=oldkoinid))).filter(sindid=oldsindid).delete()
                # ii) Διαγραφή ψήφων συμβούλων του πρώην Συνδυασμού για τα κέντρα της πρώην Κοινότητας
                #Psifoi.objects.filter(kenid__in=(Kentra.objects.filter(koinid=oldkoinid))).filter(simbid__in=(Eklsindsimb.objects.filter(eklid=eklid).filter(sindid=oldsindid))).delete()
                # iii) Διαγραφή συμβούλων του πρώην Συνδυασμού από τον Eklsimbkoin
                #Eklsimbkoin.objects.filter(eklid=eklid).filter(simbid__in=(Eklsindsimb.objects.filter(eklid=eklid).filter(sindid=oldsindid))).delete()


                # ι) Αν ο σύμβουλος του πρώην συνδυασμού υπάρχει σε προηγούμενες εκλ. αναμετρήσεις, σβήσε μόνο τα απαραίτητα στους σχετικούς πίνακες του συμβούλου, αλλιώς
                # σβήσε και το σύμβουλο (μέσω του cascade Θα σβήσουν και όλα τα σχετικά). Αυτό γίνεται για κάθε σύμβουλο του πρωην συνδυασμού
                for simbitem in Eklsindsimb.objects.filter(eklid=eklid).filter(sindid=oldsindid):
                    if Eklsindsimb.objects.filter(simbid=simbitem.simbid).filter(eklid__lt=eklid).exists():
                        Psifoi.objects.filter(kenid__in=(Kentra.objects.filter(koinid=oldkoinid))).filter(
                            simbid__in=(Eklsindsimb.objects.filter(eklid=eklid).filter(sindid=oldsindid))).delete()
                        Eklsindsimb.objects.filter(eklid=eklid).filter(sindid=oldsindid).delete()
                        Eklsimbkoin.objects.filter(eklid=eklid).filter(koinid=oldkoinid).delete()
                    else:
                        Simbouloi.objects.filter(simbid=simbitem.simbid.simbid).delete()


                # ιι) Αν ο συνδυασμός υπάρχει σε προηγούμενες εκλ. αναμετρήσεις, σβήσε μόνο τα απαραίτητα στους σχετικούς πίνακες του συνδυασμού, αλλιώς
                #σβήσε και το συνδυασμό (μέσω του cascade Θα σβήσουν και όλα τα σχετικά)
                if Eklsindkoin.objects.filter(sindid=oldsindid).filter(eklid__lt=eklid).exists():
                    Psifodeltia.objects.filter(kenid__in=(Kentra.objects.filter(koinid=oldkoinid))).filter(
                        sindid=oldsindid).delete()
                    Eklsindkoin.objects.filter(eklid=eklid).filter(sindid=oldsindid).delete()
                else:
                    Sindiasmoi.objects.filter(sindid=oldsindid.sindid).delete()

            #β) Από Καθολικό συνδυασμό --> σε Τοπικό
            elif form.cleaned_data['sindid'].eidos ==0 and oldeidosSind == 1:
                # ι) Μηδενισμός votesk στα Psifodeltia για τον πρώην συνδυασμό
                Psifodeltia.objects.filter(kenid__in=(Kentra.objects.filter(koinid=oldkoinid))).filter(sindid=oldsindid).update(votesk=0)
                # ιι) Δημιουργία εγγραφής στα Psifodeltia για κάθε κέντρο της νέας Κοινότητας για το νέο συνδυασμό
                for kentro in Kentra.objects.filter(koinid=form.cleaned_data['koinid']):
                    Psifodeltia.objects.create(
                        sindid=form.cleaned_data['sindid'],
                        kenid=kentro,
                        votesa=0,
                        votesb=0,
                        votesk=0
                    )

                # ιιι) Αν ο σύμβουλος του πρώην συνδυασμού υπάρχει σε προηγούμενες εκλ. αναμετρήσεις, σβήσε μόνο τα απαραίτητα στους σχετικούς πίνακες του συμβούλου, αλλιώς
                # σβήσε και το σύμβουλο (μέσω του cascade Θα σβήσουν και όλα τα σχετικά). Αυτό γίνεται για κάθε σύμβουλο του πρωην συνδυασμού
                for simbitem in Eklsindsimb.objects.filter(eklid=eklid).filter(sindid=oldsindid):
                    if Eklsindsimb.objects.filter(simbid=simbitem.simbid).filter(eklid__lt=eklid).exists():
                        Psifoi.objects.filter(kenid__in=(Kentra.objects.filter(koinid=oldkoinid))).filter(simbid__in=(Eklsindsimb.objects.filter(eklid=eklid).filter(sindid=oldsindid))).delete()
                        Eklsindsimb.objects.filter(eklid=eklid).filter(sindid=oldsindid).delete()
                        Eklsimbkoin.objects.filter(eklid=eklid).filter(koinid=oldkoinid).delete()
                    else:
                        Simbouloi.objects.filter(simbid=simbitem.simbid.simbid).delete()

            # γ) Από Καθολικό συνδυασμό --> σε άλλο Καθολικό
            elif form.cleaned_data['sindid'].eidos == 1 and oldeidosSind == 1:
                #  ι) Μηδενισμός votesk στα Psifodeltia για τον πρώην συνδυασμό
                Psifodeltia.objects.filter(kenid__in=(Kentra.objects.filter(koinid=oldkoinid))).filter(sindid=oldsindid).update(votesk=0)
                # ιι) Αν ο σύμβουλος του πρώην συνδυασμού υπάρχει σε προηγούμενες εκλ. αναμετρήσεις, σβήσε μόνο τα απαραίτητα στους σχετικούς πίνακες του συμβούλου, αλλιώς
                #  σβήσε και το σύμβουλο (μέσω του cascade Θα σβήσουν και όλα τα σχετικά). Αυτό γίνεται για κάθε σύμβουλο του πρωην συνδυασμού
                for simbitem in Eklsindsimb.objects.filter(eklid=eklid).filter(sindid=oldsindid):
                    if Eklsindsimb.objects.filter(simbid=simbitem.simbid).filter(eklid__lt=eklid).exists():
                        Psifoi.objects.filter(kenid__in=(Kentra.objects.filter(koinid=oldkoinid))).filter(simbid__in=(Eklsindsimb.objects.filter(eklid=eklid).filter(sindid=oldsindid))).delete()
                        Eklsindsimb.objects.filter(eklid=eklid).filter(sindid=oldsindid).delete()
                        Eklsimbkoin.objects.filter(eklid=eklid).filter(koinid=oldkoinid).delete()
                    else:
                        Simbouloi.objects.filter(simbid=simbitem.simbid.simbid).delete()

            # δ) Από Τοπικό συνδυασμό --> σε άλλο Τοπικό
            elif form.cleaned_data['sindid'].eidos == 0 and oldeidosSind == 0:
                # ι) Αν ο σύμβουλος του πρώην συνδυασμού υπάρχει σε προηγούμενες εκλ. αναμετρήσεις, σβήσε μόνο τα απαραίτητα στους σχετικούς πίνακες του συμβούλου, αλλιώς
                # σβήσε και το σύμβουλο (μέσω του cascade Θα σβήσουν και όλα τα σχετικά). Αυτό γίνεται για κάθε σύμβουλο του πρωην συνδυασμού
                for simbitem in Eklsindsimb.objects.filter(eklid=eklid).filter(sindid=oldsindid):
                    if Eklsindsimb.objects.filter(simbid=simbitem.simbid).filter(eklid__lt=eklid).exists():
                        Psifoi.objects.filter(kenid__in=(Kentra.objects.filter(koinid=oldkoinid))).filter(simbid__in=(Eklsindsimb.objects.filter(eklid=eklid).filter(sindid=oldsindid))).delete()
                        Eklsindsimb.objects.filter(eklid=eklid).filter(sindid=oldsindid).delete()
                        Eklsimbkoin.objects.filter(eklid=eklid).filter(koinid=oldkoinid).delete()
                    else:
                        Simbouloi.objects.filter(simbid=simbitem.simbid.simbid).delete()

                # ιι) Αν ο συνδυασμός υπάρχει σε προηγούμενες εκλ. αναμετρήσεις, σβήσε μόνο τα απαραίτητα στους σχετικούς πίνακες του συνδυασμού, αλλιώς
                # σβήσε και το συνδυασμό (μέσω του cascade Θα σβήσουν και όλα τα σχετικά)
                if Eklsindkoin.objects.filter(sindid=oldsindid).filter(eklid__lt=eklid).exists():
                    Psifodeltia.objects.filter(kenid__in=(Kentra.objects.filter(koinid=oldkoinid))).filter(sindid=oldsindid).delete()
                    Eklsindkoin.objects.filter(eklid=eklid).filter(sindid=oldsindid).delete()
                else:
                    Sindiasmoi.objects.filter(sindid=oldsindid.sindid).delete()

                # ιιι) Δημιουργία εγγραφής στα Psifodeltia για κάθε κέντρο της νέας Κοινότητας για το νέο συνδυασμό
                for kentro in Kentra.objects.filter(koinid=form.cleaned_data['koinid']):
                    Psifodeltia.objects.create(
                        sindid=form.cleaned_data['sindid'],
                        kenid=kentro,
                        votesa=0,
                        votesb=0,
                        votesk=0
                    )

        return redirect('eklsindkoin_list', eklid)

    context = {
        'selected_ekloges': selected_ekloges.eklid,
        'action_label': action_label,
        'all_ekloges': all_ekloges,
        'form': form
    }

    return render(request, 'Elections/eklsindkoin_form.html', context)


def eklsindkoin_delete(request, eklid, id ):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.delete_eklsindkoin'):
        raise PermissionDenied

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    obj = get_object_or_404(Eklsindkoin, id=id)
    oldeidosSind = obj.sindid.eidos
    oldsindid = obj.sindid
    oldkoinid = obj.koinid

    if request.method == 'POST':

        #αν είναι καθολικός συνδυασμός, ενημέρωση του votesk=0 στα Psifodeltia
        if oldeidosSind == 1:
            #Psifodeltia.objects.filter(sindid=obj.sindid).filter(kenid__in=(Kentra.objects.filter(eklid=eklid))).update(votesk=0)

            # ι) Μηδενισμός votesk στα Psifodeltia για τον πρώην συνδυασμό
            Psifodeltia.objects.filter(kenid__in=(Kentra.objects.filter(koinid=oldkoinid))).filter(sindid=oldsindid).update(votesk=0)

            # ιι) Διαγραφή του συνδυασμού από τον EKLSINDKOIN για την τρέχ. Εκλ. Αναμέτρηση και για τη συγκεκριμένη Κοινότητα
            Eklsindkoin.objects.filter(eklid=eklid).filter(sindid=oldsindid).filter(koinid=oldkoinid).delete()

            # ιιι) Αν ο σύμβουλος του πρώην συνδυασμού υπάρχει σε άλλες εκλ. αναμετρήσεις, σβήσε μόνο τα απαραίτητα στους σχετικούς πίνακες του συμβούλου, αλλιώς
            # σβήσε και το σύμβουλο (μέσω του cascade Θα σβήσουν και όλα τα σχετικά). Αυτό γίνεται για κάθε σύμβουλο του πρωην συνδυασμού
            for simbitem in EklallsimbVw.objects.filter(eklid=eklid).filter(toposeklogisid=oldkoinid.koinid).filter(
                    sindid=oldsindid.sindid):
                if Eklsindsimb.objects.filter(simbid=simbitem.simbid).exclude(
                        eklid=eklid).exists():  # με το exclude παίρνω μόνο αυτούς που υπάρχουν και σε άλλες εκλογές
                    Psifoi.objects.filter(kenid__in=(Kentra.objects.filter(koinid=oldkoinid.koinid))).filter(
                        simbid=simbitem.simbid).delete()
                    Eklsimbkoin.objects.filter(eklid=eklid).filter(koinid=oldkoinid).filter(
                        simbid=simbitem.simbid).delete()
                    Eklsindsimb.objects.filter(eklid=eklid).filter(sindid=oldsindid).filter(
                        simbid=simbitem.simbid).delete()

                    # σβήνω εν τέλει και  "ορφανές" εγγραφές  από τον πίνακα simbouloi (που δεν έχουν δηλαδή αντίστοιχη εγγραφή στον πίνακα EKLSINDSIMB
                    Simbouloi.objects.exclude(simbid__in=(Eklsindsimb.objects.all()).values_list('simbid')).delete()
                else:
                    Simbouloi.objects.filter(simbid=simbitem.simbid.simbid).delete()

        else:
            #Αλλιώς αν είναι Τοπικός, διαγραφή των σχετικών εγγραφών από τον πίνακα Psifodeltia
            #Psifodeltia.objects.filter(sindid=obj.sindid).filter(kenid__in=(Kentra.objects.filter(eklid=eklid))).delete()

            # ι) Αν ο συνδυασμός υπάρχει σε άλλες εκλ. αναμετρήσεις, σβήσε μόνο τα απαραίτητα στους σχετικούς πίνακες του συνδυασμού
            if Eklsindkoin.objects.filter(sindid=oldsindid).exclude(eklid=eklid).exists():
                # σβήσε τα records από Psifodeltia για το συνδυασμό και την τρεχ. εκλ. αναμέτρηση
                Psifodeltia.objects.filter(kenid__in=(Kentra.objects.filter(koinid=oldkoinid))).filter(sindid=oldsindid).delete()
                # σβήσε τα records από Eklsindkoin για το συνδυασμό και την τρεχ. εκλ. αναμέτρηση
                Eklsindkoin.objects.filter(eklid=eklid).filter(sindid=oldsindid).delete()

                # Αν ο σύμβουλος του πρώην συνδυασμού υπάρχει σε άλλες εκλ. αναμετρήσεις, σβήσε μόνο τα απαραίτητα στους σχετικούς πίνακες του συμβούλου, αλλιώς
                # σβήσε και το σύμβουλο (μέσω του cascade Θα σβήσουν και όλα τα σχετικά). Αυτό γίνεται για κάθε σύμβουλο του πρωην συνδυασμού
                for simbitem in EklallsimbVw.objects.filter(eklid=eklid).filter(toposeklogisid=oldkoinid.koinid).filter(
                        sindid=oldsindid.sindid):
                    if Eklsindsimb.objects.filter(simbid=simbitem.simbid).exclude(
                            eklid=eklid).exists():  # με το exclude παίρνω μόνο αυτούς που υπάρχουν και σε άλλες εκλογές
                        Psifoi.objects.filter(kenid__in=(Kentra.objects.filter(koinid=oldkoinid.koinid))).filter(
                            simbid=simbitem.simbid).delete()
                        Eklsimbkoin.objects.filter(eklid=eklid).filter(koinid=oldkoinid).filter(
                            simbid=simbitem.simbid).delete()
                        Eklsindsimb.objects.filter(eklid=eklid).filter(sindid=oldsindid).filter(
                            simbid=simbitem.simbid).delete()

                        # σβήνω εν τέλει και  "ορφανές" εγγραφές  από τον πίνακα simbouloi (που δεν έχουν δηλαδή αντίστοιχη εγγραφή στον πίνακα EKLSINDSIMB
                        Simbouloi.objects.exclude(simbid__in=(Eklsindsimb.objects.all()).values_list('simbid')).delete()
                    else:
                        Simbouloi.objects.filter(simbid=simbitem.simbid.simbid).delete()

            else:
                #αλλιώς αν ο συνδυασμόσ υπάρχει μόνο σ' αυτήν την εκλ. αναμέτρηση:

                # ι) Αν ο σύμβουλος του πρώην συνδυασμού υπάρχει σε άλλες εκλ. αναμετρήσεις, σβήσε μόνο τα απαραίτητα στους σχετικούς πίνακες του συμβούλου, αλλιώς
                # σβήσε και το σύμβουλο (μέσω του cascade Θα σβήσουν και όλα τα σχετικά). Αυτό γίνεται για κάθε σύμβουλο του πρωην συνδυασμού
                for simbitem in EklallsimbVw.objects.filter(eklid=eklid).filter(toposeklogisid=oldkoinid.koinid).filter(
                        sindid=oldsindid.sindid):
                    if Eklsindsimb.objects.filter(simbid=simbitem.simbid).exclude(
                            eklid=eklid).exists():  # με το exclude παίρνω μόνο αυτούς που υπάρχουν και σε άλλες εκλογές
                        Psifoi.objects.filter(kenid__in=(Kentra.objects.filter(koinid=oldkoinid.koinid))).filter(
                            simbid=simbitem.simbid).delete()
                        Eklsimbkoin.objects.filter(eklid=eklid).filter(koinid=oldkoinid).filter(
                            simbid=simbitem.simbid).delete()
                        Eklsindsimb.objects.filter(eklid=eklid).filter(sindid=oldsindid).filter(
                            simbid=simbitem.simbid).delete()

                        # σβήνω εν τέλει και  "ορφανές" εγγραφές  από τον πίνακα simbouloi (που δεν έχουν δηλαδή αντίστοιχη εγγραφή στον πίνακα EKLSINDSIMB
                        Simbouloi.objects.exclude(simbid__in=(Eklsindsimb.objects.all()).values_list('simbid')).delete()
                    else:
                        Simbouloi.objects.filter(simbid=simbitem.simbid.simbid).delete()
                # ιι) σβήσε και το συνδυασμό (μέσω του cascade Θα σβήσουν και όλα τα σχετικά(EKLSINDKOIN, EKLSINDSIMB, PSIFODELTIA))
                Sindiasmoi.objects.filter(sindid=oldsindid.sindid).delete()




        messages.success(request, "Η διαγραφή ολοκληρώθηκε")
        return redirect('eklsindkoin_list', eklid)
    context = {'selected_ekloges': selected_ekloges.eklid,
               'all_ekloges': all_ekloges,
               'object': obj
               }

    return render(request, 'Elections/confirm_sindiasmoi_delete.html', context)

def koinotites_list(request, eklid):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.view_koinotites'):
        raise PermissionDenied

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    all_koinotites=Koinotites.objects.filter(koinid__in=Eklperkoin.objects.filter(eklid=eklid).values_list('koinid'))

    context = {'all_ekloges': all_ekloges,
               'selected_ekloges': selected_ekloges.eklid,
               'all_koinotites':all_koinotites
               }

    return render(request, 'Elections/koinotites_list.html' , context)

def koinotites_add(request, eklid):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.add_koinotites'):
        raise PermissionDenied

    action_label = 'Κοινότητες - Νέα εγγραφή'

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    if request.method == 'POST':    #όταν γίνει POST των δεδομένων στη βάση
        form = KoinotitesForm(eklid, request.POST)
        if form.is_valid():
            koinotita_item = form.save(commit=False)
            koinotita_item.save()

            #print(form.cleaned_data['perid'])
            #print(form.cleaned_data['edrid'])
            #return
            #Εισαγωγή εγγραφής και στον Eklperkoin

            Eklperkoin.objects.create(eklid=Eklogestbl.objects.get(eklid=eklid),
                                   perid=form.cleaned_data['perid'],
                                   koinid=koinotita_item,
                                   edrid=form.cleaned_data['edrid']
                                   ).save()

            messages.success(request, 'Η εγγραφή ολοκληρώθηκε!')
            form = KoinotitesForm(eklid)
    else:
        form=KoinotitesForm(eklid)  #όταν ανοίγει η φόρμα για καταχώριση δεδομένων

    context = {
                'selected_ekloges': selected_ekloges.eklid,
                'action_label' : action_label,
                'all_ekloges': all_ekloges,
                'form': form
               }

    return render(request, 'Elections/koinotita_form.html', context)

def koinotites_edit(request, eklid, koinid):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.change_koinotites'):
        raise PermissionDenied

    action_label = 'Κοινότητες - Αλλαγή εγγραφής'

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    #επιλογή της συγκεκριμένης κοινότητας
    item=get_object_or_404(Koinotites, koinid=koinid)

    #παίρνω per_id, edr_id από τον Eklperkoin
    eklperkoin_item = Eklperkoin.objects.get(eklid=eklid, koinid=item.koinid)
    per_id_item = eklperkoin_item.perid
    edr_id_item = eklperkoin_item.edrid

    if request.method == 'POST':
        form = KoinotitesForm(eklid, request.POST or None, instance=item)
        if form.is_valid():
            item=form.save(commit=False)
            item.save()

            #ενημέρωση και του πίνακα Eklperkoin για τα πεδία perid, edrid
            Eklperkoin.objects.filter(eklid=eklid, koinid=koinid).update(perid=form.cleaned_data['perid'], edrid=form.cleaned_data['edrid'])
            return redirect('koinotites_list', eklid)

    else:
        # αν δεν γίνει POST φέρνω τα πεδία του μοντέλου καθως και τα extra πεδία  manually
        #print(per_id_item)
        form = KoinotitesForm(eklid, request.POST or None, instance=item, initial={'edrid':edr_id_item, 'perid': per_id_item })

    context = {
        'selected_ekloges': selected_ekloges.eklid,
        'action_label': action_label,
        'all_ekloges': all_ekloges,
        'form': form,
    }

    return render(request, 'Elections/koinotita_form.html', context)

def koinotites_delete(request, eklid, koinid ):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.delete_koinotites'):
        raise PermissionDenied

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    obj=get_object_or_404(Koinotites, koinid=koinid)

    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Η διαγραφή ολοκληρώθηκε")
        return redirect('koinotites_list', eklid)
    context={'selected_ekloges': selected_ekloges.eklid,
             'all_ekloges': all_ekloges,
             'object':obj
             }

    return render(request, 'Elections/confirm_delete.html', context)


def kentra_list(request, eklid):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.view_kentra'):
        raise PermissionDenied

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    all_kentra=Kentra.objects.filter(eklid=eklid).prefetch_related('eklid','perid','koinid')

    context = {'all_ekloges': all_ekloges,
               'selected_ekloges': selected_ekloges.eklid,
               'all_kentra':all_kentra
               }

    return render(request, 'Elections/kentra_list.html' , context)

def kentra_add(request, eklid):
    selected_ekloges = Eklogestbl.objects.prefetch_related('eklsind_set','eklsimbper_set', 'eklsimbkoin_set').get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.add_kentra'):
        raise PermissionDenied

    action_label = 'Εκλ. Κέντρα - Νέα εγγραφή'

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    if request.method == 'POST':    #όταν γίνει POST των δεδομένων στη βάση
        form = KentraForm(eklid, request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()

            # Δημιουργία εγγραφών στον πίνακα Psifodeltia για κάθε Καθολικό συνδυασμό της τρέχουσας εκλ. αναμέτρησης
            for rec in selected_ekloges.eklsind_set.all():
                Psifodeltia.objects.create(kenid=item,
                                           sindid=rec.sindid,
                                           votesa=0,
                                           votesb=0,
                                           votesk=0
                                           ).save()

            # Δημιουργία εγγραφών στον πίνακα Psifoi για κάθε δημοτικό σύμβουλο της τρέχουσας εκλ. αναμέτρησης
            for rec in selected_ekloges.eklsimbper_set.all():
                Psifoi.objects.create(kenid=item,
                                      simbid=rec.simbid,
                                      votes=0
                                      ).save()
            # Δημιουργία εγγραφών στον πίνακα Psifoi για κάθε τοπικό σύμβουλο της Κοινότητας στην οποία ανήκει το εκλ. κέντρο
            for rec in selected_ekloges.eklsimbkoin_set.filter(koinid=item.koinid):
                Psifoi.objects.create(kenid=item,
                                      simbid=rec.simbid,
                                      votes=0
                                      ).save()

            messages.success(request, 'Η εγγραφή ολοκληρώθηκε!')
            form = KentraForm(eklid, initial={'eklid':Eklogestbl.objects.get(eklid=eklid)})
    else:
        form=KentraForm(eklid, initial={'eklid':Eklogestbl.objects.get(eklid=eklid)})  #όταν ανοίγει η φόρμα για καταχώριση δεδομένων

    context = {
                'selected_ekloges': selected_ekloges.eklid,
                'action_label' : action_label,
                'all_ekloges': all_ekloges,
                'form': form
               }

    return render(request, 'Elections/kentra_form.html', context)

def kentra_edit(request, eklid, kenid):
    selected_ekloges = Eklogestbl.objects.prefetch_related('eklsimbkoin_set').get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.change_kentra'):
        raise PermissionDenied


    action_label = 'Κέντρα - Αλλαγή εγγραφής'

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    #επιλογή του συγκεκριμένου κέντρου
    item=get_object_or_404(Kentra, kenid=kenid)

    #παίρνω per_id, koin_id από τον Eklperkoin
    eklperkoin_item = Eklperkoin.objects.get(eklid=eklid, koinid=item.koinid)
    per_id_item = eklperkoin_item.perid
    koin_id_item = eklperkoin_item.koinid

    if request.method == 'POST':
        form = KentraForm(eklid, request.POST or None, instance=item)
        if form.is_valid():
            item=form.save(commit=False)
            item.save()

            #Αν αλλάξει η κοινότητα του κέντρου...
            if koin_id_item != form.cleaned_data['koinid']:
                #Διαγραφή ψήφων για τοπικούς συμβούλους της πρώην Κοινότητας
                Psifoi.objects.filter(kenid=kenid).filter(simbid__in=selected_ekloges.eklsimbkoin_set.filter(koinid=koin_id_item).values_list('simbid')).delete()

                # Δημιουργία εγγραφών στον πίνακα Psifoi για κάθε τοπικό σύμβουλο της Κοινότητας στην οποία ανήκει πλέον το εκλ. κέντρο
                for rec in selected_ekloges.eklsimbkoin_set.filter(koinid=item.koinid):
                    Psifoi.objects.create(kenid=item,
                                          simbid=rec.simbid,
                                          votes=0
                                          ).save()
            return redirect('kentra_list', eklid)
    else:
        # αν δεν γίνει POST φέρνω τα πεδία του μοντέλου καθως και τα extra πεδία  manually
        form = KentraForm(eklid, request.POST or None, instance=item, initial={'koinid':koin_id_item, 'perid': per_id_item })

    context = {
        'selected_ekloges': selected_ekloges.eklid,
        'action_label': action_label,
        'all_ekloges': all_ekloges,
        'form': form,
    }

    return render(request, 'Elections/kentra_form.html', context)

def kentra_delete(request, eklid, kenid ):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.delete_kentra'):
        raise PermissionDenied

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    obj=get_object_or_404(Kentra, kenid=kenid)

    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Η διαγραφή ολοκληρώθηκε")
        return redirect('kentra_list', eklid)
    context={'selected_ekloges': selected_ekloges.eklid,
             'all_ekloges': all_ekloges,
             'object':obj
             }

    return render(request, 'Elections/confirm_delete.html', context)

def psifodeltia_list(request, eklid):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.view_psifodeltia'):
        raise PermissionDenied

    paramstr = request.GET.get('kentraoption', '')

    try:
        paramstr = int(paramstr)
    except:
        paramstr = Kentra.objects.filter(eklid=eklid).first().kenid  # default kenid  αν δεν δοθεί


    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    all_kentra=Kentra.objects.filter(eklid=eklid).order_by('descr')

    selected_kentro = Kentra.objects.get(kenid=paramstr).kenid

    #all_psifodeltia=Psifodeltia.objects.filter(kenid__in=Kentra.objects.filter(eklid=eklid).values_list('kenid')).order_by('kenid','-votesa')
    #all_psifodeltia = Psifodeltia.objects.filter(kenid=paramstr).filter(sindid__sindid__in=(Eklsind.objects.filter(eklid=eklid).values_list('sindid'))).order_by('-votesa')
    all_psifodeltia = EklSumpsifodeltiasindKenVw.objects.filter(kenid=paramstr).filter(sindid__sindid__in=(Eklsind.objects.filter(eklid=eklid).values_list('sindid'))).order_by('-votes')


    context = {'all_ekloges': all_ekloges,
               'selected_ekloges': selected_ekloges.eklid,
               'all_psifodeltia':all_psifodeltia,
               'all_kentra':all_kentra,
               'selected_kentro':selected_kentro
               }

    return render(request, 'Elections/psifodeltia_list.html' , context)

def psifodeltia_add(request, eklid):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.add_psifodeltia'):
        raise PermissionDenied

    action_label = 'Ψηφοδέλτια Συνδυασμού σε εκλ. κέντρο - Νέα εγγραφή'

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    if request.method == 'POST':    #όταν γίνει POST των δεδομένων στη βάση
        form = PsifodeltiaForm(eklid, request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            messages.success(request, 'Η εγγραφή ολοκληρώθηκε!')
            form = PsifodeltiaForm(eklid, initial={'eklid':Eklogestbl.objects.get(eklid=eklid)})
    else:
        form=PsifodeltiaForm(eklid, initial={'eklid':Eklogestbl.objects.get(eklid=eklid)})  #όταν ανοίγει η φόρμα για καταχώριση δεδομένων

    context = {
                'selected_ekloges': selected_ekloges.eklid,
                'action_label' : action_label,
                'all_ekloges': all_ekloges,
                'form': form
               }

    return render(request, 'Elections/psifodeltia_form.html', context)

def psifodeltia_edit(request, eklid, sindid, kenid):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.change_psifodeltia'):
        raise PermissionDenied


    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    #επιλογή της συγκεκριμένης εγγραφής
    item=get_object_or_404(Psifodeltia, sindid=sindid, kenid=kenid)

    action_label = 'Ψηφοδέλτια Συνδυασμού στο εκλ. κέντρο ' + item.kenid.descr + ' - Αλλαγή εγγραφής'

    if request.method == 'POST':
        form = PsifodeltiaForm(eklid, request.POST or None, instance=item)
        if form.is_valid():
            item=form.save(commit=False)
            item.save()
            messages.success(request, 'Η εγγραφή αποθηκεύτηκε!')
            return redirect('psifodeltia_list', eklid)
    else:
        # αν δεν γίνει POST φέρνω τα πεδία του μοντέλου
        #form = PsifodeltiaForm(eklid, request.POST or None, instance=item, initial={'sindid':sind_id_item, 'kenid': ken_id_item })
        form = PsifodeltiaForm(eklid, request.POST or None, instance=item)

    context = {
        'selected_ekloges': selected_ekloges.eklid,
        'action_label': action_label,
        'all_ekloges': all_ekloges,
        'form': form,
    }

    return render(request, 'Elections/psifodeltia_form.html', context)

def psifodeltia_delete(request, eklid,  sindid, kenid ):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.delete_psifodeltia'):
        raise PermissionDenied

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    obj=get_object_or_404(Psifodeltia,  sindid=sindid, kenid=kenid)

    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Η διαγραφή ολοκληρώθηκε")
        return redirect('psifodeltia_list', eklid)
    context={'selected_ekloges': selected_ekloges.eklid,
             'all_ekloges': all_ekloges,
             'object':obj
             }

    return render(request, 'Elections/confirm_delete.html', context)

##############Ψηφοδέλτια Κοινοτήτων#######################

def psifodeltiakoin_list(request, eklid):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.view_psifodeltia'):
        raise PermissionDenied

    paramstr = request.GET.get('kentraoption', '')

    try:
        paramstr = int(paramstr)
    except:
        paramstr = Kentra.objects.filter(eklid=eklid).first().kenid  # default kenid  αν δεν δοθεί


    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    all_kentra=Kentra.objects.filter(eklid=eklid).order_by('descr')

    selected_kentro = Kentra.objects.get(kenid=paramstr).kenid

    #all_psifodeltia=Psifodeltia.objects.filter(kenid__in=Kentra.objects.filter(eklid=eklid).values_list('kenid')).order_by('kenid','-votesa')
    all_psifodeltia = Psifodeltia.objects.filter(kenid=paramstr).filter(sindid__sindid__in=(Eklsindkoin.objects.filter(eklid=eklid, koinid__koinid__in=(Kentra.objects.filter(kenid=paramstr).values_list('koinid'))).values_list('sindid'))).order_by('-votesk')

    context = {'all_ekloges': all_ekloges,
               'selected_ekloges': selected_ekloges.eklid,
               'all_psifodeltia':all_psifodeltia,
               'all_kentra':all_kentra,
               'selected_kentro':selected_kentro
               }

    return render(request, 'Elections/psifodeltiakoin_list.html' , context)

''' Δεν δίνω δυνατότητα add γιατί δημιουργείται εγγραφή στα Psifodeltia κατά την δημιουργία του συνδυασμού.
def psifodeltiakoin_add(request, eklid):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.add_psifodeltia'):
        raise PermissionDenied

    action_label = 'Ψηφοδέλτια Συνδυασμού σε εκλ. κέντρο - Νέα εγγραφή'

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    if request.method == 'POST':    #όταν γίνει POST των δεδομένων στη βάση
        form = PsifodeltiaKoinForm(eklid, request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            messages.success(request, 'Η εγγραφή ολοκληρώθηκε!')
            form = PsifodeltiaKoinForm(eklid, initial={'eklid':Eklogestbl.objects.get(eklid=eklid)})
    else:
        form=PsifodeltiaKoinForm(eklid, initial={'eklid':Eklogestbl.objects.get(eklid=eklid)})  #όταν ανοίγει η φόρμα για καταχώριση δεδομένων

    context = {
                'selected_ekloges': selected_ekloges.eklid,
                'action_label' : action_label,
                'all_ekloges': all_ekloges,
                'form': form
               }

    return render(request, 'Elections/psifodeltia_form.html', context)
'''

def psifodeltiakoin_edit(request, eklid, id):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.change_psifodeltia'):
        raise PermissionDenied


    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    #επιλογή της συγκεκριμένης εγγραφής
    item=get_object_or_404(Psifodeltia, id=id)

    action_label = 'Ψηφοδέλτια Συνδυασμού στο εκλ. κέντρο ' + item.kenid.descr + ' - Αλλαγή εγγραφής'

    if request.method == 'POST':
        form = PsifodeltiaKoinForm(eklid, request.POST or None, instance=item)
        if form.is_valid():
            item=form.save(commit=False)
            item.save()
            messages.success(request, 'Η εγγραφή αποθηκεύτηκε!')
            return redirect('psifodeltiakoin_list', eklid)
    else:
        # αν δεν γίνει POST φέρνω τα πεδία του μοντέλου
        #form = PsifodeltiaForm(eklid, request.POST or None, instance=item, initial={'sindid':sind_id_item, 'kenid': ken_id_item })
        form = PsifodeltiaKoinForm(eklid, request.POST or None, instance=item)

    context = {
        'selected_ekloges': selected_ekloges.eklid,
        'action_label': action_label,
        'all_ekloges': all_ekloges,
        'form': form,
    }

    return render(request, 'Elections/psifodeltia_form.html', context)

def psifodeltiakoin_delete(request, eklid, id ):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.delete_psifodeltia'):
        raise PermissionDenied

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    obj=get_object_or_404(Psifodeltia, id=id)

    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Η διαγραφή ολοκληρώθηκε")
        return redirect('psifodeltia_list', eklid)
    context={'selected_ekloges': selected_ekloges.eklid,
             'all_ekloges': all_ekloges,
             'object':obj
             }

    return render(request, 'Elections/confirm_delete.html', context)

def simbouloi_list(request, eklid):

    paramorder = request.GET.get('orderoption', '')
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')
    try:
        paramorder = int(paramorder)
    except:
        paramorder = 6  # default ταξινόμηση

    #selected_ekloges = Eklogestbl.objects.get(eklid=eklid).prefetch_related('eklallsimbvw_set')

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    selected_ekloges = Eklogestbl.objects.prefetch_related('eklallsimbvw_set').get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.view_simbouloi'):
        raise PermissionDenied

    all_simbouloi = selected_ekloges.eklallsimbvw_set.all().values_list('simbid', 'surname', 'firstname', 'fathername', 'toposeklogis', 'sindiasmosnew')

    if paramorder==1 or paramorder==6:
        all_simbouloi = all_simbouloi.order_by('surname', 'firstname','fathername')
    elif paramorder == 2:
        all_simbouloi = all_simbouloi.order_by('sindiasmosnew', 'surname', 'firstname','fathername')
    elif paramorder == 3:
        all_simbouloi = all_simbouloi.order_by('sindiasmosnew', 'toposeklogis', 'surname', 'firstname','fathername')
    elif paramorder == 4:
        all_simbouloi = all_simbouloi.order_by( 'toposeklogis','sindiasmosnew','surname', 'firstname','fathername')
    else:
        all_simbouloi = all_simbouloi.order_by('toposeklogis', 'surname','firstname', 'fathername')

    context = {'all_ekloges': all_ekloges,
               'selected_ekloges': selected_ekloges.eklid,
               'all_simbouloi': all_simbouloi,
               }

    return render(request, 'Elections/simbouloi_list.html', context)

def simbouloi_insert_records(form, simb_item, eklid):
    # Προσθήκη εγγραφής και στον πίνακα Eklsindsimb για τη σύνδεση του Υποψηφίου με το Συνδυασμό του
    Eklsindsimb.objects.create(eklid=Eklogestbl.objects.get(eklid=eklid),
                               sindid=form.cleaned_data['sindid'],
                               simbid=simb_item,
                               aa=form.cleaned_data['aa']
                               ).save()

    # Εισάγω και μια νέα εγγραφή στον πίνακα Eklsimbper αν είναι Δημοτικός
    # Αν δεν είναι Δημοτικός, κρύβω στο template το πεδίο Κοινότητσ
    if form.cleaned_data['eidos'] == '1':
        # Προσθήκη εγγραφής και στον πίνακα Eklsimbper, αν είναι Δημοτικός
        Eklsimbper.objects.create(eklid=Eklogestbl.objects.get(eklid=eklid),
                                  simbid=simb_item,
                                  perid=form.cleaned_data['perid']
                                  ).save()

        # Εισαγωγή εγγραφής υποψηφίου στον πίνακα Psifoi με votes=0 για κάθε κέντρο της
        # εκλ. αναμέτρησης, αφού ο δημοτικός σύμβουλος ψηφίζεται σε ΟΛΟ ΤΟ ΔΗΜΟ
        for kentro in Kentra.objects.filter(eklid=Eklogestbl.objects.get(eklid=eklid)):
            Psifoi.objects.create(
                simbid=simb_item,
                kenid=kentro,
                votes=0
            ).save()
    else:
        # Διαφορετικά προσθήκη εγγραφής και στον πίνακα Eklsimbkoin, αν είναι Τοπικός
        Eklsimbkoin.objects.create(eklid=Eklogestbl.objects.get(eklid=eklid),
                                   simbid=simb_item,
                                   koinid=form.cleaned_data['koinid']
                                   ).save()

        # Εισαγωγή εγγραφής υποψηφίου στον πίνακα Psifoi με votes=0 για κάθε κέντρο ΤΗΣ ΚΟΙΝΟΤΗΤΑΣ,
        # αφού ο ΤΟΠΙΚΟΣ σύμβουλος ψηφίζεται μόνο στην ΚΟΙΝΟΤΗΤΑ όπου είναι υποψήφιος
        for kentro in Kentra.objects.filter(koinid=form.cleaned_data['koinid']):
            Psifoi.objects.create(
                simbid=simb_item,
                kenid=kentro,
                votes=0
            ).save()


def simbouloi_add(request, eklid):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.add_simbouloia'):
        raise PermissionDenied


    action_label = 'Υποψήφιοι Σύμβουλοι - Νέα εγγραφή'

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    if request.method == 'POST':    #όταν γίνει POST των δεδομένων στη βάση
        form = SimbouloiForm(eklid, request.POST)

        #if all([form.is_valid(), sub_form.is_valid()]):
        if form.is_valid():
            #ΠΡΟΣΟΧΗ!!! Αν πρόκειται για καθαρα νέο υποψήφιο, άρα το hidden είναι κενό, κάνω save κανονικά..
            if form.cleaned_data['hiddenid'] is None:
                simb_item = form.save(commit=False)
                simb_item.save()
            else:
                #αλλιώς αν επιλέξω υποψήφιο από άλλη εκλογική αναμέτρηση, δεν τον δημιουργώ αλλά τον παίρνω από τον πίνακα Simbouloi
                simb_item=Simbouloi.objects.get(simbid=form.cleaned_data['hiddenid'])

            eklid=Eklogestbl.objects.get(eklid=eklid).eklid
            #κλήση της παρακάτω συνάρτησης για την εισαγωγή στοιχείων και σε άλλους εξαρτώμενους πίνακες (Eklsindsimb, Eklsimbper, Eklsimbkoin, Psifoi
            simbouloi_insert_records(form, simb_item, eklid)

            messages.success(request, 'Η εγγραφή ολοκληρώθηκε!' )
            return redirect('simbouloi_add', eklid)
        else:
            return HttpResponse('Σφάλμα καταχώρησης στο πεδίο: ' + form.errors)

    else:
        # όταν ανοίγει η φόρμα για καταχώριση δεδομένων
        form=SimbouloiForm(eklid, initial={'aa': 0, 'koinid':None})
       # sub_form = EklsindFormPartial()

    context = {
                'selected_ekloges': selected_ekloges.eklid,
                'action_label' : action_label,
                'all_ekloges': all_ekloges,
                'form': form,
                #'sub_form': sub_form,
               }

    return render(request, 'Elections/simbouloi_form.html', context)


def simbouloi_edit(request, eklid, simbid):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))


    if not request.user.has_perm('Elections.change_simbouloi'):
        raise PermissionDenied


    action_label = 'Υποψήφιοι Σύμβουλοι - Αλλαγή εγγραφής'

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')


    simb_item = get_object_or_404(Simbouloi, simbid=simbid)

    #ΠΡΟΣΟΧΗ!!! Τα extra πεδία  τα φορτώνω manually
    try:
        aa_field = Eklsindsimb.objects.get(simbid=simbid, eklid=eklid).aa
    except:
        aa_field=0

    sindid_field = Eklsindsimb.objects.get(simbid=simbid, eklid=eklid).sindid

    if Eklsimbper.objects.filter(simbid=simbid, eklid=eklid).exists():
        perid_field = Eklsimbper.objects.get(simbid=simbid, eklid=eklid).perid
        koinid_field = None
        eidos_field = 1
    else:
        perid_field = Eklperkoin.objects.get(koinid=(Eklsimbkoin.objects.get(simbid=simbid, eklid=eklid).koinid)).perid
        koinid_field = Eklperkoin.objects.get(koinid=(Eklsimbkoin.objects.get(simbid=simbid, eklid=eklid).koinid)).koinid
        eidos_field = 0


    if request.method == 'POST':
        form = SimbouloiForm(eklid, request.POST or None, instance=simb_item)
        if form.is_valid():

            # ΠΡΟΣΟΧΗ!!! Αν πρόκειται για τον αρχικό υποψήφιο που κάναμε edit, άρα το hidden είναι κενό, κάνω save κανονικά..

            if form.cleaned_data['hiddenid'] is None:
                simb_item = form.save(commit=False)
                simb_item.save()

                Eklsindsimb.objects.filter(eklid=eklid).filter(simbid=simbid).update(aa=form.cleaned_data['aa'], sindid=form.cleaned_data['sindid'])

                #Αν είναι Δημοτικός...
                if form.cleaned_data['eidos'] == '1':
                    #αν είναι ήδη Δημοτικός, κάνω απλά update του perid
                    if eidos_field == 1:
                        Eklsimbper.objects.filter(eklid=eklid).filter(simbid=simbid).update(perid=form.cleaned_data['perid'])

                    #ΠΡΟΣΟΧΗ ΟΜΩΣ..αν από Τοπικός έγινε Δημοτικός τότε απαιτούνται 3 ενέργειες
                    else:
                        # 1) Προσθήκη εγγραφής και στον πίνακα Eklsimbper, αν είναι Δημοτικός
                        Eklsimbper.objects.create(eklid=Eklogestbl.objects.get(eklid=eklid),
                                                  simbid=simb_item,
                                                  perid=form.cleaned_data['perid']
                                                  ).save()

                        # 2) Διαγραφή Υποψηφίου από Eklsimbkoin
                        Eklsimbkoin.objects.filter(eklid=eklid).filter(simbid=simbid).delete()

                        # 3) Διαγραφή ψήφων από πίνακα Psifoi και συγκεκριμένα όλες τις εγγραφές που έχουν τον υποψήφιο σε κέντρο της τρέχουσας εκλ. αναμέτρησης
                        Psifoi.objects.filter(simbid=simbid).filter(kenid__in=Kentra.objects.filter(eklid=eklid).values_list('kenid')).delete()

                        # 4) Εισαγωγή εγγραφής υποψηφίου στον πίνακα Psifoi με votes=0 για κάθε κέντρο της τρέχουσας
                        # εκλ. αναμέτρησης, αφού ο δημοτικός σύμβουλος ψηφίζεται σε ΟΛΟ ΤΟ ΔΗΜΟ
                        for kentro in Kentra.objects.filter(eklid=eklid):
                            Psifoi.objects.create(
                                simbid=simb_item,
                                kenid=kentro,
                                votes=0
                            ).save()

                #Αν είναι Τοπικός..
                else:
                    if eidos_field == 0:
                        # αν είναι ήδη Τοπικός, ελέγχω/κάνω για 2 ενέργειες

                        # 1) απλό update του koinid
                        Eklsimbkoin.objects.filter(eklid=eklid).filter(simbid=simbid).update(koinid=form.cleaned_data['koinid'])

                        # 2) Αν αλλάξει μόνο το koinid...
                        if koinid_field != form.cleaned_data['koinid']:

                            # α) Διαγραφή ψήφων από πίνακα Psifoi και συγκεκριμένα όλες τις εγγραφές που έχουν τον υποψήφιο σε κέντρο της τρέχουσας εκλ. αναμέτρησης
                            Psifoi.objects.filter(simbid=simbid).filter(kenid__in=Kentra.objects.filter(eklid=eklid).values_list('kenid')).delete()

                            # β) Εισαγωγή εγγραφής υποψηφίου στον πίνακα Psifoi με votes=0 για κάθε κέντρο ΤΗΣ ΚΟΙΝΟΤΗΤΑΣ,
                            # αφού ο ΤΟΠΙΚΟΣ σύμβουλος ψηφίζεται μόνο στην ΚΟΙΝΟΤΗΤΑ όπου είναι υποψήφιος
                            for kentro in Kentra.objects.filter(koinid=form.cleaned_data['koinid']):
                                Psifoi.objects.create(
                                    simbid=simb_item,
                                    kenid=kentro,
                                    votes=0
                                ).save()

                    # ΠΡΟΣΟΧΗ ΟΜΩΣ..αν από Δημοτικός έγινε Τοπικός τότε απαιτούνται 4 ενέργειες
                    else:
                        # 1) προσθήκη εγγραφής και στον πίνακα Eklsimbkoin
                        Eklsimbkoin.objects.create(eklid=Eklogestbl.objects.get(eklid=eklid),
                                                   simbid=simb_item,
                                                   koinid=form.cleaned_data['koinid']
                                                   ).save()

                        # 2) Διαγραφή Υποψηφίου και από τον Eklsimbper
                        Eklsimbper.objects.filter(eklid=eklid).filter(simbid=simbid).delete()

                        # 3) Διαγραφή ψήφων από πίνακα Psifoi και συγκεκριμένα όλες τις εγγραφές που έχουν τον υποψήφιο σε κέντρο της τρέχουσας εκλ. αναμέτρησης
                        Psifoi.objects.filter(simbid=simbid).filter(kenid__in=Kentra.objects.filter(eklid=eklid).values_list('kenid')).delete()

                        # 4) Εισαγωγή εγγραφής υποψηφίου στον πίνακα Psifoi με votes=0 για κάθε κέντρο ΤΗΣ ΚΟΙΝΟΤΗΤΑΣ,
                        # αφού ο ΤΟΠΙΚΟΣ σύμβουλος ψηφίζεται μόνο στην ΚΟΙΝΟΤΗΤΑ όπου είναι υποψήφιος
                        for kentro in Kentra.objects.filter(koinid=form.cleaned_data['koinid']):
                            Psifoi.objects.create(
                                simbid=simb_item,
                                kenid=kentro,
                                votes=0
                            ).save()

                return redirect('simbouloi_list', eklid)

            #αλλιώς αν αντικατασταθεί από υποψήφιο παλιάς εκλ. αναμέτρησης
            else:
                eklid = Eklogestbl.objects.get(eklid=eklid).eklid

                simb_item = Simbouloi.objects.get(simbid=simbid)

                #παίρνω το νέο υποψήφιο...
                new_simb_item=Simbouloi.objects.get(simbid=form.cleaned_data['hiddenid'])
                # κλήση της παρακάτω συνάρτησης για την εισαγωγή στοιχείων και σε άλλους εξαρτώμενους πίνακες (Eklsindsimb, Eklsimbper, Eklsimbkoin, Psifoi)
                simbouloi_insert_records(form, new_simb_item, eklid)

                #ο προηγούμενος διαγράφεται ΜΟΝΟ από πίνακες Eklsindsimb, Eklsimbper, Eklsimbkoin, Psifoi της τρέχουσας εκλ. αναμέτρησης
                #αν βρεθεί σε παλιές εκλ. αναμετρήσεις
                if EklallsimbVw.objects.filter(simbid=simb_item.simbid).filter(eklid__lt=eklid).exists():
                    #Simbouloi.objects.filter(simbid=simb_item.simbid).delete()
                    Eklsindsimb.objects.filter(eklid=eklid).filter(simbid=simb_item.simbid).delete()
                    Eklsimbper.objects.filter(eklid=eklid).filter(simbid=simb_item.simbid).delete()
                    Eklsimbkoin.objects.filter(eklid=eklid).filter(simbid=simb_item.simbid).delete()
                    Psifoi.objects.filter(simbid=simb_item.simbid).filter(kenid__in=Kentra.objects.filter(eklid=eklid).values_list('kenid')).delete()
                #αλλιώς διαγράφεται από παντού, αφού υπάρχει μόνο στην τρέχουσα εκλ. αναμέτρηση (μέσω του cascade option)
                else:
                    Simbouloi.objects.filter(simbid=simb_item.simbid).delete()

                messages.success(request, 'Ο υποψήφιος αντικαταστάθηκε από άλλον (προηγούμενης εκλ. αναμέτρησης) !')
                return redirect('simbouloi_list', eklid)

    else:
        #αν δεν γίνει POST φέρνω τα πεδία του μοντέλου καθως και τα extra πεδία  manually
        if Eklsimbper.objects.filter(simbid=simbid, eklid=eklid).exists():
            form = SimbouloiForm(eklid, request.POST or None, instance=simb_item,
                              initial={'aa': aa_field,
                                       'perid':perid_field.perid,
                                       'koinid':None,
                                       'sindid':sindid_field.sindid,
                                       'eidos': eidos_field})
        else:
            if sindid_field is None: #για την περίπτωση υποψηφίων που δεν έχουν συνδυασμό, όπως στις κοινότητες<300 κατ.
                initialSindid=None
            else:
                initialSindid=sindid_field.sindid

            form = SimbouloiForm(eklid, request.POST or None, instance=simb_item,
                                 initial={'aa': aa_field,
                                          'perid': perid_field.perid,
                                          'koinid': koinid_field.koinid,
                                          'sindid': initialSindid,
                                          'eidos': eidos_field})

    context = {
        'selected_ekloges': selected_ekloges.eklid,
        'action_label': action_label,
        'all_ekloges': all_ekloges,
        'form': form,
    }

    return render(request, 'Elections/simbouloi_form.html', context)



def simbouloi_delete(request, eklid, simbid ):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))


    if not request.user.has_perm('Elections.delete_simbouloi'):
        raise PermissionDenied

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    obj = get_object_or_404(Simbouloi, simbid=simbid)

    flag_found_palia = -1
    #έλεγχος αν πρόκειται για υποψήφιο που συμμετείχε και σε άλλε΅ς εκλ. αναμετρήσεις
    if EklallsimbVw.objects.filter(simbid=obj.simbid).exclude(eklid=eklid).exists():
        flag_found_palia = 1
        # Simbouloi.objects.filter(simbid=simb_item.simbid).delete()
    else:
        flag_found_palia = 0

    if request.method == 'POST':
        # parent_obj_url=obj.content_object.get_absolute_url()
        if flag_found_palia == 1:
            Eklsindsimb.objects.filter(eklid=eklid).filter(simbid=obj.simbid).delete()
            Eklsimbper.objects.filter(eklid=eklid).filter(simbid=obj.simbid).delete()
            Eklsimbkoin.objects.filter(eklid=eklid).filter(simbid=obj.simbid).delete()
            Psifoi.objects.filter(simbid=obj.simbid).filter(kenid__in=Kentra.objects.filter(eklid=eklid).values_list('kenid')).delete()
            #obj.delete()
        else:
            # αλλιώς διαγράφεται από παντού, αφού υπάρχει μόνο στην τρέχουσα εκλ. αναμέτρηση (μέσω του cascade option)
            Simbouloi.objects.filter(simbid=obj.simbid).delete()

        messages.success(request, "Η διαγραφή ολοκληρώθηκε")
        return redirect('simbouloi_list', eklid)



    context = {'selected_ekloges': selected_ekloges.eklid,
               'all_ekloges': all_ekloges,
               'object': obj,
               'flag_found_palia' : flag_found_palia,
               }


    return render(request, 'Elections/confirm_simbouloi_delete.html', context)



##Αυτό το view φορτώνει με τη βοήθεια Ajax σε dropdown μόνο τα koinid που σχετίζονται με ένα perid
def load_koinotites(request, eklid):
    #selected_ekloges = Eklogestbl.objects.get(eklid=eklid)
    #all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    perid = request.GET.get('perid')
    koinotites = Koinotites.objects.filter(koinid__in=Eklperkoin.objects.filter(eklid=eklid).filter(perid=perid).values_list('koinid')).order_by('descr')
    #sindiasmoi = Sindiasmoi.objects.filter(sindid__in=(Eklsind.objects.filter(eklid=eklid).values_list('sindid')))
    return render(request, 'Elections/koinotites_dropdown_list_options.html', {'koinotites': koinotites})

##Αυτό το view φορτώνει με τη βοήθεια Ajax σε dropdown μόνο τα sindid που σχετίζονται με ένα koinid
def load_sindiasmoi(request, eklid):
    #selected_ekloges = Eklogestbl.objects.get(eklid=eklid)
    #all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')


    koinid = request.GET.get('koinid')
    if koinid != '':
        q = Q(sindid__in=Eklsind.objects.filter(eklid=eklid).values_list('sindid')) | Q(sindid__in=Eklsindkoin.objects.filter(eklid=eklid).filter(koinid=koinid).values_list('sindid'))
    else:
        q = Q(sindid__in=Eklsind.objects.filter(eklid=eklid).values_list('sindid'))

    sindiasmoi = Sindiasmoi.objects.filter(q).order_by('descr')

    return render(request, 'Elections/sindiasmoi_dropdown_list_options.html', {'sindiasmoi': sindiasmoi})

#Αυτό το view φορτώνει με τη βοήθεια Ajax σε dropdown μόνο τα είδη κοινοτήτων που σχετίζονται με το εκλ. σύστημα
def load_koineidos(request):
    eklid = request.GET.get('eklid')

    #Αν είναι Καλλικρατικό σύστημα..
    if Eklogestbl.objects.get(eklid=eklid).sisid.sisid == 1:
        eidh = Typeofkoinotita.objects.filter(tpkid__lte=2)
    else:
        eidh = Typeofkoinotita.objects.filter(tpkid__gt=2)

    context = {
        'eidh': eidh
    }

    return render(request, 'Elections/koineidos_dropdown_list_options.html', context)

def load_simbouloi(request, eklid):

    surname = request.GET.get('surname')
    firstname = request.GET.get('firstname')
    fathername = request.GET.get('fathername')

    #Ψάχνω σε άλλε΅ς εκλ. αναμετρήσεις υποψήφιο με ίδιο surname, firstname, fathername και δεν έχουν εισαχθεί ακόμη στην τρέχουσα εκλ. αναμέτρηση
    simbouloi = EklallsimbVw.objects.exclude(eklid=eklid). \
        filter(surname__icontains=surname).filter(firstname__icontains=firstname). \
        filter(fathername__icontains=fathername). \
        exclude(simbid__in=Eklsindsimb.objects.filter(eklid=eklid).values_list('simbid',flat=True)). \
        order_by('surname', 'firstname', 'fathername')
        #simbouloi = Simbouloi.objects.filter(surname__icontains=surname).filter(firstname__icontains=firstname)

    context = {
        'simbouloi': simbouloi
    }

    return render(request, 'Elections/simbouloi_found.html', context)

def update_psifoi(request):

    votes= int(request.GET.get('votes',''))
    simbid= int(request.GET.get('simbid',''))
    kenid= int(request.GET.get('kenid',''))

    #Psifoi.objects.filter(kenid=kenid, simbid=simbid).update(votes=votes)
    ps=Psifoi.objects.get(kenid=kenid, simbid=simbid)
    ps.votes=votes
    ps.save()
    return HttpResponse('')



def psifoi_list(request, eklid, kenid=None):

    selected_ekloges = Eklogestbl.objects.prefetch_related('eklpsifoisimbvw_set').get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))


    if not request.user.has_perm('Elections.view_psifoi'):
        raise PermissionDenied

    paramorder = request.GET.get('orderoption', '')

    try:
        paramorder = int(paramorder)
    except:
        paramorder = 5  # default ταξινόμηση


    paramstr = request.GET.get('kentraoption', '')

    try:
        paramstr = int(paramstr)
    except:
        if kenid is not None:
            paramstr = kenid
        else:
            paramstr = selected_ekloges.kentra_set.all().first().kenid  #Kentra.objects.filter(eklid=eklid).first().kenid  # default kenid  αν δεν δοθεί



    all_psifoi = selected_ekloges.eklpsifoisimbvw_set.filter(kenid=paramstr).values_list('simbid', 'surname', 'firstname', 'fathername', 'sindiasmos', 'shortsind', 'simbaa', 'eidos', 'kenid', 'votes', 'koinotita')


    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    #all_kentra=Kentra.objects.filter(eklid=eklid).order_by('descr')
    all_kentra = selected_ekloges.kentra_set.all().values_list('kenid', 'descr', 'koinid').order_by('descr')
    #all_kentra = Kentra.objects.filter(eklid=eklid)

    if paramorder==1 or paramorder==5:
        all_psifoi = all_psifoi.order_by('surname', 'firstname','fathername')
    elif paramorder == 2:
        all_psifoi = all_psifoi.order_by('shortsind', 'surname', 'firstname','fathername')
    elif paramorder == 3:
        all_psifoi = all_psifoi.order_by('shortsind', 'eidos', 'surname', 'firstname','fathername')
    else:
        all_psifoi = all_psifoi.order_by('-votes')

    selected_kentro = selected_ekloges.kentra_set.get(kenid=paramstr)
    #all_psifodeltia=Psifodeltia.objects.filter(kenid__in=Kentra.objects.filter(eklid=eklid).values_list('kenid')).order_by('kenid','-votesa')
    #all_psifoi = Psifoi.objects.filter(kenid=paramstr).order_by('simbid__surname')

    context = {'all_ekloges': all_ekloges,
               'selected_ekloges': selected_ekloges.eklid,
               'all_psifoi':all_psifoi,
               'all_kentra':all_kentra,
               'selected_kentro' : selected_kentro,
               }

    return render(request, 'Elections/psifoi_list.html' , context)


def psifoi_add(request, eklid):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))


    if not request.user.has_perm('Elections.add_psifoi'):
        raise PermissionDenied

    action_label = 'Ψήφοι υποψηφίου σε εκλ. κέντρο - Νέα εγγραφή'

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    if request.method == 'POST':    #όταν γίνει POST των δεδομένων στη βάση
        form = PsifoiForm(eklid, request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            messages.success(request, 'Η εγγραφή ολοκληρώθηκε!')
            form = PsifoiForm(eklid, initial={'eklid':Eklogestbl.objects.get(eklid=eklid)})
    else:
        form=PsifoiForm(eklid, initial={'eklid':Eklogestbl.objects.get(eklid=eklid)})  #όταν ανοίγει η φόρμα για καταχώριση δεδομένων

    context = {
                'selected_ekloges': selected_ekloges.eklid,
                'action_label' : action_label,
                'all_ekloges': all_ekloges,
                'form': form
               }

    return render(request, 'Elections/psifoi_form.html', context)

def psifoi_edit(request, eklid, simbid, kenid):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))


    if not request.user.has_perm('Elections.change_psifoi'):
        raise PermissionDenied

    action_label = 'Ψήφοι υποψηφίου σε εκλ. κέντρο - Αλλαγή εγγραφής'

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    #επιλογή της συγκεκριμένης εγγραφής
    simb_item=get_object_or_404(Psifoi, simbid=simbid, kenid=kenid)

    selected_kentro = kenid

    if request.method == 'POST':
        form = PsifoiForm(eklid, request.POST or None, instance=simb_item)
        if form.is_valid():
            item=form.save(commit=False)
            item.save()
            messages.success(request, 'Η εγγραφή αποθηκεύτηκε!')
            return redirect('psifoi_list', eklid, kenid)
    else:
        # αν δεν γίνει POST φέρνω τα πεδία του μοντέλου
        #form = PsifodeltiaForm(eklid, request.POST or None, instance=item, initial={'sindid':sind_id_item, 'kenid': ken_id_item })
        form = PsifoiForm(eklid, request.POST or None, instance=simb_item)

    context = {
        'selected_ekloges': selected_ekloges.eklid,
        'selected_kentro' : selected_kentro,
        'action_label': action_label,
        'all_ekloges': all_ekloges,
        'form': form,
    }

    return render(request, 'Elections/psifoi_form.html', context)



def psifoi_delete(request, eklid, simbid, kenid ):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))


    if not request.user.has_perm('Elections.delete_psifoi'):
        raise PermissionDenied

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    obj=get_object_or_404(Psifoi, simbid=simbid, kenid=kenid)

    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Η διαγραφή ολοκληρώθηκε")
        return redirect('psifoi_list', eklid)
    context={'selected_ekloges': selected_ekloges.eklid,
             'all_ekloges': all_ekloges,
             'object':obj
             }

    return render(request, 'Elections/confirm_delete.html', context)

def edit_psifoi_kentrou(request,eklid, kenid):

    action_label='Καταχώρηση ψήφων Υποψηφίων Συμβούλων'
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')
    selected_ekloges = Eklogestbl.objects.prefetch_related('kentra_set','eklsindsimb_set').get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))


    if not request.user.has_perm('Elections.change_psifoi'):
        raise PermissionDenied

    selected_kentro = Kentra.objects.prefetch_related('psifoi_set').get(kenid=kenid)

    PsifoiFormSet = modelformset_factory(Psifoi, fields =('simbid', 'votes', 'kenid',), extra=0)

    data = request.POST or None
    formset = PsifoiFormSet(data=data, queryset= selected_kentro.psifoi_set.filter(kenid=kenid).order_by('simbid__surname' ))
    for form in formset:
        form.fields['kenid'].queryset = selected_ekloges.kentra_set.filter(kenid=form['kenid'].value()) #Kentra.objects.filter(kenid=form['kenid'].value())
        form.fields['simbid'].queryset = Simbouloi.objects.filter(simbid=form['simbid'].value())  #Simbouloi.objects.filter(simbid=form['simbid'].value()) Τα dropdown θα έχουν μόνο το σχετικό simbid

    if request.method == 'POST' and formset.is_valid():
        formset.save()
        messages.success(request, 'Οι αλλαγές αποθηκεύτηκαν!')
        return HttpResponseRedirect('/' + str(eklid) + '?eklogesoption=' + str(eklid) + '&eklkentrooption=' + str(selected_kentro.descr))
    #στο serres.gr θα βάλω: return HttpResponseRedirect('/ekloges/'+str(eklid)+ '?eklogesoption=' +str(eklid)+ '&eklkentrooption='+str(selected_kentro.descr))

    context = {'selected_ekloges': selected_ekloges.eklid,
                'selected_kentro':selected_kentro,
               'all_ekloges': all_ekloges,
               'action_label':action_label,
               'formset': formset
               }

    return render(request, 'Elections/psifoi_formset.html', context)

def edit_psifoi_kentrou2(request,eklid, kenid):

    action_label='Καταχώρηση ψήφων Υποψηφίων Συμβούλων'
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')
    selected_ekloges = Eklogestbl.objects.prefetch_related('kentra_set','eklsindsimb_set', 'eklpsifoisimbvw_set').get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))

    if not request.user.has_perm('Elections.change_psifoi'):
        raise PermissionDenied

    paramorder = request.GET.get('orderoption', '')

    try:
        paramorder = int(paramorder)
    except:
        paramorder = 1  # default ταξινόμηση

    selected_kentro = Kentra.objects.prefetch_related('psifoi_set').get(kenid=kenid)

    all_psifoi=selected_ekloges.eklpsifoisimbvw_set.filter(kenid=kenid).values_list('simbid', 'surname', 'firstname', 'fathername', 'sindiasmosnew', 'shortdescrnew', 'sindaa','eidos', 'simbaa', 'toposeklogis', 'votes', 'kenid', 'koinotita', 'id', 'kenid__perid__descr')
    if paramorder==1 or paramorder==5:
        all_psifoi = all_psifoi.order_by('sindiasmosnew', 'eidos', 'toposeklogis', 'surname', 'firstname')
    elif paramorder == 2:
        all_psifoi = all_psifoi.order_by('sindiasmosnew', 'eidos', 'surname', 'firstname')
    elif paramorder == 3:
        all_psifoi = all_psifoi.order_by('eidos', 'surname', 'firstname')
    else:
        all_psifoi = all_psifoi.order_by('surname', 'firstname')

    ####


    ####



    #form.fields['kenid'].queryset = selected_ekloges.kentra_set.filter(kenid=form['kenid'].value()) #Kentra.objects.filter(kenid=form['kenid'].value())
    #form.fields['simbid'].queryset = Simbouloi.objects.filter(simbid=form['simbid'].value())  #Simbouloi.objects.filter(simbid=form['simbid'].value()) Τα dropdown θα έχουν μόνο το σχετικό simbid

    #if request.method == 'POST' and formset.is_valid():
     #   formset.save()
    #    messages.success(request, 'Οι αλλαγές αποθηκεύτηκαν!')
    #    return HttpResponseRedirect('/' + str(eklid) + '?eklogesoption=' + str(eklid) + '&eklkentrooption=' + str(selected_kentro.descr))

    context = {'selected_ekloges': selected_ekloges.eklid,
                'selected_kentro':selected_kentro,
               'all_ekloges': all_ekloges,
               'action_label':action_label,
               'all_psifoi': all_psifoi
               }

    return render(request, 'Elections/psifoi_formset2.html', context)


def edit_psifodeltia_kentrou(request,eklid, kenid):

    action_label='Καταχώρηση ψηφοδελτίων Υποψηφίων Συνδυασμών για το Δημοτικό Συμβούλιο'
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')
    selected_ekloges = Eklogestbl.objects.prefetch_related('kentra_set','eklsind_set').get(eklid=eklid)
    all_eklsind = selected_ekloges.eklsind_set.all().order_by('descr')

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))


    if not request.user.has_perm('Elections.change_psifodeltia'):
        raise PermissionDenied

    selected_kentro = Kentra.objects.prefetch_related('psifodeltia_set').get(kenid=kenid)

    #PsifodeltiaFormSet = modelformset_factory(Psifodeltia, fields =('sindid', 'votesa', 'votesb', 'votesk','kenid',), extra=0)
    PsifodeltiaFormSet = modelformset_factory(Psifodeltia, fields=('sindid', 'votesa', 'votesb', 'kenid',),
                                              extra=0)

    data = request.POST or None
    #προσοχή: φιλτράρω μόνο τους Καθολικούς συνδυασμούς!
    formset = PsifodeltiaFormSet(data=data, queryset= selected_kentro.psifodeltia_set.filter(kenid=kenid).filter(sindid__sindid__in=(Eklsind.objects.filter(eklid=eklid).values_list('sindid'))).order_by('-sindid__eidos', 'sindid__sindid'  ))
    for form in formset:
        form.fields['kenid'].queryset = selected_ekloges.kentra_set.filter(kenid=form['kenid'].value()) #Kentra.objects.filter(kenid=form['kenid'].value())
        form.fields['sindid'].queryset = Sindiasmoi.objects.filter(sindid=form['sindid'].value())  # Τα dropdown θα έχουν μόνο το σχετικό sindid

    #for form in formset:
    #    form.fields['kenid'].disabled = True

    if request.method == 'POST' and formset.is_valid():
        formset.save()
        messages.success(request, 'Οι αλλαγές αποθηκεύτηκαν!')
        return HttpResponseRedirect('/'+str(eklid)+ '?eklogesoption=' +str(eklid)+ '&eklkentrooption='+str(selected_kentro.descr))
    #στο serres.gr θα βάλω: return HttpResponseRedirect('/ekloges/'+str(eklid)+ '?eklogesoption=' +str(eklid)+ '&eklkentrooption='+str(selected_kentro.descr))

    context = {'selected_ekloges': selected_ekloges.eklid,
                'selected_kentro':selected_kentro,
               'all_ekloges': all_ekloges,
               'action_label':action_label,
               'all_eklsind':all_eklsind,
               'formset': formset
               }

    return render(request, 'Elections/psifodeltia_formset.html', context)

def edit_psifodeltiakoin_kentrou(request,eklid, kenid):

    action_label='Καταχώρηση ψηφοδελτίων Υποψηφίων Συνδυασμών για το Τοπικό Συμβούλιο'
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')
    selected_ekloges = Eklogestbl.objects.prefetch_related('kentra_set','eklsindkoin_set').get(eklid=eklid)
    all_eklsindkoin = selected_ekloges.eklsindkoin_set.all().order_by('descr')

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))


    if not request.user.has_perm('Elections.change_psifodeltia'):
        raise PermissionDenied

    selected_kentro = Kentra.objects.prefetch_related('psifodeltia_set').get(kenid=kenid)

    #PsifodeltiaFormSet = modelformset_factory(Psifodeltia, fields =('sindid', 'votesa', 'votesb', 'votesk','kenid',), extra=0)

    PsifodeltiaKoinFormSet = modelformset_factory(Psifodeltia, fields=('sindid',  'votesk', 'kenid',), extra=0)

    data = request.POST or None

    # προσοχή: φιλτράρω  τους συνδυασμούς που έχουν εγγραφή στον πίνακα Eklsindkoin!
    koinid=selected_kentro.koinid
    formset = PsifodeltiaKoinFormSet(data=data, queryset= selected_kentro.psifodeltia_set.filter(kenid=kenid).filter(sindid__sindid__in=(Eklsindkoin.objects.filter(eklid=eklid).filter(koinid=koinid).values_list('sindid'))).order_by('-sindid__eidos', 'sindid__descr'  ))
    for form in formset:
        form.fields['kenid'].queryset = selected_ekloges.kentra_set.filter(kenid=form['kenid'].value()) #Kentra.objects.filter(kenid=form['kenid'].value())
        form.fields['sindid'].queryset = Sindiasmoi.objects.filter(sindid=form['sindid'].value())  #Simbouloi.objects.filter(simbid=form['simbid'].value()) Τα dropdown θα έχουν μόνο το σχετικό simbid

    if request.method == 'POST' and formset.is_valid():
        formset.save()
        messages.success(request, 'Οι αλλαγές αποθηκεύτηκαν!')
        return HttpResponseRedirect('/'+str(eklid)+ '?eklogesoption=' +str(eklid)+ '&eklkentrooption='+str(selected_kentro.descr))
    #στο serres.gr θα βάλω: return HttpResponseRedirect('/ekloges/'+str(eklid)+ '?eklogesoption=' +str(eklid)+ '&eklkentrooption='+str(selected_kentro.descr))

    context = {'selected_ekloges': selected_ekloges.eklid,
                'selected_kentro':selected_kentro,
               'all_ekloges': all_ekloges,
               'action_label':action_label,
               'all_eklsindkoin' : all_eklsindkoin,
               'formset': formset
               }

    return render(request, 'Elections/psifodeltiakoin_formset.html', context)


def login_user(request, eklid):

    selected_ekloges = Eklogestbl.objects.prefetch_related('kentra_set').get(eklid=eklid)

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('Elections_list')
        else:
            messages.error(request, 'Ανύπαρκτος χρήστης!')

    context = {'selected_ekloges': selected_ekloges.eklid,
               'all_ekloges': all_ekloges,
               }

    return render(request, 'Elections/login.html',context)

def logout_user(request, eklid):

    selected_ekloges = Eklogestbl.objects.prefetch_related('kentra_set').get(eklid=eklid)

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    logout(request)

    context = {'selected_ekloges': selected_ekloges.eklid,
               'all_ekloges': all_ekloges,
               }

    return render(request, 'Elections/login.html',context)

def eklsind_for_viewers(request, eklid):
    selected_ekloges = Eklogestbl.objects.prefetch_related('eklsind_set').get(eklid=eklid)

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    all_eklsind = selected_ekloges.eklsind_set.all().order_by('-edresa_teliko')
    all_pososta = EklSumpsifodeltiasindVw.objects.filter(eklid=eklid, eidos=1).order_by('-posostosindiasmou')

    context = {'all_ekloges': all_ekloges,
               'selected_ekloges': selected_ekloges.eklid,
               'all_eklsind': all_eklsind,
               'all_pososta': all_pososta ,
               }

    return render(request, 'Elections/eklsind_for_viewers.html' , context)

def eklsindkoin_for_viewers(request, eklid):

    selected_ekloges = Eklogestbl.objects.prefetch_related('eklsumpsifodeltiasindkoinvw_set', 'eklsindkoin_set').get(eklid=eklid)

    paramstr = request.GET.get('koinotitaoption', '')

    try:
        paramstr = int(paramstr)
    except:
        p = selected_ekloges.eklsumpsifodeltiasindkoinvw_set.all()
        paramstr = p[0].koinid  # default koinid θα είναι το πρώτο της λίστας αν δεν δοθεί κάτι

    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    # φιλτράρισμα επιλεγμένου κέντρου
    selected_koinotita = Koinotites.objects.get(koinid=paramstr).koinid


    # ανάκτηση όλων των κέντρων της εκλ. αναμέτρησης
    if selected_ekloges.sisid.sisid == 1:
        all_koinotites = Koinotites.objects.filter(eidos__lte=2)
    else:
        all_koinotites = Koinotites.objects.filter(eidos=4)

    ######

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    katametrimena_koinotites = EklKatametrimenaPsifoiKoinotitesOnlyVw.objects.get(eklid=eklid).katametrimena_koinotites
    all_pososta = EklSumpsifodeltiasindVw.objects.filter(eklid=eklid).order_by('-posostosindiasmou')


    all_eklsindkoin = selected_ekloges.eklsindkoin_set.filter(koinid=paramstr).order_by('-edresk_teliko')


    flagDraw = 0
    for item in all_eklsindkoin:
        if item.checkfordraw == -1:
            flagDraw = 1

    context = {'all_ekloges': all_ekloges,
               'selected_ekloges': selected_ekloges.eklid,
               'all_eklsindkoin': all_eklsindkoin,
               'all_pososta' : all_pososta,
               'selected_koinotita' :  selected_koinotita,
               'all_koinotites' : all_koinotites,
               'katametrimena_koinotites' : katametrimena_koinotites,
               'flagDraw' : flagDraw

               }

    return render(request, 'Elections/eklsindkoin_for_viewers.html' , context)

'''ΚΑΤΑΝΟΜΗ ΕΔΡΩΝ Α ΚΥΡΙΑΚΗΣ ΓΙΑ ΔΗΜΟ'''
def exec_edres_katanomiA_dimos(request, eklid):
    '''settings.DATABASES['HOST']'''
    selected_ekloges = Eklogestbl.objects.prefetch_related('eklsind_set').get(eklid=eklid)

    mySQL_conn = mysql.connector.connect(host= settings.DATABASES['default']['HOST'],
                                         database=settings.DATABASES['default']['NAME'],
                                         user=settings.DATABASES['default']['USER'],
                                         password=settings.DATABASES['default']['PASSWORD'],)


    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')
    all_eklsind = selected_ekloges.eklsind_set.all().order_by('-edresa_teliko')
    all_pososta = EklSumpsifodeltiasindVw.objects.filter(eklid=eklid, eidos=1).order_by('-posostosindiasmou')
    curTime = datetime.datetime.now()

    context = {'all_ekloges': all_ekloges,
               'selected_ekloges': selected_ekloges.eklid,
               'all_eklsind': all_eklsind,
               'all_pososta': all_pososta,
               'curTime': curTime,
               }

    try:
        cursor = mySQL_conn.cursor()
        message=0
        args=[eklid,message]
        if selected_ekloges.sisid.sisid == 1:
            result=cursor.callproc('KATANOMH_EDRWN_A_KYRIAKHS_SISTIMA_1', args)
        else:
            result=cursor.callproc('KATANOMH_EDRWN_APLH_ANALOGIKH_SISTIMA_2', args)

        mySQL_conn.commit()

        # print out User details
        #for result in cursor.stored_results():
            #print(result.fetchall())

        #cursor.execute('SELECT @message')
        print(result[1]) #Το αποτέλεσμα της output variable message της stored procedure

        if result[1] == 1:
            msg='Επιτυχής ενημέρωση!'
        else:
            msg = 'Επιτυχής ενημέρωση, αλλά προέκυψε περίπτωση ισοψηφίας ή ίσων αχρ. υπολοίπων! Θα πρέπει να διενεργηθεί κλήρωση από το Πρωτοδικείο!'

        messages.success(request, msg)
        return redirect('eklsind_for_viewers', eklid)

    except mysql.connector.Error as error:
        print("Σφάλμα κατά την εκτέλεση της διαδικασίας! {}".format(error))
        messages.error(request, 'Σφάλμα κατά την εκτέλεση της διαδικασίας!'.format(error))
    finally:
        # closing database connection.
        if (mySQL_conn.is_connected()):
            cursor.close()
            mySQL_conn.close()
            print("connection is closed")

    return render(request, 'Elections/eklsind_for_viewers.html', context)

'''ΚΑΤΑΝΟΜΗ ΕΔΡΩΝ Β ΚΥΡΙΑΚΗΣ ΓΙΑ ΔΗΜΟ - ΑΦΟΡΑ ΜΟΝΟ ΤΟ ΠΑΛΙΟ ΣΥΣΤΗΜΑ ΤΟΥ ΚΑΛΛΙΚΡΑΤΗ'''
def exec_edres_katanomiB_dimos(request, eklid):
    '''settings.DATABASES['HOST']'''
    selected_ekloges = Eklogestbl.objects.prefetch_related('eklsind_set').get(eklid=eklid)

    mySQL_conn = mysql.connector.connect(host= settings.DATABASES['default']['HOST'],
                                         database=settings.DATABASES['default']['NAME'],
                                         user=settings.DATABASES['default']['USER'],
                                         password=settings.DATABASES['default']['PASSWORD'],)


    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')
    all_eklsind = selected_ekloges.eklsind_set.all().order_by('-edresa')
    all_pososta = EklSumpsifodeltiasindVw.objects.filter(eklid=eklid, eidos=1).order_by('-posostosindiasmoub')

    context = {'all_ekloges': all_ekloges,
               'selected_ekloges': selected_ekloges.eklid,
               'all_eklsind': all_eklsind,
               'all_pososta': all_pososta,
               }

    try:
        cursor = mySQL_conn.cursor()
        message=0
        args=[eklid,message]
        if selected_ekloges.sisid.sisid == 1:
            result=cursor.callproc('KATANOMH_EDRWN_B_KYRIAKHS_SISTIMA_1', args)
            mySQL_conn.commit()
            print(result[1])  # Το αποτέλεσμα της output variable message της stored procedure
            if result[1] == 1:
                msg = 'Επιτυχής ενημέρωση!'
            else:
                msg = 'Επιτυχής ενημέρωση, αλλά προέκυψε περίπτωση ισοψηφίας ή ίσων αχρ. υπολοίπων! Θα πρέπει να διενεργηθεί κλήρωση από το Πρωτοδικείο!'

            messages.success(request, msg)
            return redirect('eklsind_for_viewers', eklid)
        else:
            messages.info(request, 'Δεν γίνεται κατανομή εδρών την Β Κυριακή στην επιλεγμένη εκλ. αναμέτρηση!')


        # print out User details
        #for result in cursor.stored_results():
            #print(result.fetchall())

        #cursor.execute('SELECT @message')


    except mysql.connector.Error as error:
        print("Σφάλμα κατά την εκτέλεση της διαδικασίας! {}".format(error))
        messages.error(request, 'Σφάλμα κατά την εκτέλεση της διαδικασίας!'.format(error))
    finally:
        # closing database connection.
        if (mySQL_conn.is_connected()):
            cursor.close()
            mySQL_conn.close()
            print("connection is closed")

    return render(request, 'Elections/eklsind_for_viewers.html', context)

'''ΚΑΤΑΝΟΜΗ ΕΔΡΩΝ ΓΙΑ ΚΟΙΝΟΤΗΤΕΣ - ΑΦΟΡΑ ΜΟΝΟ ΤΟ ΝΕΟ ΣΥΣΤΗΜΑ ΤΟΥ ΚΛΕΙΣΘΕΝΗ'''
def exec_edres_katanomi_koinotites(request, eklid):

    mySQL_conn = mysql.connector.connect(host= settings.DATABASES['default']['HOST'],
                                         database=settings.DATABASES['default']['NAME'],
                                         user=settings.DATABASES['default']['USER'],
                                         password=settings.DATABASES['default']['PASSWORD'],)

    selected_ekloges = Eklogestbl.objects.prefetch_related('eklsumpsifodeltiasindkoinvw_set', 'eklsindkoin_set').get(eklid=eklid)

    paramstr = request.GET.get('koinotitaoption', '')

    try:
        paramstr = int(paramstr)
    except:
        p = selected_ekloges.eklsumpsifodeltiasindkoinvw_set.all()
        paramstr = p[0].koinid  # default koinid θα είναι το πρώτο της λίστας αν δεν δοθεί κάτι

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    # φιλτράρισμα επιλεγμένου κέντρου
    selected_koinotita = Koinotites.objects.get(koinid=paramstr).koinid

    # ανάκτηση όλων των κέντρων της εκλ. αναμέτρησης
    if selected_ekloges.sisid.sisid == 1:
        all_koinotites = Koinotites.objects.filter(eidos__lte=2)
    else:
        all_koinotites = Koinotites.objects.filter(eidos=4)

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    all_eklsindkoin = selected_ekloges.eklsindkoin_set.filter(koinid=paramstr).order_by('-edresk_teliko')
    all_pososta = EklSumpsifodeltiasindVw.objects.filter(eklid=eklid).values_list('katametrimenak',
                                                                                  'plithoskentrwn',
                                                                                  'posostokatametrimenwnkentrwnk').distinct()

    context = {'all_ekloges': all_ekloges,
               'selected_ekloges': selected_ekloges.eklid,
               'all_eklsindkoin': all_eklsindkoin,
               'all_pososta': all_pososta,
               'selected_koinotita': selected_koinotita,
               'all_koinotites': all_koinotites,
               }

    try:
        cursor = mySQL_conn.cursor()
        message=0
        args=[eklid]
        if selected_ekloges.sisid.sisid == 2:
            result=cursor.callproc('KATANOMH_EDRWN_SE_OLES_TIS_KOINOTITES', args)
            mySQL_conn.commit()
            all_isopalies = selected_ekloges.eklsindkoin_set.filter(checkfordraw=-1).values('koinid', 'checkfordraw').distinct().order_by('koinid__descr')
            #print(result[1])  # Το αποτέλεσμα της output variable message της stored procedure
            #if result[1] == 1:
            #    msg = 'Επιτυχής ενημέρωση!'
            #else:
            #    msg = 'Επιτυχής ενημέρωση, αλλά προέκυψε περίπτωση ισοψηφίας ή ίσων αχρ. υπολοίπων! Θα πρέπει να διενεργηθεί κλήρωση από το Πρωτοδικείο!'

            #έλεγχος για την περίπτωση Κοινοτήτων όπου υπάρχει ισοπαλία
            if all_isopalies.count == 0:
                messages.success(request, 'Επιτυχής ενημέρωση!')
            else:
                koinForKlirosi = ''

                for item in all_isopalies:
                    if koinForKlirosi == '':
                        koinForKlirosi = koinForKlirosi + Koinotites.objects.get(eklperkoin__koinid=item['koinid']).descr
                    else:
                        koinForKlirosi = koinForKlirosi + ', ' + Koinotites.objects.get(eklperkoin__koinid=item['koinid']).descr

                messages.success(request, 'Επιτυχής ενημέρωση! Ισοψηφίες ή ίδια αχρησιμοποίητα υπόλοιπα στις κοινότητες: ' + koinForKlirosi)
            return redirect('eklsindkoin_for_viewers', eklid)
        else:
            messages.info(request, 'Δεν γίνεται κατανομή εδρών στην επιλεγμένη εκλ. αναμέτρηση!')


        # print out User details
        #for result in cursor.stored_results():
            #print(result.fetchall())

        #cursor.execute('SELECT @message')


    except mysql.connector.Error as error:
        print("Σφάλμα κατά την εκτέλεση της διαδικασίας! {}".format(error))
        messages.error(request, 'Σφάλμα κατά την εκτέλεση της διαδικασίας!'.format(error))
    finally:
        # closing database connection.
        if (mySQL_conn.is_connected()):
            cursor.close()
            mySQL_conn.close()
            print("connection is closed")

    return render(request, 'Elections/eklsindkoin_for_viewers.html', context)