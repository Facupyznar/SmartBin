from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user
from app.models.bin import Bin
from app.database import db
from app.models.lectura import Lectura

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    # Consultar bins del usuario actual
    bins = Bin.query.filter_by(IDUser=current_user.IDUser).all()
    for b in bins:
        lectura = b.ultima_lectura
        peso = float(lectura.peso) if lectura else 0
        b.peso_actual = peso
        b.estado = "stock bajo" if b.stock_minimo_unidades and peso < (b.peso_unitario or 1) * b.stock_minimo_unidades else "ok"
        b.cantidad_piezas = int(peso // (b.peso_unitario or 1)) if b.peso_unitario else 0
    return render_template('dashboard.html', bins=bins)


@dashboard_bp.route('/agregar_bin', methods=['GET', 'POST'])
@login_required
def agregar_bin():
    if request.method == 'POST':
        uid_hardware = request.form.get('uid_hardware')
        nombre = request.form.get('nombre')
        ubicacion = request.form.get('ubicacion')
        peso_unitario = request.form.get('peso_unitario', type=float)
        stock_minimo_unidades = request.form.get('stock_minimo_unidades', type=int)

        if not uid_hardware or not nombre:
            flash("El código del bin y el nombre son obligatorios.")
            return redirect(url_for('dashboard.agregar_bin'))

        # Validar que no esté ya registrado
        existente = Bin.query.filter_by(uid_hardware=uid_hardware).first()
        if existente:
            flash("Este SmartBin ya fue registrado.")
            return redirect(url_for('dashboard.agregar_bin'))

        # Crear el nuevo bin
        nuevo_bin = Bin(
            IDUser=current_user.IDUser,
            uid_hardware=uid_hardware,
            nombre=nombre,
            ubicacion=ubicacion,
            peso_unitario=peso_unitario,
            stock_minimo_unidades=stock_minimo_unidades
        )
        db.session.add(nuevo_bin)
        db.session.commit()

        flash("SmartBin agregado con éxito.")
        return redirect(url_for('dashboard.dashboard'))

    return render_template('agregar_bin.html')


@dashboard_bp.route('/detalle_bin/<int:bin_id>')
@login_required
def detalle_bin(bin_id):
    bin = Bin.query.get_or_404(bin_id)

    # Verificamos que el bin sea del usuario logueado
    if bin.IDUser != current_user.IDUser:
        flash("No tenés permiso para ver este SmartBin.")
        return redirect(url_for('dashboard.dashboard'))

    # Traemos las lecturas de ese bin, ordenadas por fecha
    lecturas = Lectura.query.filter_by(IDBin=bin.IDBin).order_by(Lectura.timestamp.desc()).all()
    peso = float(bin.ultima_lectura.peso) if bin.ultima_lectura else 0
    peso_unitario = bin.peso_unitario or 1  # evitar división por cero
    cantidad_estimada = int(peso // peso_unitario)  

    return render_template('detalle_bin.html', bin=bin, lecturas=lecturas, cantidad_estimada = cantidad_estimada)

@dashboard_bp.route('/configurar_bin/<int:bin_id>', methods=['POST'])
@login_required
def actualizar_config_bin(bin_id):
    bin = Bin.query.get_or_404(bin_id)
    if bin.IDUser != current_user.IDUser:
        flash("No podés modificar este bin.")
        return redirect(url_for('dashboard.dashboard'))

    bin.peso_unitario = request.form.get('peso_unitario', type=float)
    bin.stock_minimo_unidades = request.form.get('stock_minimo_unidades', type=int)
    db.session.commit()
    flash("Configuración actualizada.")
    return redirect(url_for('dashboard.configuracion'))




