from supextend.resources.internal.superset_batch_cleaner import DashboardCleaner
from supextend.core import MetastoreConnManager
from supextend.models.dashboards import Dashboard
from supextend.loggers.config import LoggingConfig


class DashboardIntern(DashboardCleaner):

    @staticmethod
    def create_intern_resource(**kwargs):
        """ Add dashboards to the metastore """

        dashboard = Dashboard(
            descriptive_id=kwargs.get('descriptive_id'),
            superset_id=kwargs.get('superset_id'),
            title=kwargs.get('title'),
            created_by=kwargs.get('created_by'),
            owners=kwargs.get('owners'),
            last_modified_on=kwargs.get('last_modified_on'),
            last_saved_by=kwargs.get('last_saved_by'),
            extra=kwargs.get('extra'),
            task=kwargs.get('task'),
            workspace=kwargs.get('workspace'),
            status=kwargs.get('status'),
        )
        for tag in kwargs.get('tags'):
            dashboard.tags.append(tag)
        with MetastoreConnManager() as session:
            session.add(dashboard)
            session.commit()
            LoggingConfig.logger.success(
                    f"Added the dashboard: {dashboard.title}.")
            return dashboard

    def update_intern_resource(self, pk, **kwargs):
        """ Updates dashboards in the metastore """

        d = self.get_intern_resource(pk)
        d.status = kwargs.get('status', d.status)
        d.delete_on = kwargs.get('delete_on', d.delete_on)
        d.last_saved_by = kwargs.get('last_saved_by', d.last_saved_by)
        d.title = kwargs.get('title', d.title)
        unique_new_tags = set(kwargs.get('tags', []))
        old_tags = d.tags
        # if tag is already a part of d.tags, skip
        # elif a tag in d.tags is not in unique_new_tags, remove the tag
        # elif a tag in unique_new_tags but not in d.tags, add the tag
        for d_tag in old_tags:
            if d_tag not in unique_new_tags:
                d.tags.remove(d_tag)
        for u_tag in unique_new_tags:
            if u_tag.title.lower() \
                    not in [tag.title.lower() for tag in old_tags]:
                d.tags.append(u_tag)
        d.descriptive_id = kwargs.get('descriptive_id', d.descriptive_id)
        d.task = kwargs.get('task', d.task)
        with MetastoreConnManager() as session:
            session.add_all([d, *unique_new_tags, *d.tags])
            session.commit()
            LoggingConfig.logger.success(f"Updated the dashboard: {d.title}.")
            return d

    @staticmethod
    def list_intern_resource():
        return Dashboard.query.all()

    def delete_intern_resource(self, pk):
        """ It is highly discouraged to remove deleted dashboards """
        pass

    @staticmethod
    def get_intern_resource(pk):
        return Dashboard.query.get(pk)
