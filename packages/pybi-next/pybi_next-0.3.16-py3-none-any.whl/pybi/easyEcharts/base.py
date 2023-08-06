from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Tuple, List, Sequence, Union

from pybi.core.components.reactiveComponent.echarts import EChartUpdateInfo
from pybi.core.dataSource import DataSourceTable

if TYPE_CHECKING:
    from pybi.core.components.reactiveComponent import EChartDatasetInfo

m_merge_keys = set(["legend", "title", "grid", "series"])


class BaseChart:
    def __init__(self) -> None:
        self.__base_opt = {
            "tooltip": {},
            "legend": {},
            "series": [],
            "title": {},
            "grid": {"containLabel": True},
        }
        self.__merge_opt = {}
        self._updateInfos: List[EChartUpdateInfo] = []

    def __add__(self, other: BaseChart):
        return ChartCollector().append(self).append(other)

    def merge(self, options: Dict):
        self.__merge_opt = options
        return self

    def get_options(self):
        return {
            **self.__base_opt,
            **{k: v for k, v in self.__merge_opt.items() if k in m_merge_keys},
        }

    def set_title(self, text: str):
        opt_title: Dict = self.__base_opt["title"]
        opt_title["text"] = text

        return self

    def hover_filter(
        self, value_type: str, table: Union[str, DataSourceTable], field: str
    ):
        """
        value_type: Literal["x", "y", "value","color","name"]
        """
        if isinstance(table, DataSourceTable):
            table = table.source_name

        self._updateInfos.append(EChartUpdateInfo("hover", value_type, table, field))

        return self

    def click_filter(
        self, value_type: str, table: Union[str, DataSourceTable], field: str
    ):
        """
        value_type: Literal["x", "y", "value","color","name"]
        """
        if isinstance(table, DataSourceTable):
            table = table.source_name

        self._updateInfos.append(EChartUpdateInfo("click", value_type, table, field))

        return self

    def _remove_filters(self, actionType: str):
        """
        actionType : 'click' | 'hover'
        """
        self._updateInfos = [
            info for info in self._updateInfos if info.actionType != actionType
        ]
        return self

    def remove_all_click_filter(self):
        return self._remove_filters("click")

    def _create_default_click_filter(self):
        pass

    def get_options_infos(
        self,
    ) -> Tuple[Dict, List[EChartUpdateInfo]]:
        raise NotImplementedError


class ChartCollector:
    def __init__(self) -> None:
        self._collector: List[BaseChart] = []

    def append(self, other: BaseChart):
        self._collector.append(other)
        return self

    def __add__(self, other: Union[ChartCollector, BaseChart]):
        if isinstance(other, BaseChart):
            other = ChartCollector().append(other)

        self._collector.extend(other._collector)
        return self
