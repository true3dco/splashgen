from base-page import BasePage



class SplashPage(BasePage):

    def config(self):
        return {
            "route": "/"
        }

    def render(self):
        if LOCAL_STORAGE.jwt_token != None:
            return REDIRECT(LoggedInHomePage.ROUTE)


        call_to_action = """(
            <Button 
                onClick=({})
                text="Deploy in less than a minute">)"""
        
        secondary_call_to_action = """
            <Button 
                onClick=({})
                text="Deploy in less than a minute"/>"""
        logo = """<Image source="" />""""
        video = """<Video source="https://youtu.be/dQw4w9WgXcQ"/>"""

        return """
        <layout_a>
            {logo}
            {call_to_action}
            {secondary_call_to_action}
            {video}
        </layout_a>"""