from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from personas.models import Persona, Domicilio
from personas.forms import PersonaForm, DomicilioForm
from django.core.paginator import Paginator
from django.conf import settings


# -------- PERSONAS --------

def mostrar_personas(request):
    personas = Persona.objects.select_related('domicilio').order_by('-id')

    paginator = Paginator(personas, getattr(settings, 'ITEMS_POR_PAGINA', 10))
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'personas.html', {'personas': page_obj})


def detalle_persona(request, id):
    persona = get_object_or_404(Persona.objects.select_related('domicilio'), pk=id)
    return render(request, 'detalle.html', {'persona': persona})


def nueva_persona(request):
    forma_persona = PersonaForm(request.POST or None)

    if request.method == 'POST':
        if forma_persona.is_valid():
            forma_persona.save()
            messages.success(request, "Usuario creado correctamente", extra_tags='green')
            return redirect('mostrar_personas')
        else:
            messages.warning(request, "No se pudo completar la acción. Revisa los datos.", extra_tags='orange')

    return render(request, 'nuevo.html', {'forma_persona': forma_persona})


def editar_persona(request, id):
    persona = get_object_or_404(Persona.objects.select_related('domicilio'), pk=id)
    forma_persona = PersonaForm(request.POST or None, instance=persona)

    if request.method == 'POST':
        if forma_persona.is_valid():
            forma_persona.save()
            messages.success(request, f"Perfil de {persona.nombre} modificado correctamente", extra_tags='green')
            return redirect('mostrar_personas')
        else:
            messages.warning(request, "No se pudo completar la edición.", extra_tags='orange')

    return render(request, 'editar.html', {'forma_persona': forma_persona})


def eliminar_persona(request, id):
    persona = get_object_or_404(Persona, pk=id)

    if request.method == 'POST':
        nombre_eliminado = f"{persona.nombre} {persona.apellido}"
        persona.delete()
        messages.error(request, f"Usuario {nombre_eliminado} eliminado permanentemente.", extra_tags='red')
    
    return redirect('mostrar_personas')


# -------- DOMICILIOS --------

def mostrar_domicilios(request):
    domicilios = Domicilio.objects.order_by('-id')

    paginator = Paginator(domicilios, getattr(settings, 'ITEMS_POR_PAGINA', 10))
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'domicilios.html', {'domicilios': page_obj})


def nuevo_domicilio(request):
    forma_domicilio = DomicilioForm(request.POST or None)

    if request.method == 'POST':
        if forma_domicilio.is_valid():
            forma_domicilio.save()
            messages.success(request, "Domicilio registrado.", extra_tags='green')
            return redirect('mostrar_domicilios')
        else:
            messages.warning(request, "Error al registrar domicilio.", extra_tags='orange')

    return render(request, 'nuevo_dom.html', {'forma_domicilio': forma_domicilio})


def editar_domicilio(request, id):
    domicilio = get_object_or_404(Domicilio, pk=id)
    forma_domicilio = DomicilioForm(request.POST or None, instance=domicilio)

    if request.method == 'POST':
        if forma_domicilio.is_valid():
            forma_domicilio.save()
            messages.success(request, "Domicilio actualizado.", extra_tags='green')
            return redirect('mostrar_domicilios')
        else:
            messages.warning(request, "Error al actualizar domicilio.", extra_tags='orange')

    return render(request, 'editar_dom.html', {
        'forma_domicilio': forma_domicilio,
        'domicilio': domicilio
    })


def eliminar_domicilio(request, id):
    domicilio = get_object_or_404(Domicilio, pk=id)

    if request.method == 'POST':
        domicilio.delete()
        messages.error(request, "Domicilio eliminado.", extra_tags='red')

    return redirect('mostrar_domicilios')

def buscar_sugerencias_personas(request):
    query = request.GET.get('term', '')
    resultados = []
    if query:
        personas = Persona.objects.filter(nombre__icontains=query) | \
                   Persona.objects.filter(apellido__icontains=query) | \
                   Persona.objects.filter(id__icontains=query) | \
                   Persona.objects.filter(email__icontains=query)
        
        for p in personas[:5]:
            resultados.append({
                'id': p.id,
                'nombre': f"{p.nombre} {p.apellido}"
            })
            
    return JsonResponse(resultados, safe=False)

def buscar_sugerencias_domicilios(request):
    query = request.GET.get('term', '')
    resultados = []
    if query:
        domicilios = Domicilio.objects.filter(calle__icontains=query) | \
                     Domicilio.objects.filter(pais__icontains=query) | \
                     Domicilio.objects.filter(no_calle__contains=query) | \
                     Domicilio.objects.filter(id__icontains=query)
        
        for d in domicilios[:5]:
            resultados.append({
                'id': d.id,
                'calle': f"{d.calle} #{d.no_calle}, {d.pais}" # Formato completo
            })
            
    return JsonResponse(resultados, safe=False)