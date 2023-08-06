from dateutil import parser
import json
from urllib.parse import urljoin
from supextend.utils.superset import TitleRefactored
from supextend.config import Config


class ChartClean(TitleRefactored):

    def __init__(self, ch_superset_res):
        try:
            _created_by = f"{ch_superset_res['created_by']['first_name']}" \
                          f" {ch_superset_res['created_by']['last_name']}"
        except TypeError:
            _created_by = Config.superset_username
        self.created_by = _created_by
        self.owners = ch_superset_res['owners']
        self.last_modified_on = parser.parse(ch_superset_res['changed_on_utc'])
        self.last_saved_by = ch_superset_res['changed_by_name']
        self.type = ch_superset_res['viz_type']
        self.url_superset = urljoin(Config.superset_base_url,
                                    ch_superset_res['url'])
        self.pk = ch_superset_res['id']
        self.status = 'unspecified'
        self.datasource = ch_superset_res['datasource_name_text']
        self.datasource_type = ch_superset_res['datasource_type']
        self.extra = json.dumps(ch_superset_res, indent=4)
        super().__init__(title=ch_superset_res['slice_name'])

    def get_owners(self):
        return [(owner['first_name'],
                 owner['last_name']) for owner in self.owners]


def ch_process_form(form):
    title = form['title']
    descriptive_id = form['descriptive_id'][:3]
    str_tags = list(filter(None, form.getlist('tags')))
    tags = str_tags[0].split(',') if str_tags else ''
    return f"#{descriptive_id} {tags} {title}"
