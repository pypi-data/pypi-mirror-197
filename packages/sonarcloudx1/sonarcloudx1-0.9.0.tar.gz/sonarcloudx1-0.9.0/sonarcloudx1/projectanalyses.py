import logging
logging.basicConfig(level=logging.INFO)
from sonarcloudx1.abstract import AbstractSonar
from sonarcloudx1	import factories

# Represents a software Project Branches
class ProjectAnalyses(AbstractSonar):

	def __init__(self,personal_access_token, sonar_url):
		super(ProjectAnalyses,self).__init__(personal_access_token=personal_access_token,sonar_url=sonar_url)
	
	def get_projectanalyses(self, project_key):
		return self.sonar.project_analyses.search_project_analyses_and_events(project=project_key)

	def get_all(self, today=False): 
		try:
			logging.info("Start function: get_projectanalyses")
			
			project_service = factories.Project(personal_access_token=self.personal_access_token,sonar_url=self.sonar_url)
			project_service.set_organization_name(organization_name = self.organization_name)
			projects = project_service.get_all()
			projectanalyses = []
			
			for project in projects:
				projectanalyses_return = self.get_projectanalyses(project['key'])
				projectanalyses_return['project'] = project
				projectanalyses.append(projectanalyses_return)

			return projectanalyses

		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Project Analyses")
		
		
