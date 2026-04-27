from django.contrib import admin
from personas.models import Domicilio, Persona


@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    # Columnas que se ven en la lista
    list_display = ('id', 'nombre_completo', 'email', 'domicilio')
    
    search_fields = ('nombre', 'apellido', 'email')
    
    list_filter = ('domicilio__pais',)
    
    ordering = ('-id',)
    
    list_per_page = 20


@admin.register(Domicilio)
class DomicilioAdmin(admin.ModelAdmin):
    list_display = ('id', 'calle', 'no_calle', 'pais', 'total_personas')
    search_fields = ('calle', 'pais')
    list_filter = ('pais',)
    ordering = ('-id',)
    list_per_page = 20

    @admin.display(description='Personas')
    def total_personas(self, obj):
        return obj.personas.count()