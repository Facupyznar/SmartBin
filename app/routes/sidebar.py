from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.bin import Bin

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

@sidebar_bp.route('/agregar-bin')
@login_required
def agregar_bin():
    return render_template('agregar_bin.html') 
