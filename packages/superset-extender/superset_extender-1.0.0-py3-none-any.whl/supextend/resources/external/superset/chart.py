from urllib.parse import urljoin
import json

from supextend.core import SupersetConnManager
from supextend.utils.superset import ChartFilter
from supextend.config import Config
from supextend.resources.external.superset import ChartSuperset
from supextend.views.charts.utils import ChartClean
from supextend.loggers.config import LoggingConfig


class ChartExtern(ChartSuperset):
    """A class to represent a chart item on
    superset that is accessed through the RESTApi.

    Methods:
    --------
    update_superset_resource(pk, title)
        Updates the `slice_name` of a chart with id=pk
        with the new slice_name: `title`
    list_superset_resource(
        page=0,
        page_size=1000,
        filter_value=0,
        column='slice_name',
        opr='chart_all_text')
        Filters charts on superset and retrieves a response of size `page_size`.
        `filter_value` is 0 with no condition but can be: eg. `Obsolete`.
        (default page=0, default page_size=1000, default filter_value=0,
        default column='slice_name')
        (default opr='chart_all_text')
    get_superset_resource(pk)
        Retrieves one chart from the superset api based on the id=pk
    delete_superset_resource(pk)
        Deletes one chart from the superset api based on the id=pk
    create_superset_resource(**kwargs)
        It is not advised to implement this method as the main
        purpose is not to provide escalating rights.
    """

    @staticmethod
    def update_superset_resource(pk, title):
        """
        Updates the `slice_name` of a chart with id=pk.

        Parameters:
        -----------
        pk: int
            The chart identification number on superset.
        title: str
            The new chart's `slice_name`.
        """

        url = urljoin(Config.superset_base_url, f"/api/v1/chart/{str(pk)}")
        body = {
            "chart_title": title
        }
        with SupersetConnManager(
                base_url=Config.superset_base_url,
                username=Config.superset_username,
                password=Config.superset_password) as s:
            auth_headers, session = s
            response = session.put(
                    str(url),
                    headers=auth_headers,
                    data=json.dumps(body))
            if response.status_code == 200:
                LoggingConfig.logger.success(f"Updated the chart"
                                             f" ID:{pk} to "
                                             f"{body['chart_title']}")
            elif response.status_code == 404:
                LoggingConfig.logger.error(f"Missing: the chart "
                                           f"with ID: {pk} is not found.")
            else:
                LoggingConfig.logger.warning(f"{response.status_code} "
                                             f"- Something went wrong")
            return response.json()

    @staticmethod
    def list_superset_resource(page: int = 0,
                               page_size: int = 1000,
                               filter_value: str = 0,
                               column: str = 'slice_name',
                               opr: str = 'chart_all_text',
                               ):
        """
        Filters charts on superset and retrieves a response of size `page_size`.

        Parameters:
        -----------
        page: int
            The corresponding page in the UI to list resources.
        page_size: int
            The size(number) of charts to collect.
        filter_value: str
            The term used to filter by.
        column: str
            The column type (default: slice_name).
        opr: str
            (default: chart_all_text).
        """

        chart_filter = ChartFilter(
            page, page_size,
            filter_value, column, opr
        )
        url = urljoin(Config.superset_base_url, '/api/v1/chart')
        get_params = chart_filter.get_params
        with SupersetConnManager(
                base_url=Config.superset_base_url,
                username=Config.superset_username,
                password=Config.superset_password) as s:
            auth_headers, session = s
            response = session.get(
                    str(url),
                    params=get_params,
                    headers=auth_headers)
            if response.status_code == 200:
                LoggingConfig.logger.success(f"Retrieved the chart"
                                             f" list: Total "
                                             f"{len(response.json()['result'])}"
                                             f" Charts")
            elif response.status_code == 404:
                LoggingConfig.logger.error("Missing: "
                                           "the charts were not found.")
            else:
                LoggingConfig.logger.warning(f"{response.status_code}"
                                             f" - Something went wrong")
            cleaned_response = \
                [ChartClean(ch) for ch in response.json()['result']]

            return cleaned_response

    @staticmethod
    def get_superset_resource(pk):
        """
        Retrieves one chart from the superset api based on the id=pk.

        Parameters:
        -----------
        pk: int
            The chart identification number on superset.
        """

        url = urljoin(Config.superset_base_url, f"/api/v1/chart/{str(pk)}")
        with SupersetConnManager(
                base_url=Config.superset_base_url,
                username=Config.superset_username,
                password=Config.superset_password) as s:
            auth_headers, session = s
        response = session.get(str(url), headers=auth_headers)
        if response.status_code == 200:
            LoggingConfig.logger.success(f"Retrieved the chart"
                                         f" with ID: {pk} from superset.")
        elif response.status_code == 404:
            LoggingConfig.logger.error(f"Missing: the chart"
                                       f" with ID: {pk} is not found.")
        else:
            LoggingConfig.logger.warning(f"{response.status_code}"
                                         f" - Something went wrong "
                                         f"with the chart, ID: {pk}.")
        return response.json()

    @staticmethod
    def delete_superset_resource(pk):
        """
        Deletes one chart from the superset api based on the id=pk.

        Parameters:
        -----------
        pk: int
            The chart identification number on superset.
        """

        url = urljoin(Config.superset_base_url, f"/api/v1/chart/{str(pk)}")
        with SupersetConnManager(
                base_url=Config.superset_base_url,
                username=Config.superset_username,
                password=Config.superset_password) as s:
            auth_headers, session = s
            response = session.delete(url, headers=auth_headers)
            if response.status_code == 200:
                LoggingConfig.logger.warning(f"Deleted the chart"
                                             f" with ID: {pk} from superset.")
            elif response.status_code == 404:
                LoggingConfig.logger.error(f"Missing: the chart"
                                           f" with ID: {pk} is not found.")
            else:
                LoggingConfig.logger.error(f"{response.status_code}"
                                           f" - Something went wrong"
                                           f" with the chart, ID: {pk}.")
            return response.json()

    def create_superset_resource(self, **kwargs):
        """It is not advised to implement this method
         as the main purpose is not to provide escalating rights."""
        pass
