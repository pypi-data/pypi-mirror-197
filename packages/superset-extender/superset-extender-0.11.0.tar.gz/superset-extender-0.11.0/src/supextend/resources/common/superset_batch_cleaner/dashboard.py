from urllib.parse import urljoin
import random

from supextend.resources\
    .internal.superset_batch_cleaner.dashboard import DashboardIntern
from supextend.resources\
    .external.superset.dashboard import DashboardExtern
from supextend.resources\
    .common.superset_batch_cleaner.tag import TagResourceManager
from supextend.utils.superset import TitleRefactored
from supextend.models.tags import Tag
from supextend.utils.superset import color_generator
from supextend.config import Config


class DashboardResourceManager(DashboardIntern, DashboardExtern):
    """A class to represent resource management
    for both Internal and External(Superset) dashboards.

    Methods:
    --------
    list_all()
        Combines results from both
        the superset api call and the metastore call.
        This is done for the convenience in data presentation.
    """

    def list_all(self):
        """
        Combines results from both
        the superset api call and the metastore call.
        returns a dict of the combined data.
        """

        ds_intern = self.list_intern_resource()
        ds_superset = self.list_superset_resource()
        ds_intern_ref = [{
            'title': dash.title,
            'created_by': dash.created_by,
            'owners': dash.owners,
            'last_modified_on': dash.last_modified_on,
            'last_saved_by': dash.last_saved_by,
            'tags': dash.tags,
            'descriptive_id': dash.descriptive_id,
            'status': dash.status,
            'url_superset': None,
            'superset_pk': None,
            'id': f"{count}-{dash.title}".replace(' ', ''),
            'kind': 'internal',
            'airflow_url': urljoin(
                Config.airflow_base_url,
                f"/taskinstance/list/?flt1_dag_id_equals={dash.task.dag_name}"
                f"&_flt_3_task_id={dash.task.task_name}") if dash.task
            else None,
            'airflow_run_id': dash.task.run_id if dash.task else None
        } for count, dash in enumerate(ds_intern)]

        ds_superset_ref = [{
            'title': dash.get_title(),
            'created_by': dash.created_by,
            'owners': dash.get_owners(),
            'last_modified_on': dash.last_modified_on,
            'last_saved_by': dash.last_saved_by,
            'tags': dash.get_tags(),
            'descriptive_id': dash.get_descriptive_id(),
            'status': dash.status,
            'url_superset': dash.url_superset,
            'superset_pk': dash.pk,
            'id': f"{count}-{dash.get_title()}".replace(' ', ''),
            'airflow_url': None,
            'airflow_run_id': None,
            'kind': 'external'
        } for count, dash in enumerate(ds_superset)]

        return ds_intern_ref + ds_superset_ref

    def update_resource(self,
                        intern_id,
                        unrefined_superset_title,
                        last_saved_by):
        """
        Updates an existing dashboard in the metastore with the new changes
        from a new title.

        """
        colors = color_generator()
        t = TitleRefactored(unrefined_superset_title)
        desc_id = t.get_descriptive_id()
        n_tags = t.get_formatted_tags()
        f_title = t.get_formatted_title()
        n_superset_title = t.reformat()

        tags = []
        for tag in n_tags:
            tag_exists = Tag.query.filter_by(title=tag).first()
            if tag_exists:
                tags.append(tag_exists)
            else:
                new_tag = TagResourceManager.create_intern_resource(
                    title=tag,
                    color=random.choice(colors)
                )
                tags.append(new_tag)

        dash = self.update_intern_resource(
            pk=intern_id,
            title=f_title,
            tags=tags,
            descriptive_id=desc_id,
            last_saved_by=last_saved_by
        )
        self.update_superset_resource(
            pk=dash.superset_id,
            title=n_superset_title
        )
