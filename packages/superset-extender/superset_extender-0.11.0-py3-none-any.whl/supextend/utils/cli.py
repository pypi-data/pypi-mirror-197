import click
from supextend.resources.internal.superset_batch_cleaner \
    .airflow_entrypoint import AirflowExec
from supextend.config import Config
from supextend.initialization import db
from . import __version__
from supextend.loggers.config import LoggingConfig


@click.option('-rc',
              '--remove-charts',
              default=True,
              show_default=True,
              help="'false' ensures charts are not removed")
@click.option('-rd',
              '--remove-dashboards',
              default=True,
              show_default=True,
              help="'false' ensures dashboards are not removed")
@click.option('-p',
              '--page-size',
              default=0,
              help="Number of items to report on")
@click.option('-f',
              '--filter-by',
              default='Obsolete',
              show_default=True, help="Word to filter by")
@click.option('-s',
              '--safe',
              default=True,
              show_default=True,
              help="Safety net. Delete entities when 'false'")
def clean_superset(
        safe,
        filter_by,
        page_size,
        remove_dashboards,
        remove_charts
        ):
    """ Batch delete obsolete entities on Superset. """

    removable_dash = None
    removable_charts = None
    if safe:
        LoggingConfig.logger.warning("Start cleanup task in SAFE mode,"
                                     " no items will be removed from Superset "
                                     "but status will be modified"
                                     " in metastore tables.")
    else:
        LoggingConfig.logger.warning("Start cleaning task"
                                     " without SAFE mode, "
                                     "items will be removed from Superset and "
                                     "it is not recoverable.")

    charts, dashboards = AirflowExec.collect_entities(
            charts_filter_val=filter_by,
            dashboards_filter_val=filter_by,
            size=page_size
            )
    if remove_dashboards:
        removable_dash = dashboards
    else:
        LoggingConfig.logger.info("Dashboards will not be removed."
                                  " (Flags '-rd' or "
                                  "'--remove-dashboards' are present)")
    if remove_charts:
        removable_charts = charts
    else:
        LoggingConfig.logger.info("Charts will not be removed."
                                  "  (Flags '-rc' or "
                                  "'--remove-charts' are present)")
    AirflowExec.remove_entities(
            charts=removable_charts,
            dashboards=removable_dash,
            task_id=Config.airflow_task_name,
            dag_id=Config.airflow_dag_name,
            task_run_id=Config.airflow_run_id,
            safe=safe
            )


@click.option('-p',
              '--page-size',
              default=0,
              help="Number of items to report on")
@click.option('-f',
              '--filter-by',
              help="Word to filter by")
def report_superset(filter_by, page_size):
    """ Reads superset charts and dashboards from superset. """

    LoggingConfig.logger.info("Retrieve items for reports.")
    charts, dashboards = AirflowExec.collect_entities(
            charts_filter_val=filter_by,
            dashboards_filter_val=filter_by,
            size=page_size
            )
    AirflowExec.report(charts, dashboards)


def version():
    """ Print the Superset-Extender version number
        and the compatible Superset version."""

    print(f"Superset-Extender {__version__}\nSuperset 2.0")


def init():
    """Creates database."""

    LoggingConfig.logger.info(
            "Instantiate tables in the metastore if none exist.")
    db.create_all()

    LoggingConfig.logger.info("Collect Superset data.")
    AirflowExec.init_metastore()


def drop_db():
    """Cleans database."""

    LoggingConfig.logger.warning(
            "Dropped all tables in the metastore. This action is irreversible")
    db.drop_all()


def init_app(app):
    # add multiple commands in a bulk.
    for command in [
            clean_superset,
            report_superset,
            init,
            drop_db,
            version]:
        app.cli.add_command(app.cli.command()(command))
