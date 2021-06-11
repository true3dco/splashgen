from splashgen import launch
from splashgen.app_templates import SplashSite
from splashgen.components import Form, TextInput, EmailInput, SelectInput

site = SplashSite(title="Form example")
site.headline = "Form example"
site.subtext = "This template illustrates how to add a custom form into your code"

# NOTE: You can omit the first argument to just use inputs with placeholders
inputs = [
    TextInput(id="name", label="Name", required=True,
              placeholder="First and Last"),
    EmailInput(id="email", label="Email address", required=True),
    SelectInput(id="role", label="Role", options=[
        # You can specify a (text, value) tuple, or just provide text, and the
        # value will be a slugified version of the text.
        ("CEO/Founder", "exec"),
        "Engineer",
        "Other"])
]
site.call_to_action = Form(endpoint="http://postman-echo.com/post",
                           inputs=inputs,
                           submit_text="Get Started")

launch(site)
