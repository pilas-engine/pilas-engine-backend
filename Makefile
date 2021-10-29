VERSION=$(shell git describe --tags)
NOMBRE=pilas-engine-backend

N=[0m
R=[00;31m
G=[01;32m
Y=[01;33m
B=[01;34m
L=[01;30m

DB_NOMBRE_DEL_DUMP=~/Dropbox/backups/pilas-engine-backend/pilas-engine-backend_`date +'%Y%m%d_%Hhs%Mmin'`.dump
DB_DUMP_MAS_RECIENTE=`ls -Art ~/Dropbox/backups/pilas-engine-backend/pilas-engine-backend_*.dump  | tail -n 1`

comandos:
	@echo ""
	@echo "${B}Comandos disponibles para ${G}${NOMBRE}${N} (versión: ${VERSION})"
	@echo ""
	@echo "  ${Y}Para desarrolladores${N}"
	@echo ""
	@echo "    ${G}iniciar${N}                   Instala todas las dependencias."
	@echo "    ${G}crear_migraciones${N}         Genera las migraciones."
	@echo "    ${G}migrar${N}                    Ejecuta las migraciones."
	@echo "    ${G}actualizar_pilas${N}          Actualiza pilas desde un directorio externo."
	@echo "    ${G}test${N}                      Ejecuta los tests."
	@echo "    ${G}test_live${N}                 Ejecuta los tests de forma continua."
	@echo "    ${G}ejecutar${N}                  Ejecuta el servidor en modo desarrollo."
	@echo "    ${G}test_server${N}               Ejecuta el servidor en modo test."
	@echo "    ${G}shell${N}                     Ejecuta un intérprete de python."
	@echo "    ${G}version${N}                   Incrementa la versión."
	@echo "    ${G}deploy${N}                    Realiza un deploy de la aplicación."
	@echo "    ${G}realizar_backup_desde_produccion${N}   "
	@echo "    ${G}cargar_ultimo_dump_localmente{N}   "
	@echo ""
	@echo ""


iniciar:
	@pipenv install

crear_migraciones:
	@pipenv run python manage.py makemigrations

migrar:
	@pipenv run python manage.py migrate --noinput

deploy:
	@git push dokku master

clear:
	dropdb --if-exists pilas-engine-backend-test -e; createdb pilas-engine-backend-test
	@clear;

test: clear migrar
	@echo "${G}Ejecutando tests ...${N}"
	pipenv run flake8; pipenv run python manage.py test 

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

actualizar_pilas:
	@cp ../pilas-engine/public/pilas-engine.js static/
	@cp ../pilas-engine/public/imagenes-0.png static/
	@cp ../pilas-engine/public/imagenes.json static/
	@cp ../pilas-engine/public/ceferino.json static/
	@cp ../pilas-engine/public/ceferino.png static/
	@cp ../pilas-engine/public/ceferino.scon static/
	@cp ../pilas-engine/public/nineslice.js static/
	@cp ../pilas-engine/public/phaser.js static/
	@cp ../pilas-engine/public/robot.json static/
	@cp ../pilas-engine/public/robot.png static/
	@cp ../pilas-engine/public/robot.scon static/
	@cp -r ../pilas-engine/public/fuentes static/
	@cp -r ../pilas-engine/public/sonidos static/

realizar_backup_desde_produccion:
	@echo "${G}Creando el archivo ${DB_NOMBRE_DEL_DUMP}${N}"
	@ssh dokku@pilas-engine.com.ar postgres:export pilas-engine-backend > ${DB_NOMBRE_DEL_DUMP}
	@rsync -vP "root@pilas-engine.com.ar:/var/lib/dokku/data/storage/pilas-engine-backend/imagenes/*" ./media_archivos_locales/imagenes/
	@rsync -vP "root@pilas-engine.com.ar:/var/lib/dokku/data/storage/pilas-engine-backend/proyectos/*" ./media_archivos_locales/proyectos/

cargar_ultimo_dump_localmente:
	@echo "${G}Se cargará el dump mas reciente: ${DB_DUMP_MAS_RECIENTE}${N}"
	dropdb --if-exists pilas-engine-backend -e; createdb pilas-engine-backend
	pg_restore --no-acl --no-owner -d pilas-engine-backend ${DB_DUMP_MAS_RECIENTE}
