# HellP2P

El proyecto es una red peer to peer (P2P), que utiliza TCP/IP para comunicarse. El proyecto se encuentra en desarrollo, asi que sientete en libertad de clonarlo y realizar los cambios que desees. :D.

## Use

Para iniciar el cliente-servidor de p2p, ejecutar:

```shell
python3 p2p.py user.pf
```

Donde user.pf es el archivo de perfil de usuario dentro de la carpeta profiles.

## Estructura del archivo profile

```json
{
    "myself": "Cain",
    "port": 7015,
    "neighbors": {
        "Timoteo": [
            "127.0.0.1",
            7014
        ],
        "Judas": [
            "127.0.0.1",
            7016
        ],
        "Faraon": [
            "127.0.0.1",
            7017
        ]
    }
}
```

## Pruebas

Para crear una red P2P de prueba podemos ejecutar el archivo **grafos.py**, que genera un grafo de 30 nodos y sus respectivos archivos **.pf** en el directorio **profile**. Este codigo utiliza el archivo **nombres.txt** para especificar los nombre a los nodos.

```shell
python3 grafos-view/grafos.py
```

Luego de esto, seleccionamos dos nombres del grafo y configuramos la siguiente linea en el archivo **test.py**.

```python
users = ['nodoI', 'nodoF']
```

Ejecutar el archivo python.

```shell
python3 test.py
```

Finalmente ejecutar los dos nodos manualmente, para realizar las pruebas de envio.

```shell
python3 p2p.py nodoI
```

```shell
python3 p2p.py nodoF
```

## I'm stuck, step programmer...?

Si es que el codigo empieza a generar fallas y el uso del CPU se dispara... Ejecuta el siguiente comando para detener los procesos de los otros nodos que se ejecutan en segundo plano.

```shell
python3 clear-ps.py
```

*Existe la posibilidad que si tienes otro codigo en python externo al proyecto que ejecute un servidor de escucha usando python, tambien se muera XD.*

## TO-DO
- Configurar un TTL para los envios.
- Cifrado de mensajes.
- Identificar cada usuario con un UID.
- Optimizar envios de mensajes (no entrar en bucles).

By DsDs, for now XD