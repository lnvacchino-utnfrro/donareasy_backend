from django.shortcuts import render
from .models import Donante

# Create your views here.
def altaDonante(request):

    if request.method=="POST":
        
        nombre=request.POST["nombre"]
        apellido=request.POST["apellido"] 
        email = request.POST["email"]
        edad = request.POST["edad"]

        donante = Donante(nombre=nombre,apellido=apellido,email=email,edad=edad)
        donante.save(force_insert=True)

        return render(request, "ABMs/abm_donante.html")
    return render(request, "ABMs/abm_donante.html")
