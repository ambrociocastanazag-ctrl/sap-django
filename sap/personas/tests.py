from django.test import TestCase, Client
from django.urls import reverse
from personas.models import Persona, Domicilio


# ──────────────────────────────────────────────
#  TESTS DEL MODELO
# ──────────────────────────────────────────────

class DomicilioModelTest(TestCase):

    def setUp(self):
        self.domicilio = Domicilio.objects.create(
            calle='Calle Reforma',
            no_calle='24-B',
            pais='Guatemala'
        )

    def test_str(self):
        self.assertEqual(str(self.domicilio), 'Calle Reforma #24-B, Guatemala')

    def test_campos(self):
        self.assertEqual(self.domicilio.calle, 'Calle Reforma')
        self.assertEqual(self.domicilio.no_calle, '24-B')
        self.assertEqual(self.domicilio.pais, 'Guatemala')


class PersonaModelTest(TestCase):

    def setUp(self):
        self.domicilio = Domicilio.objects.create(
            calle='Calle Reforma',
            no_calle='24-B',
            pais='Guatemala'
        )
        self.persona = Persona.objects.create(
            nombre='Juan',
            apellido='Pérez',
            email='juan@email.com',
            domicilio=self.domicilio
        )

    def test_str(self):
        self.assertEqual(str(self.persona), 'Juan Pérez — juan@email.com')

    def test_nombre_completo(self):
        self.assertEqual(self.persona.nombre_completo, 'Juan Pérez')

    def test_email_unico(self):
        # Intentar crear otra persona con el mismo email debe fallar
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Persona.objects.create(
                nombre='Pedro',
                apellido='López',
                email='juan@email.com',  # email duplicado
            )

    def test_persona_sin_domicilio(self):
        persona = Persona.objects.create(
            nombre='Ana',
            apellido='García',
            email='ana@email.com',
        )
        self.assertIsNone(persona.domicilio)


# ──────────────────────────────────────────────
#  TESTS DE VISTAS
# ──────────────────────────────────────────────

class PersonaViewsTest(TestCase):

    def setUp(self):
        # Cliente de pruebas — simula un navegador
        self.client = Client()

        # Creamos un usuario para las vistas protegidas por login
        from django.contrib.auth.models import User
        self.user = User.objects.create_user(
            username='tester',
            password='testpass123'
        )

        self.domicilio = Domicilio.objects.create(
            calle='Calle Reforma',
            no_calle='10',
            pais='Guatemala'
        )
        self.persona = Persona.objects.create(
            nombre='Juan',
            apellido='Pérez',
            email='juan@email.com',
            domicilio=self.domicilio
        )

    def test_lista_personas_requiere_login(self):
        # Sin login debe redirigir al login
        response = self.client.get(reverse('mostrar_personas'))
        self.assertEqual(response.status_code, 302)

    def test_lista_personas_con_login(self):
        self.client.login(username='tester', password='testpass123')
        response = self.client.get(reverse('mostrar_personas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Juan')

    def test_detalle_persona(self):
        self.client.login(username='tester', password='testpass123')
        response = self.client.get(reverse('detalle_persona', args=[self.persona.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'juan@email.com')

    def test_detalle_persona_no_existe(self):
        self.client.login(username='tester', password='testpass123')
        response = self.client.get(reverse('detalle_persona', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_crear_persona(self):
        self.client.login(username='tester', password='testpass123')
        response = self.client.post(reverse('nueva_persona'), {
            'nombre': 'María',
            'apellido': 'López',
            'email': 'maria@email.com',
            'domicilio': self.domicilio.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Persona.objects.filter(email='maria@email.com').exists())

    def test_eliminar_persona(self):
        self.client.login(username='tester', password='testpass123')
        response = self.client.post(reverse('eliminar_persona', args=[self.persona.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Persona.objects.filter(id=self.persona.id).exists())

    def test_busqueda_personas(self):
        self.client.login(username='tester', password='testpass123')
        response = self.client.get(reverse('buscar_personas'), {'term': 'Juan'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['nombre'], 'Juan Pérez')