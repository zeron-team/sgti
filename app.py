from flask import Flask, render_template, redirect, url_for, request, flash, session
from config import Config
from models import db, Usuario, ClienteProducto, Servidor, Cliente, Producto, Proveedor  # Asegúrate de importar Proveedor
from routes.servidor_routes import servidor_bp
from routes.cliente_routes import cliente_bp
from routes.usuario_routes import usuario_bp
from routes.proveedor_routes import proveedor_bp
from routes.producto_routes import producto_bp
from routes.tipo_os_routes import tipo_os_bp
import pymysql
from flask_migrate import Migrate
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta

# Inicializar PyMySQL
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    today = datetime.today()
    end_of_week = today + timedelta(days=7-today.weekday())
    end_of_month = (today.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
    next_month = today + timedelta(days=30)

    this_week = ClienteProducto.query.filter(ClienteProducto.fecha_vencimiento <= end_of_week).all()
    this_month = ClienteProducto.query.filter(
        ClienteProducto.fecha_vencimiento > end_of_week,
        ClienteProducto.fecha_vencimiento <= end_of_month
    ).all()
    more_than_one_month = ClienteProducto.query.filter(ClienteProducto.fecha_vencimiento > next_month).all()

    servidores = Servidor.query.all()
    clientes = Cliente.query.all()
    productos = Producto.query.all()
    proveedores = Proveedor.query.all()

    return render_template(
        'dashboard.html', 
        this_week=this_week, 
        this_month=this_month, 
        more_than_one_month=more_than_one_month,
        servidores=servidores,
        clientes=clientes,
        productos=productos,
        proveedores=proveedores
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        user = Usuario.query.filter_by(usuario=usuario).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('home'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

app.register_blueprint(servidor_bp)
app.register_blueprint(cliente_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(proveedor_bp)
app.register_blueprint(producto_bp)
app.register_blueprint(tipo_os_bp)

if __name__ == '__main__':
    app.run(debug=True)
