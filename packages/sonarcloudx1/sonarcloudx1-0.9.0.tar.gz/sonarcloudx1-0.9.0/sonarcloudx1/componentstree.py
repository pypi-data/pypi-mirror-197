import logging
logging.basicConfig(level=logging.INFO)
from sonarcloudx1.abstract import AbstractSonar
from sonarcloudx1	import factories

# Represents a software Components
class ComponentsTree(AbstractSonar):

	def __init__(self,personal_access_token, sonar_url):
		super(ComponentsTree,self).__init__(personal_access_token=personal_access_token,sonar_url=sonar_url)
	
	def get_components_tree(self, project_key):
		return self.sonar.components.get_components_tree(project_key)

	def get_all(self, today=False): 
		try:
			logging.info("Start function: get_components_tree")
			
			project_service = factories.ProjectFactory(personal_access_token=self.personal_access_token,sonar_url=self.sonar_url)
			project_service.set_organization_name(organization_name = self.organization_name)
			projects = project_service.get_all()
			components_tree = []
			
			for project in projects:
				component_tree_return = self.get_components_tree(project['key'])
				component_tree_return['project'] = project
				components_tree.append(component_tree_return)

			
			return components_tree

		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Components Tree")
		
		
