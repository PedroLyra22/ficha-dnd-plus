import os
import re
import uuid
import json

from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, jsonify, \
  send_from_directory, abort

from app import db
from app.forms import CharacterSheetForm
from app.models import User, AdvancementType, HitPointType, ConfigSheet, CharacterSheet, AttributeConfigType

bp = Blueprint('main', __name__)

SLUG_TO_FILENAME = {
    'barbaro': 'barbarian',
    'bardo': 'bard',
    'clerigo': 'cleric',
    'druida': 'druid',
    'guerreiro': 'fighter',
    'monge': 'monk',
    'paladino': 'paladin',
    'patrulheiro': 'ranger',
    'ladino': 'rogue',
    'feiticeiro': 'sorcerer',
    'bruxo': 'warlock',
    'mago': 'wizard',
}


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
  character_sheets = CharacterSheet.query.filter_by(user_id=user.id).all()
  return render_template('user/show.html', user=user, character_sheets=character_sheets)


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
    attribute_config_type = AttributeConfigType(request.form.get('attribute_config_type'))

    new_config = ConfigSheet(
      homebrew=homebrew,
      expanded_rules=expanded_rules,
      dice_rolling=dice_rolling,
      advancement_type=advancement_type,
      hit_point_type=hit_point_type,
      attribute_config_type=attribute_config_type,
      feat_prerequisites=feat_prerequisites,
      multiclass_prerequisites=multiclass_prerequisites,
      mark_level_scaled_spells=mark_level_scaled_spells
    )
    db.session.add(new_config)
    db.session.commit()

    flash('Configuração criada com sucesso!', 'success')
    return redirect(url_for('main.create_character_sheet'))

  return render_template('config_sheet/create.html', config={}, advancement_types=AdvancementType,
                         hit_point_types=HitPointType, attribute_config_types=AttributeConfigType)


@bp.route('/character_sheets/new', methods=['GET', 'POST'])
def create_character_sheet():
  form = CharacterSheetForm()

  with open('app/db/classes.json', encoding='utf-8') as f:
    classes_data = json.load(f)

  classes = sorted(classes_data['classes_data'].items(), key=lambda x: x[1]['name'])
  form.class_slug.choices = [(slug, data['name']) for slug, data in classes]

  if form.validate_on_submit():
    user = User.query.first()
    if not user:
      flash('Nenhum usuário encontrado. Crie um usuário primeiro.', 'danger')
      return redirect(url_for('main.create_user'))

    config_sheet = ConfigSheet.query.order_by(ConfigSheet.id.desc()).first()
    if not config_sheet:
      flash('Nenhuma configuração de ficha encontrada. Crie uma primeiro.', 'danger')
      return redirect(url_for('main.create_config_sheet'))

    character_sheet = CharacterSheet(
      name=form.name.data,
      class_slug=form.class_slug.data,
      level=1,
      user_id=user.id,
      config_sheet_id=config_sheet.id
    )
    db.session.add(character_sheet)
    db.session.commit()

    flash('Ficha de personagem criada com sucesso! Agora, escolha as características da sua classe.', 'success')

    return redirect(url_for('main.class_traits', sheet_id=character_sheet.id))

  return render_template('character_sheets/new.html', form=form, classes=classes_data['classes_data'])


@bp.route('/class_traits/<int:sheet_id>', methods=['GET', 'POST'])
def class_traits(sheet_id):
    sheet = CharacterSheet.query.get_or_404(sheet_id)
    class_slug = sheet.class_slug

    filename = SLUG_TO_FILENAME.get(class_slug)
    if not filename:
        abort(404, description=f"Mapeamento para o slug de classe '{class_slug}' não encontrado.")

    try:
        with open(f'app/db/character_classes/{filename}.json', encoding='utf-8') as f:
            class_data = json.load(f)
    except FileNotFoundError:
        abort(404, description=f"Arquivo JSON para a classe '{class_slug}' ('{filename}.json') não encontrado.")

    class_info = class_data.get(class_slug, {})
    progression_level_1 = class_info.get('progression', {}).get('1', [])

    if request.method == 'POST':
        sheet.class_features = request.form.to_dict(flat=False)
        db.session.commit()

        flash(f'Características de {class_info.get("name", class_slug)} salvas com sucesso!', 'success')
        return redirect(url_for('main.show_character_sheet', sheet_id=sheet_id))

    features_with_choices = [
        item for item in progression_level_1 if 'choices' in item
    ]

    return render_template('class_traits.html',
                           sheet=sheet,
                           class_info=class_info,
                           features_with_choices=features_with_choices)


@bp.route('/character_sheet/<int:sheet_id>')
def show_character_sheet(sheet_id):
    sheet = CharacterSheet.query.get_or_404(sheet_id)
    class_slug = sheet.class_slug

    filename = SLUG_TO_FILENAME.get(class_slug)
    if not filename:
        try:
            with open('app/db/classes.json', encoding='utf-8') as f:
                all_classes_data = json.load(f)
            class_data = all_classes_data['classes_data'].get(class_slug)
            if not class_data:
                abort(404, description=f"Classe '{class_slug}' não encontrada.")
            return render_template('character_sheets/show.html', sheet=sheet, class_data=class_data)
        except (FileNotFoundError, KeyError):
            abort(404)

    try:
        with open(f'app/db/character_classes/{filename}.json', encoding='utf-8') as f:
            class_data_full = json.load(f)
            class_data = class_data_full.get(class_slug, {})
    except FileNotFoundError:
        abort(404, description=f"Arquivo JSON para a classe '{class_slug}' ('{filename}.json') não encontrado.")

    return render_template('character_sheets/show.html', sheet=sheet, class_data=class_data)

@bp.route('/character_sheet/<int:sheet_id>/delete', methods=['POST'])
def delete_character_sheet(sheet_id):
    sheet = CharacterSheet.query.get_or_404(sheet_id)
    user_id = sheet.user_id
    sheet_name = sheet.name

    db.session.delete(sheet)
    db.session.commit()

    flash(f'Ficha de personagem "{sheet_name}" foi apagada com sucesso!', 'success')
    return redirect(url_for('main.show_user', user_id=user_id))