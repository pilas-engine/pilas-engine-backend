from rest_framework.test import APITestCase
from fixture import CODIGO


class APIProyectoTests(APITestCase):

    def test_puede_subir_un_proyecto(self):
        data = {
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

    def test_puede_enviar_un_proyecto_completo(self):
        codigo = CODIGO

        data = {
            "codigo_serializado": codigo,
            "ver_codigo": True
        }

        response = self.client.post("/proyecto/subir", data, format="json")
        self.assertEqual(response.json()['ok'], True)

    def test_puede_enviar_un_proyecto_por_partes(self):
        codigo = CODIGO

        codigo_primer_parte = codigo[:600]
        codigo_segunda_parte = codigo[600:]

        response = self.client.post("/proyecto/subir", {
            "codigo_serializado": codigo_primer_parte,
            "ver_codigo": True
        }, format="json")

        self.assertEqual(response.json()['ok'], True)

        hash = response.json()['hash']

        response = self.client.post("/proyecto/subir", {
            "codigo_serializado": codigo_segunda_parte,
            "ver_codigo": True,
            "hash": hash
        }, format="json")

        response = self.client.get("/proyecto/obtener/" + hash)
        self.assertEqual(response.json()['serializado'], CODIGO)
