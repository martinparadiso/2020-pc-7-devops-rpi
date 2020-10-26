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
