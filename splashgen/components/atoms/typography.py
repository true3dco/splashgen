from splashgen.components import Component, Html


class Headline(Component):
    def __init__(self, text: str = "") -> None:
        super().__init__()
        self.text = text


class Subtext(Component):
    def __init__(self, text: str = "") -> None:
        super().__init__()
        self.text = text
