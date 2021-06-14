from zenweb import WebPage

class BasePage(WebPage):
    def branding(self):
        return {
            "primary_color": "#32CBEA",
            "secondary_color": "#063F1B"
        }