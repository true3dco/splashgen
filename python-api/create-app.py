from base-page import BasePage


class CreateAppPage(BasePage):

    def config(self):
        return {
            "route": "/apps/{self.full_name}/delete"
        }

    def render(self):
        if LOCAL_STORAGE.jwt_token != None:
            return REDIRECT(LoggedInHomePage.ROUTE)


        response = Request(
            "https://cxpme86mmi.execute-api.us-east-2.amazonaws.com/repos",
            body={"jwt_token": LOCAL_STORAGE.jwt_token})
        
        repo_list = []
        for repo in response.data:
            repo_list.append(
                {
                    "name": repo.name,
                    "branch": repo.default_branch,
                    "createButton": Request("https://cxpme86mmi.execute-api.us-east-2.amazonaws.com/zenweb-github-create-webhook", body={"repo": repo.full_name}) # URL Param
                }
            )

   
        return """
        <layout_d>
            <h1>Which repo would you like to deploy?</h1>
            {repo_list}
        </layout_c>"""