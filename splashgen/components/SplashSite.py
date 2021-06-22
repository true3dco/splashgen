from splashgen import Component, MetaTags
from os import path
from PIL import Image
from urlextract import URLExtract
from validate_email import validate_email

_ASSET_DIR = path.join(path.dirname(__file__), '../assets')


def _is_email(url):
    return bool(validate_email(
        url, check_dns=False, check_blacklist=False, check_smtp=False))


# TODO: Render favicons, touch icon, splash icons, etc.
# TODO: Support BG color?
class SplashSite(Component):
    meta: MetaTags
    headline: str
    subtext: str
    call_to_action: Component
    hero_image: str
    enable_splashgen_analytics: bool
    """Set this to false to disable analytics.

    We use analytics in order to better understand product usage, and *never*
    track any personally-identifiable information on users visiting your site.
    """

    def __init__(self, title: str = "Splash Site", logo: str = None, meta: MetaTags = None, theme: str = "light") -> str:
        super().__init__()
        self.title = title
        if not logo:
            logo = path.join(_ASSET_DIR, "logo-default.png")
        self.logo = logo
        self.meta = meta
        if theme not in ["light", "dark"]:
            raise ValueError(
                "Invalid theme option. Please specify 'light' or 'dark'")
        self.theme = theme
        self.headline = "Fill out your headline here by assigning to `headline`"
        self.subtext = "Fill out subtext by assigning to `subtext`"
        self.call_to_action = None
        self.hero_image = None
        self.favicon_img = self.logo
        self.enable_splashgen_analytics = True

    def render(self) -> str:
        self._process_links()
        logo_url = self.write_asset_to_build(self.logo)
        if self.hero_image:
            hero_img_url = self.write_asset_to_build(self.hero_image)
        else:
            hero_img_url = None
        favicons = self._gen_favicons()
        return self.into_template("splash_site.html.jinja", extras={
            "logo": logo_url,
            "favicons": favicons,
            "hero_image": hero_img_url,
        })

    def _process_links(self):
        extractor = URLExtract(extract_email=True)
        for url in extractor.gen_urls(self.subtext):
            if _is_email(url):
                href = f"mailto:{url}"
            else:
                href = url
            link = f"<a href={href}>{url}</a>"
            self.subtext = self.subtext.replace(url, link)

    def _gen_favicons(self):
        favicons = []
        with Image.open(self.favicon_img) as img:
            for size in [16, 32, 64]:
                favicon_info = {
                    "rel": "icon",
                    "type": "image/png",
                    "size": f"{size}x{size}",
                    "filename": f"favicon-{size}x{size}.png"
                }
                resized = img.resize((size, size))
                resized.save(path.join(self.build_dir,
                             favicon_info["filename"]))
                favicons.append(favicon_info)
        return favicons
