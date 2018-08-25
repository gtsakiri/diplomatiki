import xlwt
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from .models import  Eklogestbl, EklSumpsifodeltiasindVw,EklPosostasindPerVw,Perifereies, \
      EklSumpsifoisimbPerVw, EklSumpsifoisimbKoinVw, Koinotites, EklSumpsifodeltiasindKenVw, \
      Kentra, EklPsifoisimbVw
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


def export_psifodeltiasind_ken(request,eklid, selected_order):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="psifodeltiasind_ken.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('data')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.height = 280
    font_style.font.bold = True

    ws.write(row_num, 0, 'Ψηφοδέλτια συνδυασμών ανά εκλ. κέντρο', font_style)

    row_num += 2

    firstrow = EklSumpsifodeltiasindVw.objects.filter(eklid=eklid).values_list('katametrimena', 'plithoskentrwn','posostokatametrimenwnkentrwn').distinct()
    # for col_num in range(len(firstrow[0])):
    ws.write(row_num, 0,'Στα ' + str(firstrow[0][0]) + ' από τα ' + str(firstrow[0][1]) + ' εκλ. κέντρα (Ποσοστό ' + str(firstrow[0][2]) + '%)', font_style)

    font_style = xlwt.XFStyle()
    font_style.font.height = 240
    font_style.font.bold = True

    row_num += 2

    columns = ['Εκλ. Κέντρο', 'Συνδυασμός', 'Ψηφοδέλτια',]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    #rows = EklSumpsifoisimbPerVw.objects.filter(eklid=eklid).values_list('sindiasmos', 'surname', 'firstname', 'fathername', 'toposeklogis', 'sumvotes')
    if selected_order == 1 or selected_order == 4:
        rows = EklSumpsifodeltiasindKenVw.objects.filter(eklid=eklid).values_list('kentro', 'sindiasmos', 'votes').order_by('kentro','-votes')
    elif selected_order == 1 or selected_order == 4:
        rows = EklSumpsifodeltiasindKenVw.objects.filter(eklid=eklid).values_list('kentro', 'sindiasmos','votes').order_by('kentro', 'sindiasmos')
    else:
        rows = EklSumpsifodeltiasindKenVw.objects.filter(eklid=eklid).values_list('kentro', 'sindiasmos', 'votes').order_by('sindiasmos','kentro',)

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

    columns = ['Εκλ. Κέντρο', 'Επώνυμο', 'Όνομα', 'Όν. Πατρός', 'Συνδυασμός', 'Ψήφοι']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    #rows = EklSumpsifoisimbPerVw.objects.filter(eklid=eklid).values_list('sindiasmos', 'surname', 'firstname', 'fathername', 'toposeklogis', 'sumvotes')
    if selected_order == 1 or selected_order == 5:
        rows = EklPsifoisimbVw.objects.filter(eklid=eklid).values_list('kentro', 'surname', 'firstname', 'fathername', 'sindiasmos', 'votes').order_by('kenid','sindiasmos', '-votes')
    elif selected_order == 2:
        rows = EklPsifoisimbVw.objects.filter(eklid=eklid).values_list('kentro', 'surname', 'firstname', 'fathername', 'sindiasmos', 'votes').order_by('kenid', 'sindiasmos','surname')
    elif selected_order == 3:
        rows = EklPsifoisimbVw.objects.filter(eklid=eklid).values_list('kentro', 'surname', 'firstname', 'fathername','sindiasmos', 'votes').order_by('kenid','surname')
    else:
        rows = EklPsifoisimbVw.objects.filter(eklid=eklid).values_list('kentro', 'surname', 'firstname', 'fathername', 'sindiasmos', 'votes').order_by('-votes')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def Elections_list(request):

    paramstr=request.GET.get('eklogesoption','')

    try:
        paramstr = int(paramstr)
    except:
        paramstr = 2 #default eklid (εκλογες 2019) αν δεν δοθεί

    #φιλτράρισμα επιλεγμένης εκλ. αναμέτρησης
    selected_ekloges = Eklogestbl.objects.filter(eklid=paramstr)
    #επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση για να επιλεγεί η τελευταία αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')
    context = {'selected_ekloges':selected_ekloges, 'all_ekloges':all_ekloges}
    return render(request, 'Elections/Elections_list.html',context)


def pososta_telika(request, eklid):

#ΠΟΣΟΣΤΑ ΣΥΝΔΥΑΣΜΩΝ ΣΕ ΟΛΟ ΤΟ ΔΗΜΟ


    # φιλτράρισμα επιλεγμένης εκλ. αναμέτρησης
    selected_ekloges = Eklogestbl.objects.filter(eklid=eklid)
    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')
    #ανάκτηση εγγραφών επιλεγμένης εκλ. αναμέτρησης από το σχετικό database view
    all_pososta = EklSumpsifodeltiasindVw.objects.filter(eklid=eklid).order_by('-posostosindiasmou')
    context = {'all_pososta':all_pososta, 'all_ekloges':all_ekloges, 'selected_ekloges':selected_ekloges}
    return render(request, 'Elections/pososta_telika.html',context)

def pososta_perifereies(request, eklid):

# ΠΟΣΟΣΤΑ ΣΥΝΔΥΑΣΜΩΝ ΑΝΑ ΕΚΛΟΓΙΚΗ ΠΕΡΙΦΕΡΕΙΑ
    paramstr = request.GET.get('perifereiaoption','')

    try:
        paramstr = int(paramstr)
    except:
        paramstr = 1  # default perid  αν δεν δοθεί

    # φιλτράρισμα επιλεγμένης εκλ. αναμέτρησης
    selected_ekloges = Eklogestbl.objects.filter(eklid=eklid)
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
               'selected_ekloges':selected_ekloges,
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
        paramstr = 1 # default perid  αν δεν δοθεί


    try:
        paramorder = int(paramorder)
    except:
        paramorder = 4  # default ταξινόμηση

    #φιλτράρισμα επιλεγμένης εκλ. αναμέτρησης
    selected_ekloges = Eklogestbl.objects.filter(eklid=eklid)
    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    # φιλτράρισμα επιλεγμένης περιφέρειας
    selected_perifereia = Perifereies.objects.filter(perid=paramstr)

    selected_order = paramorder

    #ανάκτηση όλων των περιφερειών
    all_perifereies=Perifereies.objects.all()
    #ανάκτηση εγγραφών επιλεγμένης εκλ. αναμέτρησης από το σχετικό database view
    all_pososta = EklSumpsifodeltiasindVw.objects.filter(eklid=eklid).order_by('-posostosindiasmou')

    if paramorder==1:
        all_psifoi = EklSumpsifoisimbPerVw.objects.filter(eklid=eklid).filter(toposeklogisid=paramstr).order_by('sindiasmos','-sumvotes')
    elif paramorder==2 :
        all_psifoi = EklSumpsifoisimbPerVw.objects.filter(eklid=eklid).filter(toposeklogisid=paramstr).order_by('sindiasmos','surname')
    else:
        all_psifoi = EklSumpsifoisimbPerVw.objects.filter(eklid=eklid).filter(toposeklogisid=paramstr).order_by('-sumvotes')

    context = {'all_psifoi':all_psifoi,
                'all_pososta':all_pososta,
               'all_ekloges':all_ekloges,
               'selected_ekloges':selected_ekloges,
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
    selected_ekloges = Eklogestbl.objects.filter(eklid=eklid)
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
               'selected_ekloges':selected_ekloges,
               'all_koinotites':all_koinotites,
               'selected_koinotita': selected_koinotita,
               'selected_order':selected_order,
               'selected_menu':selected_menu,}
    return render(request, 'Elections/psifoisimb_koinotites.html',context)

def psifodeltiasind_ken(request, eklid):

# ΨΗΦΟΙ ΣΥΝΔΥΑΣΜΩΝ ΑΝΑ ΕΚΛ. ΚΕΝΤΡΟ

    paramstr = request.GET.get('kentrooption','')
    paramorder = request.GET.get('orderoption','')

    try:
        paramstr = int(paramstr)
    except:
        p = EklSumpsifodeltiasindKenVw.objects.filter(eklid=eklid).order_by('kentro')
        paramstr=p[0].kenid  # default kenid θα είναι το πρώτο της λίστας αν δεν δοθεί κάτι

    try:
        paramorder = int(paramorder)
    except:
        paramorder = 4  # default ταξινόμηση

    # φιλτράρισμα επιλεγμένης εκλ. αναμέτρησης
    selected_ekloges = Eklogestbl.objects.filter(eklid=eklid)
    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    # φιλτράρισμα επιλεγμένου κέντρου
    selected_kentro = Kentra.objects.filter(kenid=paramstr)

    selected_order = paramorder

    #ανάκτηση όλων των κέντρων της εκλ. αναμέτρησης
    all_kentra=Kentra.objects.filter(eklid=eklid)
    #ανάκτηση εγγραφών επιλεγμένης εκλ. αναμέτρησης από το σχετικό database view
    all_pososta = EklSumpsifodeltiasindVw.objects.filter(eklid=eklid).order_by('-posostosindiasmou')

    if paramorder == 1 or paramorder == 4:
        all_psifodeltia = EklSumpsifodeltiasindKenVw.objects.filter(kenid=paramstr).order_by('-votes')
    elif paramorder == 2:
        all_psifodeltia = EklSumpsifodeltiasindKenVw.objects.filter(kenid=paramstr).order_by('sindiasmos')
    else:
        all_psifodeltia = EklSumpsifodeltiasindKenVw.objects.filter(kenid=paramstr).order_by('sindiasmos','kentro')


    context = {'all_psifodeltia':all_psifodeltia,
                'all_pososta':all_pososta,
               'all_ekloges':all_ekloges,
               'selected_ekloges':selected_ekloges,
               'all_kentra':all_kentra,
               'selected_kentro': selected_kentro,
               'selected_order':selected_order,
               }
    return render(request, 'Elections/psifodeltiasind_ken.html',context)

def psifoisimb_ken(request, eklid):

# ΨΗΦΟΙ ΣΥΜΒΟΥΛΩΝ ΑΝΑ ΕΚΛ. ΚΕΝΤΡΟ

    paramstr = request.GET.get('kentrooption','')
    paramorder = request.GET.get('orderoption','')

    try:
        paramstr = int(paramstr)
    except:
        p = EklPsifoisimbVw.objects.filter(eklid=eklid).order_by('kentro')
        paramstr=p[0].kenid  # default kenid θα είναι το πρώτο της λίστας αν δεν δοθεί κάτι

    try:
        paramorder = int(paramorder)
    except:
        paramorder = 5  # default ταξινόμηση

    # φιλτράρισμα επιλεγμένης εκλ. αναμέτρησης
    selected_ekloges = Eklogestbl.objects.filter(eklid=eklid)
    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    # φιλτράρισμα επιλεγμένου κέντρου
    selected_kentro = Kentra.objects.filter(kenid=paramstr)

    selected_order = paramorder

    #ανάκτηση όλων των κέντρων της εκλ. αναμέτρησης
    all_kentra=Kentra.objects.filter(eklid=eklid)
    #ανάκτηση εγγραφών επιλεγμένης εκλ. αναμέτρησης από το σχετικό database view
    all_pososta = EklSumpsifodeltiasindVw.objects.filter(eklid=eklid).order_by('-posostosindiasmou')

    if paramorder==1 or paramorder==5:
        all_psifoi = EklPsifoisimbVw.objects.filter(kenid=paramstr).order_by('sindiasmos','-votes')
    elif paramorder == 2:
        all_psifoi = EklPsifoisimbVw.objects.filter(kenid=paramstr).order_by('sindiasmos','surname')
    elif paramorder == 3:
        all_psifoi = EklPsifoisimbVw.objects.filter(kenid=paramstr).order_by('surname')
    else:
        all_psifoi = EklPsifoisimbVw.objects.filter(kenid=paramstr).order_by('votes')


    context = {'all_psifoi':all_psifoi,
                'all_pososta':all_pososta,
               'all_ekloges':all_ekloges,
               'selected_ekloges':selected_ekloges,
               'all_kentra':all_kentra,
               'selected_kentro': selected_kentro,
               'selected_order':selected_order,
               }
    return render(request, 'Elections/psifoisimb_ken.html',context)

