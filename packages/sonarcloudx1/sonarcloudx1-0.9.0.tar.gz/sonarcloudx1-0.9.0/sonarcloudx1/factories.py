import factory
from .project import Project
from .components import Components
from .projectbranches import ProjectBranches
from .projectanalyses import ProjectAnalyses
from .projectpullrequests import ProjectPullRequests
from .projectlinks import ProjectLinks
from .users import Users
from .metrics import Metrics
from .metrictypes import MetricTypes
from .issues import Issues
from .componentstree import ComponentsTree

class ProjectFactory(factory.Factory):
    
    class Meta:
        model = Project
        
    personal_access_token = None
    sonar_url = None

class ComponentsFactory(factory.Factory):
    
    class Meta:
        model = Components

    personal_access_token = None
    sonar_url = None

class ProjectBranchesFactory(factory.Factory):
    
    class Meta:
        model = ProjectBranches

    personal_access_token = None
    sonar_url = None

class ProjectAnalysesFactory(factory.Factory):
    
    class Meta:
        model = ProjectAnalyses

    personal_access_token = None
    sonar_url = None

class ProjectPullRequestsFactory(factory.Factory):
    
    class Meta:
        model = ProjectPullRequests

    personal_access_token = None
    sonar_url = None

class ProjectLinksFactory(factory.Factory):
    
    class Meta:
        model = ProjectLinks

    personal_access_token = None
    sonar_url = None

class UsersFactory(factory.Factory):
    
    class Meta:
        model = Users

    personal_access_token = None
    sonar_url = None

class MetricsFactory(factory.Factory):
    
    class Meta:
        model = Metrics

    personal_access_token = None
    sonar_url = None

class MetricTypesFactory(factory.Factory):
    
    class Meta:
        model = MetricTypes

    personal_access_token = None
    sonar_url = None


class IssuesFactory(factory.Factory):
    
    class Meta:
        model = Issues

    personal_access_token = None
    sonar_url = None

class ComponentsTree(factory.Factory):
    
    class Meta:
        model = ComponentsTree

    personal_access_token = None
    sonar_url = None
