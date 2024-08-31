from flask import Blueprint, render_template, redirect, url_for, request, flash
from models import db, Proveedor

proveedor_bp = Blueprint('proveedor_bp', __name__)

@proveedor_bp.route('/proveedores')
def listar_proveedores():
    proveedores = Proveedor.query.all()
    return render_template('proveedores.html', proveedores=proveedores)

@proveedor_bp.route('/proveedores/nuevo', methods=['GET', 'POST'])
def nuevo_proveedor():
    if request.method == 'POST':
        nombre = request.form['nombre']
        fecha_contrato = request.form.get('fecha_contrato')
        periodo = request.form.get('periodo')

        nuevo_proveedor = Proveedor(nombre=nombre, fecha_contrato=fecha_contrato, periodo=periodo)
        db.session.add(nuevo_proveedor)
        db.session.commit()
        flash('Proveedor creado exitosamente!', 'success')
        return redirect(url_for('proveedor_bp.listar_proveedores'))
    return render_template('nuevo_proveedor.html')

@proveedor_bp.route('/proveedores/<int:id>/editar', methods=['GET', 'POST'])
def editar_proveedor(id):
    proveedor = Proveedor.query.get_or_404(id)
    if request.method == 'POST':
        proveedor.nombre = request.form['nombre']
        proveedor.fecha_contrato = request.form.get('fecha_contrato')
        proveedor.periodo = request.form.get('periodo')

        db.session.commit()
        flash('Proveedor actualizado exitosamente!', 'success')
        return redirect(url_for('proveedor_bp.listar_proveedores'))
    return render_template('editar_proveedor.html', proveedor=proveedor)

@proveedor_bp.route('/proveedores/<int:id>/eliminar', methods=['POST'])
def eliminar_proveedor(id):
    proveedor = Proveedor.query.get_or_404(id)
    db.session.delete(proveedor)
    db.session.commit()
    flash('Proveedor eliminado exitosamente')
    return redirect(url_for('proveedor_bp.listar_proveedores'))
