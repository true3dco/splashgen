from .base import Template


class PricingPage(Template):

    headline: str
    subtext: str
    pricing_cards = None # : list[PricingCard]

    template = "pricing_page.html.jinja"

    def __init__(self, **kwargs) -> str:
        super().__init__(**kwargs)

        self.headline = "Fill out your headline here by assigning to `headline`"
        self.subtext = "Fill out subtext by assigning to `subtext`"
        self.pricingCards = None
