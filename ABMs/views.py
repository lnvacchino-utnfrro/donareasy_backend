from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Donante
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    return render(request, "ABMs/index.html")

def altaDonante(request):
    # if this is a POST request we need to process the form data
    if request.method=="POST":
        # create a form instance and populate it with data from the request:
        #form = NameForm(request.POST)
        # check whether it's valid:
        #if form.is_valid():

        # process the data in form.cleaned_data as required
        nombre=request.POST["nombre"]
        apellido=request.POST["apellido"] 
        email = request.POST["email"]
        edad = request.POST["edad"]

        donante = Donante(nombre=nombre,apellido=apellido,email=email,edad=edad)
        donante.save(force_insert=True)
        
        # redirect to a new URL:
        return HttpResponse('<html><body><h1>Donante Agregado</h1></body></html>')
        #return render(request, "ABMs/abm_donante.html")
    else:
        return render(request, "ABMs/alta_donante.html")

def bajaDonante(request,id_donante):
    # FALTA AGREGAR TRY EXCEPT
    Donante.objects.get(id__exact = id_donante).delete()

    return HttpResponse('<html><body><h1>Donante %s Eliminado</h1></body></html>' %(id_donante))

def modificarDonante(request,id_donante):
    # if this is a POST request we need to process the form data
    if request.method=="POST":
        # create a form instance and populate it with data from the request:
        # form = NameForm(request.POST)
        # check whether it's valid:
        # if form.is_valid():

        # process the data in form.cleaned_data as required
        donante = Donante.objects.get(id__exact = id_donante)

        donante.nombre=request.POST["nombre"]
        donante.apellido=request.POST["apellido"] 
        donante.email = request.POST["email"]
        donante.edad = request.POST["edad"]

        donante.save(force_update=True)

        # redirect to a new URL:
        return HttpResponse('<html><body><h1>Donante Actualizado</h1></body></html>')
        #return render(request, "ABMs/abm_donante.html")
    else:
        donante = Donante.objects.get(id__exact = id_donante)

        diccionario = { "id_donante": donante.id,
                        "nombre":   donante.nombre,
                        "apellido": donante.apellido,
                        "email":    donante.email,
                        "edad":     donante.edad}

        return render(request, "ABMs/modif_donante.html", diccionario)

def buscarDonante(request,id_donante):
    try:
        donante = Donante.objects.get(id__exact = id_donante)

        diccionario = { "id":       donante.id,
                        "nombre":   donante.nombre,
                        "apellido": donante.apellido,
                        "email":    donante.email,
                        "edad":     donante.edad}

        return render(request, "ABMs/donante.html", diccionario)

    except ObjectDoesNotExist:
        return HttpResponse('<html><body><h1>El donante no existe</h1></body></html>')

