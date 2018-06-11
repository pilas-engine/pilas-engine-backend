import sys
import io
import os

ROJO = '\x1b[31m'
AZUL = '\x1b[34m'
RESTAURAR = '\x1b[0m'
#print('\x1b[31mfoo\x1b[0m')


if len(sys.argv) != 4:
    print(ROJO + "Numero incorrecto de argumentos." + RESTAURAR)
    print("Uso:")
    print("")
    print("  python generar.py aplicacion modulo modulo_plural")
    print("")
    print("Por ejemplo:")
    print("")
    print(AZUL + "  python generar.py spider Sociedad sociedades" + RESTAURAR)
    print("")
    sys.exit(1)

aplicacion = sys.argv[1]
modelo = sys.argv[2]
modelo_plural = sys.argv[3]
modelo_minusculas = modelo.lower()

archivos = [
    "templates/admin.py"
]

def obtener_ruta_absoluta(origen):
    este_directorio = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(este_directorio, origen)

def sustituir_nombres(linea):
    linea = linea.replace('Modelo', modelo)
    linea = linea.replace('modelo_plural', modelo_plural)
    linea = linea.replace('aplicacion', aplicacion)
    linea = linea.replace('modelo', modelo_minusculas)
    return linea

def aplicar_template(origen, destino):
    print("- Creando el archivo {}".format(destino))
    archivo = io.open(destino, 'w')

    for line in io.open(obtener_ruta_absoluta(origen), 'r'):
        line = sustituir_nombres(line)
        archivo.write(line)

    archivo.close()

def imprimir_ayuda_sobre_urls():
    ejemplo = [
        'from aplicacion.views.modelo import ModeloViewSet',
        '',
        'router.register("modelo_plural", ModeloViewSet)'
    ]

    for linea in ejemplo:
        print(AZUL + sustituir_nombres(linea) + RESTAURAR)

def imprimir_ayuda_sobre_admin():
    ejemplo = [
        'from aplicacion.admin_classes.modelo import Modelo, ModeloAdmin',
        '',
        'admin.site.register(Modelo, ModeloAdmin)'
    ]

    for linea in ejemplo:
        print(AZUL + sustituir_nombres(linea) + RESTAURAR)

print("")
aplicar_template("templates/admin.py", "%s/admin_classes/%s.py" % (aplicacion, modelo_minusculas))
aplicar_template("templates/model.py", "%s/models/%s.py" % (aplicacion, modelo_minusculas))
aplicar_template("templates/serializador.py", "%s/serializers/%s.py" % (aplicacion, modelo_minusculas))
aplicar_template("templates/view.py", "%s/views/%s.py" % (aplicacion, modelo_minusculas))
aplicar_template("templates/tests.py", "%s/tests/tests_api_%s.py" % (aplicacion, modelo_minusculas))

print("")
print("Se crearon todos los archivos, ahora solo queda que")
print("incluyas estas dos lineas en el archivo urls.py:")
print("")

imprimir_ayuda_sobre_urls()
print("")

print("y estas dos lineas en el archivo admin.py:")
print("")
imprimir_ayuda_sobre_admin()
print("")

print("Por último, recodá ejecutar los comandos: make crear_migraciones y make migrar")
print("")
