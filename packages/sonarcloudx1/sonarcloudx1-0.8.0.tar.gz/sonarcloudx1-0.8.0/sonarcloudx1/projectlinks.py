import logging
logging.basicConfig(level=logging.INFO)
from sonarcloudx1.abstract import AbstractSonar
from sonarcloudx1	import factories

# Represents a software Project Links
class ProjectLinks(AbstractSonar):

	def __init__(self,personal_access_token, sonar_url):
		super(ProjectLinks,self).__init__(personal_access_token=personal_access_token,sonar_url=sonar_url)
	
	def get_projectlinks(self, project_key):
		return self.sonar.project_links.search_project_links(project_key)

	def get_all(self, today=False): 
		try:
			logging.info("Start function: get_projectlinks")
			
			project_service = factories.Project(personal_access_token=self.personal_access_token,sonar_url=self.sonar_url)
			project_service.set_organization_name(organization_name = self.organization_name)
			projects = project_service.get_all()
			projectlinks = []
			
			for project in projects:
				projectlinks_return = self.get_projectlinks(project['key'])
				projectlinks_return['project'] = project
				projectlinks.append(projectlinks_return)

			return projectlinks

		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Project Links")
		
		
