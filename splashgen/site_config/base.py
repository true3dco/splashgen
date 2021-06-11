from typing import NamedTuple, Optional
from os import path


class Link(NamedTuple):
    href: str
    text: str


class SEO(NamedTuple):
    title: str
    description: Optional[str] = None
    canonical_url: Optional[str] = None
    site_image: Optional[str] = None


class Branding(NamedTuple):
    name: str
    logo: Optional[str] = None
    # TODO: Use Literal["light", "dark"] instead
    theme: str = "light"


_ASSET_DIR = path.join(path.dirname(__file__), "..", "assets")
DEFAULT_BRANDING = Branding(
    name="Web App", logo=path.join(_ASSET_DIR, "logo-default.png"))
