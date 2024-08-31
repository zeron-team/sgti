from flask import Blueprint, render_template, redirect, url_for, request, flash
from models import db, Usuario

usuario_bp = Blueprint('usuario_bp', __name__)

@usuario_bp.route('/usuarios')
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios.html', usuarios=usuarios)

@usuario_bp.route('/usuarios/nuevo', methods=['GET', 'POST'])
def nuevo_usuario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        usuario = request.form['usuario']
        password = request.form['password']
        rol = request.form['rol']

        nuevo_usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            email=email,
            usuario=usuario,
            rol=rol
        )
        nuevo_usuario.set_password(password)

        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('Usuario agregado exitosamente')
        return redirect(url_for('usuario_bp.listar_usuarios'))

    return render_template('nuevo_usuario.html')

@usuario_bp.route('/usuarios/<int:id>/editar', methods=['GET', 'POST'])
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    if request.method == 'POST':
        usuario.nombre = request.form['nombre']
        usuario.apellido = request.form['apellido']
        usuario.email = request.form['email']
        usuario.usuario = request.form['usuario']
        usuario.rol = request.form['rol']

        if 'password' in request.form and request.form['password']:
            usuario.set_password(request.form['password'])

        db.session.commit()
        flash('Usuario actualizado exitosamente')
        return redirect(url_for('usuario_bp.listar_usuarios'))

    return render_template('editar_usuario.html', usuario=usuario)

@usuario_bp.route('/usuarios/<int:id>/eliminar', methods=['POST'])
def eliminar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario eliminado exitosamente')
    return redirect(url_for('usuario_bp.listar_usuarios'))
