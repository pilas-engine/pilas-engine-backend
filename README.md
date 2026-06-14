# pilas-engine-backend

Backend que permite guardar juegos y vincular usuarios a proyectos

[![CircleCI](https://circleci.com/gh/pilas-engine/pilas-engine-backend.svg?style=svg)](https://circleci.com/gh/pilas-engine/pilas-engine-backend)

## ¿Cómo usar esto?

Primero se tiene que crear un entorno virtual de esta forma:

```
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

 y luego aplicar migraciones y ejecutar el servidor:
 
```
make migrar
make ejecutar
```
