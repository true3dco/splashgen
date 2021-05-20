from splashgen import Component


class CTAButton(Component):
    def __init__(self, link: str, text: str) -> None:
        self.link = link
        self.text = text

    def render(self) -> str:
        return f'<a href="{self.link}" class="btn btn-primary btn-lg px-4">{self.text}</a>'
