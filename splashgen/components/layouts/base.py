from typing import List
from splashgen.components import Component, Children, Html


class Layout(Component):
    def __init__(self, children: List[Component] = None) -> None:
        super().__init__()
        self.children = children or []

    def render(self) -> Component:
        # This should probably be overridden!
        return Html(f"""<div>{Children(self.children)}</div>""")
