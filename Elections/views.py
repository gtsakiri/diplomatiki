import xlwt
from django.contrib import  messages
from django.contrib.auth import  authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from django.forms import DateInput, modelformset_factory
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, render_to_response

from .models import Eklogestbl, EklSumpsifodeltiasindVw, EklPosostasindPerVw, Perifereies, \
    EklSumpsifoisimbPerVw, EklSumpsifoisimbKoinVw, Koinotites, EklSumpsifodeltiasindKenVw, \
    Kentra, EklPsifoisimbVw, Edres, Sistima, Sindiasmoi, Eklsind, Eklper, Edreskoin, Typeofkoinotita, Eklperkoin, \
    Eklsindkoin, Psifodeltia, Simbouloi, EklSumpsifoisimbWithIdVw, Eklsimbper, Eklsindsimb, Eklsimbkoin, EklallsimbVw, \
    Psifoi, EklSumpsifoisimbVw, EklSumpsifodeltiasindKoinVw, EklSumpsifodeltiasindKoinVw
from .forms import EdresForm, SistimaForm, EklogestblForm, SindiasmoiForm, EklsindForm, PerifereiesForm, EdresKoinForm, \
    TypeofkoinotitaForm, KoinotitesForm, EklsindkoinForm, KentraForm, PsifodeltiaForm, SimbouloiForm, PsifoiForm
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

    firstrow = EklSumpsifodeltiasindVw.objects.filter(eklid=eklid).values_list('katametrimena', 'plithoskentrwn','posostokatametrimenwnkentrwn').distinct()
    # for col_num in range(len(firstrow[0])):
    ws.write(row_num, 0,'Στα ' + str(firstrow[0][0]) + ' από τα ' + str(firstrow[0][1]) + ' εκλ. κέντρα (Ποσοστό ' + str(firstrow[0][2]) + '%)', font_style)

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
        rows = EklSumpsifoisimbPerVw.objects.filter(eklid=eklid).values_list('sindiasmos', 'surname', 'firstname', 'fathername', 'toposeklogis', 'sumvotes').order_by('sindiasmos','-sumvotes')
    elif selected_order == 2:
        rows = EklSumpsifoisimbPerVw.objects.filter(eklid=eklid).values_list('sindiasmos', 'surname', 'firstname', 'fathername', 'toposeklogis', 'sumvotes').order_by('sindiasmos','surname')
    else:
        rows = EklSumpsifoisimbPerVw.objects.filter(eklid=eklid).values_list('sindiasmos', 'surname', 'firstname', 'fathername', 'toposeklogis', 'sumvotes').order_by('-sumvotes')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def export_psifoikoin_xls(request,eklid, selected_order):
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



    firstrow=EklSumpsifodeltiasindVw.objects.filter(eklid=eklid).values_list('katametrimena', 'plithoskentrwn','posostokatametrimenwnkentrwn').distinct()
    #for col_num in range(len(firstrow[0])):
    ws.write(row_num, 0, 'Στα ' + str(firstrow[0][0])+ ' από τα '+ str(firstrow[0][1]) + ' εκλ. κέντρα (Ποσοστό ' + str(firstrow[0][2])+'%)', font_style)

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
        rows = EklSumpsifoisimbKoinVw.objects.filter(eklid=eklid).values_list('sindiasmos', 'surname', 'firstname', 'fathername', 'toposeklogis', 'sumvotes').order_by('toposeklogis','sindiasmos','-sumvotes')
    elif selected_order == 2:
        rows = EklSumpsifoisimbKoinVw.objects.filter(eklid=eklid).values_list('sindiasmos', 'surname', 'firstname', 'fathername', 'toposeklogis', 'sumvotes').order_by('toposeklogis','sindiasmos','surname')
    elif selected_order == 3:
        rows = EklSumpsifoisimbKoinVw.objects.filter(eklid=eklid).values_list('sindiasmos', 'surname', 'firstname', 'fathername', 'toposeklogis', 'sumvotes').order_by('toposeklogis','-sumvotes')
    elif selected_order == 4:
        rows = EklSumpsifoisimbKoinVw.objects.filter(eklid=eklid).values_list('sindiasmos', 'surname', 'firstname', 'fathername', 'toposeklogis','sumvotes').order_by('toposeklogis', 'surname')
    else:
        rows = EklSumpsifoisimbKoinVw.objects.filter(eklid=eklid).values_list('sindiasmos', 'surname', 'firstname', 'fathername', 'toposeklogis', 'sumvotes').order_by('toposeklogis','-sumvotes')

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
        ws.write(row_num, 0, 'Ψηφοδέλτια συνδυασμών ανά εκλ. κέντρο - Α Κυριακή', font_style)
    elif sunday == 1:
        ws.write(row_num, 0, 'Ψηφοδέλτια συνδυασμών ανά εκλ. κέντρο - Β Κυριακή', font_style)
    else:
        ws.write(row_num, 0, 'Ψηφοδέλτια συνδυασμών ανά εκλ. κέντρο - Τοπικά Συμβούλια', font_style)

    row_num += 2

    if sunday == 1:
        firstrow = EklSumpsifodeltiasindVw.objects.filter(eklid=eklid).values_list('katametrimena', 'plithoskentrwn','posostokatametrimenwnkentrwn').distinct()
    elif sunday == 2:
        firstrow = EklSumpsifodeltiasindVw.objects.filter(eklid=eklid).values_list('katametrimenab', 'plithoskentrwn','posostokatametrimenwnkentrwnb').distinct()
    else:
        firstrow = EklSumpsifodeltiasindVw.objects.filter(eklid=eklid).values_list('katametrimenak', 'plithoskentrwn','posostokatametrimenwnkentrwnk').distinct()

    # for col_num in range(len(firstrow[0])):

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


    ws.write(row_num, 0,'Στα ' + str(katametrimena) + ' από τα ' + str(sinoloKentrwn) + ' εκλ. κέντρα (Ποσοστό ' + str(pososto_katametrimenwn) + '%)', font_style)

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
        rows = EklSumpsifodeltiasindKenVw.objects.filter(eklid=eklid).values_list('kentro', 'sindiasmos', 'votes')
    elif sunday == 2:
        rows = EklSumpsifodeltiasindKenVw.objects.filter(eklid=eklid).values_list('kentro', 'sindiasmos', 'votesb')
    else:
        rows = EklSumpsifodeltiasindKenVw.objects.filter(eklid=eklid).values_list('kentro', 'sindiasmos', 'votesk')


    #rows = EklSumpsifoisimbPerVw.objects.filter(eklid=eklid).values_list('sindiasmos', 'surname', 'firstname', 'fathername', 'toposeklogis', 'sumvotes')
    if selected_order == 1 or selected_order == 4:
        if sunday == 1:
            rows = rows.order_by('kentro','-votes')
        elif sunday == 2:
            rows = rows.order_by('kentro','-votesb')
        else:
            rows = rows.order_by('kentro','-votesk')


    elif selected_order == 2:
        rows = rows.order_by('kentro', 'sindiasmos')
    else:
        rows = rows.order_by('sindiasmos','kentro',)

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def export_psifodeltiasind_koin(request, eklid, selected_order):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="psifodeltiasind_koin.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('data')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.height = 280
    font_style.font.bold = True

    ws.write(row_num, 0, 'Ψηφοδέλτια συνδυασμών για την ανάδειξη Τοπικού Συμβουλίου ανά Κοινότητα', font_style)

    row_num += 2

    firstrow = EklSumpsifodeltiasindVw.objects.filter(eklid=eklid).values_list('katametrimenak', 'plithoskentrwn','posostokatametrimenwnkentrwnk').distinct()

    # for col_num in range(len(firstrow[0])):

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


    ws.write(row_num, 0,'Στα ' + str(katametrimena) + ' από τα ' + str(sinoloKentrwn) + ' εκλ. κέντρα (Ποσοστό ' + str(pososto_katametrimenwn) + '%)', font_style)

    font_style = xlwt.XFStyle()
    font_style.font.height = 240
    font_style.font.bold = True

    row_num += 2

    columns = ['Κοινότητα', 'Συνδυασμός', 'Ψηφοδέλτια',]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = EklSumpsifodeltiasindKoinVw.objects.filter(eklid=eklid).values_list('descr', 'sindiasmos', 'sumsindiasmou')


    #rows = EklSumpsifoisimbPerVw.objects.filter(eklid=eklid).values_list('sindiasmos', 'surname', 'firstname', 'fathername', 'toposeklogis', 'sumvotes')
    if selected_order == 1 or selected_order == 4:
        rows = rows.order_by('descr','-sumsindiasmou')
    elif selected_order == 2:
        rows = rows.order_by('descr', 'sindiasmos')
    else:
        rows = rows.order_by('sindiasmos','descr',)

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

    firstrow = EklSumpsifodeltiasindVw.objects.filter(eklid=eklid).values_list('katametrimena', 'plithoskentrwn','posostokatametrimenwnkentrwn').distinct()
    # for col_num in range(len(firstrow[0])):
    ws.write(row_num, 0,'Στα ' + str(firstrow[0][0]) + ' από τα ' + str(firstrow[0][1]) + ' εκλ. κέντρα (Ποσοστό ' + str(firstrow[0][2]) + '%)', font_style)

    font_style = xlwt.XFStyle()
    font_style.font.height = 240
    font_style.font.bold = True

    row_num += 2

    columns = ['Εκλ. Κέντρο', 'Επώνυμο', 'Όνομα', 'Όν. Πατρός', 'Είδος', 'Συνδυασμός', 'Ψήφοι']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    #rows = EklSumpsifoisimbPerVw.objects.filter(eklid=eklid).values_list('sindiasmos', 'surname', 'firstname', 'fathername', 'toposeklogis', 'sumvotes')
    if selected_order == 1 or selected_order == 6:
        rows = EklPsifoisimbVw.objects.filter(eklid=eklid).values_list('kentro', 'surname', 'firstname', 'fathername', 'eidos', 'sindiasmos', 'votes').order_by('kenid','sindiasmos', '-votes')
    elif selected_order == 2:
        rows = EklPsifoisimbVw.objects.filter(eklid=eklid).values_list('kentro', 'surname', 'firstname', 'fathername', 'eidos', 'sindiasmos', 'votes').order_by('kenid', 'sindiasmos','surname')
    elif selected_order == 3:
        rows = EklPsifoisimbVw.objects.filter(eklid=eklid).values_list('kentro', 'surname', 'firstname', 'fathername','eidos', 'sindiasmos', 'votes').order_by('kenid','surname')
    elif selected_order == 4:
        rows = EklPsifoisimbVw.objects.filter(eklid=eklid).values_list('kentro', 'surname', 'firstname', 'fathername','eidos', 'sindiasmos', 'votes').order_by('kenid','-votes')
    else:
        rows = EklPsifoisimbVw.objects.filter(eklid=eklid).values_list('kentro', 'surname', 'firstname', 'fathername', 'eidos', 'sindiasmos', 'votes').order_by('kenid','eidos','-votes')

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


def pososta_telika(request, eklid):

#ΠΟΣΟΣΤΑ ΣΥΝΔΥΑΣΜΩΝ ΣΕ ΟΛΟ ΤΟ ΔΗΜΟ

    # φιλτράρισμα επιλεγμένης εκλ. αναμέτρησης
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)
    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')
    #ανάκτηση εγγραφών επιλεγμένης εκλ. αναμέτρησης από το σχετικό database view (μόνο καθολικοί συνδυασμοί επιλέγονται)
    all_pososta = EklSumpsifodeltiasindVw.objects.filter(eklid=eklid, eidos=1).order_by('-posostosindiasmou')

    context = {'all_pososta':all_pososta, 'all_ekloges':all_ekloges, 'selected_ekloges':selected_ekloges.eklid}

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
    selected_perifereia = Perifereies.objects.filter(perid=paramstr)
    #ανάκτηση όλων των περιφερειών
    all_perifereies=Perifereies.objects.all()
    #ανάκτηση εγγραφών επιλεγμένης εκλ. αναμέτρησης από το σχετικό database view
    all_pososta = EklSumpsifodeltiasindVw.objects.filter(eklid=eklid).order_by('-posostosindiasmou')
    all_posostaper = EklPosostasindPerVw.objects.filter(eklid=eklid).filter(perid=paramstr)
    context = {'all_posostaper':all_posostaper,
                'all_pososta':all_pososta,
               'all_ekloges':all_ekloges,
               'selected_ekloges':selected_ekloges.eklid,
               'all_perifereies':all_perifereies,
               'selected_perifereia': selected_perifereia,}
    return render(request, 'Elections/pososta_perifereies.html',context)

def psifoisimb_perifereies(request, eklid):

# ΚΑΤΑΤΑΞΗ ΤΠΟΨΗΦΙΩΝ ΔΗΜ. ΣΥΜΒΟΥΛΩΝ

    paramstr = request.GET.get('perifereiaoption','')
    paramorder = request.GET.get('orderoption','')

    try:
        paramstr = int(paramstr)
    except:
        paramstr = 0 # default perid  αν δεν δοθεί


    try:
        paramorder = int(paramorder)
    except:
        paramorder = 4  # default ταξινόμηση

    #φιλτράρισμα επιλεγμένης εκλ. αναμέτρησης
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)
    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    # φιλτράρισμα επιλεγμένης περιφέρειας
    if paramstr == 0: #επιλογή: "ΑΝΕΞΑΡΤΗΤΟΥ ΕΚΛ. ΠΕΡΙΦΕΡΕΙΑΣ"
        selected_perifereia = 0
        all_psifoi = EklSumpsifoisimbWithIdVw.objects.filter(eklid=eklid).order_by('-sumvotes')  #retrieve Από το EklSumpsifoisimbWithIdVw
    else:
        selected_perifereia = Perifereies.objects.get(perid=paramstr).perid                      #retrieve Από το EklSumpsifoisimbPerVw
        all_psifoi = EklSumpsifoisimbPerVw.objects.filter(eklid=eklid).filter(toposeklogisid=paramstr)

    selected_order = paramorder

    #ανάκτηση όλων των περιφερειών
    all_perifereies=Perifereies.objects.all()
    #ανάκτηση εγγραφών επιλεγμένης εκλ. αναμέτρησης από το σχετικό database view
    #all_pososta = EklSumpsifodeltiasindVw.objects.filter(eklid=eklid).order_by('-posostosindiasmou')

    if paramorder==1:
        all_psifoi = all_psifoi.order_by('sindiasmos','-sumvotes')
    elif paramorder==2 :
        all_psifoi = all_psifoi.order_by('sindiasmos','surname')
    else:
        all_psifoi = all_psifoi.order_by('-sumvotes')

    context = {'all_psifoi':all_psifoi,
               # 'all_pososta':all_pososta,
               'all_ekloges':all_ekloges,
               'selected_ekloges':selected_ekloges.eklid,
               'all_perifereies':all_perifereies,
               'selected_perifereia': selected_perifereia,
               'selected_order':selected_order,}
    return render(request, 'Elections/psifoisimb_perifereies.html',context)


def psifoisimb_koinotites(request, eklid, eidoskoinotitas):

# ΚΑΤΑΤΑΞΗ ΤΠΟΨΗΦΙΩΝ ΣΥΜΒΟΥΛΩΝ ΚΟΙΝΟΤΗΤΩΝ

    paramstr = request.GET.get('koinotitaoption','')
    paramorder = request.GET.get('orderoption','')

    try:
        paramstr = int(paramstr)
    except:
        p = EklSumpsifoisimbKoinVw.objects.filter(eklid=eklid).filter(eidoskoinotitas=eidoskoinotitas).order_by('toposeklogisid')
        paramstr=p[0].toposeklogisid  # default toposeklogisid θα είναι ο πρώτος της λίστας αν δεν δοθεί κάτι

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

    #ανάκτηση όλων των κοινοτητων
    all_koinotites=Koinotites.objects.all().filter(eidos=eidoskoinotitas)
    #ανάκτηση εγγραφών επιλεγμένης εκλ. αναμέτρησης από το σχετικό database view
    all_pososta = EklSumpsifodeltiasindVw.objects.filter(eklid=eklid).order_by('-posostosindiasmou')

    if paramorder==1:
        all_psifoi = EklSumpsifoisimbKoinVw.objects.filter(toposeklogisid=paramstr).order_by('sindiasmos','-sumvotes')
    elif paramorder==2 :
        all_psifoi = EklSumpsifoisimbKoinVw.objects.filter(toposeklogisid=paramstr).order_by('sindiasmos','surname')
    elif paramorder==3:
        all_psifoi = EklSumpsifoisimbKoinVw.objects.filter(toposeklogisid=paramstr).order_by('-sumvotes')
    elif paramorder==4:
        all_psifoi = EklSumpsifoisimbKoinVw.objects.filter(toposeklogisid=paramstr).order_by('surname')
    else:
        all_psifoi = EklSumpsifoisimbKoinVw.objects.filter(toposeklogisid=paramstr).order_by('-sumvotes')

    context = {'all_psifoi':all_psifoi,
                'all_pososta':all_pososta,
               'all_ekloges':all_ekloges,
               'selected_ekloges':selected_ekloges.eklid,
               'all_koinotites':all_koinotites,
               'selected_koinotita': selected_koinotita,
               'selected_order':selected_order,
               'selected_menu':selected_menu,}
    return render(request, 'Elections/psifoisimb_koinotites.html',context)

def psifodeltiasindken(request, eklid, sunday):

# ΨΗΦΟΙ ΣΥΝΔΥΑΣΜΩΝ ΑΝΑ ΕΚΛ. ΚΕΝΤΡΟ
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

    selected_order = paramorder

    #ανάκτηση όλων των κέντρων της εκλ. αναμέτρησης
    all_kentra= selected_ekloges.kentra_set.all()
    #ανάκτηση εγγραφών επιλεγμένης εκλ. αναμέτρησης από το σχετικό database view
    all_pososta = selected_ekloges.eklsumpsifodeltiasindvw_set.all().order_by('-posostosindiasmou')

    if paramorder == 1 or paramorder == 4:
        #Α Κυριακή sunday=1, Β Κυριακή sunday=2, Εκλογές Κοινότητας sunday=3,
        if sunday == 1:
            all_psifodeltia = selected_ekloges.eklsumpsifodeltiasindkenvw_set.filter(kenid=paramstr).order_by('-votes')
        elif sunday == 2:
            all_psifodeltia = selected_ekloges.eklsumpsifodeltiasindkenvw_set.filter(kenid=paramstr).order_by('-votesb')
        else:
            all_psifodeltia = selected_ekloges.eklsumpsifodeltiasindkenvw_set.filter(kenid=paramstr).order_by('-votesk')
    elif paramorder == 2:
        all_psifodeltia = selected_ekloges.eklsumpsifodeltiasindkenvw_set.filter(kenid=paramstr).order_by('sindiasmos')
    else:
        all_psifodeltia = selected_ekloges.eklsumpsifodeltiasindkenvw_set.filter(kenid=paramstr).order_by('sindiasmos','kentro')


    context = {'all_psifodeltia':all_psifodeltia,
                'all_pososta':all_pososta,
               'sunday': sunday,
               'all_ekloges':all_ekloges,
               'selected_ekloges':selected_ekloges.eklid,
               'all_kentra':all_kentra,
               'selected_kentro': selected_kentro,
               'selected_order':selected_order,
               }
    return render(request, 'Elections/psifodeltiasind_ken.html',context)

def psifodeltiasindkoin(request, eklid):

# ΨΗΦΟΙ ΣΥΝΔΥΑΣΜΩΝ ΑΝΑ ΕΚΛ. ΚΕΝΤΡΟ
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
    all_koinotites= Koinotites.objects.filter(eidos=4)

    #ανάκτηση εγγραφών επιλεγμένης εκλ. αναμέτρησης από το σχετικό database view
    #all_pososta = selected_ekloges.eklsumpsifodeltiasindvw_set.all().order_by('-posostosindiasmou')

    if paramorder == 1 or paramorder == 4:
        all_psifodeltia = selected_ekloges.eklsumpsifodeltiasindkoinvw_set.filter(koinid=paramstr).order_by('-sumsindiasmou')
    elif paramorder == 2:
        all_psifodeltia = selected_ekloges.eklsumpsifodeltiasindkoinvw_set.filter(koinid=paramstr).order_by('sindiasmos')
    else:
        all_psifodeltia = selected_ekloges.eklsumpsifodeltiasindkoinvw_set.filter(koinid=paramstr).order_by('sindiasmos','descr')


    context = {'all_psifodeltia': all_psifodeltia,
               'all_ekloges': all_ekloges,
               'selected_ekloges': selected_ekloges.eklid,
               'all_koinotites': all_koinotites,
               'selected_koinotita': selected_koinotita,
               'selected_order':selected_order,
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
        paramstr=p[0].kenid.kenid  # default kenid θα είναι το πρώτο της λίστας αν δεν δοθεί κάτι

    try:
        paramorder = int(paramorder)
    except:
        paramorder = 4  # default ταξινόμηση


    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    # φιλτράρισμα επιλεγμένου κέντρου
    selected_kentro = selected_ekloges.kentra_set.get(kenid=paramstr).kenid

    selected_order = paramorder

    #ανάκτηση όλων των κέντρων της εκλ. αναμέτρησης
    all_kentra=Kentra.objects.filter(eklid=eklid)
    #ανάκτηση εγγραφών επιλεγμένης εκλ. αναμέτρησης από το σχετικό database view
    all_pososta = EklSumpsifodeltiasindVw.objects.filter(eklid=eklid).order_by('-posostosindiasmou')

    if paramorder==1 or paramorder==6:
        all_psifoi = EklPsifoisimbVw.objects.filter(kenid=paramstr).order_by('sindiasmos','-votes')
    elif paramorder == 2:
        all_psifoi = EklPsifoisimbVw.objects.filter(kenid=paramstr).order_by('sindiasmos','surname')
    elif paramorder == 3:
        all_psifoi = EklPsifoisimbVw.objects.filter(kenid=paramstr).order_by('surname')
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

            # Εισάγω και μια νέα εγγραφή στον πίνακα EKLSIND αν είναι καθολικός συνδυασμός
            #Αν δεν είναι καθολικός, κρύβω στο template και το ΑΑ
            if sind_item.eidos == 1:
                Eklsind.objects.create(eklid=Eklogestbl.objects.get(eklid=eklid),
                                       sindid=sind_item,
                                       aa = form.cleaned_data['aa'],
                                       edresa=0,
                                       edresa_ypol=0,
                                       edresa_teliko=0,
                                       edresb=0,
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

                # Εισαγωγή εγγραφής υποψηφίου στον πίνακα Psifoi με votes=0 για κάθε κέντρο ΤΗΣ ΚΟΙΝΟΤΗΤΑΣ,
                # αφού ο ΤΟΠΙΚΟΣ σύμβουλος ψηφίζεται μόνο στην ΚΟΙΝΟΤΗΤΑ όπου είναι υποψήφιος
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

            pic = form.cleaned_data['photo']
            if not pic:
                pic = 'sindiasmoi/elections.jpg'
                sind_item.photo=pic

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
                #1) Αν είναι ήδη Τοπικός Συνδυασμός, κάνω απλά Update τα πεδία aa, koinid, proedros στον Eklsind
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
        # parent_obj_url=obj.content_object.get_absolute_url()
        obj.delete()
        messages.success(request, "Η διαγραφή ολοκληρώθηκε")
        return redirect('sindiasmoi_list', eklid)
    context = {'selected_ekloges': selected_ekloges.eklid,
               'all_ekloges': all_ekloges,
               'object': obj
               }

    return render(request, 'Elections/confirm_delete.html', context)


def eklsind_list(request, eklid):
    selected_ekloges = Eklogestbl.objects.get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))


    if not request.user.has_perm('Elections.view_eklsind'):
        raise PermissionDenied

    #selected_ekloges = Eklogestbl.objects.prefetch_related('eklsind_set').get(eklid=eklid)

    #all_simbouloi = selected_ekloges.eklallsimbvw_set.all().values_list('simbid', 'surname', 'firstname', 'fathername','toposeklogis', 'sindiasmos')

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    all_eklsind = Eklsind.objects.filter(eklid=eklid)
    #all_eklsind = selected_ekloges.eklsind_set().all()

    context = {'all_ekloges': all_ekloges,
               'selected_ekloges': selected_ekloges.eklid,
               'all_eklsind': all_eklsind,
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
        form = EklsindForm(eklid, request.POST ) #ΠΡΟΣΟΧΗ! περνάω σαν παράμετρο το eklid, γιατί στη φόρμα γίνεται αρχικοποίηση με αυτή την παράμετρο
        if form.is_valid():
            sind_item = form.save(commit=False)
            sind_item.save()
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
    form = EklsindForm(0, request.POST or None,  instance=item)

    if form.is_valid():
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
        # parent_obj_url=obj.content_object.get_absolute_url()
        obj.delete()
        messages.success(request, "Η διαγραφή ολοκληρώθηκε")
        return redirect('eklsind_list', eklid)
    context = {'selected_ekloges': selected_ekloges.eklid,
               'all_ekloges': all_ekloges,
               'object': obj
               }

    return render(request, 'Elections/confirm_delete.html', context)


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

    all_eklsindkoin = selected_ekloges.eklsindkoin_set.all()

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
        form = EklsindkoinForm(eklid, request.POST ) #ΠΡΟΣΟΧΗ! περνάω σαν παράμετρο το eklid, γιατί στη φόρμα γίνεται αρχικοποίηση με αυτή την παράμετρο
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
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

    #περνάω παράμετρο eklid=0, για να μπορεί να εμφανίσει στο dropdown sindid το συνδυασμό
    #γιατί διαφορετικά το αποκλείει σύμφωνα με την αρχικοποίηση που κάνω στη φόρμα EklsindForm
    form = EklsindkoinForm(eklid, request.POST or None,  instance=item)

    if form.is_valid():
        form.save()

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
    if request.method == 'POST':
        # parent_obj_url=obj.content_object.get_absolute_url()
        obj.delete()
        messages.success(request, "Η διαγραφή ολοκληρώθηκε")
        return redirect('eklsindkoin_list', eklid)
    context = {'selected_ekloges': selected_ekloges.eklid,
               'all_ekloges': all_ekloges,
               'object': obj
               }

    return render(request, 'Elections/confirm_delete.html', context)

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
    all_psifodeltia = Psifodeltia.objects.filter(kenid=paramstr)

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

def psifodeltia_edit(request, eklid, id):
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

def psifodeltia_delete(request, eklid, id ):
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

    all_simbouloi = selected_ekloges.eklallsimbvw_set.all().values_list('simbid', 'surname', 'firstname', 'fathername', 'toposeklogis', 'sindiasmos')

    if paramorder==1 or paramorder==6:
        all_simbouloi = all_simbouloi.order_by('surname', 'firstname','fathername')
    elif paramorder == 2:
        all_simbouloi = all_simbouloi.order_by('sindiasmos', 'surname', 'firstname','fathername')
    elif paramorder == 3:
        all_simbouloi = all_simbouloi.order_by('sindiasmos', 'toposeklogis', 'surname', 'firstname','fathername')
    elif paramorder == 4:
        all_simbouloi = all_simbouloi.order_by( 'toposeklogis','sindiasmos','surname', 'firstname','fathername')
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
        # Διαφορετικά προσθήκη εγγραφής και στον πίνακα Eklsimbperkoin, αν είναι Τοπικός
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
                        # 1) προσθήκη εγγραφής και στον πίνακα Eklsimbperkoin
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
    if request.method == 'POST':
        # parent_obj_url=obj.content_object.get_absolute_url()
        obj.delete()
        messages.success(request, "Η διαγραφή ολοκληρώθηκε")
        return redirect('simbouloi_list', eklid)
    context = {'selected_ekloges': selected_ekloges.eklid,
               'all_ekloges': all_ekloges,
               'object': obj
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

    q = Q(sindid__in=Eklsind.objects.filter(eklid=eklid).values_list('sindid')) | Q(sindid__in=Eklsindkoin.objects.filter(eklid=eklid).filter(koinid=koinid).values_list('sindid'))

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

    #Ψάχνω σε προηγούμενες εκλ. αναμετρήσεις υποψήφιο με ίδιο surname, firstname, fathername και δεν έχουν εισαχθεί ακόμη στην τρέχουσα εκλ. αναμέτρηση
    simbouloi = EklallsimbVw.objects.filter(eklid__lt=eklid). \
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

    Psifoi.objects.filter(kenid=kenid, simbid=simbid).update(votes=votes)
    return HttpResponse('');



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

    all_psifoi=selected_ekloges.eklpsifoisimbvw_set.filter(kenid=kenid).values_list('simbid', 'surname', 'firstname', 'fathername', 'sindiasmos', 'shortsind', 'sindaa','eidos', 'simbaa', 'toposeklogis', 'votes', 'kenid', 'koinotita', 'id', 'kenid__perid__descr')
    if paramorder==1 or paramorder==5:
        all_psifoi = all_psifoi.order_by('sindaa', 'eidos', 'toposeklogis', 'surname')
    elif paramorder == 2:
        all_psifoi = all_psifoi.order_by('sindaa', 'eidos', 'surname')
    elif paramorder == 3:
        all_psifoi = all_psifoi.order_by('eidos', 'surname')
    else:
        all_psifoi = all_psifoi.order_by('surname')



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

    action_label='Καταχώρηση ψηφοδελτίων Υποψηφίων Συνδυασμών'
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')
    selected_ekloges = Eklogestbl.objects.prefetch_related('kentra_set','eklsind_set').get(eklid=eklid)

    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format('/accounts/login/'+str(selected_ekloges.eklid),request.path))


    if not request.user.has_perm('Elections.change_psifodeltia'):
        raise PermissionDenied

    selected_kentro = Kentra.objects.prefetch_related('psifodeltia_set').get(kenid=kenid)

    PsifodeltiaFormSet = modelformset_factory(Psifodeltia, fields =('sindid', 'votesa', 'votesb', 'votesk','kenid',), extra=0)

    data = request.POST or None
    formset = PsifodeltiaFormSet(data=data, queryset= selected_kentro.psifodeltia_set.filter(kenid=kenid).order_by('-sindid__eidos', 'sindid__descr'  ))
    for form in formset:
        form.fields['kenid'].queryset = selected_ekloges.kentra_set.filter(kenid=form['kenid'].value()) #Kentra.objects.filter(kenid=form['kenid'].value())
        form.fields['sindid'].queryset = Sindiasmoi.objects.filter(sindid=form['sindid'].value())  #Simbouloi.objects.filter(simbid=form['simbid'].value()) Τα dropdown θα έχουν μόνο το σχετικό simbid

    if request.method == 'POST' and formset.is_valid():
        formset.save()
        messages.success(request, 'Οι αλλαγές αποθηκεύτηκαν!')
        return HttpResponseRedirect('/'+str(eklid)+ '?eklogesoption=' +str(eklid)+ '&eklkentrooption='+str(selected_kentro.descr))

    context = {'selected_ekloges': selected_ekloges.eklid,
                'selected_kentro':selected_kentro,
               'all_ekloges': all_ekloges,
               'action_label':action_label,
               'formset': formset
               }

    return render(request, 'Elections/psifodeltia_formset.html', context)

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