from splashgen.components import Component


class StackLayout(Component):
    def __init__(self, direction: str = "horizontal", spacing: int = 8) -> None:
        super().__init__()
        self.direction = direction
        self.spacing = spacing
