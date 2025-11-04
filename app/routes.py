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

    flash('Ficha de personagem criada com sucesso!', 'success')

    if character_sheet.class_slug == 'clerigo':
        return redirect(url_for('main.cleric_traits', sheet_id=character_sheet.id))

    return redirect(url_for('main.show_user', user_id=user.id))

  return render_template('character_sheets/new.html', form=form, classes=classes_data['classes_data'])


@bp.route('/cleric/traits/<int:sheet_id>', methods=['GET', 'POST'])
def cleric_traits(sheet_id):
    sheet = CharacterSheet.query.get_or_404(sheet_id)

    if request.method == 'POST':
        base_traits_selection = request.form.getlist('base_traits')
        divine_order_selection = request.form.get('divine_order')

        if len(base_traits_selection) != 2:
            flash('Você deve escolher exatamente duas perícias.', 'danger')
            return redirect(url_for('main.cleric_traits', sheet_id=sheet_id))

        sheet.class_features = {
            'base_traits': base_traits_selection,
            'divine_order': divine_order_selection
        }
        db.session.commit()

        flash('Traços de Clérigo salvos com sucesso!', 'success')
        return redirect(url_for('main.show_character_sheet', sheet_id=sheet_id))

    with open('app/db/cleric.json', encoding='utf-8') as f:
        cleric_data = json.load(f)

    cleric_info = cleric_data['clerigo']
    progression_level_1 = cleric_info['progression']['1']

    base_traits = next((item for item in progression_level_1 if item.get('title') == 'Perícias Base'), None)
    spellcasting = next((item for item in progression_level_1 if item.get('name') == 'Conjuração'), None)
    divine_order = next((item for item in progression_level_1 if item.get('title') == 'Ordem Divina'), None)

    return render_template('cleric_traits.html',
                           sheet=sheet,
                           cleric=cleric_info,
                           base_traits=base_traits,
                           spellcasting=spellcasting,
                           divine_order=divine_order)


@bp.route('/character_sheet/<int:sheet_id>')
def show_character_sheet(sheet_id):
    sheet = CharacterSheet.query.get_or_404(sheet_id)
    class_slug = sheet.class_slug

    json_file_name = f'{class_slug}.json' if class_slug != 'clerigo' else 'cleric.json'
    if class_slug == 'barbaro':
        json_file_name = 'barbarian.json'
    elif class_slug == 'mago':
        json_file_name = 'wizard.json'
    if class_slug == 'clerigo':
        json_file_name = 'cleric.json'
    else:

        try:
            with open('app/db/classes.json', encoding='utf-8') as f:
                all_classes_data = json.load(f)
            class_data = all_classes_data['classes_data'].get(class_slug)
            return render_template('character_sheets/show.html', sheet=sheet, class_data=class_data)
        except (FileNotFoundError, KeyError):
            abort(404)

    try:
        with open(os.path.join('app/db', json_file_name), encoding='utf-8') as f:
            class_data_full = json.load(f)
            class_data = class_data_full.get(class_slug, class_data_full)

    except FileNotFoundError:
        abort(404)

    return render_template('character_sheets/show.html', sheet=sheet, class_data=class_data)



