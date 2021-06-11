from typing import List
from splashgen.generators import Component
from splashgen.site_config import Link


class AppHeader(Component):
    def __init__(self, logo: str = "", name: str = "", links: List[Link] = None, actions: List[Component] = None) -> None:
        super().__init__()
        self.logo = logo
        self.name = name
        self.links = links or []
        self.actions = actions or []
