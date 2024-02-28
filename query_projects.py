from notion_client import Client
import os

from setup import setup
from setup import project_db_setup as project

outputFilePath = setup.project_list_file_path
notion_token = setup.notion_token

project_database = project.projects_database

os.environ['notion_token'] = notion_token
notion = Client(auth=os.environ['notion_token'])

my_page = notion.databases.query(
    **{
        "database_id": project_database,
        "filter": {
            "or": [
                {
                    "property": project.status_select,
                    "select": {
                        "equals": "Incomplete"
                    }
                },
                {
                    "property": project.status_select,
                    "select": {
                        "equals": "In Progress"
                    }
                },
                {
                    "property": project.status_select,
                    "select": {
                        "equals": "Rolling"
                    }
                },
            ]
        }
    }
)

results = my_page['results']

trimmedResults = []
for result in results:
    trimmedResults.append(result['properties'])

def listNames(arr):
    output = ""
    for item in arr:
        try:
            output += (item[project.title]['title'][0]['text']['content']) + "\n"
        except:
            output += ""
    return output


outputText = listNames(trimmedResults)

with open(outputFilePath, 'w') as f:
    f.write(outputText)
