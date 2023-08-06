from dateutil import parser
import json
from urllib.parse import urljoin
from supextend.utils.superset import TitleRefactored
from supextend.config import Config


class DashboardClean(TitleRefactored):

    def __init__(self, dash_superset_res):
        try:
            _created_by = f"{dash_superset_res['created_by']['first_name']}" \
                          f" {dash_superset_res['created_by']['last_name']}"
        except TypeError:
            _created_by = Config.superset_username
        self.created_by = _created_by
        self.owners = dash_superset_res['owners']
        self.last_modified_on = parser\
            .parse(dash_superset_res['changed_on_utc'])
        self.last_saved_by = dash_superset_res['changed_by_name']
        self.status = dash_superset_res['status']
        self.url_superset = urljoin(Config.superset_base_url,
                                    dash_superset_res['url'])
        self.pk = dash_superset_res['id']
        self.extra = json.dumps(dash_superset_res, indent=4)
        super().__init__(title=dash_superset_res['dashboard_title'])

    def get_owners(self):
        return [(owner['first_name'],
                 owner['last_name']) for owner in self.owners]


def dash_process_form(form):
    title = form['title']
    descriptive_id = form['descriptive_id'][:3]
    str_tags = list(filter(None, form.getlist('tags')))
    tags = str_tags[0].split(',') if str_tags else ''
    return f"#{descriptive_id} {tags} {title}"
