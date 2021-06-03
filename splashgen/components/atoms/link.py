from typing import List
from splashgen.components import Component, Html


class Link(Component):
    def __init__(self, href: str, text: str = None, classlist: List[str] = None) -> None:
        super().__init__()
        self.href = href
        if self.text is None:
            self.text = self.href
        self.classlist = classlist or []

    def render(self) -> Component:
        return Html(f"""<a href="{self.href}" class="{' '.join(self.classlist)}">{self.text}</a>""")
