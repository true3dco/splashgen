from typing import Tuple
from urllib.parse import ParseResult, urlparse

import query_string
import urlexpander

from splashgen import Component


class MailchimpSignup(Component):
    _url_cache = {}
    bot_buster_id: str

    def __init__(self, signup_form_url: str, button_text: str = "Sign up"):
        super().__init__()

        ps, qs = self._parse_signup_url(signup_form_url)
        self.signup_form_url = ps.geturl()
        self.bot_buster_id = f'b_{qs["u"]}_{qs["id"]}'
        self.button_text = button_text

    def render(self) -> str:
        return self.into_template("mailchimp_signup.html.jinja")

    def _parse_signup_url(self, url: str) -> Tuple[ParseResult, dict]:
        expanded_url = self._url_cache.get(url, urlexpander.expand(url))
        if "list-manage.com/subscribe" not in expanded_url:
            raise ValueError(
                "It doesn't look like you gave us a MailChimp URL form")
        ps = urlparse(expanded_url)
        ps = ps._replace(path=f"{ps.path}/post")
        qs = query_string.parse(ps.query)
        return ps, qs
