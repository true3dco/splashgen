from splashgen import Component


class Link(Component):
    def __init__(self, link: str, text: str) -> None:
        self.link = link
        self.text = text

    def render(self) -> str:
        return f'<a href="{self.link}">{self.text}</a>'
