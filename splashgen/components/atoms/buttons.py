from typing import List
from splashgen.components import Component
from . import Link


class PrimaryButton(Component):
    def __init__(self, link: Link = None, text: str = "") -> None:
        super().__init__()
        self.link = link
        self.text = text


class SecondaryButton(Component):
    def __init__(self, link: Link = None, text: str = "") -> None:
        super().__init__()
        self.link = link
        self.text = text
