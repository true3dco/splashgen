from splashgen.generators import Component


class CTAButtonSecondary(Component):
    def __init__(self, link: str, text: str) -> None:
        self.link = link
        self.text = text

    def render(self) -> str:
        return f'<a href="{self.link}" class="btn btn-secondary btn-lg px-4">{self.text}</a>'
