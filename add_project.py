from notion_client import Client
import os
from datetime import date
import datetime
import sys

import setup.setup as setup
import setup.project_db_setup as project
import setup.master_project_db_setup as master_project

notion_token = setup.notion_token

projects_database = project.projects_database
master_projects_database = master_project.master_projects_database

os.environ['notion_token'] = notion_token
notion = Client(auth=os.environ['notion_token'])

print("enter project name")
entry_name = input()
print("enter status (hit enter for default value)")
entry_status = input()
print("enter due date (hit enter for today's date)")
entry_date = input()
print("enter parent master project name")
entry_master_project = input()

valid_status = project.status_select_restrictions
if valid_status != [] and entry_status not in valid_status:
    print('status was not valid')
    sys.exit()

if (entry_status == ""):
    entry_status = project.status_select_default_value

if (entry_date == ""):
    entry_date = str(date.today())

print('master query - line 56')
master_project_query = notion.databases.query(
    **{
        "database_id": master_projects_database,
        "filter": {
            "and": [
                {
                    "property": project.title,
                    "title": {
                        "contains": entry_master_project
                    }
                },
            ]
        }
    }
)

try:
    master_project_id = master_project_query['results'][0]['id']
except:
    print('there was no master project found from the query using your project name')

properties = {
    project.title: {
        "title": [
            {
                "text": {
                    "content": entry_name
                }
            }
        ]
    },
    project.status_select: {
        "select": {
            "name": entry_status
        }
    },
    project.date: {
        "date": {
            "start": entry_date
        }
    }, 
    project.master_projects_db_relation: {
        "relation": [
            {
                "id": master_project_id
            }
        ]
    }
}

print('project query for duplicates - line 112')
my_page = notion.databases.query(
    **{
        "database_id": projects_database,
        "filter": {
            "and": [
                {
                    "property": project.title,
                    "title": {
                        "contains": entry_name
                    }
                },
                {
                    "property": project.master_projects_db_relation,
                    "relation": {
                        "contains": master_project_id
                    }
                }
            ]
        }
    }
)

results = my_page['results']

if (results == []):
    print('create project - line 138')
    new_page = notion.pages.create(
        **{
            'parent': {
                'database_id': projects_database,
            },
            'properties': properties
        })

    new_id = new_page['id']
    print('new task created!')
    print(new_id)

else:
    print('there is already a project with this name')
    print(results[0]['id'])
