from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event
from sign.models import Guest
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.shortcuts import render,get_object_or_404
from django.http import request
# Create your views here.

def index(request):
   return render(request, "index.html")

def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        usr = auth.authenticate(username=username, password=password)
        if usr is not None:
            auth.login(request,usr)
            request.session['usr'] = username
            response = HttpResponseRedirect('/event_manage/')
            return response
        else:
            return render(request, 'index.html', {'error': 'username or password is wrong!'})
    else:
        return render(request, 'index.html', {'error': 'username or password is wrong!'})



@login_required
def event_manage(request):
    event_list = Event.objects.all()
    # username = request.COOKIES.get('usr', '')
    username = request.session.get('usr', '')
    paginator=Paginator(event_list,2)
    page=request.GET.get('page')
    try:
        contacts=paginator.page(page)
    except PageNotAnInteger:
        contacts=paginator.page(1)
    except EmptyPage:
        contacts=paginator.page(paginator.num_pages)
    return render(request, "event_manage.html", {"usr": username,"events": contacts})

@login_required
def guest_manage(request):
    guest_list = Guest.objects.all()
    username = request.session.get('usr', '')
    paginator=Paginator(guest_list,5)
    page=request.GET.get('page')
    try:
        contacts=paginator.page(page)
    except PageNotAnInteger:
        contacts=paginator.page(1)
    except EmptyPage:
        contacts=paginator.page(paginator.num_pages)

    return render(request, "guest_manage.html", {"usr": username,"guests": contacts})

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/index/')

@login_required
def search_name(request):
    username = request.session.get('usr', '')
    search_name = request.GET.get("name", "")
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, "event_manage.html", {"usr": username, "events": event_list})


@login_required
def search_guest_name(request):
    username = request.session.get('usr', '')
    search_guest_name = request.GET.get("name", "")
    guest_list = Guest.objects.filter(realname__contains=search_guest_name)
    return render(request, "guest_manage.html", {"usr": username, "guests": guest_list})


@login_required
def sign_index(request,event_id):
    event=get_object_or_404(Event,id=event_id)
    return render(request,"sign_index.html",{'event':event})


@login_required
def sign_index_action(request,event_id):
    event=get_object_or_404(Event,id=event_id)
    phone=request.POST.get('phone','')

    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request,'sign_index.html',{'event':event,'hint':'phone error.'})

    result = Guest.objects.get(phone=phone,event_id=event_id)
    if result.sign:
        return render(request,'sign_index.html',{'event':event,'hint':"user has sign in."})
    else:
        Guest.objects.filter(phone=phone,event_id=event_id).update(sign='1')
        return render(request,'sign_index.html',{'event':event,'hint':"sign in success!",'guest':result})