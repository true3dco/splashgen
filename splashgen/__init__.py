import pathlib
import shutil
from abc import ABC, abstractmethod
from dataclasses import dataclass
from os import path

from jinja2 import Environment, PackageLoader
from PIL import Image

jinja = Environment(loader=PackageLoader("splashgen"), autoescape=False)

_assigned_component = None

_ASSET_DIR = path.join(path.dirname(__file__), 'assets')


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
        uri = f"/{path.basename(dest)}"
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


class CTAButton(Component):
    def __init__(self, link: str, text: str) -> None:
        self.link = link
        self.text = text

    def render(self) -> str:
        return f'<a href="{self.link}" class="btn btn-primary btn-lg px-4">{self.text}</a>'


@dataclass
class MetaTags:
    title: str
    description: str
    image: str
    canonical_url: str


# TODO: Render favicons, touch icon, splash icons, etc.
# TODO: Support BG color?
class SplashSite(Component):
    meta: MetaTags
    headline: str
    subtext: str
    call_to_action: Component
    enable_splashgen_analytics: bool
    """Set this to false to disable analytics.

    We use analytics in order to better understand product usage, and *never*
    track any personally-identifiable information on users visiting your site.
    """

    def __init__(self, title: str = "Splash Site", logo: str = None, meta: MetaTags = None, theme: str = "light") -> str:
        super().__init__()
        self.title = title
        if not logo:
            logo = path.join(_ASSET_DIR, "logo-default.png")
        self.logo = logo
        self.meta = meta
        if theme not in ["light", "dark"]:
            raise ValueError(
                "Invalid theme option. Please specify 'light' or 'dark'")
        self.theme = theme
        self.headline = "Fill out your headline here by assigning to `headline`"
        self.subtext = "Fill out subtext by assigning to `subtext`"
        self.call_to_action = None
        self.favicon_img = self.logo
        self.enable_splashgen_analytics = True

    def render(self) -> str:
        logo_url = self.write_asset_to_build(self.logo)
        favicons = self._gen_favicons()
        return self.into_template("splash_site.html.jinja", extras={
            "logo": logo_url,
            "favicons": favicons
        })

    def _gen_favicons(self):
        favicons = []
        with Image.open(self.favicon_img) as img:
            for size in [16, 32, 64]:
                favicon_info = {
                    "rel": "icon",
                    "type": "image/png",
                    "size": f"{size}x{size}",
                    "filename": f"favicon-{size}x{size}.png"
                }
                resized = img.resize((size, size))
                resized.save(path.join(self.build_dir,
                             favicon_info["filename"]))
                favicons.append(favicon_info)
        return favicons


def launch(root: Component) -> None:
    global _assigned_component
    _assigned_component = root
