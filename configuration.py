class AppConfiguration:
    """App Configuration is responisble for controlling app details"""
    def __init__(self, app_name, app_version, app_desciption, contributers, source):
        self.app_name = app_name
        self.app_version = app_version
        self.app_description = app_desciption
        self.contributers = contributers
        self.source = source

class ProjectManager:
    """Project manager manages your projects name and the users username"""
    def __init__(self, project_name, username):
        self.project_name = project_name
        self.user = f"@{username}"


application = AppConfiguration(
  app_name="Design Labs",
  app_desciption="Pass Null",
  app_version="1,0",
  contributers=['CastyiGlitchxz'],
  source=None,
)
