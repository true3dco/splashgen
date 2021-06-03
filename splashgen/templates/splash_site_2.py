from splashgen.components import *
from splashgen.components.layouts import CenteredHeroLayout, StackLayout, NavContentLayout
from .base import WebApp, WebPage


class SplashSite2(WebApp):
    nav_bar_center_link: Link
    nav_bar_right_link: Link
    headline: str
    subtext: str
    primary_call_to_action: PrimaryButton
    secondary_call_to_action: SecondaryButton
    hero_video: str

    layout = NavContentLayout()

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
        self.pricing_structure = None
        self.sign_in_link = ""

    def generate(self):
        # Determines nav_logo and nav_title
        self.layout.branding = self.branding
        self.layout.nav_actions.append(
            Link(self.sign_in_link, "Sign In"))

        # is_homepage = Don't show in nav, but make clickable in Logo
        homepage = WebPage(layout=self.layout, is_homepage=True)
        homepage.content = CenteredHeroLayout(children=[
            Headline(self.headline),
            Subtext(self.subtext),
            CTABar(primary=self.primary_call_to_action,
                   secondary=self.secondary_call_to_action),
            Video(self.write_asset_to_build(self.hero_video)
                  ) if self.hero_video is not None else None,
        ])
        self.add_page(homepage)

        # Shows up in the nav as "Pricing", shows up in the url as "/pricing"
        pricing = WebPage(template=self.layout, title="Pricing")
        pricing.content = StackLayout(direction="vertical", children=[
            Headline("Affordable pricing for everyone"),
            Subtext("Cancel whenever you want. Eject to html/css/js anytime."),
            # PricingUI(pricing_structure=self.pricing_structure)
        ])
        self.add_page(pricing)

        return super().generate()
