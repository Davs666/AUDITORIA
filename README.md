# API de Python para Spotify

Este proyecto es una API simple para trabajar con listas de reproducción de Spotify utilizando Python.

## Instalación

Para usar esta API, necesitarás instalarla primero. Puedes hacerlo ejecutando el siguiente comando en tu terminal:

```bash
pip install spotify-api
```

## Uso

1. **Obtener credenciales de Spotify**: Necesitas obtener credenciales de autenticación de Spotify. Puedes crear una aplicación en el [Panel de Desarrolladores de Spotify](https://developer.spotify.com/dashboard/applications).

2. **Iniciar la API**: Una vez tengas las credenciales, puedes iniciar la API en tu código Python:

```python
from spotify_api import SpotifyAPI

# Configurar las credenciales de autenticación
CLIENT_ID = 'tu_client_id'
CLIENT_SECRET = 'tu_client_secret'
REDIRECT_URI = 'tu_redirect_uri'

# Iniciar la instancia de la API
spotify = SpotifyAPI(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

# Aquí puedes empezar a usar la API, por ejemplo:
# Crear una nueva lista de reproducción
playlist_id = spotify.create_playlist('Mi lista de reproducción')

# Agregar canciones a la lista de reproducción
tracks = ['spotify:track:5R0fvkvkfnUTbG7Rxjvnb2', 'spotify:track:2g8vzjoM0kbIy5Jf4gUTjL']
spotify.add_tracks_to_playlist(playlist_id, tracks)

# Editar el nombre de la lista de reproducción
spotify.change_playlist_name(playlist_id, 'Mi lista de reproducción actualizada')

# Eliminar la lista de reproducción
spotify.delete_playlist(playlist_id)
```

## Contribución

¡Si quieres contribuir, genial! Si no estás seguro de cómo hacerlo, no te preocupes, ¡todos empezamos desde algún lugar! Si tienes alguna pregunta o sugerencia, por favor háznoslo saber abriendo un issue en este repositorio.

## Licencia

Este proyecto está bajo la Licencia MIT. Puedes encontrar más detalles en el archivo [LICENSE](LICENSE).

## Contacto

Si tienes alguna pregunta o necesitas ayuda, no dudes en ponerte en contacto con nosotros a través de nuestro correo electrónico: contacto@spotify-api.com.
