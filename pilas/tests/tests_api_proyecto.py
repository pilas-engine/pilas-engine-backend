from rest_framework.test import APITestCase
from fixture import CODIGO
from pilas.models.proyecto import Proyecto
from pilas.models.tag import Tag


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
            "ver_codigo": True,
            "cantidad_de_partes": 2,
            "numero_de_parte": 0,
        }, format="json")

        self.assertEqual(response.json()['ok'], True)

        hash = response.json()['hash']

        response = self.client.post("/proyecto/subir", {
            "codigo_serializado": codigo_segunda_parte,
            "ver_codigo": True,
            "hash": hash,
            "cantidad_de_partes": 2,
            "numero_de_parte": 1,
        }, format="json")

        response = self.client.get("/proyecto/obtener/" + hash)
        self.assertEqual(response.json()['serializado'], CODIGO)

    def test_puede_obtener_una_lista_de_proyectos_para_explorar(self):
        response = self.client.get("/explorar/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["proyectos"]), 0)

        for x in range(38):
            Proyecto.objects.create(hash="123")

        response = self.client.get("/explorar/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["proyectos"]), 10)
        self.assertEqual(response.data["total"], 38)
        self.assertEqual(response.data["paginas"], 4)
        self.assertEqual(response.data["pagina"], 1)

        response = self.client.get("/explorar/?pagina=4")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["proyectos"]), 8)


    def test_puede_filtrar_proyectos_con_etiquetas(self):
        codigo = CODIGO

        data1 = {
            "codigo_serializado": codigo,
            "tags": ['demo'],
            "ver_codigo": True
        }

        data2 = {
            "codigo_serializado": codigo,
            "tags": ['demo', 'otra-etiqueta'],
            "ver_codigo": True
        }

        # Un proyecto se crea sin etiquetas.
        Proyecto.objects.create(hash="123")

        # Otro proyecto tiene una sola etiqueta "demo".
        response = self.client.post("/proyecto/subir", data1, format="json")
        self.assertEqual(response.json()['ok'], True)

        # El tercer proyecto, tiene dos etiquetas "demo" y "otra-etiqueta".
        response = self.client.post("/proyecto/subir", data2, format="json")
        self.assertEqual(response.json()['ok'], True)

        # Dados tres proyectos, dos con etiquetas, la
        # vista principal tiene que retornar los 3 juntos.
        response = self.client.get("/explorar/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["proyectos"]), 3)

        # Si solicita solamente los que tiene la etiqueta "demo"
        # tiene que retornar solo dos.
        response = self.client.get("/explorar/?etiqueta=demo")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["proyectos"]), 2)

        # Si solicita los que tengan una etiqueta inexistente debería
        # retorna vacío.
        response = self.client.get("/explorar/?etiqueta=test123")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["proyectos"]), 0)

        # Si pide los que tiene etiqueta "otra-etiqueta" tiene que
        # aparecer solo uno.
        response = self.client.get("/explorar/?etiqueta=otra-etiqueta")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["proyectos"]), 1)
