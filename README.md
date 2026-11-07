<div align="center">

# Sistema de Gestión Bibliotecaria

**Proyecto académico · Ingeniería de Sistemas · Django + SQLite**

[Descripción](#-descripción) · [Modelo de datos](#-modelo-de-datos) · [Instalación](#-instalación-y-ejecución) · [Administración](#-acceso-al-panel-administrativo) · [Diagramas](#-documentación-visual)

</div>

---

## Descripción

Sistema de información para administrar las operaciones básicas de una biblioteca. Permite organizar el catálogo bibliográfico y sus autores, controlar los ejemplares físicos, registrar lectores y gestionar préstamos y devoluciones desde el panel de administración de Django.

Este repositorio corresponde a un ejercicio académico. Está diseñado para ejecutarse localmente con SQLite y puede ampliarse posteriormente con una interfaz pública para lectores.

## Objetivos

- Centralizar la información de libros y autores.
- Diferenciar cada libro de sus copias físicas mediante ejemplares con código de inventario.
- Mantener el registro de lectores.
- Registrar préstamos y asociar uno o varios ejemplares a cada préstamo.
- Guardar la fecha de devolución de cada ejemplar prestado.
- Aplicar relaciones normalizadas y administrar los registros desde Django Admin.

## Integrantes

- Integrante 1: **Jhonner Bernal**
- Integrante 2: **Donhard Correa**
- Integrante 3: **Ronald Carmona**


## Tecnologías

| Tecnología | Uso |
|---|---|
| Python | Lenguaje principal |
| Django 5.2 | Framework web, ORM y panel administrativo |
| SQLite | Base de datos local |
| HTML/CSS del admin | Interfaz administrativa proporcionada por Django |
| Git y GitHub | Control de versiones y entrega del proyecto |

## Funcionalidades

- **Autores:** registrar nombre, apellido, nacionalidad y fecha de nacimiento.
- **Libros:** gestionar título, ISBN, editorial, año, género y descripción.
- **Ejemplares:** identificar cada copia física, ubicación y estado (disponible, prestado, mantenimiento o perdido).
- **Lectores:** registrar documento, nombres, apellidos, correo, teléfono y estado de actividad.
- **Préstamos:** asociar un lector, fechas, estado y observaciones.
- **Detalles del préstamo:** vincular cada préstamo con ejemplares concretos y registrar su devolución y condición.
- **Autoría:** permitir que un libro tenga varios autores y que un autor participe en varios libros.
- **Administración integrada:** búsquedas, filtros y formularios inline para ejemplares, autores de un libro y detalles de préstamo.

## Modelo de datos

El diseño utiliza siete tablas principales:

| Tabla | Propósito | Tipo de entidad |
|---|---|---|
| `tbl_autor` | Datos de autores | Fuerte |
| `tbl_libro` | Datos bibliográficos | Fuerte |
| `tbl_ejemplar` | Copias físicas asociadas a un libro | Débil / dependiente |
| `tbl_lector` | Personas que solicitan libros | Fuerte |
| `tbl_prestamo` | Cabecera de cada préstamo | Fuerte |
| `tbl_detalle_prestamo` | Ejemplares incluidos en un préstamo y devolución | Intermedia |
| `tbl_libro_autor` | Relación muchos a muchos entre libros y autores | Intermedia |

### Relaciones y cardinalidades

- **Libro 1:N Ejemplar:** un libro puede tener múltiples copias físicas; cada ejemplar pertenece a un libro.
- **Lector 1:N Préstamo:** un lector puede tener varios préstamos; cada préstamo pertenece a un lector.
- **Préstamo N:M Ejemplar:** se resuelve mediante `DetallePrestamo`, que guarda la fecha y condición de devolución por ejemplar.
- **Libro N:M Autor:** se resuelve mediante `LibroAutor`.

**Convención de nombres:** tablas `tbl_` + nombre en singular; llave primaria `pk_` + prefijo + `_id` (p. ej. `pk_lib_id`); llave foránea `fk_` + prefijo de la tabla referenciada + `_id` (p. ej. `fk_lib_id`); columnas normales con el prefijo de su tabla (p. ej. `lib_titulo`). Los modelos de Django usan exactamente esos nombres.

Las tablas intermedias evitan guardar listas de autores o ejemplares dentro de una sola columna. Los ISBN, documentos, correos y códigos de inventario tienen restricciones de unicidad. Los modelos usan claves foráneas y tipos de datos adecuados.

## Documentación visual

Los diagramas se encuentran en `docs/`:

- [`diagrama_actores.png`](docs/diagrama_actores.png): actores y casos de uso del sistema.
- [`diagrama_er.png`](docs/diagrama_er.png): tablas, columnas, claves y cardinalidades.

## Estructura del proyecto

```text
sistema-biblioteca/
├── autores/                 # Modelo y administración de autores
├── config/                  # Configuración principal de Django
├── detalle_prestamo/        # Ejemplares y devolución por préstamo
├── docs/                    # Diagramas (actores y ER)
├── ejemplares/              # Copias físicas de cada libro
├── lectores/                # Personas lectoras
├── libro_autor/             # Relación N:M entre libro y autor
├── libros/                  # Modelo principal de libros
├── prestamos/               # Cabecera del préstamo
├── .gitignore
├── db.sqlite3               # Base de datos con datos de prueba
├── manage.py
├── README.md
└── requirements.txt
```

## Instalación y ejecución

### 1. Requisitos previos

Instala Python 3.10 o superior y Git. Comprueba las instalaciones:

```bash
python --version
pip --version
git --version
```

### 2. Descargar o clonar el repositorio

```bash
git clone https://github.com/Jhobe01/sistema-biblioteca.git
cd sistema-biblioteca
```

Si ya descargaste este proyecto como ZIP, descomprímelo y abre la carpeta `sistema-biblioteca` en Visual Studio Code.

### 3. Crear y activar el entorno virtual

**Windows (PowerShell):**

```powershell
python -m venv venv
.env\Scripts\Activate.ps1
```

**Windows (CMD):**

```bat
python -m venv venv
venv\Scriptsctivate.bat
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Instalar dependencias

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Aplicar migraciones

Las carpetas `migrations/` ya vienen en el repositorio. La base `db.sqlite3` incluida ya está migrada y con datos, pero si quieres reconstruirla desde cero:

```bash
python manage.py migrate
```

Si modificas algún modelo, ejecuta antes `python manage.py makemigrations` y vuelve a migrar.

### 6. Superusuario

| Usuario | `Jhobe` |
| Contraseña | `LinkStart` |

> Son credenciales de práctica solo para este proyecto académico. Si reconstruyes la base, crea uno nuevo con `python manage.py createsuperuser`.

### 7. Iniciar el servidor

```bash
python manage.py runserver
```

Abre [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) e inicia sesión con el superusuario que acabas de crear.

## Acceso al panel administrativo

Django Admin permite crear, consultar, editar y eliminar registros según los permisos de la cuenta. Cada modelo dispone de columnas visibles, búsqueda y filtros. En el formulario de un libro se pueden administrar los ejemplares y las relaciones de autoría; en el formulario de préstamo se agregan los detalles correspondientes.

### Orden recomendado para cargar datos

1. Crear autores.
2. Crear libros y añadir autores en el inline de autoría.
3. Añadir ejemplares desde el inline de cada libro.
4. Registrar lectores.
5. Crear préstamos y añadir ejemplares en sus detalles.
6. Cuando un ejemplar sea devuelto, diligenciar la fecha y la condición de devolución en el detalle correspondiente.

## Datos de prueba

En la prueba ya se incluyen datos en las siete tablas: 6 autores, 5 libros, 6 ejemplares, 3 lectores, 4 préstamos, 4 detalles de préstamo y 6 relaciones libro-autor. Puedes verlos y editarlos desde `/admin/`.

## Reglas y decisiones del modelo

- El ISBN, documento del lector, correo y código de inventario no se pueden repetir.
- La tabla de ejemplares depende del libro al que pertenece; al eliminar un libro se eliminan sus ejemplares asociados.
- No se permite eliminar un lector con préstamos asociados (`PROTECT`), para preservar la trazabilidad.
- Un mismo ejemplar no se puede repetir dos veces en los detalles de un mismo préstamo.
- La fecha de devolución es opcional hasta que el ejemplar sea devuelto.
- La aplicación usa la zona horaria `America/Bogota`.

## Licencia y uso

Proyecto desarrollado con fines académicos.