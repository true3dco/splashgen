from typing import Optional
from splashgen.components import *
from splashgen.components.layouts import CenteredHeroLayout, StackLayout, NavContentLayout
from splashgen.core import WebApp, WebPage


# TODO: WebApp has nav_links + nav_actions + layout + SEO + Branding, etc.
class SaasMarketingSite(WebApp):
    homepage_headline: str
    homepage_subtext: str
    homepage_demo_video_youtube_id: Optional[str]
    homepage_primary_call_to_action: PrimaryButton
    homepage_secondary_call_to_action: SecondaryButton

    # This comes from WebApp
    layout = NavContentLayout()

    def __init__(self, **kwargs) -> str:
        super().__init__(**kwargs)

        self.homepage_headline = "Fill out your headline here by assigning to `headline`"
        self.homepage_subtext = "Fill out subtext by assigning to `subtext`"
        self.homepage_demo_video_youtube_id = None
        self.homepage_primary_call_to_action = None
        self.homepage_secondary_call_to_action = None

        # TODO: Other stuff
        self.pricing_structure = None

    def generate(self):
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
        pricing = WebPage(title="Pricing")
        pricing.content = StackLayout(direction="vertical", alignx="center", children=[
            Headline("Affordable pricing for everyone"),
            Subtext("Cancel whenever you want. Eject to html/css/js anytime."),
            # PricingUI(pricing_structure=self.pricing_structure)
        ])
        self.add_page(pricing)

        return super().generate()
