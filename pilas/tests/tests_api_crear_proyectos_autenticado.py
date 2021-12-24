from rest_framework.test import APITestCase
from pilas.tests.utilidades import autenticar
from pilas.models.perfil import Perfil
from pilas.models.proyecto import Proyecto


class APICrearProyectosAutenticadoTests(APITestCase):

    def test_puede_autenticarse_y_registrar_proyecto(self):
        # crea el usuario
        datos = {
            'usuario': 'hugo',
            'email': 'hugo@gmail.com',
            'password': 'dev123',
        }

        response = self.client.post('/perfiles/crear-usuario', datos, format='json')
        self.assertEqual(response.status_code, 200)

        # obtiene token
        auth_data = {
            'username': 'hugo',
            'password': 'dev123',
        }

        response = self.client.post('/login/', auth_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["token"])

        # No hay ningún proyecto por el momento
        self.assertEqual(Proyecto.objects.count(), 0)

        # Sube un proyecto simple
        data = {
            "codigo_serializado": "ASDASD",
        }

        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        response = self.client.post("/proyecto/subir", data, format="json")
        self.assertEqual(response.json()["ok"], True)
        self.assertTrue(response.json()["hash"])

        # Valida que se creó el proyecto
        self.assertEqual(Proyecto.objects.count(), 1)

        # Obtiene el usuario creado
        perfil = Perfil.objects.get(nombre="hugo")
        self.assertEqual(perfil.proyectos.count(), 1)
