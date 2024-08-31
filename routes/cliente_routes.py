from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from models import db, Cliente, Producto, ClienteProducto, ClienteLicencia, ClienteCredencial, Servidor

cliente_bp = Blueprint('cliente_bp', __name__)

@cliente_bp.route('/clientes')
def listar_clientes():
    clientes = Cliente.query.all()
    return render_template('clientes.html', clientes=clientes)

@cliente_bp.route('/clientes/credenciales')
def listar_credenciales():
    credenciales = ClienteCredencial.query.join(Cliente).all()
    return render_template('listar_credenciales.html', credenciales=credenciales)

@cliente_bp.route('/clientes/nuevo', methods=['GET', 'POST'])
def nuevo_cliente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        contacto = request.form.get('contacto')
        email = request.form.get('email')
        servidor_id = request.form.get('servidor_id')

        nuevo_cliente = Cliente(nombre=nombre, contacto=contacto, email=email, servidor_id=servidor_id)
        db.session.add(nuevo_cliente)
        db.session.commit()

        productos = request.form.getlist('producto_id[]')
        versiones = request.form.getlist('version[]')
        cantidades = request.form.getlist('cantidad[]')
        fechas_compra = request.form.getlist('fecha_compra[]')
        fechas_vencimiento = request.form.getlist('fecha_vencimiento[]')

        for producto_id, version, cantidad, fecha_compra, fecha_vencimiento in zip(productos, versiones, cantidades, fechas_compra, fechas_vencimiento):
            cliente_producto = ClienteProducto(
                cliente_id=nuevo_cliente.id,
                producto_id=producto_id,
                version=version,
                cantidad=cantidad,
                fecha_compra=fecha_compra,
                fecha_vencimiento=fecha_vencimiento
            )
            db.session.add(cliente_producto)

        productos_licencia = request.form.getlist('producto_licencia[]')
        puertos = request.form.getlist('puerto[]')
        usuarios = request.form.getlist('usuario[]')
        claves = request.form.getlist('clave[]')

        for producto, puerto, usuario, clave in zip(productos_licencia, puertos, usuarios, claves):
            cliente_licencia = ClienteLicencia(
                cliente_id=nuevo_cliente.id,
                producto=producto,
                puerto=puerto,
                usuario=usuario,
                clave=clave
            )
            db.session.add(cliente_licencia)

        nombres_credencial = request.form.getlist('nombre_credencial[]')
        apellidos_credencial = request.form.getlist('apellido[]')
        usuarios_credencial = request.form.getlist('usuario_credencial[]')
        claves_credencial = request.form.getlist('clave_credencial[]')
        emails_credencial = request.form.getlist('email_credencial[]')
        productos_credencial = request.form.getlist('producto_credencial[]')

        for nombre, apellido, usuario, clave, email, producto in zip(nombres_credencial, apellidos_credencial, usuarios_credencial, claves_credencial, emails_credencial, productos_credencial):
            cliente_credencial = ClienteCredencial(
                cliente_id=nuevo_cliente.id,
                nombre=nombre,
                apellido=apellido,
                usuario=usuario,
                clave=clave,
                email=email,
                producto=producto
            )
            db.session.add(cliente_credencial)

        db.session.commit()

        flash('Cliente y productos creados exitosamente!', 'success')
        return redirect(url_for('cliente_bp.listar_clientes'))
    
    productos = Producto.query.all()
    servidores = Servidor.query.all()
    return render_template('nuevo_cliente.html', productos=productos, servidores=servidores)

@cliente_bp.route('/clientes/<int:id>/editar', methods=['GET', 'POST'])
def editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    servidores = Servidor.query.all()
    productos = Producto.query.all()
    if request.method == 'POST':
        cliente.nombre = request.form['nombre']
        cliente.contacto = request.form['contacto']
        cliente.email = request.form['email']
        cliente.servidor_id = request.form['servidor_id']

        db.session.commit()

        ClienteProducto.query.filter_by(cliente_id=cliente.id).delete()

        productos = request.form.getlist('producto_id[]')
        versiones = request.form.getlist('version[]')
        cantidades = request.form.getlist('cantidad[]')
        fechas_compra = request.form.getlist('fecha_compra[]')
        fechas_vencimiento = request.form.getlist('fecha_vencimiento[]')

        for producto_id, version, cantidad, fecha_compra, fecha_vencimiento in zip(productos, versiones, cantidades, fechas_compra, fechas_vencimiento):
            cliente_producto = ClienteProducto(
                cliente_id=cliente.id,
                producto_id=producto_id,
                version=version,
                cantidad=cantidad,
                fecha_compra=fecha_compra,
                fecha_vencimiento=fecha_vencimiento
            )
            db.session.add(cliente_producto)

        ClienteLicencia.query.filter_by(cliente_id=cliente.id).delete()

        productos_licencia = request.form.getlist('producto_licencia[]')
        puertos = request.form.getlist('puerto[]')
        usuarios = request.form.getlist('usuario[]')
        claves = request.form.getlist('clave[]')

        for producto, puerto, usuario, clave in zip(productos_licencia, puertos, usuarios, claves):
            cliente_licencia = ClienteLicencia(
                cliente_id=cliente.id,
                producto=producto,
                puerto=puerto,
                usuario=usuario,
                clave=clave
            )
            db.session.add(cliente_licencia)

        ClienteCredencial.query.filter_by(cliente_id=cliente.id).delete()

        nombres_credencial = request.form.getlist('nombre_credencial[]')
        apellidos_credencial = request.form.getlist('apellido[]')
        usuarios_credencial = request.form.getlist('usuario_credencial[]')
        claves_credencial = request.form.getlist('clave_credencial[]')
        emails_credencial = request.form.getlist('email_credencial[]')
        productos_credencial = request.form.getlist('producto_credencial[]')

        for nombre, apellido, usuario, clave, email, producto in zip(nombres_credencial, apellidos_credencial, usuarios_credencial, claves_credencial, emails_credencial, productos_credencial):
            cliente_credencial = ClienteCredencial(
                cliente_id=cliente.id,
                nombre=nombre,
                apellido=apellido,
                usuario=usuario,
                clave=clave,
                email=email,
                producto=producto
            )
            db.session.add(cliente_credencial)

        db.session.commit()

        flash('Cliente actualizado exitosamente', 'success')
        return redirect(url_for('cliente_bp.listar_clientes'))
    
    cliente_productos = ClienteProducto.query.filter_by(cliente_id=cliente.id).all()
    cliente_licencias = ClienteLicencia.query.filter_by(cliente_id=cliente.id).all()
    cliente_credenciales = ClienteCredencial.query.filter_by(cliente_id=cliente.id).all()
    return render_template('editar_cliente.html', cliente=cliente, servidores=servidores, productos=productos, cliente_productos=cliente_productos, cliente_licencias=cliente_licencias, cliente_credenciales=cliente_credenciales)

@cliente_bp.route('/clientes/<int:id>/eliminar', methods=['POST'])
def eliminar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    ClienteProducto.query.filter_by(cliente_id=cliente.id).delete()
    ClienteLicencia.query.filter_by(cliente_id=cliente.id).delete()
    ClienteCredencial.query.filter_by(cliente_id=cliente.id).delete()
    db.session.delete(cliente)
    db.session.commit()
    flash('Cliente eliminado exitosamente')
    return redirect(url_for('cliente_bp.listar_clientes'))

@cliente_bp.route('/clientes/<int:id>', methods=['GET'])
def ver_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    cliente_productos = ClienteProducto.query.filter_by(cliente_id=cliente.id).all()
    cliente_licencias = ClienteLicencia.query.filter_by(cliente_id=cliente.id).all()
    cliente_credenciales = ClienteCredencial.query.filter_by(cliente_id=cliente.id).all()
    return render_template('ver_cliente.html', cliente=cliente, cliente_productos=cliente_productos, cliente_licencias=cliente_licencias, cliente_credenciales=cliente_credenciales)
