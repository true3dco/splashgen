from splashgen import Component


class PricingCard(Component):
    def __init__(self, tier: str = "<<TIER>>", price_description: str = "<<PRICE_DESCRIPTION>>", call_to_action: Component = None) -> None:
        self.tier = tier
        self.price_description = price_description
        self.call_to_action: Component = call_to_action 
        self.feature_checklist: list[str] = None

    def render(self) -> str:
        return f"""
        <div">
            <div>
                <p>{self.tier}</p>
                <p>{self.price_description}</p>
                {self.call_to_action}
            </div>
            <div>
              {self.feature_checklist}
            </div>
        </div>
        """
