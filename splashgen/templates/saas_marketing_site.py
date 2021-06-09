from typing import Optional

from splashgen.components import *
from splashgen.components.layouts import (CenteredHeroLayout, NavContentLayout,
                                          StackLayout)
from splashgen.generators import Component, WebApp, WebPage
from splashgen.site_config.pricing import PricingStructure


# TODO: WebApp has nav_links + nav_actions + layout + SEO + Branding, etc.
class SaasMarketingSite(WebApp):
    sign_in_link: Optional[str]

    homepage_headline: str
    homepage_subtext: str
    homepage_demo_video_youtube_id: Optional[str]
    homepage_primary_call_to_action: PrimaryButton
    homepage_secondary_call_to_action: SecondaryButton

    pricing_page_headline: str
    pricing_page_subtext: str
    pricing_structure: Optional[PricingStructure]

    # This comes from WebApp
    layout = NavContentLayout()

    def __init__(self, **kwargs) -> str:
        super().__init__(**kwargs)

        self.sign_in_link = None

        self.homepage_headline = "Fill out your headline here by assigning to `headline`"
        self.homepage_subtext = "Fill out subtext by assigning to `subtext`"
        self.homepage_demo_video_youtube_id = None
        self.homepage_primary_call_to_action = None
        self.homepage_secondary_call_to_action = None

        self.pricing_page_headline = "Pricing"
        self.pricing_page_subtext = "Pricing Information"
        self.pricing_structure = None

    def generate(self):
        if self.sign_in_link:
            self.nav_actions.append(self.sign_in_link)

        # is_homepage = Don't show in nav, but make clickable in Logo
        homepage = WebPage(is_homepage=True)
        homepage.content = CenteredHeroLayout(children=[
            Headline(self.homepage_headline),
            Subtext(self.homepage_subtext),
            CTABar(primary=self.homepage_primary_call_to_action,
                   secondary=self.homepage_secondary_call_to_action),
            YouTubeEmbed(
                id=self.homepage_demo_video_youtube_id) if self.homepage_demo_video_youtube_id is not None else None,
        ])
        self.add_page(homepage)

        # Shows up in the nav as "Pricing", shows up in the url as "/pricing"
        if self.pricing_structure:
            pricing = WebPage(title="Pricing")
            pricing.content = StackLayout(direction="vertical", alignx="center", children=[
                Headline(self.pricing_page_headline),
                Subtext(self.pricing_page_subtext),
                PricingUI(structure=self.pricing_structure)
            ])
            self.add_page(pricing)

        return super().generate()
