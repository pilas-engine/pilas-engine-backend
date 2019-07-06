from rest_framework.test import APITestCase


class APIProyectoTests(APITestCase):

    def test_puede_subir_un_proyecto(self):
        data = {
            "codigo": "demo {}",
            "codigo_serializado": "ASDASD",
        }

        response = self.client.post("/proyecto/subir", data, format="json")
        self.assertEqual(response.json()["ok"], True)
        self.assertTrue(response.json()["hash"])

    def test_obtiene_un_error_al_subir_un_proyecto_incompleto(self):
        data = {}
        response = self.client.post("/proyecto/subir", data, format="json")
        self.assertEqual(response.json()["ok"], False)
        self.assertEqual(response.json()["error"], "Faltan parámetros")
