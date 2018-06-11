from rest_framework.test import APITestCase

class APIModeloTests(APITestCase):

    def test_puede_listar_los_modelo_plural(self):
        response = self.client.get('/api/modelo_plural')
        self.assertEqual(len(response.data['results']), 0)
