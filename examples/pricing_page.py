from splashgen import launch
from splashgen.components import PricingCard, CTAButton
from splashgen.templates import PricingPage

site = PricingPage(title="Splashgen - Splash Pages Built In Python",
                  theme="dark")
site.headline = "Get started immediately!"
site.subtext = """
Splashgen's plans scale for any organization—from startups to Fortune 500s
"""

freeCard = PricingCard(tier="Free", price_description="Free forever.")
freeCard.call_to_action = CTAButton(
    "https://github.com/true3dco/splashgen", "Get Started")
freeCard.feature_checklist = ["Custom Code", "Unlimited pages", "Continuous deployment"]

teamsCard = PricingCard(tier="Teams", price_description="8$/month.")
teamsCard.call_to_action = CTAButton(
    "https://github.com/true3dco/splashgen", "Sign up")
teamsCard.feature_checklist = [
    "All of the features of free", 
    "Analytics", 
    "Custom domains",]

site.pricing_cards = [freeCard, teamsCard]


launch(site)
