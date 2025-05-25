from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user
from app.models.bin import Bin
from app.database import db

sidebar_bp = Blueprint('sidebar', __name__)

@sidebar_bp.route('/dashboard')
@login_required
def dashboard():
    # Consultar bins del usuario actual
    bins = Bin.query.filter_by(IDUser=current_user.IDUser).all()
    # Simular estado
    for b in bins:
        lectura = b.ultima_lectura
        peso = lectura.peso if lectura else 0
        stock_minimo = 300  # Podés mover esto a un campo de base de datos después
        b.estado = "stock bajo" if peso < stock_minimo else "ok"
    return render_template('dashboard.html', bins=bins)

@sidebar_bp.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html')

@sidebar_bp.route('/configuracion')
@login_required
def configuracion():
    return render_template('configuracion.html')

@sidebar_bp.route('/agregar_bin', methods=['GET', 'POST'])
@login_required
def agregar_bin():
    if request.method == 'POST':
        uid_hardware = request.form.get('uid_hardware')
        nombre = request.form.get('nombre')
        ubicacion = request.form.get('ubicacion')

        if not uid_hardware or not nombre:
            flash("El código del bin y el nombre son obligatorios.")
            return redirect(url_for('sidebar.agregar_bin'))

        # Validar que no esté ya registrado
        existente = Bin.query.filter_by(uid_hardware=uid_hardware).first()
        if existente:
            flash("Este SmartBin ya fue registrado.")
            return redirect(url_for('sidebar.agregar_bin'))

        # Crear el nuevo bin
        nuevo_bin = Bin(
            IDUser=current_user.IDUser,
            uid_hardware=uid_hardware,
            nombre=nombre,
            ubicacion=ubicacion
        )
        db.session.add(nuevo_bin)
        db.session.commit()

        flash("SmartBin agregado con éxito.")
        return redirect(url_for('sidebar.dashboard'))

    return render_template('agregar_bin.html')
