from django.shortcuts import render

from personas.models import Persona, Domicilio
# Create your views here.

def bienvenido(request):
    no_personas = Persona.objects.count()
    return render(request, 'bienvenido.html', {'no_personas':no_personas})

