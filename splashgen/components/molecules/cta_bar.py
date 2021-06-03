from splashgen.components import Component
from splashgen.components.layouts import StackLayout


class CTABar(Component):
    def __init__(self, primary: Component, secondary: Component) -> None:
        super().__init__()
        self.primary = primary
        self.secondary = secondary

    def render(self) -> Component:
        return StackLayout(direction="horizontal", children=[
            self.primary,
            self.secondary
        ])
