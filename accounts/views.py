from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import  messages


from Elections.models import Eklogestbl


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
            redirect_url=request.GET.get('next', 'Elections_list' )
            messages.success(request, 'Συνδέθηκες ως {}'.format(user.username))
            return redirect(redirect_url, selected_ekloges.eklid )
        else:
            messages.error(request, 'Ανύπαρκτος χρήστης!')

    context = {'selected_ekloges': selected_ekloges.eklid,
               'all_ekloges': all_ekloges,
               }

    return render(request, 'accounts/login.html',context)
    #return HttpResponse('user login')

def logout_user(request, eklid):

    selected_ekloges = Eklogestbl.objects.prefetch_related('kentra_set').get(eklid=eklid)
    action_label = ''

    # επιλογή όλων των εκλ. αναμετρήσεων με visible=1 και κάνω φθίνουσα ταξινόμηση  αν δεν δοθεί παράμετρος
    all_ekloges = Eklogestbl.objects.filter(visible=1).order_by('-eklid')

    logout(request)

    #return redirect('Elections_list', selected_ekloges.eklid)
    return redirect('accounts:login', selected_ekloges.eklid)