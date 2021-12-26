from rest_framework.test import APITestCase
from pilas.tests.utilidades import autenticar
from pilas.models.tag import Tag

class APIBuscarEtiquetasTests(APITestCase):

    def test_puede_buscar_por_etiquetas(self):
        Tag.objects.create(nombre="club")
        Tag.objects.create(nombre="club-de-chicas-programadoras")
        Tag.objects.create(nombre="pilas")

        response = self.client.get('/buscar-etiquetas/?query=club')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        response = self.client.get('/buscar-etiquetas/?query=pilas')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
