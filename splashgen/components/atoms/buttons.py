from typing import List
from splashgen.components import Component
from . import Link


# TODO: OnClick
# TODO: Button Component
class _Button(Component):
    def __init__(self, classnames: List[str], link: Link = None, text: str = "") -> None:
        super().__init__()
        self.classnames = classnames
        self.link = link
        self.text = text

    def html(self):
        if self.link is not None:
            self.link.classlist.extend(self.classnames)
            return self.link.html()
        return f"""<button class="btn btn-primary btn-lg">{self.text}</button>"""


class PrimaryButton(_Button):
    def __init__(self, link: Link = None, text: str = "") -> None:
        super().__init__(["btn", "btn-primary",
                          "btn-lg"], link=link, text=text)


class SecondaryButton(Component):
    def __init__(self, link: Link = None, text: str = "") -> None:
        super().__init__(["btn", "btn-secondary",
                          "btn-lg"], link=link, text=text)
