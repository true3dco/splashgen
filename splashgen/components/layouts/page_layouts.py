from typing import List
from splashgen.app_config import Branding, DEFAULT_BRANDING, Link
from splashgen.generators import Component


class NavContentLayout(Component):
    def __init__(self, links: List[Link] = None, actions: List[Component] = None, children: List[Component] = None) -> None:
        super().__init__()
        self.links = links or []
        self.actions = actions or []
        self.children = children or []


class CenteredHeroLayout(Component):
    def __init__(self, children: List[Component]) -> None:
        super().__init__()
        self.children = children or []
