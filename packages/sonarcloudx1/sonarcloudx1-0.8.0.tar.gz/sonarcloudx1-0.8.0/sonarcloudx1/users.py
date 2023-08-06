import logging
logging.basicConfig(level=logging.INFO)
from sonarcloudx1.abstract import AbstractSonar

# Represents a software Project
class Users(AbstractSonar):

	def __init__(self,personal_access_token, sonar_url):
		super(Users,self).__init__(personal_access_token=personal_access_token,sonar_url=sonar_url)
	
	def get_all(self, today=False): 
		users = []
		try:
			logging.info("Start function: get_users")
			
			users = list(self.sonar.users.search_users())
			
			
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Users")
		
		return users	
