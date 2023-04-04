
from django.shortcuts import render

from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from django.http import HttpResponseRedirect

from .settings import START_URL
        

def login(request):

    if(len(request.POST.get('username', '')) > 0 and len(request.POST.get('password', '')) > 0):
        try:
            u = User.objects.get(username=request.POST.get('username'))
            
            user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))

            if check_password(u.password, make_password(request.POST.get('password'))):
                return HttpResponseRedirect(START_URL)
            else:
                raise PermissionDenied

        except User.DoesNotExist:
            return render(request, "ticketreader/login.html", {"error_message": "No ."})
        
        except PermissionDenied:
            return render(request, "ticketreader/login.html", {"error_message": "No denied."})
        
        else:
            return HttpResponseRedirect(self.get_success_url())

    return render(request, "ticketreader/login.html")

    return render(request, "ticketreader/login.html")

def register(request):
    return render(request, "ticketreader/register.html")