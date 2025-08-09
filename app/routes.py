import os
import re
import uuid

from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, jsonify, \
    send_from_directory, abort

from app import db
from app.forms import CharacterClassForm
from app.models import User, AdvancementType, HitPointType, ConfigSheet, ClassType, CharacterSheet, \
    CharacterSheetAttribute, CharacterSheetSkill

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

        advancement_type = AdvancementType(request.form.get('advancement_type'))
        hit_point_type = HitPointType(request.form.get('hit_point_type'))

        new_config = ConfigSheet(
            homebrew=homebrew,
            expanded_rules=expanded_rules,
            dice_rolling=dice_rolling,
            advancement_type=advancement_type,
            hit_point_type=hit_point_type,
            feat_prerequisites=feat_prerequisites,
            multiclass_prerequisites=multiclass_prerequisites,
            mark_level_scaled_spells=mark_level_scaled_spells
        )
        db.session.add(new_config)
        db.session.commit()

        flash('Configuração criada com sucesso!', 'success')
        return redirect(url_for('main.create_character_sheet', config_sheet_id=new_config.id))

    return render_template('config_sheet/create.html', config={}, advancement_types=AdvancementType, hit_point_types=HitPointType)

@bp.route('/select_class', methods=['GET', 'POST'])
def select_class():
    form = CharacterClassForm()

    ordem_prioritaria = ["Bárbaro", "Bardo"]

    todas_as_classes = ClassType.query.all()
    classes_ordenadas = sorted(todas_as_classes, key=lambda c: (
        ordem_prioritaria.index(c.name) if c.name in ordem_prioritaria else float('inf'),
        c.name
    ))

    form.character_class.choices = [(c.id, c.name) for c in classes_ordenadas]

    if form.validate_on_submit():
        selected_class_id = form.character_class.data
        selected_class = ClassType.query.get(selected_class_id)
        return f'<h1>Você selecionou: {selected_class.name}</h1>'

    return render_template('select_class_template.html', title='Selecionar Classe', form=form)


@bp.route('/character_sheet/new/<int:config_sheet_id>', methods=['GET', 'POST'])
def create_character_sheet(config_sheet_id):
    config_sheet = ConfigSheet.query.get_or_404(config_sheet_id)
    class_types = ClassType.query.order_by(ClassType.name).all()

    if request.method == 'POST':
        character_name = request.form.get('character_name')
        class_type_id = request.form.get('class_type_id')
        level = request.form.get('level', 1, type=int)

        new_character = CharacterSheet(
            name=character_name,
            level=level,
            config_sheet_id=config_sheet.id,
            class_type_id=class_type_id,
            user_id=1
        )
        db.session.add(new_character)
        db.session.commit()

        new_attributes = CharacterSheetAttribute(
            character_sheet_id=new_character.id,
            strength=request.form.get('strength', 10, type=int),
            dexterity=request.form.get('dexterity', 10, type=int),
            constitution=request.form.get('constitution', 10, type=int),
            intelligence=request.form.get('intelligence', 10, type=int),
            wisdom=request.form.get('wisdom', 10, type=int),
            charisma=request.form.get('charisma', 10, type=int)
        )
        db.session.add(new_attributes)

        new_skills = CharacterSheetSkill(character_sheet_id=new_character.id)
        db.session.add(new_skills)

        db.session.commit()

        flash('Ficha de personagem criada com sucesso!', 'success')
        return redirect(url_for('main.index'))

    return render_template('character_sheet/new.html',
                           class_types=class_types,
                           config_sheet=config_sheet)