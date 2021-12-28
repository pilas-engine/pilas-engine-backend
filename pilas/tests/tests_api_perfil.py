from rest_framework.test import APITestCase
from pilas.models.proyecto import Proyecto
from pilas.tests.utilidades import autenticar
from pilas.models.perfil import Perfil

class APIPerfilTests(APITestCase):

    def test_puede_listar_los_perfiles(self):
        autenticar(self.client)
        response = self.client.get('/api/perfiles')
        self.assertEqual(response.status_code, 200)

    def test_se_puede_autenticar(self):
        self.crear_usuario()

        auth_data = {
            'username': 'hugo',
            'password': 'dev123'
        }

        response = self.client.post('/login/', auth_data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in response.data)

    def test_se_puede_autenticar_y_obtener_datos_del_usuario(self):
        self.crear_usuario()

        auth_data = {
            'username': 'hugo',
            'password': 'dev123'
        }

        response = self.client.post('/login/', auth_data, format='json')

        self.assertEqual(response.status_code, 200)
        token = response.data["token"]

        # Si consulta mi-perfil sin token falla
        response = self.client.get(f"/perfiles/mi-perfil")
        self.assertEqual(response.status_code, 401)

        # Si consulta mi-perfil con un token retorna los datos
        # del usuario
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(f"/perfiles/mi-perfil")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['nombre'], 'hugo')

    def test_puede_consultar_los_juegos_de_un_usuario(self):
        perfil = self.crear_usuario()

        auth_data = {
            'username': 'hugo',
            'password': 'dev123'
        }

        response = self.client.post('/login/', auth_data, format='json')

        self.assertEqual(response.status_code, 200)
        token = response.data["token"]

        # En total se hacen 3 proyectos, pero solo dos son del
        # perfil autenticado.
        Proyecto.objects.create(hash="1")
        Proyecto.objects.create(hash="2", perfil=perfil)
        Proyecto.objects.create(hash="3", perfil=perfil)

        # Si consulta mi-perfil con un token retorna los datos
        # del usuario
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(f"/perfiles/mis-juegos")

        self.assertEqual(response.data['total'], 2)


    def test_falla_si_el_password_es_incorrecto(self):
        self.crear_usuario()
        auth_data = {
            'username': 'hugo',
            'password': 'asdfasdfasdfasdfasdf123',
        }

        response = self.client.post('/login/', auth_data, format='json')
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

        response = self.client.post('/login/', auth_data, format='json')

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
        self.crear_usuario()

        auth_data = {
            'username': 'hugo',
            'password': 'dev123'
        }

        response = self.client.post('/login/', auth_data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in response.data)
        token = response.data['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/sesion/')

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 200)

