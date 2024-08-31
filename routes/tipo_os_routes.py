from flask import Blueprint, render_template, redirect, url_for, request, flash
from models import db, TipoOS

tipo_os_bp = Blueprint('tipo_os_bp', __name__)

@tipo_os_bp.route('/tipos-os')
def listar_tipos_os():
    tipos_os = TipoOS.query.all()
    return render_template('tipo_os.html', tipos_os=tipos_os)

@tipo_os_bp.route('/tipo-os/nuevo', methods=['GET', 'POST'])
def nuevo_tipo_os():
    if request.method == 'POST':
        nombre = request.form['nombre']
        version = request.form['version']
        nuevo_tipo_os = TipoOS(nombre=nombre, version=version)
        db.session.add(nuevo_tipo_os)
        db.session.commit()
        flash('Tipo de OS creado exitosamente!', 'success')
        return redirect(url_for('tipo_os_bp.listar_tipos_os'))
    return render_template('nuevo_tipo_os.html')

@tipo_os_bp.route('/tipo-os/<int:id>/editar', methods=['GET', 'POST'])
def editar_tipo_os(id):
    tipo_os = TipoOS.query.get_or_404(id)
    if request.method == 'POST':
        tipo_os.nombre = request.form['nombre']
        tipo_os.version = request.form['version']
        db.session.commit()
        flash('Tipo de OS actualizado exitosamente!', 'success')
        return redirect(url_for('tipo_os_bp.listar_tipos_os'))
    return render_template('editar_tipo_os.html', tipo_os=tipo_os)

@tipo_os_bp.route('/tipo-os/<int:id>/eliminar', methods=['POST'])
def eliminar_tipo_os(id):
    tipo_os = TipoOS.query.get_or_404(id)
    db.session.delete(tipo_os)
    db.session.commit()
    flash('Tipo de OS eliminado exitosamente')
    return redirect(url_for('tipo_os_bp.listar_tipos_os'))
