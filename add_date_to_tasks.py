from notion_client import Client
import os
import datetime

import setup.setup as setup
import setup.task_db_setup as task_db_setup

notion_token = setup.notion_token
tasks_database_id = task_db_setup.tasks_database

os.environ['notion_token'] = notion_token
notion = Client(auth=os.environ['notion_token'])

# creates a new notion page and adds it to specified database
query = notion.databases.query(
    **{
        "database_id": tasks_database_id,
        "filter": {
            "and": [
                # example of a select property
                {
                    "property": task_db_setup.date,
                    "date": {
                        "is_not_empty": True,
                    }
                },
                {
                    "property": task_db_setup.day_select,
                    "select": {
                        "is_empty": True,
                    }
                },
            ]
        },
    }
)

tasks = query['results']

for task in tasks:
    task_id = task['id']
    date = task['properties'][task_db_setup.date]['date']['start']
    formattedDate = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%A')

    notion.pages.update(
        **{
            "page_id": task_id,
            "properties": {
                task_db_setup.day_select : {
                    "select": {
                        "name": formattedDate
                    }
                }
            }
        }
    )
