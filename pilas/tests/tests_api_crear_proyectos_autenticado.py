from rest_framework.test import APITestCase
from pilas.tests.utilidades import autenticar
from pilas.models.perfil import Perfil

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

        response = self.client.post('/api-token-auth/', auth_data, format='json')
        self.assertEqual(response.status_code, 200)

        self.assertTrue(response.data["token"], 200)




