# Proyecto final Programacion- Flask 

## Descripción del Proyecto

Este proyecto es una aplicación web para la gestión de películas, diseñada para permitir a los usuarios registrados agregar, editar y eliminar información sobre películas, así como comentar sobre ellas. Los usuarios no registrados pueden acceder en modo público con funcionalidades limitadas.

- Funcionalidades Principales
* Gestión de Películas: Cada película incluye título, año, director, género, sinopsis y un enlace a una imagen representativa. Los directores y géneros se eligen de listas predefinidas.
* Comentarios: Los usuarios pueden comentar sobre las películas, y estas opiniones influyen en las restricciones de edición y eliminación.
* Filtrado y Consulta: Posibilidad de seleccionar un director y obtener todas sus películas.

- Control de Acceso:
* Los usuarios registrados pueden agregar, editar y eliminar películas con restricciones específicas basadas en la presencia de comentarios de otros usuarios.
* Los usuarios no registrados no pueden editar ni eliminar películas.

- Endpoints de Servicios Web
  El sistema proporciona servicios web a través de endpoints que devuelven documentos en formato JSON, incluyendo:
* Lista de directores presentes en la plataforma.
* Lista de géneros presentes en la plataforma.
* Lista de películas dirigidas por un director en particular.
* Lista de películas con imagen de portada agregada.
* ABM (Alta, Baja, Modificación) de cada película.

- Usuarios y Autenticación
No se requiere la funcionalidad de registro de nuevos usuarios; se utiliza un conjunto de usuarios precargados que pueden acceder al sistema mediante una pantalla de login. Los usuarios no registrados pueden acceder al modo público.
