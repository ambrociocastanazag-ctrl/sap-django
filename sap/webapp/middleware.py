from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Rutas que CUALQUIERA puede ver (sin loguearse)
        rutas_publicas = [
            reverse('bienvenido'), 
            reverse('login'),  
        ]
        
        # 2. Si NO está autenticado y la ruta NO es pública ni de sistema
        if not request.user.is_authenticated:
            es_ruta_sistema = request.path.startswith('/admin/') or request.path.startswith('/static/')
            if request.path not in rutas_publicas and not es_ruta_sistema:
                return redirect('login') # Lo mandamos a loguearse

        response = self.get_response(request)
        return response