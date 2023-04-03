from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
# from django.template import loader

from .models import Storage, Item

# Create your views here.


def index(request):
    latest_storage_list = Storage.objects.order_by("name")[:5]
    context = {"latest_storage_list": latest_storage_list}
    return render(request, "grocery/index.html", context)

    '''
    template = loader.get_template('grocery/index.html')
    context = {
        "latest_storage_list" : latest_storage_list
    }
    return HttpResponse(template.render(context))
    '''


def detail(request, storage_id):
    storage = get_object_or_404(Storage, pk=storage_id)
    return render(request, "grocery/detail.html", {"storage": storage})

    '''
    try:
        storage = Storage.objects.get(pk=storage_id)
    except Storage.DoesNotExist:
        raise Http404("Storage does not exist")

    return render(request, "grocery/detail.html", {"storage":storage})
    '''


def store(request, storage_id):
    storage = get_object_or_404(Storage, pk=storage_id)
    try:
        i = Item.objects.create(storage=storage, name=request.POST["name"])
        i.save()

    except (KeyError):
        return render(request, "storage/detail.html", {"storage": storage, "error_message": "No s'ha pogut afegit el producte."})

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
