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
