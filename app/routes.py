import os
import re
import uuid

from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, jsonify, send_from_directory

from app import db
from app.models import User, AdvancementType, HitPointType, ConfigSheet

bp = Blueprint('main', __name__)

@bp.route('/')
def index():

    return render_template('index.html')

@bp.route('/users')
def index_user():
    users = User.query.all()
    return render_template('user/index.html', users=users)

@bp.route('/users/new', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']


        if not nome or not email:
            flash('Nome e e-mail são obrigatórios!', 'danger')
            return render_template('user/create.html', nome=nome, email=email)

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Este e-mail já está cadastrado.', 'danger')
            return render_template('user/create.html', nome=nome, email=email)

        new_user = User(nome=nome, email=email)
        db.session.add(new_user)
        db.session.commit()
        flash('Usuário criado com sucesso!', 'success')
        return redirect(url_for('main.index_user'))
    return render_template('user/create.html')

@bp.route('/users/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    user_name = user.nome
    db.session.delete(user)
    db.session.commit()
    flash(f'Usuário "{user_name}" foi apagado com sucesso!', 'success')
    return redirect(url_for('main.index_user'))

@bp.route('/users/update/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']

        if not nome or not email:
            flash('Nome e e-mail são obrigatórios!', 'danger')
            return render_template('user/update.html', user=user)

        existing_user = User.query.filter(User.email == email, User.id != user_id).first()
        if existing_user:
            flash('Este e-mail já está cadastrado em outra conta.', 'danger')
            return render_template('user/update.html', user=user)

        user.nome = nome
        user.email = email

        db.session.commit()

        flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('main.index_user'))

    return render_template('user/update.html', user=user)

@bp.route('/users/<int:user_id>')
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user/show.html', user=user)

@bp.route('/config_sheets/new', methods=['GET', 'POST'])
def create_config_sheet():
    if request.method == 'POST':
        homebrew = 'homebrew' in request.form
        expanded_rules = 'expanded_rules' in request.form
        dice_rolling = 'dice_rolling' in request.form
        feat_prerequisites = 'feat_prerequisites' in request.form
        multiclass_prerequisites = 'multiclass_prerequisites' in request.form
        mark_level_scaled_spells = 'mark_level_scaled_spells' in request.form

        new_config = ConfigSheet(
            homebrew=homebrew,
            expanded_rules=expanded_rules,
            dice_rolling=dice_rolling,
            advancement_type=AdvancementType(request.form.get('advancement_type')),
            hit_point_type=HitPointType(request.form.get('hit_point_type')),
            feat_prerequisites=feat_prerequisites,
            multiclass_prerequisites=multiclass_prerequisites,
            mark_level_scaled_spells=mark_level_scaled_spells
        )
        db.session.add(new_config)
        db.session.commit()
        flash('Configuração criada com sucesso!', 'success')
        return redirect(url_for('main.index'))

    return render_template('config_sheet/create.html', config={}, advancement_types=AdvancementType, hit_point_types=HitPointType)

@bp.route('character_sheets/new', methods=['GET', 'POST'])
def create_character_sheet():
    if request.method == 'POST':
