import pathlib
import shutil
from abc import ABC, abstractmethod
from dataclasses import dataclass
from os import path

from jinja2 import Environment, PackageLoader


jinja = Environment(loader=PackageLoader("splashgen"), autoescape=False)

_assigned_component = None


class Component(ABC):
    jinja = jinja
    build_dir = "build"

    @abstractmethod
    def render(self) -> str:
        pass

    def __str__(self) -> str:
        return self.render()

    def write_asset_to_build(self, src: str) -> str:
        self._mkbuild()
        dest = shutil.copy(src, path.join(self.build_dir, path.basename(src)))
        uri = f"{path.basename(dest)}"
        return uri

    def into_template(self, template: str, extras: dict = None):
        tmpl = self.jinja.get_template(template)
        data = self.__dict__
        if extras is None:
            extras = {}
        context = {**data, **extras}
        return tmpl.render(**context)

    def _mkbuild(self):
        pathlib.Path(self.build_dir).mkdir(parents=True, exist_ok=True)


@dataclass
class MetaTags:
    title: str
    description: str
    image: str
    canonical_url: str


def launch(root: Component) -> None:
    global _assigned_component
    _assigned_component = root
