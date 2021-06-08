from typing import List
from splashgen.generators import Component


class StackLayout(Component):
    def __init__(self, direction: str = "horizontal", spacing: int = 8, alignx: str = "center", aligny: str = "center", children: List[Component] = None) -> None:
        super().__init__()
        self.direction = direction
        self.spacing = spacing
        self.alignx = alignx
        self.aligny = aligny
        self.children = children or []
