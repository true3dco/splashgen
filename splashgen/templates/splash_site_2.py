from typing import Dict
from splashgen.components import CTAButton, CTAButtonSecondary, Link
from .base import Template


class SplashSite2(Template):
    nav_bar_center_link: Link
    nav_bar_right_link: Link
    headline: str
    subtext: str
    primary_call_to_action: CTAButton
    secondary_call_to_action: CTAButtonSecondary
    hero_video: str

    template = "splash_site_2.html.jinja"

    def __init__(self, **kwargs) -> str:
        super().__init__(**kwargs)

        self.headline = "Fill out your headline here by assigning to `headline`"
        self.subtext = "Fill out subtext by assigning to `subtext`"
        self.call_to_action = None
        self.primary_call_to_action = None
        self.secondary_call_to_action = None
        self.hero_video = None
        self.nav_bar_center_link = None
        self.nav_bar_right_link = None

    def prep_extras(self) -> Dict:
        if self.hero_video:
            hero_video_url = self.write_asset_to_build(self.hero_video)
        else:
            hero_video_url = None
        return {
            "hero_video": hero_video_url,
        }
