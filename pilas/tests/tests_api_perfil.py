from rest_framework.test import APITestCase
from pilas.tests.utilidades import autenticar
from pilas.models.perfil import Perfil

class APIPerfilTests(APITestCase):

    def test_puede_listar_los_perfiles(self):
        autenticar(self.client)
        response = self.client.get('/api/perfiles')
        self.assertEqual(len(response.data['results']), 1)

    def test_se_puede_autenticar(self):
        self.crear_usuario()

        auth_data = {
            'username': 'hugo',
            'password': 'dev123'
        }

        response = self.client.post('/api-token-auth/', auth_data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in response.data)

    def test_se_puede_autenticar_y_obtener_datos_del_usuario(self):
        self.crear_usuario()

        auth_data = {
            'username': 'hugo',
            'password': 'dev123'
        }

        response = self.client.post('/api-token-auth/', auth_data, format='json')

        self.assertEqual(response.status_code, 200)
        token = response.data["token"]

        #response = self.client.get(f"/perfiles/obtener-perfil-desde-token/{token}", auth_data, format='json')


    def test_falla_si_el_password_es_incorrecto(self):
        self.crear_usuario()
        auth_data = {
            'username': 'hugo',
            'password': 'asdfasdfasdfasdfasdf123',
        }

        response = self.client.post('/api-token-auth/', auth_data, format='json')
        self.assertEqual(response.status_code, 400)

    def crear_usuario(self):
        mi_perfil = Perfil.crear_con_usuario("hugo", "hugo")
        usuario = mi_perfil.user
        usuario.set_password("dev123")
        usuario.save()
        return mi_perfil

    def test_puede_crear_y_autenticar_un_usuario_nuevo(self):
        datos = {
            'usuario': 'pepe',
            'email': 'pepe@gmail.com',
            'password': '123',
        }

        response = self.client.post('/perfiles/crear-usuario', datos, format='json')
        self.assertEqual(response.status_code, 200)



        # Una vez creado el usuario se asegura de poder ingresar.

        auth_data = {
            'username': 'pepe',
            'password': '123'
        }

        response = self.client.post('/api-token-auth/', auth_data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in response.data)

    def test_falla_si_el_usuario_ya_existe(self):
        datos = {
            'usuario': 'pepe',
            'email': 'pepe@gmail.com',
            'password': '123',
        }

        response = self.client.post('/perfiles/crear-usuario', datos, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/perfiles/crear-usuario', datos, format='json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()["error"], "El usuario ya existe")

    def test_puede_consultar_la_sesion(self):
        response = self.client.get('/sesion/')
        print(response.data)

    def _____DISABLED____se_puede_autenticar_y_cerrar_session(self):
        self.crear_usuario()

        auth_data = {
            'username': 'hugo',
            'password': 'dev123'
        }

        response = self.client.post('/api-token-auth/', auth_data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in response.data)
        token = response.data['token']

        self.client.credentials(authorization='Token ' + token)
        response = self.client.get('/api-token-logout/', format='json')
        self.assertEqual(response.status_code, 200)
