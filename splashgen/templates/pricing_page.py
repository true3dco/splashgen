from splashgen import Component, MetaTags

from os import path

_ASSET_DIR = path.join(path.dirname(__file__), '../assets')


class PricingPage(Component):
    meta: MetaTags

    headline: str
    subtext: str
    
    # Only supports 2 pricing cards for now
    pricing_cards = None# : list[PricingCard]


    def __init__(self, title: str = "Pricing Page 2", logo: str = None, meta: MetaTags = None, theme: str = "light") -> str:
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

        self.pricingCards = None

        self.enable_splashgen_analytics = True


    def render(self) -> str:
        logo_url = self.write_asset_to_build(self.logo)

        favicons = self._gen_favicons()
        return self.into_template("pricing_page.html.jinja", extras={
            "logo": logo_url,
            "favicons": favicons,
        })


