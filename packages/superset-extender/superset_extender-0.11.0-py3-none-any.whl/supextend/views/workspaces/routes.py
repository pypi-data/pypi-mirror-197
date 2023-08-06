from flask import (render_template, url_for, flash,
                   redirect, request, Blueprint, g)
from supextend.initialization import oidc
from flask_login import login_required, current_user
from supextend.config import Config
from supextend.resources.common.workspace_extension \
    .workspace import WorkspaceResourceManager
from supextend.resources.common.superset_batch_cleaner \
    .dashboard import DashboardResourceManager
from supextend.models.owners import Owner
from supextend.utils.superset import check_auth

workspaces = Blueprint('workspaces', __name__)
wp_resource_manager = WorkspaceResourceManager()


@workspaces.before_request
def before_request():
    if oidc.user_loggedin:
        current_user = oidc.user_getinfo(
                ['preferred_username', 'given_name', 'family_name'])
        owner_exists = Owner.query \
            .filter_by(username=current_user.get('preferred_username')).first()
        if owner_exists:
            current_user['color'] = owner_exists.color
        else:
            current_user['color'] = '#B9B7BD'
        g.user = current_user
    else:
        g.user = None


@workspaces.route("/", methods=['GET', 'POST'])
@workspaces.route("/home", methods=['GET', 'POST'])
@check_auth(login_required, oidc.require_login)
def home():
    all_ds = DashboardResourceManager.list_intern_resource()
    return render_template(
            'superset/workspaces/index.html',
            workspaces=wp_resource_manager.list_intern_resource(),
            dashboards=all_ds
            )


@workspaces.route("/workspace/new", methods=['GET', 'POST'])
@check_auth(login_required, oidc.require_login)
def create_workspace():
    username = None
    if g.user:
        username = g.user.preferred_username
    elif current_user.is_authenticated:
        username = current_user.username
    else:
        username = Config.superset_username
    if request.method == 'POST' and username:
        wp_resource_manager.create_intern_resource(
                title=request.form['title'],
                color=request.form['color'],
                created_by=username,
                description=request.form['description']
                )
        flash('New workspace successfully created', 'success')
        return redirect(url_for('workspaces.home'))
    flash('Unable to create the new workspace please resubmit the form',
          'danger')
    return render_template(
            'superset/workspaces/index.html'
            )


@workspaces.route("/workspace/<int:workspace_id>/dashboards",
                  methods=['GET', 'POST'])
@check_auth(login_required, oidc.require_login)
def list_dashboard_workspace(workspace_id):
    wp = wp_resource_manager.get_intern_resource(workspace_id)

    return render_template(
            'superset/dashboards/index.html',
            workspace_id=wp.id,
            workspace_title=wp.title,
            dashboards=wp.dashboards
            )


@workspaces.route("/workspace/<int:workspace_id>/charts",
                  methods=['GET', 'POST'])
@check_auth(login_required, oidc.require_login)
def list_chart_workspace(workspace_id):
    wp = wp_resource_manager.get_intern_resource(workspace_id)
    return render_template(
            'superset/charts/index.html',
            workspace_title=wp.title,
            workspace_id=workspace_id,
            charts=wp.charts
            )


@workspaces.route("/workspace/<int:workspace_id>/update",
                  methods=['GET', 'POST'])
@check_auth(login_required, oidc.require_login)
def update_workspace(workspace_id):
    if request.method == 'POST':
        wp_resource_manager.update_intern_resource(
                workspace_id,
                title=request.form['title'],
                color=request.form['color'],
                description=request.form['description'],
                created_by=Config.superset_username,
                )
        flash('Workspace successfully updated', 'success')
    return redirect(url_for('workspaces.home'))


@workspaces.route("/workspace/<int:workspace_id>/delete",
                  methods=['POST', 'GET'])
@check_auth(login_required, oidc.require_login)
def delete_workspace(workspace_id):
    if request.method == 'POST' and request.form['confirm'] == 'DELETE':
        wp_resource_manager.delete_intern_resource(workspace_id)
        flash('Workspace was removed', 'success')
    return redirect(url_for('workspaces.home'))


@workspaces.route("/workspace/<int:workspace_id>/add_dashboard",
                  methods=['POST', 'GET'])
@check_auth(login_required, oidc.require_login)
def add_dashboards(workspace_id):
    """ Adds dashboards to a workspace """
    wp = wp_resource_manager.get_intern_resource(workspace_id)
    if request.method == 'POST':
        ids = request.form.getlist('dashboards')
        dashboards = [DashboardResourceManager
                      .get_intern_resource(id_) for id_ in ids]
        wp_resource_manager.add_dashboards(wp, dashboards)
        return redirect(url_for('workspaces.list_dashboard_workspace',
                                workspace_id=workspace_id))
    return redirect(url_for('workspaces.home'))
