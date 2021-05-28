from typing import Dict
from splashgen import Component
from .base import Template


class SplashSite(Template):
    headline: str
    subtext: str
    call_to_action: Component
    hero_image: str

    template = "splash_site.html.jinja"

    def __init__(self, **kwargs) -> str:
        super().__init__(**kwargs)

        self.headline = "Fill out your headline here by assigning to `headline`"
        self.subtext = "Fill out subtext by assigning to `subtext`"
        self.call_to_action = None
        self.hero_image = None

    def prep_extras(self) -> Dict:
        if self.hero_image:
            hero_img_url = self.write_asset_to_build(self.hero_image)
        else:
            hero_img_url = None
        return {
            "hero_image": hero_img_url,
        }
