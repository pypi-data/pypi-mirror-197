from re import sub, split
import colorsys
from flask_wtf.csrf import CSRFProtect
from flask_login import current_user
from supextend.initialization import oidc
from dataclasses import dataclass, field
from supextend.config import Config


@dataclass
class GetFilter:
    page: int
    page_size: int
    filter_value: str
    column: str
    opr: str
    get_params: dict = field(init=False)

    def __post_init__(self):
        self.get_params = {
            "q": f"(filters:!((col:{self.column},"
                 f"opr:{self.opr},"
                 f"value:{self.filter_value})),"
                 f"order_column:changed_on_delta_humanized,"
                 f"order_direction:desc,"
                 f"page:{self.page},"
                 f"page_size:{self.page_size})" if self.filter_value
            else f"(order_column:changed_on_delta_humanized,"
                 f"order_direction:desc,"
                 f"page:{self.page},page_size:{self.page_size})"
        }


@dataclass
class ChartFilter(GetFilter):
    page: int = 0
    page_size: int = 1000
    filter_value: str = 0
    column: str = 'slice_name'
    opr: str = 'chart_all_text'


@dataclass
class DashboardFilter(GetFilter):
    page: int = 0
    page_size: int = 1000
    filter_value: str = 0
    column: str = 'dashboard_title'
    opr: str = 'title_or_slug'


class TitleRefactored:

    def __init__(self, title):
        self._title = title

    def get_title(self):
        return self.has_correct_title()[1]

    def get_formatted_title(self):
        return self.get_title().capitalize()

    def get_descriptive_id(self):
        return self.has_correct_id()[1]

    def get_formatted_desc_id(self):
        return self.get_descriptive_id().upper()

    def get_tags(self):
        return self.has_correct_tags()[1]

    def get_formatted_tags(self):
        return [self.make_camel_case(tag) for tag in self.get_tags()]

    def has_correct_id(self):
        is_correct = False
        desc_id = self._id()
        if desc_id.isupper() and desc_id[1:].isalpha():
            is_correct = True
        return is_correct, desc_id[1:]

    def has_correct_tags(self):
        is_correct = False
        sub_list = []
        str_tags = self._tags_str()
        if str_tags.startswith('[') and str_tags.endswith(']'):
            # str: "[A, B, C]" becomes list: ['A', 'B', 'C']
            sub_list = str_tags.strip('][').replace(" ", "").split(',')
            # Check CamelCase tags
            is_camel_case = all(self.is_camel_case(tag) for tag in sub_list)
            # Lookup duplicates and check for empty tags
            if len(sub_list) == len(set(sub_list)) and ''\
                    not in sub_list and is_camel_case:
                is_correct = True
        return is_correct, \
            [''.join(e for e in tag if e.isalnum()) for tag in sub_list]

    def _tags_str(self):
        start_tag_idx = self._title.find('[')
        end_tag_idx = self._title.find(']') + 1
        return self._title[start_tag_idx:end_tag_idx]

    def _id(self):
        return self._title[self._title.find('#'):self._title.find('#') + 4]

    def _title_str(self):
        title_without_id = self._title.replace(self._id(), "")
        return title_without_id.replace(str(self._tags_str()), "").strip()

    def has_correct_title(self):
        is_correct = False
        title = self._title_str()
        is_capitalized = title[0].isupper() if title else False
        if is_capitalized:
            is_correct = True
        return is_correct, title

    def reformat(self):
        formatted = ''
        tags_list = self.get_tags()
        title = self.get_title()
        desc_id = self.get_descriptive_id()

        if desc_id:
            formatted += f"#{desc_id} ".upper()
        if tags_list:
            f = ', '.join(self.make_camel_case(tag) for tag in tags_list)
            formatted += f"[{f}] ".replace("'", "")
        formatted += title.capitalize()
        return formatted

    @staticmethod
    def make_camel_case(word):
        if word:
            word = sub(r"(_|-)+", " ", word).title().replace(" ", "")
            return word.capitalize()

    @staticmethod
    def is_camel_case(word):
        return word != word.lower() and word != word.upper() and "_" not in word


def color_generator(size=Config.color_palette_size):
    hsv_tuples = [(x * 1.0 / size, 0.5, 0.5) for x in range(size)]
    colors = []
    for rgb in hsv_tuples:
        rgb = map(lambda x: int(x * 255), colorsys.hsv_to_rgb(*rgb))
        colors.append('#%02x%02x%02x' % tuple(rgb))
    return colors


def check_auth(
        flask_login_req_dec,
        oidc_login_req_dec,
        support_oidc=Config.oauth):
    def wrapper(func):
        if support_oidc:
            return oidc_login_req_dec(func)
        return flask_login_req_dec(func)

    return wrapper


def get_normalized_title(nonconforming_title):
    capt = nonconforming_title.capitalize()
    list_t = capt.split(' ')
    i = [w[0].upper() for w in list_t if w[0].isalpha()]
    idx = []
    full_t = ' '.join(["".join(split("[^a-zA-Z]*", w)) for w in list_t])
    if len(i) == 1:
        idx = list(i[0]) + ['X', 'X']
    elif len(i) == 2:
        idx = list(i[:2]) + ['X']
    elif len(i) > 2:
        idx = i

    return f"#{''.join(idx[:3])} [Internal] {full_t}"


def get_current_user_fullname():
    fullname = str()
    oidc_user = None
    if oidc.user_loggedin:
        oidc_user = oidc.user_getinfo(
            ['preferred_username', 'given_name', 'family_name'])
    if oidc_user:
        fullname = f"{oidc_user['given_name']} {oidc_user['family_name']}"
    elif current_user:
        fullname = f"{current_user.first_name} {current_user.last_name}"
    else:
        fullname = Config.superset_username
    return fullname


csrf = CSRFProtect()
