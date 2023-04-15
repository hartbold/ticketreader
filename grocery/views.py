import os
import re
import json

from urllib.parse import unquote

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse_lazy # reverse - reverse_lazy (para class based)
from django.views import generic
from django.core.files.storage import default_storage

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.datastructures import MultiValueDictKeyError
from django.http import JsonResponse

from . import utils

from .settings import UPLOAD_PATH_TICKETS
# from django.template import loader

from .models import Storage, Item, Ticket, Product

# Create your views here.


@login_required
def store(request, storage_id):
    storage = get_object_or_404(Storage, pk=storage_id)

    try:

        if (not len(request.POST["name"])):
            raise KeyError

        i = Item.objects.create(
            storage=storage, user=request.user, name=request.POST["name"],
            amount=int('0'+(request.POST['amount'])), unit=request.POST['unit'])
        i.save()

    except (KeyError):
        return render(request, "grocery/detail.html", {"storage": storage, "unit_choices": Item.UNIT_CHOICES, "error_message": "El producte no te nom i no s'ha introduït"})

    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def upload(request, storage_id):
    storage = get_object_or_404(Storage, pk=storage_id)

    text = "Hi ha hagut un error"
    items = []

    if request.method == 'POST':

        try:
            img_stream = request.FILES['croppedImage']

            # print(request.FILES, request.POST, img_stream)
            #  img_stream = base64.b64encode(img_stream).decode()
            filename = img_stream.name
            filepath = os.path.join(UPLOAD_PATH_TICKETS, filename)

            if not img_stream or filename == '' or not utils.allowed_file(img_stream):
                return JsonResponse({"error_message": "No s'ha pogut carregar la imatge"}, safe=False)

            # todo ok save the file
            with default_storage.open(filepath, 'wb+') as destination:
                for chunk in img_stream.chunks():
                    destination.write(chunk)

            # Reading image using OCR
            text = utils.get_img_text(filepath)
            print(text)
            productes = utils.get_products(text)
            print(productes)
            items = json.loads(productes)
            print(items)

        except MultiValueDictKeyError:
            return JsonResponse({"error_message": "MultiValueDictKeyError"}, safe=False)
        except json.decoder.JSONDecodeError:
            return JsonResponse({"error_message": "JSONDecodeError"}, safe=False)

# .replace("\n", "<br>")
    return JsonResponse({"error_message": text, "items_processed": items}, safe=False)


@login_required
def savetiquet(request, storage_id):
    storage = get_object_or_404(Storage, pk=storage_id)
    try:

        if (not len(request.POST['raw-text'])):
            raise KeyError

        total = 0
        clean_productes = {}

        for i in request.POST.items():

            key = i[0]
            value = i[1]

            key = key.replace("%5B", "[").replace("%5D", "]")
            # print(key.replace("%5B", "[").replace("%5D", "]"))

            if key.find("producte") == -1:
                continue

            id = (re.findall(r'\d+', key)[0])
            key = (re.findall(r'(name|amount|price|unit)', key)[0])

            if id not in clean_productes.keys():
                clean_productes[id] = {}

            if key not in clean_productes[id].keys():
                clean_productes[id][key] = ""

            clean_productes[id][key] = value  # request.POST.get(og_i)
            if (key == "price"):
                total += float(value)

        tiquet = Ticket.objects.create(
            user=request.user,
            storage=storage,
            total=total,
            processedText=unquote(request.POST['raw-text']).replace("+", " ")
        )
        tiquet.save()

        print(clean_productes)

        for id in clean_productes.keys():

            values = clean_productes[id]

            print(values)

            item = Item.objects.create(
                storage=storage,
                user=request.user,
                name=unquote(values["name"]).replace("+", " "),
                unit=values["unit"],
                amount=values["amount"]
            )
            print(item)
            item.save()

            prod = Product.objects.create(
                ticket=tiquet,
                name=unquote(values["name"]).replace("+", " "),
                # name_clear=i["unit"],
                price=float(values["price"])
            )
            print(prod)
            prod.save()

    except KeyError as e:
        
        tiquet.delete()
        return render(request, "grocery/detail.html", {"storage": storage, "unit_choices": Item.UNIT_CHOICES, "error_message": e})

    # return HttpResponseRedirect(url('grocery:detail', storage.id))
    return HttpResponseRedirect("/grocery/" + storage.id)


@login_required
def ticket(request, storage_id):
    storage = get_object_or_404(Storage, pk=storage_id)

    return render(request, "grocery/ticket.html", {"storage": storage, "unit_choices": Item.UNIT_CHOICES})


@method_decorator(login_required, name='dispatch')
class IndexView(generic.ListView):
    template_name = "grocery/index.html"
    context_object_name = "latest_storage_list"

    def get_queryset(self):
        try:
            return Storage.objects.filter(users=self.request.user)
        except (Storage.DoesNotExist):
            return []


@login_required
def detail(request, storage_id):
    storage = get_object_or_404(Storage, pk=storage_id)
    return render(request, "grocery/detail.html", {"storage": storage, "unit_choices": Item.UNIT_CHOICES})


# DEPRECATED ------------------------------


@login_required
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


@method_decorator(login_required, name='dispatch')
class DetailView(generic.DetailView):
    model = Storage
    template_name = "grocery/detail.html"

# DEPRECATED

    '''
    try:
        storage = Storage.objects.get(pk=storage_id)
    except Storage.DoesNotExist:
        raise Http404("Storage does not exist")

    return render(request, "grocery/detail.html", {"storage":storage})
    '''
