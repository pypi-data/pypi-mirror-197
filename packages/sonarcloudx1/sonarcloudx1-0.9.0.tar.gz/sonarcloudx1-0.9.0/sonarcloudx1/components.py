import logging
logging.basicConfig(level=logging.INFO)
from sonarcloudx1.abstract import AbstractSonar
from sonarcloudx1	import factories

# Represents a software Components
class Components(AbstractSonar):

	def __init__(self,personal_access_token, sonar_url):
		super(Components,self).__init__(personal_access_token=personal_access_token,sonar_url=sonar_url)
	
	def get_components(self, project_key):
		return self.sonar.components.get_project_component_and_ancestors(project_key)

	def get_all(self, today=False): 
		try:
			logging.info("Start function: get_components")
			
			project_service = factories.ProjectFactory(personal_access_token=self.personal_access_token,sonar_url=self.sonar_url)
			project_service.set_organization_name(organization_name = self.organization_name)
			projects = project_service.get_all()
			components = []
			
			for project in projects:
				components_return = self.get_components(project['key'])
				components_return['project'] = project
				components.append(components_return)

			
			return components

		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Components")
		
		
