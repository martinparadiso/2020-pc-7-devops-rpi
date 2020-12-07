# CI/CD con Docker, Raspberry Pi y Github Actions

## Como usar

Primero necesario habilitar la interfaz I2C en la Raspberry:

```
raspi-config > 5 Interfacing Options > P5C I2C
```

La manera más sencilla de hacer un deploy es mediante docker-compose:

```yaml
version: "3"

services:

        temperature_reader:
                image: ghcr.io/martinparadiso/temperature_reader:latest
                container_name: temperature_reader
                ports: 
                        - 5000:5000
                devices:
                        - "/dev/i2c-1"
```

## Secrets para build

| Secret        | Funcion                                              |
| ------------- | ---------------------------------------------------- |
| CR_PAT        | Es necesario proporcionar acceso al registro de github tal como se especifica en https://github.com/marketplace/actions/docker-login#github-container-registry |
| IMAGE_PATH    | El nombre de la imagen. En este caso como se va a guardar en Github es necesario que sea de la forma "ghcr.io/<user>/<nombre>" donde el user es el dueño del repositorio |
| DASHBOARD_URL | URL (o IP) de la Dashboard del sistema, para poder indicarle que una build fue satisfactoria |
