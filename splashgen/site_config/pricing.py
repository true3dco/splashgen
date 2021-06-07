from typing import List, NamedTuple, Optional

from .base import Link


class FeatureList(NamedTuple):
    headline: str = "Includes"
    features: List[str] = []


class Tier(NamedTuple):
    name: str
    price_per_month: float
    call_to_action: Link
    description: Optional[str] = None
    feature_list: Optional[FeatureList] = None
    recommended: bool = False


class Faq(NamedTuple):
    question: str
    answer: str


class PricingStructure(NamedTuple):
    tiers: List[Tier]
    faqs: List[Faq]
