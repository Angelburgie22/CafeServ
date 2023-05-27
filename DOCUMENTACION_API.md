# Documentación de la API CafeServ

## Protocolo estándar para requests

1. Se envía el request en al servidor HTTP. Si el método usado es `POST`, se
debe enviar un diccionario JSON con los parametros. Si es `GET`, los parametros
van como se indique.
Regularmente las rutas se encuentran bajo /api/

2. El servidor se encarga de validar el request, lo procesa y envía la respuesta.

3. El cliente procesa la respuesta:

    - Se analiza el código HTTP devuelto. Si el código es erroneo (400-599), la
        operación se toma automáticamente como inválida/fallida.

    - Si, en cambio, el código es ok (2xx), se analiza el diccionario JSON: si
        el miembro 'success' no es verdadero, la operación se toma como fallida.

4. El cliente actúa sobre la respuesta.

Toda respuesta del servidor tiene el miembro `'success'`, y en caso de ser este
falso, la razón del fallo se indica en el miembro `'reason'`

## API

### *auth*
Llamadas para login del usuario

Locación:
`/api/auth/`

#### `/create`
Crea una sesión de usuario. Devuelve un identificador al usuario.

Método:
`POST`

Argumentos:
- `user`: Email o nombre de usuario.
- `passwd`: Contraseña del usuario
- `token`: Token CSRF. Obtenido de `/api/auth/get_login_token` (temporal, en un
    futuro puede cambiar).

Respuesta:
- `identifier`: El tipo de identificador devuelto para demostrar el inicio de
    sesión. Por el momento, el único valor válido es `cookies`.

#### `/close`
Cierra una sesión abierta.

Método:
`DELETE`

Argumentos:
Ninguno

Respuesta:
Ninguna

### *Carta*
API para listado y búsqueda de platillos.

Locación:
`/api/carta`

#### `/info_platillo`
Describe la información del platillo especificado.

Método:
`GET`

Argumentos:
El platillo se especifica por medio de una subruta.
Ejemplo: `/api/carta/info_platillo/72` (SUJETO A CAMBIO, después se normalizará
    la api para usar JSON o parametros de query HTTP)

Respuesta:
- `id`: El id del platillo
- `nombre`: El nombre a desplegar del platillo
- `adimentos`: Lista de adimentos disponibles para añadir a la orden:
    - `id`: id del adimento
    - `nombre`: Nombre del adimento

