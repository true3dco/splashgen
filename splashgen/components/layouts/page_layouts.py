from typing import List
from splashgen.core import Branding, DEFAULT_BRANDING
from splashgen.components import Component, Link, AppHeader
from .stack import StackLayout


class PageLayout(Component):
    def __init__(self, branding: Branding = None, children: List[Component] = None) -> None:
        super().__init__(children)
        self.branding = branding or DEFAULT_BRANDING


class NavContentLayout(Component):
    def __init__(self, links: List[Link] = None, actions: List[Component] = None, branding: Branding = None, children: List[Component] = None) -> None:
        super().__init__(branding, children)
        self.nav_links = links or []
        self.nav_actions = actions or []
        self.children = children or []

    def ui(self) -> Component:
        return StackLayout(direction="vertical", spacing=0, children=[
            AppHeader(logo=self.branding.logo,
                      name=self.branding.name,
                      links=self.nav_links,
                      actions=self.nav_actions),
            *self.children
        ])
