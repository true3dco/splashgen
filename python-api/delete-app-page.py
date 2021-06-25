from base-page import BasePage


class DeleteAppPage(BasePage):

    def config(self):
        return {
            "route": "/apps/{self.full_name}/delete"
        }

    def render(self):
        if LOCAL_STORAGE.jwt_token != None:
            return REDIRECT(LoggedInHomePage.ROUTE)


        delete_button = """(
            <Button 
                onClick=({})
                text="Yes">)"""
        back_out_button = """(
            <Button 
                onClick=({})
                text="No">)"""
        
   
        return """
        <layout_c>
            <h1>Are you sure you want to delete {self.full_name}?</h1>
            {delete_button}
            {back_out_button}
        </layout_c>"""