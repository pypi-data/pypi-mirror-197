import logging
logging.basicConfig(level=logging.INFO)
from sonarcloudx1.abstract import AbstractSonar

# Represents a software Metric Types
class MetricTypes(AbstractSonar):

	def __init__(self,personal_access_token, sonar_url):
		super(MetricTypes,self).__init__(personal_access_token=personal_access_token,sonar_url=sonar_url)
	
	def get_all(self, today=False): 
		metrictypes = []
		try:
			logging.info("Start function: get_metrictypes")
			
			metrictypes = self.sonar.metrics.get_metrics_types()
			
			
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Metric Types")
		
		return metrictypes	
