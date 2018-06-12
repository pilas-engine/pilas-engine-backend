from rest_framework.test import APITestCase
from pilas.tests.utilidades import autenticar

class APIProyectoTests(APITestCase):

    def test_puede_listar_los_proyectos(self):
        autenticar(self.client)
        response = self.client.get('/api/proyectos')
        self.assertEqual(len(response.data['results']), 0)
