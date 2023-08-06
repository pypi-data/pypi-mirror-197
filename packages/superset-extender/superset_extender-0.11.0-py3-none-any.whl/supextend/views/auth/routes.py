from flask import render_template, url_for, flash, redirect, request, Blueprint
from supextend.initialization import oidc, bcrypt
from flask_login import login_user, current_user, logout_user
from supextend.models.owners import Owner
from supextend.resources.common.superset_batch_cleaner\
    .owner import OwnerResourceManager
from supextend.views.auth.forms import (
    RegistrationForm,
    LoginForm,
    PasswordRegistrationForm
    )

auth = Blueprint('auth', __name__)
owner_resource_manager = OwnerResourceManager()


@auth.route("/register", methods=['GET', 'POST'])
def register():
    """
    Workflow:
    -----------
    case 1: Owner is already in the metastore (automatically added via
    'supextend init')
        To register, the owner needs to present their username and password
    case 2: Owner is not in the metastore
        To register, the owner needs to present their first name, last name
        along with
        their username and password

    """
    if current_user.is_authenticated:
        return redirect(url_for('workspaces.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # check owner exist
        owner = Owner.query.filter_by(username=form.username.data).first()
        if owner:
            if not owner.password:
                owner_resource_manager.update_intern_resource(
                        pk=owner.id,
                        password=form.password.data
                        )
            else:
                flash(f'The user {owner.username} is already registered',
                      'warning')
                return redirect(url_for('auth.login'))
        else:
            owner_resource_manager.create_intern_resource(
                    username=form.username.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    password=form.password.data
                    )
        flash('You are now able to login', 'success')
        return redirect(url_for('auth.login'))
    return render_template('superset/auth/register.html', form=form)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('workspaces.home'))
    form = LoginForm()
    if form.validate_on_submit():
        owner = Owner.query.filter_by(username=form.username.data).first()
        if owner:
            # this is in the metastore
            if owner.password:
                # check pass if correct login else register pass
                if bcrypt.check_password_hash(owner.password,
                                              form.password.data):
                    login_user(owner, remember=form.remember.data)
                    next_page = request.args.get('next')
                    return redirect(next_page) if next_page \
                        else redirect(url_for('workspaces.home'))
            else:
                flash(
                        f"Login Unsuccessful. "
                        f"Please register the superset password"
                        f" for the user: {owner.username}",
                        'warning')
                return redirect(url_for('auth.register_pwd',
                                        owner_id=owner.id))
        flash('Login Unsuccessful. '
              'Please check username and password',
              'danger')
    return render_template('superset/auth/login.html', form=form)


@auth.route("/owner/<int:owner_id>/update", methods=['GET', 'POST'])
def register_pwd(owner_id):
    if current_user.is_authenticated:
        return redirect(url_for('workspaces.home'))
    owner = Owner.query.get_or_404(owner_id)

    form = PasswordRegistrationForm()
    if form.validate_on_submit():
        if not owner.password:
            owner_resource_manager.update_intern_resource(
                    pk=owner.id,
                    password=form.password.data
                    )
            flash('Password registered! You are now able to login',
                  'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Password already registered for this user', 'danger')
    form.username.data = owner.username
    form.first_name.data = owner.first_name
    form.last_name.data = owner.last_name
    return render_template('superset/auth/register.html', form=form)


@auth.route("/logout")
def logout():
    logout_user()
    oidc.logout()
    return redirect(url_for('workspaces.home'))
