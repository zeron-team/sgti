from flask import Blueprint, render_template, redirect, url_for, request, flash
from models import db, Producto, Cliente

producto_bp = Blueprint('producto_bp', __name__)

@producto_bp.route('/productos')
def listar_productos():
    productos = Producto.query.all()
    return render_template('productos.html', productos=productos)

@producto_bp.route('/producto/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form.get('descripcion')
        cliente_id = request.form.get('cliente_id')
        
        if cliente_id == '':
            cliente_id = None

        nuevo_producto = Producto(nombre=nombre, descripcion=descripcion, cliente_id=cliente_id)
        db.session.add(nuevo_producto)
        db.session.commit()
        flash('Producto creado exitosamente!', 'success')
        return redirect(url_for('producto_bp.listar_productos'))
    
    clientes = Cliente.query.all()
    return render_template('nuevo_producto.html', clientes=clientes)

@producto_bp.route('/producto/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    if request.method == 'POST':
        producto.nombre = request.form['nombre']
        producto.descripcion = request.form['descripcion']
        cliente_id = request.form.get('cliente_id')
        
        if cliente_id == '':
            cliente_id = None
        producto.cliente_id = cliente_id

        db.session.commit()
        flash('Producto actualizado exitosamente!', 'success')
        return redirect(url_for('producto_bp.listar_productos'))

    clientes = Cliente.query.all()
    return render_template('editar_producto.html', producto=producto, clientes=clientes)

@producto_bp.route('/producto/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    flash('Producto eliminado exitosamente')
    return redirect(url_for('producto_bp.listar_productos'))
