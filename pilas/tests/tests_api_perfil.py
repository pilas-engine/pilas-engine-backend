from rest_framework.test import APITestCase
from pilas.tests.utilidades import autenticar

class APIPerfilTests(APITestCase):

    def test_puede_listar_los_perfiles(self):
        autenticar(self.client)
        response = self.client.get('/api/perfiles')
        self.assertEqual(len(response.data['results']), 1)
