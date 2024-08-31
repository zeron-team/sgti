# Sistema de Gestion TI

## Estructura

```txt
/proyectos/sgti/
|-- /app/
|   |-- __init__.py
|   |-- models.py
|   |-- routes/
|   |   |-- __init__.py
|   |   |-- cliente_routes.py
|   |   |-- producto_routes.py
|   |   |-- proveedor_routes.py
|   |   |-- servidor_routes.py
|   |   |-- usuario_routes.py
|   |-- templates/
|   |   |-- dashboard.html
|   |   |-- login.html
|   |   |-- editar_usuario.html
|   |   |-- nuevo_usuario.html
|   |   |-- usuarios.html
|   |-- static/
|   |   |-- css/
|   |   |   |-- styles.css
|   |   |-- img/
|   |   |   |-- KaiZen2B.png
|-- /venv/
|-- app.py
|-- config.py
|-- wsgi.py
|-- requirements.txt

```
## requerimientos

- correr requirements.tx

-   ```txt  
    pip install -r requirements.tx
    ```
## run



## SQL

```sql
CREATE TABLE servidores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    ip VARCHAR(15) NOT NULL,
    cpu VARCHAR(50),
    ram VARCHAR(50),
    disco VARCHAR(50),
    sistema_operativo VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

```sql
CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    contacto VARCHAR(100),
    email VARCHAR(100),
    servidor_id INT,
    FOREIGN KEY (servidor_id) REFERENCES servidores(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

```sql
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255) NOT NULL,
    rol ENUM('Admin', 'Usuario') DEFAULT 'Usuario',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

```
