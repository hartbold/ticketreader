
from django.shortcuts import render

from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from django.http import HttpResponseRedirect

from .settings import START_URL, LOGIN_URL
        

def login(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect(START_URL)

    if(len(request.POST.get('username', '')) > 0 and len(request.POST.get('password', '')) > 0):
        try:

            user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
            if user is not None:
                # A backend authenticated the credentials
                auth_login(request, user=user)
                return HttpResponseRedirect(START_URL)
            else:
                # No backend authenticated the credentials
                raise PermissionDenied

                # return render(request, "ticketreader/login.html", {"error_message": "No ."})

            '''u = User.objects.get(username=request.POST.get('username'))
            
            print(u.password)
            print(make_password(request.POST.get('password')))

            if check_password(u.password, make_password(request.POST.get('password'))):
                
            else:
                raise PermissionDenied'''

        except User.DoesNotExist:
            return render(request, "ticketreader/login.html", {"error_message": "No ."})
        
        except PermissionDenied:
            return render(request, "ticketreader/login.html", {"error_message": "No denied."})
        
    return render(request, "ticketreader/login.html")

def register(request):

    if(len(request.POST.get('username', '')) > 0 and len(request.POST.get('password', '')) > 0):
        try:
            u = User.objects.get(username=request.POST.get('username'))
        except User.DoesNotExist:
            u = User.objects.create_user(username=request.POST.get('username'), password=request.POST.get('password'))
            u.save()
            return HttpResponseRedirect(START_URL)

    return render(request, "ticketreader/register.html")