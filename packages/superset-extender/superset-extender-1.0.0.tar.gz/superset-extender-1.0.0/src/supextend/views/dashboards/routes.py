import json
from flask import (render_template, url_for, flash,
                   redirect, request, Blueprint, g)
from flask_login import login_required
from supextend.initialization import oidc
from supextend.views.dashboards.utils import dash_process_form
from supextend.resources.common.superset_batch_cleaner\
    .dashboard import DashboardResourceManager
from supextend.resources.internal.superset_batch_cleaner\
    .airflow_entrypoint import AirflowExec
from supextend.utils.superset import (
    check_auth,
    get_normalized_title,
    get_current_user_fullname
    )

dashboards = Blueprint('dashboards', __name__)
ds_resource_manager = DashboardResourceManager()


@dashboards.before_request
def before_request():
    if oidc.user_loggedin:
        g.user = oidc.user_getinfo(
                ['preferred_username', 'given_name', 'family_name'])
    else:
        g.user = None


@dashboards.route("/dashboard/", methods=['GET', 'POST'])
@check_auth(login_required, oidc.require_login)
def home():
    ds = ds_resource_manager.list_all()
    return render_template('superset/dashboards/index.html', dashboards=ds)


@dashboards.route("/workspace/<int:workspace_pk>"
                  "/dashboard/<int:dashboard_pk>/<dashboard_status>/update",
                  methods=['GET', 'POST'])
@check_auth(login_required, oidc.require_login)
def update_dashboard(dashboard_pk, workspace_pk, dashboard_status):
    if request.method == 'POST':
        if dashboard_status != 'published':
            ds_resource_manager.update_resource(
                intern_id=dashboard_pk,
                unrefined_superset_title=dash_process_form(request.form),
                last_saved_by=get_current_user_fullname()
            )
            flash('Dashboard successfully updated', 'success')
        else:
            flash('Cannot edit published dashboards', 'danger')

    return redirect(url_for('workspaces.list_dashboard_workspace',
                            workspace_id=workspace_pk))


@dashboards.route("/workspace/<int:workspace_pk>/dashboard/compliant",
                  methods=['GET', 'POST'])
@check_auth(login_required, oidc.require_login)
def make_compliant(workspace_pk):
    upd_ids = set(request.form.getlist('dashboard_id'))

    if request.method == 'POST':
        dashbds = [ds_resource_manager
                   .get_intern_resource(id_) for id_ in upd_ids]
        for d in dashbds:
            title = json.loads(d.extra)['dashboard_title']
            if d.status != 'published':
                ds_resource_manager.update_resource(
                    intern_id=d.id,
                    unrefined_superset_title=get_normalized_title(title),
                    last_saved_by=get_current_user_fullname()
                )
            else:
                flash(f'Cannot edit published dashboards: {title}', 'warning')
    return redirect(url_for('workspaces.list_dashboard_workspace',
                            workspace_id=workspace_pk))


@dashboards.route("/workspace/<int:workspace_id>/refresh_cache")
@check_auth(login_required, oidc.require_login)
def refresh_cache_dashboard(workspace_id):
    AirflowExec.init_metastore()
    flash('The data was successfully collected', 'success')
    return redirect(url_for('workspaces.list_dashboard_workspace',
                            workspace_id=workspace_id))
