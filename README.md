# 📱 Mi Móvil

**Mi Móvil** es un sistema de gestión de ventas e inventario para una tienda de dispositivos móviles y accesorios. Permite gestionar productos, ventas, reparaciones y clientes de forma eficiente y moderna. Incluye un panel de control con funcionalidades CRUD, filtros de búsqueda y una interfaz atractiva.

---

## 🚀 Funcionalidades principales

- **Autenticación de usuarios** con roles y permisos.
- **Gestión de productos** con imagen, código, stock y categorías.
- **CRUD de ventas** con control de stock.
- **Gestión de clientes** asociados a ventas.
- **Despliegue fácil con Docker**.

---

## 🛠️ Tecnologías utilizadas

- **Backend:** Django + Django REST Framework
- **Frontend:** HTML5, Bootstrap, JavaScript
- **Base de datos:** PostgreSQL
- **Contenedores:** Docker y Docker Compose

---

## 📦 Instalación y despliegue

### 1. Clona el repositorio

```bash
git clone https://github.com/StickMora/Mi-Movil.git
cd mi-movil
```

### 2. Configura el archivo .env

Crea un archivo .env con las siguientes variables y carga los datos

POSTGRES_DB=""
POSTGRES_USER=""
POSTGRES_PASSWORD=""
EMAIL_USER=""
EMAIL_PASS=""

### 3. Migraciones
Ingresar al contenedor de la imagen de django

```bash
>docker exec -it mi_movil bash
```

Para correr y generar los migrations en la base de datos se deben ejecutar los siguientes comandos:

```bash
python manage.py makemigrations

python manage.py migrate
```


### 4 Construye y levanta los contenedores
```bash
docker-compose up --build
```


Para establecer los permisos, desde la consola de postgres se debe ejecutar una consulta como la siguiente:

```sql
postgres>ALTER USER <nombre de usuario> WITH SUPERUSER;
```
