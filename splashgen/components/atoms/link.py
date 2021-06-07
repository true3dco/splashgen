from typing import List
from splashgen.components import Component


class Link(Component):
    def __init__(self, href: str, text: str = None, classlist: List[str] = None) -> None:
        super().__init__()
        self.href = href
        if text is None:
            self.text = self.href
        else:
            self.text = text
        self.classlist = classlist or []
