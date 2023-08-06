from prettytable import PrettyTable
import random
from datetime import datetime

from supextend.resources.common.superset_batch_cleaner \
    .chart import ChartResourceManager
from supextend.resources.common.superset_batch_cleaner \
    .dashboard import DashboardResourceManager
from supextend.resources.common.superset_batch_cleaner \
    .airflow_task_instance import AirflowTaskInstanceResourceManager
from supextend.resources.common.superset_batch_cleaner \
    .owner import OwnerResourceManager
from supextend.resources.common.superset_batch_cleaner \
    .tag import TagResourceManager
from supextend.resources.common.workspace_extension \
    .workspace import WorkspaceResourceManager
from supextend.models.owners import Owner
from supextend.models.tags import Tag
from supextend.models.workspaces import Workspace
from supextend.models.dashboards import Dashboard
from supextend.models.charts import Chart
from supextend.loggers.config import LoggingConfig
from supextend.utils.superset import color_generator


class AirflowExec:
    charts_m = ChartResourceManager()
    dashboards_m = DashboardResourceManager()
    tasks_m = AirflowTaskInstanceResourceManager()
    owner_m = OwnerResourceManager()
    tag_m = TagResourceManager()
    wp_m = WorkspaceResourceManager()

    @classmethod
    def collect_entities(
            cls,
            size,
            charts_filter_val='Obsolete',
            dashboards_filter_val='Obsolete'
            ):
        charts = cls.charts_m.list_superset_resource(
                filter_value=charts_filter_val,
                page_size=size)
        dashboards = cls.dashboards_m.list_superset_resource(
                filter_value=dashboards_filter_val,
                page_size=size)
        return charts, dashboards

    @classmethod
    def remove_entities(cls,
                        task_id,
                        dag_id,
                        task_run_id,
                        safe=True,
                        charts=None,
                        dashboards=None
                        ):

        airflow_task = cls.tasks_m.create_intern_resource(
                task_name=task_id,
                dag_name=dag_id,
                run_id=task_run_id
                )

        workspace_default_exists = Workspace.query. \
            filter_by(title='Default').first()
        if workspace_default_exists:
            workspace = workspace_default_exists
            LoggingConfig.logger.info("Skip [Deleted]"
                                      " workspace already exists")
        else:
            workspace = cls.wp_m.create_intern_resource(
                    title='Default',
                    color='#aea79f',
                    created_by='Default',
                    description='This workspace automatically'
                                ' contains all dashboards '
                                'and charts after initialization'
                    )

        # save dashboards
        del_dash = []
        if dashboards:
            del_dash = cls._save_deleted_dashboards(
                    dashboards,
                    airflow_task,
                    workspace,
                    safe)

        # save charts
        del_charts = []
        if charts:
            del_charts = cls._save_deleted_charts(
                    charts,
                    airflow_task,
                    workspace,
                    safe)

        return del_charts, del_dash

    @classmethod
    def report(cls, charts, dashboards):
        print(cls.dashboard_report(dashboards))
        print(cls.chart_report(charts))

    @staticmethod
    def dashboard_report(dashboards):
        report = PrettyTable()
        report.title = 'Dashboard report'
        columns = {
                "#": 5,
                "Dashboard title": 25,
                "Last modified by": 25,
                "Last modified on": 25,
                "Status": 25,
                "Created by": 25,
                "Owners": 50
                }
        report.field_names = columns.keys()
        report._max_width = columns
        for idx, dash in enumerate(dashboards):
            report.add_row([
                    idx + 1,
                    dash.reformat(),
                    dash.last_saved_by,
                    dash.last_modified_on.strftime("%d %b, %Y at %H:%M:%S"),
                    dash.status,
                    dash.created_by,
                    ', '.join(f"{owner[1]} "
                              f"{owner[0]}" for owner in dash.get_owners())
                    ])
        return report

    @staticmethod
    def chart_report(charts):
        report = PrettyTable()
        report.title = 'Charts report'
        columns = {
                "#": 5,
                "Chart title": 25,
                "Last modified by": 25,
                "Last modified on": 25,
                "Chart type": 25,
                "Created by": 25,
                "Owners": 50
                }
        report.field_names = columns.keys()
        report._max_width = columns
        for idx, chart in enumerate(charts):
            report.add_row([
                    idx + 1,
                    chart.reformat(),
                    chart.last_saved_by,
                    chart.last_modified_on.strftime("%d %b, %Y at %H:%M:%S"),
                    chart.type,
                    chart.created_by,
                    ', '.join(f"{owner[1]} "
                              f"{owner[0]}" for owner in chart.get_owners())
                    ])
        return report

    @classmethod
    def _save_deleted_charts(cls, charts, airflow_task, workspace, safe=True):
        deleted_charts = []
        colors = color_generator()
        for chart in charts:
            if not safe:
                cls.charts_m.delete_superset_resource(chart.pk)
            owners = []
            for owner in chart.owners:
                owner_exists = Owner.query. \
                    filter_by(username=owner['username']).first()
                if owner_exists:
                    owners.append(owner_exists)
                else:
                    new_owner = cls.owner_m.create_intern_resource(
                            first_name=owner['first_name'],
                            last_name=owner['last_name'],
                            username=owner['username'],
                            color=random.choice(colors)
                            )
                    owners.append(new_owner)

            tags = []
            for tag in chart.get_formatted_tags():
                tag_exists = Tag.query.filter_by(title=tag).first()
                if tag_exists:
                    tags.append(tag_exists)
                else:
                    new_tag = cls.tag_m.create_intern_resource(
                            title=tag,
                            color=random.choice(colors)
                            )
                    tags.append(new_tag)
            chart_exists = Chart.query.filter_by(superset_id=chart.pk).first()
            if chart_exists:
                if chart_exists.status == 'deleted':
                    LoggingConfig.logger.info(
                            f"Skip [{chart.get_formatted_title()}] chart"
                            f" is already deleted and in metastore.")
                else:
                    cls.charts_m.update_intern_resource(
                            pk=chart_exists.id,
                            status='deleted',
                            title=chart_exists.title,
                            descriptive_id=chart_exists.descriptive_id,
                            deleted_on=datetime.utcnow,
                            task=airflow_task
                            )
            else:
                cls.charts_m.create_intern_resource(
                        descriptive_id=chart.get_descriptive_id(),
                        superset_id=chart.pk,
                        status="deleted",
                        title=chart.get_formatted_title(),
                        created_by=chart.created_by,
                        owners=owners,
                        last_modified_on=chart.last_modified_on,
                        last_saved_by=chart.last_saved_by,
                        extra=str(chart.extra),
                        task=airflow_task,
                        workspace=workspace,
                        tags=tags,
                        chart_type=chart.type,
                        datasource=chart.datasource,
                        datasource_type=chart.datasource_type
                        )
                deleted_charts.append(chart)
        return deleted_charts

    @classmethod
    def _save_deleted_dashboards(cls,
                                 dashboards,
                                 airflow_task,
                                 workspace,
                                 safe=True
                                 ):
        deleted_dashboards = []
        colors = color_generator()
        for dashboard in dashboards:
            if not safe:
                cls.dashboards_m.delete_superset_resource(dashboard.pk)

            owners = []
            for owner in dashboard.owners:
                owner_exists = Owner.query. \
                    filter_by(username=owner['username']).first()
                if owner_exists:
                    owners.append(owner_exists)
                else:
                    new_owner = cls.owner_m.create_intern_resource(
                            first_name=owner['first_name'],
                            last_name=owner['last_name'],
                            username=owner['username'],
                            color=random.choice(colors)
                            )
                    owners.append(new_owner)

            tags = []
            for tag in dashboard.get_formatted_tags():
                tag_exists = Tag.query.filter_by(title=tag).first()
                if tag_exists:
                    tags.append(tag_exists)
                else:
                    new_tag = cls.tag_m.create_intern_resource(
                            title=tag,
                            color=random.choice(colors)
                            )
                    tags.append(new_tag)
            dashboard_exists = Dashboard.query. \
                filter_by(superset_id=dashboard.pk).first()
            if dashboard_exists:
                if dashboard_exists.status == 'deleted':
                    LoggingConfig.logger.info(
                            f"Skip [{dashboard.get_formatted_title()}] "
                            f"dashboard is already "
                            f"deleted and in metastore.")
                else:
                    cls.dashboards_m.update_intern_resource(
                            pk=dashboard_exists.id,
                            status='deleted',
                            title=dashboard_exists.title,
                            deleted_on=datetime.utcnow,
                            descriptive_id=dashboard_exists.descriptive_id,
                            task=airflow_task
                            )
            else:
                cls.dashboards_m.create_intern_resource(
                        descriptive_id=dashboard.get_formatted_desc_id(),
                        superset_id=dashboard.pk,
                        status="deleted",
                        title=dashboard.get_formatted_title(),
                        created_by=dashboard.created_by,
                        owners=owners,
                        last_modified_on=dashboard.last_modified_on,
                        last_saved_by=dashboard.last_saved_by,
                        extra=str(dashboard.extra),
                        task=airflow_task,
                        workspace=workspace,
                        tags=tags,
                        )
                deleted_dashboards.append(dashboard)
        return deleted_dashboards

    @classmethod
    def init_metastore(cls):
        _size = 1000_000_000
        _filter_chart = str()
        _filter_dashboard = str()
        charts, dashboards = cls.collect_entities(
                size=_size,
                charts_filter_val=_filter_chart,
                dashboards_filter_val=_filter_dashboard
                )

        workspace_default_exists = Workspace.query. \
            filter_by(title='Default').first()
        if workspace_default_exists:
            workspace = workspace_default_exists
            LoggingConfig.logger.info("Skip [Default]"
                                      " workspace already exists")
        else:
            workspace = cls.wp_m.create_intern_resource(
                    title='Default',
                    color='#aea79f',
                    created_by='Default',
                    description='This workspace'
                                ' automatically contains all '
                                'dashboards and charts after initialization'
                    )
            LoggingConfig.logger.success("Created The [Default] workspace")
        cls._init_meta_dashboards(dashboards, workspace)
        cls._init_meta_charts(charts, workspace)
        LoggingConfig.logger.success("Initialization complete. "
                                     "The Metastore is up to date")

    @classmethod
    def _init_meta_charts(cls, charts, workspace):
        count_init = 0
        colors = color_generator()
        for chart in charts:
            owners = []
            for owner in chart.owners:
                owner_exists = Owner.query. \
                    filter_by(username=owner['username']).first()
                if owner_exists:
                    owners.append(owner_exists)
                else:
                    new_owner = cls.owner_m.create_intern_resource(
                            first_name=owner['first_name'],
                            last_name=owner['last_name'],
                            username=owner['username'],
                            color=random.choice(colors)
                            )
                    owners.append(new_owner)

            tags = []
            for tag in chart.get_formatted_tags():
                tag_exists = Tag.query.filter_by(title=tag).first()
                if tag_exists:
                    tags.append(tag_exists)
                else:
                    new_tag = cls.tag_m.create_intern_resource(
                            title=tag,
                            color=random.choice(colors)
                            )
                    tags.append(new_tag)
            chart_exists = Chart.query.filter_by(superset_id=chart.pk).first()
            if chart_exists:
                LoggingConfig.logger.info(
                        f"Skip [{chart.get_formatted_title()}] chart"
                        f" is already present in metastore.")
            else:
                cls.charts_m.create_intern_resource(
                        descriptive_id=chart.get_descriptive_id(),
                        superset_id=chart.pk,
                        status=chart.status,
                        title=chart.get_formatted_title(),
                        created_by=chart.created_by,
                        owners=owners,
                        last_modified_on=chart.last_modified_on,
                        last_saved_by=chart.last_saved_by,
                        extra=str(chart.extra),
                        task=None,
                        workspace=workspace,
                        tags=tags,
                        chart_type=chart.type,
                        datasource=chart.datasource,
                        datasource_type=chart.datasource_type
                        )
                count_init += 1
        LoggingConfig.logger.success(f"Initialized [{count_init}] charts.")

    @classmethod
    def _init_meta_dashboards(cls, dashboards, workspace):
        count_init = 0
        colors = color_generator()

        for dashboard in dashboards:
            LoggingConfig.logger.info(
                    f"Init: {dashboard.get_formatted_title()}")
            owners = []
            for owner in dashboard.owners:
                owner_exists = Owner.query. \
                    filter_by(username=owner['username']).first()
                if owner_exists:
                    owners.append(owner_exists)
                else:
                    new_owner = cls.owner_m.create_intern_resource(
                            first_name=owner['first_name'],
                            last_name=owner['last_name'],
                            username=owner['username'],
                            color=random.choice(colors)
                            )
                    owners.append(new_owner)

            tags = []
            for tag in dashboard.get_formatted_tags():
                tag_exists = Tag.query.filter_by(title=tag).first()
                if tag_exists:
                    tags.append(tag_exists)
                else:
                    new_tag = cls.tag_m.create_intern_resource(
                            title=tag,
                            color=random.choice(colors)
                            )
                    tags.append(new_tag)
            dashboard_exists = Dashboard.query. \
                filter_by(superset_id=dashboard.pk).first()
            if dashboard_exists:
                LoggingConfig.logger.info(
                        f"Skip [{dashboard.get_formatted_title()}] dashboard"
                        f" is already present and in metastore.")
            else:
                cls.dashboards_m.create_intern_resource(
                        descriptive_id=dashboard.get_formatted_desc_id(),
                        superset_id=dashboard.pk,
                        status=dashboard.status,
                        title=dashboard.get_formatted_title(),
                        created_by=dashboard.created_by,
                        owners=owners,
                        last_modified_on=dashboard.last_modified_on,
                        last_saved_by=dashboard.last_saved_by,
                        extra=str(dashboard.extra),
                        task=None,
                        workspace=workspace,
                        tags=tags,
                        )
                count_init += 1
        LoggingConfig.logger.success(f"Initialized [{count_init}] dashboards.")
