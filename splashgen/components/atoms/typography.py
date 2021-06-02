from splashgen.components import Component


class Headline(Component):
    def __init__(self, text: str = "") -> None:
        super().__init__()
        self.text = text

    def html(self) -> str:
        return f"""<h1 class="display-5 fw-bold">{self.text}</h1>"""
