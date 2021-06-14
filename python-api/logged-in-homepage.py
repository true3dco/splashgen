
from base-page import BasePage

class LoggedInHomePage(BasePage):
    
    def config(self):
        return {
            "route": "/apps"
        }

    def render(self):
        if LOCAL_STORAGE.jwt_token == None:
            return REDIRECT(SplashGenHomePage.ROUTE)



        response = Request(
            "https://cxpme86mmi.execute-api.us-east-2.amazonaws.com/apps",
            body={"jwt_token": LOCAL_STORAGE.jwt_token})
        
        app_list = []
        for app in response.data:
            app_list.append(
                {
                    "name": app.name,
                    "branch": app.default_branch,
                    "deleteButton": REDIRECT(DeleteAppPage.Route(full_name=full_name)) # URL Param
                }
            )

        deploy_app = """(
            <Button 
                onClick=({REDIRECT(CreateAppPage.Route)})
                text="New Web App">)"""
        

         
        app_table = """
        <Table
            TopRightButton={deploy_app}
            Contents={app_list}>
        </Table>
        """

        return """
        <layout_b>
            {app_table}
        </layout_b>"""