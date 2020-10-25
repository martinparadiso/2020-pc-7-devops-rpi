# Lector de temperatura dentro de Docker

Este contenedor simplemente devuelve la temperatuara en formato json a través
del puerto 5000. Para ejecutarlo es necesario previamente haber habilitado
la interfaz I2C en la Raspberry Pi. Para correrlo es necesario darle el
dispositivo I2C.

Para construir la imagen, y ejecutarla, supiniendo que el dispositivo se llama
`/dev/i2c-1` (puede variar, en alguna documentación aparce como 0):

```sh
docker build --tag temp_reader .
docker run --device /dev/i2c-1 -d temp_reader
```

Para hacer la petición hay que conseguir la IP del contenedor con 
`docker inspect <container_name>` y hacer un curl:

```sh
curl <container_ip>:5000
```

## Notas

- Actualmente está ejecutando el server de desarrollo que viene con Flask, lo 
  cual es altamente no recomendado.
- El puerto utilizado es el 5000, por default de Flask

