class appConfiguration:
    """App Configuration is responisble for controlling app details"""
    def __init__(self, appName, appVersion, appDesciption, contributers, source):
        self.appName = appName
        self.appVersion = appVersion
        self.appDescription = appDesciption
        self.contributers = contributers
        self.source = source

class projectManager:
    """Project manager manages your projects name and the users username"""
    def __init__(self, projectName, username):
        self.projectName = projectName
        self.user = f"@{username}"


application = appConfiguration(
  appName="Design Labs",
  appDesciption="Pass Null",
  appVersion="1,0",
  contributers=['CastyiGlitchxz'],
  source=None,
)
