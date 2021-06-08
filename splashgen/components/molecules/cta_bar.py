from splashgen.generators import Component


class CTABar(Component):
    def __init__(self, primary: Component, secondary: Component) -> None:
        super().__init__()
        self.primary = primary
        self.secondary = secondary
