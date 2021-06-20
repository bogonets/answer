# -*- coding: utf-8 -*-

from typing import List
from aiohttp import web
from recc.core.context import Context
from aiohttp.web_request import Request
from aiohttp.web_routedef import AbstractRouteDef
from recc.log.logging import recc_http_logger as logger
from recc.http.v1.common import (
    PATH_PREFIX_EXTRA_AIRJOY,
    no_name,
    at_session,
    response_ok,
    response_ok_without_detail,
    k_project,
)
import datetime
import random

path_get_manage_data_metric = "/project/{proj}/manage/metric"
path_get_manage_data_non_metric = "/project/{proj}/manage/non-metric"

path_post_manage_data_metric = "/project/{proj}/manage/metric/edit"
path_post_manage_data_non_metric = "/project/{proj}/manage/non-metric/edit"
path_post_manage_device_signal = "/project/{proj}/manage/signal"

path_post_manage_edit = "/project/{proj}/manage/edit"

path_get_agency_list = "/project/{proj}/agency"
path_get_graph_term = "/project/{proj}/graph/term"
path_get_graph_live = "/project/{proj}/graph/live/agency/{agency}"

path_get_project_ids = "/project/{proj}/ids"
path_get_project_members = "/project/{proj}/members"
path_add_project_member = "/project/{proj}/member/add"
path_edit_project_member_auth = "/project/{proj}/member/auth/edit"
path_delete_project_member = "/project/{proj}/member/delete"


class MetricData:
    def __init__(self, x: str, y: float):
        self.x = x
        self.y = y

    def to_json(self):
        return {"x": self.x, "y": self.y}


class GraphData:
    def __init__(self, label: str, data: float):
        self.label = label
        self.data = data

    def to_json(self):
        return {"label": self.label, "data": self.data}


class AirjoyV1:
    """
    API version 1.0 - Extra - AirJoy Router class.
    """

    def __init__(self, context: Context):
        self._context = context
        self._app = web.Application()
        self._app.add_routes(self._get_routers())

    def _get_routers(self) -> List[AbstractRouteDef]:
        # fmt: off
        return [
            web.get("/test", self.on_airjoy_test),
            web.get(path_get_manage_data_non_metric,
                    self.on_get_manage_non_metric_data),
            web.get(path_get_manage_data_metric,
                    self.on_get_manage_metric_data),
            web.post(path_post_manage_data_non_metric,
                     self.on_post_manage_non_metric_data),
            web.post(path_post_manage_data_metric,
                     self.on_post_manage_metric_data),
            web.get(path_get_agency_list,
                    self.on_get_agency_list),
            web.post(path_get_graph_term,
                     self.on_get_graph_term),
            web.get(path_get_graph_live,
                    self.on_get_graph_live),
            web.post(path_post_manage_device_signal,
                     self.on_post_manage_device_signal),
            web.post(path_post_manage_edit,
                     self.on_post_manage_edit),
            web.get(path_get_project_ids,
                    self.on_get_project_ids),
            web.get(path_get_project_members,
                    self.on_get_project_members),
            web.post(path_add_project_member,
                     self.on_add_project_member),
            web.post(path_edit_project_member_auth,
                     self.on_edit_project_member_auth),
            web.post(path_delete_project_member,
                     self.on_delete_project_member)
        ]
        # fmt: on

    @property
    def app(self) -> web.Application:
        return self._app

    def add_parent_app(self, parent_app: web.Application) -> None:
        assert self._app is not None
        assert parent_app is not None
        parent_app.add_subapp(PATH_PREFIX_EXTRA_AIRJOY, self._app)

    async def on_airjoy_test(self, request: Request):
        session = request[at_session]
        username = session.audience
        logger.info(f"on_airjoy_test(session={username})")
        # json: dict = await request.json()
        assert self
        return response_ok(no_name)

    async def on_get_manage_non_metric_data(self, request: Request):
        name = "get-non-metric-data"
        session = request[at_session]
        username = session.audience
        projname = request.match_info[k_project]
        logger.info(
            f"on_get_airjoy_manage_non_metric_data(session={username},"
            f"project={projname})"
        )

        result = [
            {
                "serial": "serial1",
                "wifi": "wifi1",
                "agency": "agency1",
                "install_date": "date1",
                "install_location": "location1",
                "as": "as1",
                "firmware_version": "v1",
                "kiosk": "kiosk1",
                "install_type": "type1",
                "filter_life": "life1",
            },
            {
                "serial": "abcd",
                "wifi": "wifi1",
                "agency": "abcd",
                "install_date": "date1",
                "install_location": "location1",
                "as": "as1",
                "firmware_version": "v1",
                "kiosk": "kiosk1",
                "install_type": "type1",
                "filter_life": "life1",
            },
        ]
        assert self
        return response_ok_without_detail(name, result)

    async def on_get_manage_metric_data(self, request: Request):
        name = "get-metric-data"
        session = request[at_session]
        username = session.audience
        projname = request.match_info[k_project]
        logger.info(
            f"on_get_airjoy_manage_non_metric_data(session={username},"
            f"project={projname})"
        )

        result = [
            {
                "serial": "serial1",
                "on_off": True,
                "sleep": False,
                "wind_control": 1,
                "auto": True,
                "temperature": 20,
                "moisture": 50,
                "pm10": 10,
                "pm25": 20,
                "co2": 0.5,
                "voc": "voc1",
                "etc": "etc1",
            },
            {
                "serial": "abcd",
                "on_off": True,
                "sleep": False,
                "wind_control": 1,
                "auto": True,
                "temperature": 20,
                "moisture": 50,
                "pm10": 10,
                "pm25": 20,
                "co2": 0.5,
                "voc": "voc1",
                "etc": "etc1",
            },
        ]
        assert self
        return response_ok_without_detail(name, result)

    async def on_post_manage_non_metric_data(self, request: Request):
        name = "post-non-metric-data"
        session = request[at_session]
        username = session.audience
        projname = request.match_info[k_project]

        json = await request.json()

        logger.info(
            f"on_post_airjoy_manage_non_metric_data(session={username},"
            f"project={projname})"
        )
        logger.info(f"request={json}")

        # result 를 나중에 수정 된 이후의 select 데이터로 변경..?

        assert self
        return response_ok_without_detail(name)

    async def on_post_manage_metric_data(self, request: Request):
        name = "post-metric-data"
        session = request[at_session]
        username = session.audience
        projname = request.match_info[k_project]

        # result : update target.
        #   serial : ""
        #   key : value
        json = await request.json()

        logger.info(
            f"on_post_airjoy_manage_non_metric_data(session={username},"
            f"project={projname})"
        )
        logger.info(f"request={json}")

        assert self
        return response_ok_without_detail(name)

    async def on_get_agency_list(self, request: Request):
        name = "get-agency-list"
        session = request[at_session]
        username = session.audience
        projname = request.match_info[k_project]
        logger.info(f"on_get_agency_list(session={username}," f"project={projname})")

        result = [
            {"id": 1, "name": "agency1"},
            {"id": 2, "name": "agency2"},
            {"id": 3, "name": "agency3"},
        ]
        assert self
        return response_ok_without_detail(name, result)

    async def on_get_graph_term(self, request: Request):
        name = "get-graph-term"
        session = request[at_session]
        username = session.audience
        projname = request.match_info[k_project]

        # request parsing
        json = await request.json()

        logger.info(f"on_get_graph_term(session={username}," f"project={projname})")
        logger.info(f"request={json}")

        result = self.test_term_data()

        assert self
        return response_ok_without_detail(name, result)

    async def on_get_graph_live(self, request: Request):
        name = "get-graph-live"
        session = request[at_session]
        username = session.audience
        projname = request.match_info[k_project]
        agency = request.match_info["agency"]

        logger.info(
            f"on_get_graph_live(session={username}, project={projname}, agency={agency}"
        )

        assert self
        return response_ok_without_detail(name, self.live_data())

    async def on_post_manage_device_signal(self, request: Request):
        name = "post-device-signal"
        session = request[at_session]
        username = session.audience
        projname = request.match_info[k_project]

        # request parsing
        json = await request.json()

        logger.info(
            f"on_post_manage_device_signal(session={username}," f"project={projname})"
        )
        logger.info(f"request={json}")

        assert self
        return response_ok_without_detail(name)

    async def on_post_manage_edit(self, request: Request):
        name = "post-manage-edit"
        session = request[at_session]
        username = session.audience
        projname = request.match_info[k_project]

        # request parsing
        json = await request.json()

        logger.info(f"on_post_manage_edit(session={username}," f"project={projname})")
        logger.info(f"request={json}")

        assert self
        return response_ok_without_detail(name)

    async def on_get_project_ids(self, request: Request):
        name = "get_project_ids"
        # session = request[at_session]
        # username = session.audience
        projname = request.match_info[k_project]

        assert self
        return response_ok_without_detail(name, self.get_project_ids(projname))

    def get_project_ids(self, project):
        # project 에 없는 ids
        ids = [
            "wooruang",
            "zer0",
            "yoonsu",
        ]
        assert self
        return ids

    async def on_get_project_members(self, request: Request):
        name = "get_project_members"
        # session = request[at_session]
        # username = session.audience
        projname = request.match_info[k_project]

        assert self
        return response_ok_without_detail(name, self.get_project_members(projname))

    def get_project_members(self, project):
        # project 에 있는 members
        members = [
            {
                "id": "sunhongyi",
                "auth": {
                    "en": "administrator",
                    "ko": "관리자",
                },
            },
            {
                "id": "sunhongyi2",
                "auth": {
                    "en": "operator",
                    "ko": "부관리자",
                },
            },
            {
                "id": "sunhongyi3",
                "auth": {
                    "en": "guest",
                    "ko": "게스트",
                },
            },
        ]
        assert self
        return members

    async def on_add_project_member(self, request: Request):
        name = "add_project_member"
        # session = request[at_session]
        # username = session.audience
        # projname = request.match_info[k_project]

        # json = await request.json()

        # add member...

        assert self
        return response_ok_without_detail(name)

    # path_edit_project_member_auth = "/project/{proj}/member/auth/edit"
    async def on_edit_project_member_auth(self, request: Request):
        name = "edit_project_member_auth"
        # session = request[at_session]
        # username = session.audience
        # projname = request.match_info[k_project]

        # json = await request.json()

        # edit member auth...

        assert self
        return response_ok_without_detail(name)

    # path_delete_project_member = "/project/{proj}/member/delete"
    async def on_delete_project_member(self, request: Request):
        name = "delete_project_member"
        # session = request[at_session]
        # username = session.audience
        # projname = request.match_info[k_project]

        # json = await request.json()

        # delete member in project...

        assert self
        return response_ok_without_detail(name)

    def obj_dict(self, obj):
        assert self
        return obj.__dict__

    def live_data(self):
        label = self.get_now_seconds()
        temp_data = GraphData(label="온도", data=[])
        moi_data = GraphData(label="습도", data=[])
        pm10_data = GraphData(label="PM10", data=[])
        pm25_data = GraphData(label="PM2.5", data=[])
        co2_data = GraphData(label="CO2", data=[])
        voc_data = GraphData(label="VOC", data=[])

        temp_data.data.append(self.get_random_float())
        moi_data.data.append(self.get_random_float())
        pm10_data.data.append(self.get_random_float())
        pm25_data.data.append(self.get_random_float())
        co2_data.data.append(self.get_random_float())
        voc_data.data.append(self.get_random_float())

        dataset = []
        dataset.append(temp_data.to_json())
        dataset.append(moi_data.to_json())
        dataset.append(pm10_data.to_json())
        dataset.append(pm25_data.to_json())
        dataset.append(co2_data.to_json())
        dataset.append(voc_data.to_json())

        live_data = {"label": label, "datasets": dataset}

        assert self
        return live_data

    def test_term_data(self):
        labels = self.get_random_dates()
        temp_data = GraphData(label="온도", data=[])
        moi_data = GraphData(label="습도", data=[])
        pm10_data = GraphData(label="PM10", data=[])
        pm25_data = GraphData(label="PM2.5", data=[])
        co2_data = GraphData(label="CO2", data=[])
        voc_data = GraphData(label="VOC", data=[])

        for i in range(10):
            temp_data.data.append(self.get_random_float())
            moi_data.data.append(self.get_random_float())
            pm10_data.data.append(self.get_random_float())
            co2_data.data.append(self.get_random_float())
            pm25_data.data.append(self.get_random_float())
            voc_data.data.append(self.get_random_float())

        dataset = []
        dataset.append(temp_data.to_json())
        dataset.append(moi_data.to_json())
        dataset.append(pm10_data.to_json())
        dataset.append(pm25_data.to_json())
        dataset.append(co2_data.to_json())
        dataset.append(voc_data.to_json())

        term_data = {"labels": labels, "datasets": dataset}

        return term_data

    def get_random_dates(self):
        dates = []
        # start = datetime.datetime(2020, 3, 1, 00, 00, 00)
        # end = datetime.datetime(2020, 3, 30, 00, 00, 00)

        start = datetime.datetime.now()

        for i in range(10):
            temp_date = start + datetime.timedelta(days=i)
            dates.append(temp_date.strftime("%Y/%m/%d"))

        assert self
        return dates

    def get_now_seconds(self):
        assert self
        return datetime.datetime.now().strftime("%H:%M:%S")
        # return datetime.datetime.now().isoformat(" ", "seconds")

    def get_random_float(self):
        assert self
        return round(random.random(), 2)

    def get_random_metric(self, x: str):
        data = []
        for i in range(10):
            data.append(MetricData(x=x, y=round(random.random(), 2)))
        assert self
        return data

    def random_date(self, start, end):
        """Generate a random datetime between `start` and `end`"""
        assert self
        random_date = start + datetime.timedelta(
            # Get a random amount of seconds between `start` and `end`
            seconds=random.randint(0, int((end - start).total_seconds())),
        )
        result = random_date.strftime("%c")
        return result
