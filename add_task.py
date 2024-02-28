from notion_client import Client
import os
from datetime import date
import datetime
import sys
import json

import setup.setup as setup
from setup import project_db_setup as project
from setup import task_db_setup as task

notion_token = setup.notion_token
tasks_database = task.tasks_database
projects_database = project.projects_database

os.environ['notion_token'] = notion_token
notion = Client(auth=os.environ['notion_token'])

print("enter task name")
entry_name = input()
print("enter status (hit enter for default value)")
entry_status = input()
print("enter due date (hit enter for today's date)")
entry_date = input()
print("enter parent project name")
entry_main_project = input()

if (entry_status == ""):
    entry_status = task.status_select_default_value

if (entry_date == ""):
    entry_date = str(date.today())

formattedDate = datetime.datetime.strptime(entry_date, '%Y-%m-%d').strftime('%A')

project_query = notion.databases.query(
    **{
        "database_id": projects_database,
        "filter": {
            "and": [
                {
                    "property": project.title,
                    "title": {
                        "contains": entry_main_project,
                    }
                },
            ]
        }
    }
)

try:
    project_id = project_query['results'][0]['id']
except:
    print('there was no project found from the query using your project name')

properties = {
    task.title: {
        "title": [
            {
                "text": {
                    "content": entry_name
                }
            }
        ]
    },
    task.status_select: {
        "select": {
            "name": entry_status
        }
    },
    task.date: {
        "date": {
            "start": entry_date
        }
    }, 
    task.day_select: {
        "select": {
            "name": formattedDate
        }
    },
    task.projects_db_relation: {
        "relation": [
            {
                "id": project_id
            }
        ]
    }
}

my_page = notion.databases.query(
    **{
        "database_id": tasks_database,
        "filter": {
            "and": [
                {
                    "property": task.title,
                    "title": {
                        "contains": entry_name
                    }
                },
                {
                    "property": task.projects_db_relation,
                    "relation": {
                        "contains": project_id
                    }
                }
            ]
        }
    }
)

results = my_page['results']

if (results == []):
    new_page = notion.pages.create(
        **{
            'parent': {
                'database_id': tasks_database,
            },
            'properties': properties
        })

    new_id = new_page['id']
    print('new task created!')
    print(new_id)

else:
    print('there is already a task with this name')
    print(results[0]['id'])
