import json

from flask import (render_template, url_for, flash,
                   redirect, request, Blueprint, g)
from flask_login import login_required
from supextend.initialization import oidc
from supextend.views.charts.utils import ch_process_form
from supextend.resources.common.superset_batch_cleaner\
    .chart import ChartResourceManager
from supextend.resources.internal.superset_batch_cleaner\
    .airflow_entrypoint import AirflowExec
from supextend.utils.superset import (
    check_auth,
    get_normalized_title,
    get_current_user_fullname
    )

charts = Blueprint('charts', __name__)
ch_resource_manager = ChartResourceManager()


@charts.before_request
def before_request():
    if oidc.user_loggedin:
        g.user = oidc.user_getinfo(
                ['preferred_username', 'given_name', 'family_name'])
    else:
        g.user = None


@charts.route("/chart/", methods=['GET', 'POST'])
@check_auth(login_required, oidc.require_login)
def home():
    ch = ch_resource_manager.list_all()
    return render_template('superset/charts/index.html', charts=ch)


@charts.route("/workspace/<int:workspace_pk>/chart/<int:chart_pk>/update",
              methods=['GET', 'POST'])
@check_auth(login_required,
            oidc.require_login)
def update_chart(chart_pk, workspace_pk):
    if request.method == 'POST':
        ch_resource_manager.update_resource(
            intern_id=chart_pk,
            unrefined_superset_title=ch_process_form(request.form),
            last_saved_by=get_current_user_fullname()
        )
        flash('Chart successfully updated', 'success')
    return redirect(url_for('workspaces.list_chart_workspace',
                            workspace_id=workspace_pk))


@charts.route("/workspace/<int:workspace_pk>/chart/compliant",
              methods=['GET', 'POST'])
@check_auth(login_required,
            oidc.require_login)
def make_compliant(workspace_pk):
    upd_ids = set(request.form.getlist('chart_id'))

    if request.method == 'POST':
        charts = [ch_resource_manager
                  .get_intern_resource(id_) for id_ in upd_ids]
        for c in charts:
            title = json.loads(c.extra)['slice_name']
            ch_resource_manager.update_resource(
                intern_id=c.id,
                unrefined_superset_title=get_normalized_title(title),
                last_saved_by=get_current_user_fullname()
            )
    return redirect(url_for('workspaces.list_chart_workspace',
                            workspace_id=workspace_pk))


@charts.route("/workspace/<int:workspace_id>/refresh_cache")
@check_auth(login_required, oidc.require_login)
def refresh_cache_chart(workspace_id):
    AirflowExec.init_metastore()
    flash('The data was successfully updated', 'success')
    return redirect(url_for('workspaces.list_chart_workspace',
                            workspace_id=workspace_id))
