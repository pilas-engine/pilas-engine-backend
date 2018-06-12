from pilas.models.perfil import Perfil

def autenticar(client):
    perfil = Perfil.crear_con_usuario("nombre", "usuario")
    client.login(username='usuario', login='123')
    client.force_authenticate(user=perfil.user)
