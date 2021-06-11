from os import path
from splashgen import launch
from splashgen.app_config import Branding, SEO, Link
from splashgen.app_config.pricing import PricingStructure, Tier, FeatureList, Faq
from splashgen.components import PrimaryButton, SecondaryButton
from splashgen.app_templates import SaasMarketingSite

app = SaasMarketingSite(
    branding=Branding(
        name="Splashgen Hosting",
        logo=path.join(path.dirname(__file__), "splashgen-hosting-logo.svg"),
        theme="dark"),
    seo=SEO(
        title="Splashgen Hosting – Build and deploy landing pages in pure python",
        description="All it takes is a github repo and 10 lines of python. Get started for free!",
        canonical_url="https://splashgen.sh",
        site_image="https://splashgen.sh/splashgen-logo.svg",
    ))
app.sign_in_link = Link("/signin", "Sign up")

app.homepage_headline = "Build your splash page 2 in python effortlessly"
app.homepage_subtext = """
In less than 20 lines of python, create clean and beautiful splash pages with
Splashgen. Don't waste time with no-code tools when you already know how to
code.
"""
app.homepage_demo_video_youtube_id = "HpovwbPGEoo"
app.homepage_primary_call_to_action = PrimaryButton(link=Link(
    "https://github.com/true3dco/splashgen", "View on GitHub"))
app.homepage_secondary_call_to_action = SecondaryButton(link=Link(
    "https://github.com/true3dco/splashgen", "View on GitHub"))

app.pricing_page_headline = "Affordable pricing for everyone"
app.pricing_page_subtext = "Cancel whenever you want. Eject to html/css/js anytime."
app.pricing_structure = PricingStructure(
    tiers=[
        Tier(
            name="Basic",
            description="Some description of the basic plan",
            price_per_month=0,
            call_to_action=Link(
                "/signup", "Get started for free"
            ),
            feature_list=FeatureList("Get up and running quickly", [
                "Hosting from our global CDN",
                "Instant deploys for GitHub",
                "Automatic building and generating of all your assets"
            ])
        ),
        Tier(
            name="Premium",
            recommended=True,
            description="When you're ready to go live",
            price_per_month=2,
            call_to_action=Link("/signup", "Sign up"),
            feature_list=FeatureList("Everything from basic, plus", [
                "Custom domain names",
                "what",
                "else",
                "will",
                "we",
                "offer"
            ])
        )
    ],
    faqs=[
        Faq("What if I want to move off python?", "No problem! Simply eject"),
        Faq("Do you support languages besides python?",
            "No, but let us know if this is something you want!")
    ]
)

launch(app)
