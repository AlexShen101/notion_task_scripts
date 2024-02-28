from notion_client import Client
import os

from setup import setup
from setup import master_project_db_setup as master_project

outputFilePath = setup.master_project_list_file_path
notion_token = setup.notion_token

master_project_database = master_project.master_projects_database

os.environ['notion_token'] = notion_token
notion = Client(auth=os.environ['notion_token'])

my_page = notion.databases.query(
    **{
        "database_id": master_project_database,
        "filter": {
            "or": [
                {
                    "property": master_project.status_select,
                    "select": {
                        "equals": "In progress"
                    }
                },
                {
                    "property": master_project.status_select,
                    "select": {
                        "equals": "No status"
                    }
                },
            ]
        }
    }
)

results = my_page['results']

trimmedResults = []
for result in results:
    print(result)
    trimmedResults.append(result['properties'])

def listNames(arr):
    output = ""
    for item in arr:
        try:
            output += (item[master_project.title]['title'][0]['text']['content']) + "\n"
        except:
            output += ""
    return output


outputText = listNames(trimmedResults)

with open(outputFilePath, 'w') as f:
    f.write(outputText)
