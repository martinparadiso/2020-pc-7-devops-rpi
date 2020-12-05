# Manejador de versiones dockerizado

Para poder cambiar las versiones, es necesario usar un contenedor aparte con
acceso al daemon de Docker que se encargue de manejar las versiones.

## Configuración

Para que el sistema funcione de manera correcta la siguiente información debe
ser suministrada al momento de ejecutar el contenedor.

### Variables de entorno

| Variable          | Obligatoria   | Descripción                                                       |
| ----------------- | ------------- | ----------------------------------------------------------------- |
| CONTAINER_IMAGE   | Si            | Imagen de Docker a utilizar en el dispositivo                     |
| POLL_INTERVAL     | No            | Intervalo entre actualizaciones, en minutos. Por defecto es 30    |

### Archivos

| Archivo               | Path interno  | Uso                                   |
| --------------------- | ------------- | ------------------------------------- |
| `docker_config.json`  | `/app/data`   | Configuración del daemon de docker    |
| `tag`                 | `/app/data`   | Tag/versión de la imagen              |

#### `docker_config.py`

Es necesario definir la configuración del contenedor a ejecutar en un archivo
aparte. Dado que el administrador utiliza la librería `docker-py` para
comunicarse con el daemon de docker la configuración debe realizarse en un
archivo `json`, que luego internamente será convertido a un diccionario de
python:

```json
{
    "ports" : {
        "80" : 80,
        "443" : 443
    }
}
```

Los nombres de los parámetros son similares a los utilizados por `docker` y
`docker-compose`, pueden verificarse en la siguiente url, en la sección `run`.

https://docker-py.readthedocs.io/en/stable/containers.html#docker.models.containers.ContainerCollection.run

Los siguientes parámetros serán ignorados, ya que son establecidos por el
administrador:

- `detach`
- `name`

El archivo se recarga cada vez que se actualiza el contenedor, por lo que se
puede cambiar la configuración sin tener que reiniciar el administrador.

#### `tag`

Debido a que la versión (más específicamente el tag de la imágen) se puede
cambiar de manera dinámica a través de HTTP, es necesario almacenar en un
archivo aparte el tag.

En caso de que el tag que se eligió no se encuentre disponible se utiliza el tag
por defecto que es `latest`. 
