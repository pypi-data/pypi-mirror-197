from pybi.core.components.component import Component
from .componentTag import ComponentTag
from bs4 import BeautifulSoup


class TextComponent(Component):
    def __init__(self, content: str) -> None:
        super().__init__(ComponentTag.Text)
        self.content = content


class UploadComponent(Component):
    def __init__(self) -> None:
        super().__init__(ComponentTag.Upload)


class IconComponent(Component):
    def __init__(self, svg: str, size: str, color: str) -> None:
        super().__init__(ComponentTag.Icon)

        s = BeautifulSoup(svg, "html.parser")

        del s.find("svg")["width"]
        del s.find("svg")["height"]
        self.svg = str(s)
        self.size = size
        self.color = color
