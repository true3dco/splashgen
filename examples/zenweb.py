from splashgen import MetaTags, SplashSite, launch
from splashgen.integrations import MailchimpSignup

site = SplashSite(title="ZenWeb – Python Internal Web Apps",
                  logo="./logo.svg")
site.headline = "Effortless internal tools for your backend services"
site.subtext = """
Write simple code that plugs directly into your infrastructure, and let ZenWeb
turn it into a web app that anyone on your team can use.
Stop getting pinged every time an on-call engineer needs a script run,
and start automating your domain expertise.
"""
# This could probably be made easier
site.meta = MetaTags(title=site.headline,
                     description="Automate your domain expertise. Sign up to join our pilot program!",
                     image="https://t3dmedia.s3.amazonaws.com/_notvideos/zwbg.png",
                     canonical_url="https://zenweb.dev")
site.signup_form = MailchimpSignup(
    "http://eepurl.com/hw4od9", button_text="Join our pilot")

launch(site)
