from splashgen import launch
from splashgen.components import CTAButton, CTAButtonSecondary, Link
from splashgen.templates import SplashSite2

site = SplashSite2(title="Splashgen 2 - Splash Pages Built In Python",
                   theme="dark")

site.nav_bar_center_link = Link(
    "https://github.com/true3dco/splashgen", "About Us"
)
site.nav_bar_right_link = Link(
    "https://github.com/true3dco/splashgen", "Sign Up"
)

site.headline = "Build your splash page 2 in python effortlessly"
site.subtext = """
In less than 20 lines of python, create clean and beautiful splash pages with
Splashgen. Don't waste time with no-code tools when you already know how to
code.
"""
site.primary_call_to_action = CTAButton(
    "https://github.com/true3dco/splashgen", "View on GitHub")
site.secondary_call_to_action = CTAButtonSecondary(
    "https://github.com/true3dco/splashgen", "View on GitHub")

launch(site)
