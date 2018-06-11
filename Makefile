VERSION=$(shell git describe --tags)
NOMBRE=pilas-engine-backend

N=[0m
R=[00;31m
G=[01;32m
Y=[01;33m
B=[01;34m
L=[01;30m

DB_NOMBRE_DEL_DUMP= ~/Dropbox/4cores/Backups/pilas-engine-backend/pilas-engine-backend_`date +'%Y%m%d_%Hhs%Mmin'`.dump
DB_DUMP_MAS_RECIENTE=`ls -Art ~/Dropbox/4cores/Backups/pilas-engine-backend/pilas-engine-backend_*.dump  | tail -n 1`

comandos:
	@echo ""
	@echo "${B}Comandos disponibles para ${G}${NOMBRE}${N} (versión: ${VERSION})"
	@echo ""
	@echo "  ${Y}Para desarrolladores${N}"
	@echo ""
	@echo "    ${G}iniciar${N}                            Instala todas las dependencias."
	@echo "    ${G}crear_migraciones${N}                  Genera las migraciones."
	@echo "    ${G}migrar${N}                             Ejecuta las migraciones."
	@echo "    ${G}test${N}                               Ejecuta los tests."
	@echo "    ${G}test_live${N}                          Ejecuta los tests de forma continua."
	@echo "    ${G}ejecutar${N}                           Ejecuta el servidor en modo desarrollo."
	@echo "    ${G}test_server${N}                        Ejecuta el servidor en modo test."
	@echo "    ${G}shell${N}                              Ejecuta un intérprete de python."
	@echo "    ${G}version${N}                            Incrementa la versión."
	@echo "    ${G}realizar_backup_desde_produccion${N}   Incrementa la versión."
	@echo ""
	@echo ""


iniciar:
	@pipenv install

crear_migraciones:
	@pipenv run python manage.py makemigrations

migrar:
	@pipenv run python manage.py migrate --noinput

clear:
	dropdb --if-exists pilas-engine-backend-test -e; createdb pilas-engine-backend-test
	@clear;

test: clear migrar
	@echo "${G}Ejecutando tests ...${N}"
	pipenv run flake8;pipenv run python manage.py test # -v 2

test_live:
	@make test; watchmedo shell-command --patterns="*.py" --recursive --command='make test' .

ejecutar:
	@pipenv run python manage.py runserver


testserver:
	@pipenv run python manage.py testserver fixture.json

shell:
	@pipenv run python manage.py shell -i ipython

version:
	@pipenv run bumpversion patch --verbose
	@git push
	@git push --tags


realizar_backup_desde_produccion:
	@echo "${G}Creando el archivo ${DB_NOMBRE_DEL_DUMP}${N}"
	@ssh dokku@hugoruscitti.com.ar postgres:export pilas-engine-backend > ${DB_NOMBRE_DEL_DUMP}

cargar_ultimo_dump_localmente:
	@echo "${G}Se cargará el dump mas reciente: ${DB_DUMP_MAS_RECIENTE}${N}"
	dropdb --if-exists pilas-engine-backend -e; createdb pilas-engine-backend
	pg_restore --no-acl --no-owner -d pilas-engine-backend ${DB_DUMP_MAS_RECIENTE}
