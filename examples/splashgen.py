from os import path
from splashgen import MetaTags, SplashSite, launch
from splashgen.integrations import MailchimpSignup

site = SplashSite(title="Splashgen – Splash Pages Built In Python",
                  logo=path.join(path.dirname(__file__), "logo.png"),
                  theme="dark")
site.headline = "Effortlessly build your splash page in python"
site.subtext = """
In less than 30 lines of python, create beautiful and clean splash pages with Splashgen.
Don''t play around with no code tools when you already know how to code. 
"""
site.meta = MetaTags(title=site.headline,
                     description="Build you splash page in Python. Sign up to join our pilot program!",
                     image="https://t3dmedia.s3.amazonaws.com/_notvideos/zwbg.png",
                     canonical_url="https://zenweb.dev")
site.call_to_action = MailchimpSignup(
    "http://eepurl.com/hw4od9", button_text="Join our pilot")

launch(site)
