from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user
from app.models.bin import Bin
from app.database import db

sidebar_bp = Blueprint('sidebar', __name__)


@sidebar_bp.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html')

@sidebar_bp.route('/configuracion', methods=['GET'])
@login_required
def configuracion():
    bins = Bin.query.filter_by(IDUser=current_user.IDUser).all()
    return render_template('configuracion.html', bins=bins)


