from os import path
from splashgen import MetaTags, launch
from splashgen.components import SplashSite
from splashgen.integrations import MailchimpSignup

site = SplashSite(title="ZenWeb – Python Internal Web Apps",
                  logo=path.join(path.dirname(__file__), "zenweb-logo.png"),
                  theme="dark")
site.headline = "Effortless internal tools for your backend services"
site.subtext = """
Write simple code that plugs directly into your infrastructure, and let ZenWeb
turn it into a web app that anyone on your team can use.
Stop getting pinged every time an on-call engineer needs a script run,
and start automating your domain expertise.
"""
site.meta = MetaTags(title=site.headline,
                     description="Automate your domain expertise. Sign up to join our pilot program!",
                     image="https://t3dmedia.s3.amazonaws.com/_notvideos/zwbg.png",
                     canonical_url="https://zenweb.dev")
site.call_to_action = MailchimpSignup(
    "http://eepurl.com/hw4od9", button_text="Join our pilot")

launch(site)
