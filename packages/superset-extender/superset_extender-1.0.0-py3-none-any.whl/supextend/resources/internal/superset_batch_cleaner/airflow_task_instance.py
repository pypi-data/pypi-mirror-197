from supextend.resources\
    .internal.superset_batch_cleaner import AirflowTaskInstanceCleaner
from supextend.core import MetastoreConnManager
from supextend.models.airflow_task_instances import AirflowTaskInstance
from supextend.loggers.config import LoggingConfig


class AirflowTaskInstanceIntern(AirflowTaskInstanceCleaner):

    @staticmethod
    def create_intern_resource(**kwargs):
        """ Add deleted airflow to the metastore """

        task_name = kwargs.get('task_name')
        dag_name = kwargs.get('dag_name')
        run_id = kwargs.get('run_id')
        removed_charts = kwargs.get('removed_charts', None)
        removed_dashboards = kwargs.get('removed_dashboards', None)

        airflow = AirflowTaskInstance(
            task_name=task_name,
            dag_name=dag_name,
            run_id=run_id
        )
        if removed_charts:
            for chart in removed_charts:
                airflow.removed_charts.append(chart)

        if removed_dashboards:
            for dash in removed_dashboards:
                airflow.removed_dashboards.append(dash)
        with MetastoreConnManager() as session:
            session.add(airflow)
            session.commit()
            LoggingConfig.logger.success(
                    f"Added the task: {airflow.task_name}.")
            return airflow

    def update_intern_resource(self, pk, **kwargs):
        """ It is highly discouraged to update this instance. """
        pass

    @staticmethod
    def list_intern_resource():
        return AirflowTaskInstance.query.all()

    def delete_intern_resource(self, pk):
        """ It is highly discouraged to remove this instance. """
        pass

    @staticmethod
    def get_intern_resource(pk):
        return AirflowTaskInstance.query.get(pk)
