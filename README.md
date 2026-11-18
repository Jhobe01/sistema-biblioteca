# Sistema de Biblioteca

## Descripción
Sistema de información web para gestionar una biblioteca: catálogo de libros y autores, ejemplares físicos, lectores y préstamos. Está pensado para el personal bibliotecario, que registra y controla los préstamos desde una interfaz propia, y para el administrador, que gestiona todos los datos desde el panel de administración de Django.

## Integrantes
- Jhonner Bernal – Jhobe01
- Donhard Correa – Tuusje
- Ronald Carmona – ------

## Tecnologías
- Django 5.2 (base de datos SQLite)
- Bootstrap 5.3.3 y Bootstrap Icons 1.11.3, incluidos **por CDN** en `templates/base.html` (se necesita conexión a internet para ver los estilos)
- Estilos propios y paleta de colores en `static/css/estilos.css`

## Tablas principales
| Tabla | Descripción |
| --- | --- |
| `tbl_autor` | Autores de los libros |
| `tbl_libro` | Libros del catálogo (un registro por título o tomo) |
| `tbl_ejemplar` | Copias físicas de cada libro (entidad débil de `tbl_libro`, relación 1:N) |
| `tbl_lector` | Personas que piden libros prestados |
| `tbl_prestamo` | Cabecera del préstamo: lector, fechas y estado (relación 1:N con lector) |
| `tbl_detalle_prestamo` | Tabla intermedia del N:M entre préstamos y ejemplares |
| `tbl_libro_autor` | Tabla intermedia del N:M entre libros y autores |

## Diagramas
- Actores: docs/diagrama_actores.png
- Entidad-relación: docs/diagrama_er.png

## Funcionalidades
- **Proceso con CRUD completo: Préstamos** (lector y ejemplares prestados), desde la interfaz:
  - Listar: `/prestamos/`
  - Crear: `/prestamos/nuevo/`
  - Detalle: `/prestamos/<id>/`
  - Editar: `/prestamos/<id>/editar/`
  - Eliminar (con página de confirmación): `/prestamos/<id>/eliminar/`
- Funcionalidades adicionales:
  - Inicio y cierre de sesión (`/ingresar/`, `/salir/`); todas las páginas exigen sesión (`@login_required`).
  - Panel de inicio con resumen (`/`).
  - Catálogo de libros con búsqueda por título, ISBN o autor y filtro por género (`/libros/`, `/libros/<id>/`).
  - Búsqueda por lector o número y filtro por estado en la lista de préstamos, con paginación.
  - Validaciones: fecha límite no anterior a la del préstamo, ejemplares no repetidos, al menos un ejemplar por préstamo y solo ejemplares disponibles.
  - El estado de los ejemplares se actualiza solo (prestado/disponible) y el préstamo pasa a "devuelto" cuando se devuelven todos sus ejemplares.
  - Mensajes de confirmación y de error.
- El panel de administración sigue disponible en `/admin/`.

## Cómo ejecutar el proyecto
1. git clone <https://github.com/Jhobe01/sistema-biblioteca>
2. python -m venv venv
3. venv\Scripts\activate   (Linux/macOS: source venv/bin/activate)
4. pip install -r requirements.txt
5. python manage.py migrate
6. python manage.py runserver

Luego abre http://127.0.0.1:8000/ e inicia sesión.

## Usuarios de prueba
- Superusuario del admin: usuario `Jhobe` y contraseña `LinkStart`

## Licencia y uso

Proyecto desarrollado con fines académicos.