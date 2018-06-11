from rest_framework.test import APITestCase

class APIProyectoTests(APITestCase):

    def test_puede_listar_los_proyectos(self):
        response = self.client.get('/api/proyectos')
        self.assertEqual(len(response.data['results']), 0)
