from typing import NamedTuple, Literal


class Link(NamedTuple):
    href: str
    text: str


class SEO(NamedTuple):
    title: str
    description: str
    canonical_url: str
    site_image: str


class Branding(NamedTuple):
    name: str
    logo: str
    # TODO: Use Literal["light", "dark"] instead
    theme: str
