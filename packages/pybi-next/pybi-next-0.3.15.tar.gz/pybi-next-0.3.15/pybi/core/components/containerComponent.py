from __future__ import annotations
from typing import TYPE_CHECKING, Union, List, Optional

from .componentTag import ComponentTag
from .component import Component

if TYPE_CHECKING:
    from pybi.app import App


class ContainerComponent(Component):
    def __init__(self, tag: ComponentTag, appHost: Optional[App] = None) -> None:
        super().__init__(tag)

        # TODO: maybe use weak ref?
        self._appHost = appHost

        self.children: List[Component] = []

    def _add_children(self, stat: Component):
        self.children.append(stat)
        return self

    def __enter__(self):
        if self._appHost:
            self._appHost._with_temp_host_stack.append(self)
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self._appHost:
            self._appHost._with_temp_host_stack.pop()


class BoxComponent(ContainerComponent):
    def __init__(self, appHost: Optional[App] = None) -> None:
        super().__init__(ComponentTag.Box, appHost)


class FlowBoxComponent(ContainerComponent):
    def __init__(self, appHost: Optional[App] = None) -> None:
        super().__init__(ComponentTag.FlowBox, appHost)

    def __get_item__(self, idx: int):
        return self.children[idx]


class GridBoxComponent(ContainerComponent):
    def __init__(self, areas: List[List[str]], appHost: Optional[App] = None) -> None:
        super().__init__(ComponentTag.GridBox, appHost)
        self.__areas = areas
        self.__columns_sizes: List[str] = []
        self.__rows_sizes: List[str] = []

    def set_columns_sizes(self, sizes: List[Union[str, int]]):
        """
        >>> set_columns_sizes([1,2,2])
        >>> set_columns_sizes(['150px','1fr','2fr'])
        >>> set_columns_sizes(['150px','1fr','minmax(100px, 1fr)'])
        """
        self.__columns_sizes = [f"{s}fr" if isinstance(s, int) else s for s in sizes]
        return self

    def set_rows_sizes(self, sizes: List[Union[str, int]]):
        """
        >>> set_rows_sizes([1,2,2])
        >>> set_rows_sizes(['150px','1fr','2fr'])
        >>> set_rows_sizes(['150px','1fr','minmax(100px, 1fr)'])
        """
        self.__rows_sizes = [f"{s}fr" if isinstance(s, int) else s for s in sizes]
        return self

    def __get_item__(self, idx: int):
        return self.children[idx]

    def _to_json_dict(self):
        data = super()._to_json_dict()
        data["areas"] = GridBoxComponent.areas_array2str(self.__areas)

        areas_cols_len = max(map(len, self.__areas))
        cols_size = GridBoxComponent.padded_grid_template(
            self.__columns_sizes, areas_cols_len
        )

        areas_rows_len = len(self.__areas)
        rows_size = GridBoxComponent.padded_grid_template(
            self.__rows_sizes, areas_rows_len
        )

        data["gridTemplateColumns"] = " ".join(cols_size)
        data["gridTemplateRows"] = " ".join(rows_size)

        return data

    @staticmethod
    def padded_grid_template(sizes: List[str], real_size: int):
        """
        >>> sizes = ['1rf']
        >>> real_size = 3
        >>> padded_grid_template(sizes,real_size)
        >>> ['1rf','auto','auto']
        """
        diff_len = real_size - len(sizes)
        sizes = sizes.copy()

        if diff_len > 0:
            sizes.extend(["auto"] * diff_len)
        return sizes

    @staticmethod
    def areas_array2str(areas_array: List[List[str]]):
        """
        >>> input = [
            ["sc1", "sc2"],
            ["sc3"],
            ["table"] * 4
        ]
        >>> areas_array2str(input)
        >>> '"sc1 sc2 . ." "sc3 . . ." "table table table table"'
        """
        max_len = max(map(len, areas_array))

        fix_empty = (
            [*line, *(["."] * (max_len - len(line)))] if len(line) < max_len else line
            for line in areas_array
        )

        line2str = (f'"{" ".join(line)}"' for line in fix_empty)
        return " ".join(line2str)

    @staticmethod
    def areas_str2array(areas: str) -> List[List[str]]:
        """
        >>> input='''
            sc1 sc2
            sc3
            table table table table
        '''
        >>> areas_str2array(input)
        >>> [
            ["sc1", "sc2"],
            ["sc3"],
            ["table", "table", "table", "table"]
        ]
        """
        pass

        lines = (line.strip() for line in areas.splitlines())
        remove_empty_rows = (line for line in lines if len(line) > 0)
        splie_space = (line.split() for line in remove_empty_rows)
        return list(splie_space)


class ColBoxComponent(ContainerComponent):
    def __init__(
        self, spec: Optional[List[int]] = None, appHost: Optional[App] = None
    ) -> None:
        super().__init__(ComponentTag.ColBox, appHost)

        if spec is None:
            spec = [1, 1]

        self.spec = spec

        assert self._appHost is not None, "self._appHost must be app instance"

    def __getitem__(self, idx: int):
        return self.children[idx]


class TabsComponent(ContainerComponent):
    def __init__(
        self, names: List[str], mode="narrowing", appHost: Optional[App] = None
    ) -> None:
        """
        mode: 'fullWidth' | 'narrowing'
        """
        super().__init__(ComponentTag.Tabs, appHost)
        if len(names) > len(set(names)):
            raise Exception("names cannot be duplicated")
        self.names = names
        self.mode = mode

        self.__name2idx = {name: idx for idx, name in enumerate(self.names)}

        for _ in range(len(self.names)):
            self._add_children(BoxComponent(appHost))

    def __getitem__(self, idx: Union[int, str]):
        if isinstance(idx, str):
            if idx not in self.__name2idx:
                raise Exception(f"tab name[{idx}] not found")
            idx = self.__name2idx[idx]

        res = self.children[idx]
        assert isinstance(res, ContainerComponent)
        return res
