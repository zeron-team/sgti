from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from models import db, Servidor, TipoOS, Proveedor, Cliente
import subprocess
import logging

servidor_bp = Blueprint('servidor_bp', __name__)

logging.basicConfig(level=logging.DEBUG)

# Ruta para listar servidores
@servidor_bp.route('/servidores')
def listar_servidores():
    servidores = Servidor.query.options(db.joinedload(Servidor.tipo_os)).all()
    return render_template('servidores.html', servidores=servidores)

@servidor_bp.route('/servidores/nuevo', methods=['GET', 'POST'])
def nuevo_servidor():
    if request.method == 'POST':
        nombre = request.form['nombre']
        ip = request.form['ip']
        cpu = request.form['cpu']
        ram = request.form['ram']
        disco = request.form['disco']
        tipo_os_id = request.form['tipo_os_id']
        proveedor_id = request.form['proveedor_id']

        nuevo_servidor = Servidor(
            nombre=nombre,
            ip=ip,
            cpu=cpu,
            ram=ram,
            disco=disco,
            tipo_os_id=tipo_os_id,
            proveedor_id=proveedor_id
        )

        db.session.add(nuevo_servidor)
        db.session.commit()
        flash('Servidor agregado exitosamente')
        return redirect(url_for('servidor_bp.listar_servidores'))

    proveedores = Proveedor.query.all()
    tipos_os = TipoOS.query.all()
    return render_template('nuevo_servidor.html', proveedores=proveedores, tipos_os=tipos_os)

@servidor_bp.route('/servidores/<int:id>/editar', methods=['GET', 'POST'])
def editar_servidor(id):
    servidor = Servidor.query.get_or_404(id)
    if request.method == 'POST':
        servidor.nombre = request.form['nombre']
        servidor.ip = request.form['ip']
        servidor.cpu = request.form['cpu']
        servidor.ram = request.form['ram']
        servidor.disco = request.form['disco']
        servidor.tipo_os_id = request.form['tipo_os_id']
        servidor.proveedor_id = request.form['proveedor_id']

        db.session.commit()
        flash('Servidor actualizado exitosamente')
        return redirect(url_for('servidor_bp.listar_servidores'))

    proveedores = Proveedor.query.all()
    tipos_os = TipoOS.query.all()
    return render_template('editar_servidor.html', servidor=servidor, proveedores=proveedores, tipos_os=tipos_os)

@servidor_bp.route('/servidores/<int:id>/eliminar', methods=['POST'])
def eliminar_servidor(id):
    servidor = Servidor.query.get_or_404(id)
    db.session.delete(servidor)
    db.session.commit()
    flash('Servidor eliminado exitosamente')
    return redirect(url_for('servidor_bp.listar_servidores'))

@servidor_bp.route('/servidores/ping/<int:id>', methods=['POST'])
def ping_servidor(id):
    servidor = Servidor.query.get_or_404(id)
    try:
        logging.debug(f"Pinging IP: {servidor.ip}")
        response = subprocess.run(['ping', '-c', '3', servidor.ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.debug(f"Ping response: {response.stdout}")
        logging.debug(f"Ping error: {response.stderr}")
        is_active = response.returncode == 0
        logging.debug(f"Ping is_active: {is_active}")
    except Exception as e:
        logging.error(f"Error pinging server: {e}")
        is_active = False
    return jsonify({'is_active': is_active})
