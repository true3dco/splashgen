import pathlib
import shutil
from abc import ABC, abstractmethod
from dataclasses import dataclass
from os import path

from jinja2 import Environment, FileSystemLoader


_assigned_component = None


class Component(ABC):
    jinja = None
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

    def into_template(self, template_file: str, extras: dict = None):
        jinja = Environment(loader=FileSystemLoader(searchpath=path.dirname(template_file)), autoescape=False)
        tmpl = jinja.get_template(path.basename(template_file))
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
