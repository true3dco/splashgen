from splashgen.components import Component, Html


class Headline(Component):
    def __init__(self, text: str = "") -> None:
        super().__init__()
        self.text = text

    def render(self) -> Component:
        return Html(f"""<h1 class="display-5 fw-bold">{self.text}</h1>""")
