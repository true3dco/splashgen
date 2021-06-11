from splashgen.generators import Component
from splashgen.app_config.pricing import PricingStructure


class PricingUI(Component):
    def __init__(self, structure: PricingStructure) -> None:
        super().__init__()
        self.structure = structure
