# SonarCloudX

## General Information
* **Software**: SonarCloud
* **Author**: Carlos Henrique Maulaz de Freitas
* **Author's e-mail**:carlosmaulaz@gmail.com
* **Source Repository**: [https://gitlab.com/immigrant-data-driven-development/libs/application/sonarcloud](https://gitlab.com/immigrant-data-driven-development/libs/application/sonarcloud.git)  

## Goal
O SonarCloud é um serviço de análise de códifo desenvolvido para detectar problemas em 25 diferentes linguagens de programação. O objetivo da lib é extrair os dados de uma organização na ferramenta.

	
## Instalation

To install sonarcloudX, run this command in your terminal:
```bash
pip install sonarcloudx1
```

## Usage

```python

from sonarcloudX1 import factories
from pprint import pprint 

sonar_url = "https://sonarcloud.io"
personal_access_token =  "sonarcloud_token"

service = factories.ProjectFactory(personal_access_token=personal_access_token,sonar_url=sonar_url)
service.set_organization_name(organization_name = 'organization_name')
results = service.get_all(today=False)

print(results)

pprint (len(results))

for item in results:
    pprint (item.__dict__)

```
    
  