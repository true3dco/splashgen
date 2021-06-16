from os import path
from typing import Dict

from PIL import Image
from splashgen import Component, MetaTags

_ASSET_DIR = path.join(path.dirname(__file__), '../assets')


# TODO: Render favicons, touch icon, splash icons, etc.
# TODO: Support BG color?
class Template(Component):
    template = ""

    enable_splashgen_analytics: bool
    """Set this to false to disable analytics.

    We use analytics in order to better understand product usage, and *never*
    track any personally-identifiable information on users visiting your site.
    """

    def __init__(self, title: str = "Website", logo: str = None, meta: MetaTags = None, theme: str = "light") -> None:
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
        self.favicon_img = self.logo
        self.enable_splashgen_analytics = True

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

    def render(self) -> str:
        if not self.template:
            raise ValueError("A Jinja template path must must be supplied "
                             "to the template attribute.")
        logo_url = self.write_asset_to_build(self.logo)
        favicons = self._gen_favicons()
        return self.into_template(self.template, extras={
            "logo": logo_url,
            "favicons": favicons,
            **self.prep_extras(),
        })

    def prep_extras(self) -> Dict:
        """Override in subclasses to supply extra information to templates"""
        return {}
