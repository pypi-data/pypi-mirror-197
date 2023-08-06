from urllib.parse import urljoin
import random

from supextend.resources\
    .internal.superset_batch_cleaner.chart import ChartIntern
from supextend.resources\
    .external.superset.chart import ChartExtern
from supextend.resources\
    .common.superset_batch_cleaner.tag import TagResourceManager
from supextend.utils.superset import TitleRefactored
from supextend.models.tags import Tag
from supextend.utils.superset import color_generator
from supextend.config import Config


class ChartResourceManager(ChartIntern, ChartExtern):
    """A class to represent resource management for
    both Internal and External(Superset) charts.

    Methods:
    --------
    list_all()
        Combines results from both the
        superset api call and the metastore call.
        This is done for the convenience in data presentation.
    """

    def list_all(self):
        """
        Combines results from both the
        superset api call and the metastore call.
        returns a dict of the combined data.
        """

        ch_intern = self.list_intern_resource()
        ch_superset = self.list_superset_resource()
        ch_intern_ref = [{
            'title': ch.title,
            'created_by': ch.created_by,
            'owners': ch.owners,
            'last_modified_on': ch.last_modified_on,
            'last_saved_by': ch.last_saved_by,
            'tags': ch.tags,
            'descriptive_id': ch.descriptive_id,
            'type': ch.type,
            'status': ch.status,
            'url_superset': None,
            'superset_pk': None,
            'id': f"{count}-{ch.title}".replace(' ', ''),
            'kind': 'internal',
            'airflow_url': urljoin(
                    Config.airflow_base_url,
                    f"/taskinstance/list/?flt1_dag_id_equals="
                    f"{ch.task.dag_name}&_flt_3_task_id={ch.task.task_name}"),
            'airflow_run_id': ch.task.run_id
        } for count, ch in enumerate(ch_intern)]

        ch_superset_ref = [{
            'title': ch.get_title(),
            'created_by': ch.created_by,
            'owners': ch.get_owners(),
            'last_modified_on': ch.last_modified_on,
            'last_saved_by': ch.last_saved_by,
            'tags': ch.get_tags(),
            'descriptive_id': ch.get_descriptive_id(),
            'type': ch.type,
            'status': None,
            'url_superset': ch.url_superset,
            'superset_pk': ch.pk,
            'id': f"{count}-{ch.get_title()}".replace(' ', ''),
            'airflow_url': None,
            'airflow_run_id': None,
            'kind': 'external'
        } for count, ch in enumerate(ch_superset)]

        return ch_intern_ref + ch_superset_ref

    def update_resource(self,
                        intern_id,
                        unrefined_superset_title,
                        last_saved_by):
        """
        Updates an existing chart in the metastore with the new changes
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

        chart = self.update_intern_resource(
            pk=intern_id,
            title=f_title,
            tags=tags,
            descriptive_id=desc_id,
            last_saved_by=last_saved_by
        )
        self.update_superset_resource(
            pk=chart.superset_id,
            title=n_superset_title
        )
