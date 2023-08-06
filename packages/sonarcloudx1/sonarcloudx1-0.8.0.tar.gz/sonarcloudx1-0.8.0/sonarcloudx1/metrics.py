import logging
logging.basicConfig(level=logging.INFO)
from sonarcloudx1.abstract import AbstractSonar

# Represents a software Project
class Metrics(AbstractSonar):

	def __init__(self,personal_access_token, sonar_url):
		super(Metrics,self).__init__(personal_access_token=personal_access_token,sonar_url=sonar_url)
	
	def get_all(self, today=False): 
		metrics = []
		try:
			logging.info("Start function: get_metrics")
			
			metrics = self.sonar.metrics.search_metrics()
			
			
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Metrics")
		
		return metrics	
