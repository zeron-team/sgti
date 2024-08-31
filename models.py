from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Proveedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    fecha_contrato = db.Column(db.Date)
    periodo = db.Column(db.Enum('semanal', 'mensual', 'bimestral', 'trimestral', 'semestral', 'anual'), default='mensual')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    servidores = db.relationship('Servidor', back_populates='proveedor')

class Servidor(db.Model):
    __tablename__ = 'servidor'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    ip = db.Column(db.String(100), nullable=False)
    cpu = db.Column(db.String(100))
    ram = db.Column(db.String(100))
    disco = db.Column(db.String(100))
    tipo_os_id = db.Column(db.Integer, db.ForeignKey('tipo_os.id'))
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'))
    tipo_os = db.relationship('TipoOS', back_populates='servidores')
    proveedor = db.relationship('Proveedor', back_populates='servidores')
    clientes = db.relationship('Cliente', back_populates='servidor')

class Producto(db.Model):
    __tablename__ = 'producto'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    version = db.Column(db.String(50))  # Añadido nuevo campo
    descripcion = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    clientes = db.relationship('ClienteProducto', back_populates='producto')

class Cliente(db.Model):
    __tablename__ = 'cliente'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    contacto = db.Column(db.String(100))
    email = db.Column(db.String(100))
    servidor_id = db.Column(db.Integer, db.ForeignKey('servidor.id'))
    servidor = db.relationship('Servidor', back_populates='clientes')
    productos = db.relationship('ClienteProducto', back_populates='cliente', cascade="all, delete-orphan")
    licencias = db.relationship('ClienteLicencia', back_populates='cliente', cascade="all, delete-orphan")
    credenciales = db.relationship('ClienteCredencial', back_populates='cliente', cascade="all, delete-orphan")

class ClienteProducto(db.Model):
    __tablename__ = 'cliente_producto'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    version = db.Column(db.String(50))
    cantidad = db.Column(db.Integer)
    fecha_compra = db.Column(db.Date)
    fecha_vencimiento = db.Column(db.Date)
    cliente = db.relationship('Cliente', back_populates='productos')
    producto = db.relationship('Producto', back_populates='clientes')

class ClienteLicencia(db.Model):
    __tablename__ = 'cliente_licencia'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    producto = db.Column(db.String(100))
    puerto = db.Column(db.String(50))
    usuario = db.Column(db.String(100))
    clave = db.Column(db.String(100))
    cliente = db.relationship('Cliente', back_populates='licencias')

class ClienteCredencial(db.Model):
    __tablename__ = 'cliente_credencial'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100))
    usuario = db.Column(db.String(100), nullable=False)
    clave = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    producto = db.Column(db.String(100))

    cliente = db.relationship('Cliente', back_populates='credenciales')

class TipoOS(db.Model):
    __tablename__ = 'tipo_os'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    version = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    servidores = db.relationship('Servidor', back_populates='tipo_os')

    def __str__(self):
        return f"{self.nombre} {self.version}"


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Enum('Admin', 'Usuario'), default='Usuario')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
