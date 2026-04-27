from django.urls import path
from personas import views

urlpatterns = [
    # Personas
    path('', views.mostrar_personas, name='mostrar_personas'),
    path('nueva/', views.nueva_persona, name='nueva_persona'),
    path('<int:id>/', views.detalle_persona, name='detalle_persona'),
    path('<int:id>/editar/', views.editar_persona, name='editar_persona'),
    path('<int:id>/eliminar/', views.eliminar_persona, name='eliminar_persona'),

    # Domicilios
    path('domicilios/', views.mostrar_domicilios, name='mostrar_domicilios'),
    path('domicilios/nuevo/', views.nuevo_domicilio, name='nuevo_domicilio'),
    path('domicilios/<int:id>/editar/', views.editar_domicilio, name='editar_domicilio'),
    path('domicilios/<int:id>/eliminar/', views.eliminar_domicilio, name='eliminar_domicilio'),

    # Búsqueda AJAX
    path('buscar/', views.buscar_sugerencias_personas, name='buscar_personas'),
    path('domicilios/buscar/', views.buscar_sugerencias_domicilios, name='buscar_domicilio'),
]