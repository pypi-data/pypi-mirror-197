from supextend.resources.internal.superset_batch_cleaner import ChartCleaner
from supextend.core import MetastoreConnManager
from supextend.models.charts import Chart
from supextend.loggers.config import LoggingConfig


class ChartIntern(ChartCleaner):

    @staticmethod
    def create_intern_resource(**kwargs):
        """ Add deleted charts to the metastore """

        chart = Chart(
            descriptive_id=kwargs.get('descriptive_id'),
            superset_id=kwargs.get('superset_id'),
            title=kwargs.get('title'),
            type=kwargs.get('chart_type'),
            created_by=kwargs.get('created_by'),
            owners=kwargs.get('owners'),
            last_modified_on=kwargs.get('last_modified_on'),
            last_saved_by=kwargs.get('last_saved_by'),
            extra=kwargs.get('extra'),
            task=kwargs.get('task'),
            workspace=kwargs.get('workspace'),
            status=kwargs.get('status'),
            datasource=kwargs.get('datasource'),
            datasource_type=kwargs.get('datasource_type')
        )
        for tag in kwargs.get('tags'):
            chart.tags.append(tag)
        with MetastoreConnManager() as session:
            session.add(chart)
            session.commit()
            LoggingConfig.logger.success(f"Added the chart: {chart.title}.")
            return chart

    def update_intern_resource(self, pk, **kwargs):
        """ Updates charts in the metastore """

        c = self.get_intern_resource(pk)
        c.status = kwargs.get('status', c.status)
        c.title = kwargs.get('title', c.title)
        c.delete_on = kwargs.get('delete_on', c.delete_on)
        c.last_saved_by = kwargs.get('last_saved_by', c.last_saved_by)
        unique_new_tags = set(kwargs.get('tags', []))
        old_tags = c.tags
        # if tag is already a part of c.tags, skip
        # elif a tag in c.tags is not in unique_new_tags, remove the tag
        # elif a tag in unique_new_tags but not in c.tags, add the tag
        for d_tag in old_tags:
            if d_tag not in unique_new_tags:
                c.tags.remove(d_tag)
        for u_tag in unique_new_tags:
            if u_tag.title.lower() \
                    not in [tag.title.lower() for tag in old_tags]:
                c.tags.append(u_tag)
        c.descriptive_id = kwargs.get('descriptive_id', c.descriptive_id)
        c.task = kwargs.get('task', c.task)
        with MetastoreConnManager() as session:
            session.add_all([c, *unique_new_tags, *c.tags])
            session.commit()
            LoggingConfig.logger.success(f"Updated the dashboard: {c.title}.")
            return c

    @staticmethod
    def list_intern_resource():
        return Chart.query.all()

    def delete_intern_resource(self, pk):
        """ It is highly discouraged to remove deleted charts """
        pass

    @staticmethod
    def get_intern_resource(pk):
        return Chart.query.get(pk)
