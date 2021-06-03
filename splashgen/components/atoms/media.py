import mimetypes
from os import path
from typing import Tuple
from splashgen.components import Component, Html


class Video(Component):
    mime: str

    def __init__(self, src: str, aspect_ratio: Tuple[int, int] = None) -> None:
        super().__init__()
        self.src = str
        mime, _ = mimetypes.guess_type(self.src)
        if not mime:
            raise ValueError(
                f"Could not determine MIME type for video {path.basename(src)}")
        self.mime = mime
        self.aspect_ratio = aspect_ratio or (16, 9)

    def render(self) -> Component:
        ar = f"{self.aspect_ratio[0]}by{self.aspect_ratio[1]}"
        return Html(f"""
        <div class="embed-responsive embed-responsive-{ar}">
            <video controls class="embed-responsive-item">
                <source src="{self.src}" type="{self.mime}"
            </video>
            Sorry, your browser doesn't support videos.
        </div>
        """)
