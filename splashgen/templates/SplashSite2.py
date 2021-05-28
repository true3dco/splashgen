from splashgen import Component, MetaTags
from splashgen.components import CTAButton, CTAButtonSecondary, Link

from os import path

_ASSET_DIR = path.join(path.dirname(__file__), '../assets')


# TODO: Render favicons, touch icon, splash icons, etc.
# TODO: Support BG color?
class SplashSite2(Component):
    meta: MetaTags

    nav_bar_center_link: Link
    nav_bar_right_link: Link

    headline: str
    subtext: str
    primary_call_to_action: CTAButton
    secondary_call_to_action: CTAButtonSecondary
    
    hero_video: str

    enable_splashgen_analytics: bool
    """Set this to false to disable analytics.

    We use analytics in order to better understand product usage, and *never*
    track any personally-identifiable information on users visiting your site.
    """

    def __init__(self, title: str = "Splash Site 2", logo: str = None, meta: MetaTags = None, theme: str = "light") -> str:
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

        # Splash site 2 fields
        self.headline = "Fill out your headline here by assigning to `headline`"
        self.subtext = "Fill out subtext by assigning to `subtext`"
        self.call_to_action = None
        self.primary_call_to_action = None
        self.secondary_call_to_action = None

        self.hero_video = None

        self.nav_bar_center_link = None
        self.nav_bar_right_link = None
        
        self.enable_splashgen_analytics = True

    def render(self) -> str:
        logo_url = self.write_asset_to_build(self.logo)

        if self.hero_video is None:
            self.hero_video = path.join(_ASSET_DIR, "video-default.mp4")
        hero_video_url = self.write_asset_to_build(self.hero_video)

        favicons = self._gen_favicons()
        return self.into_template("splash_site_2.html.jinja", extras={
            "logo": logo_url,
            "favicons": favicons,
            "hero_video": hero_video_url,
        })


