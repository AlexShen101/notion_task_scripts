
## About
This project is deprecated since the Notion API has undergone significant updates since the script's development. While the script functionalities might not work as intended, this repository serves as a reference for those interested in building similar tools. 
The initial purpose was to provide students and professionals with a Notion task manager, adding functionality to their existing Notion setups. 

This project offered scripts for:
- Quickly adding tasks: Streamline task creation within your Notion workflow.
- Quickly adding projects: Simplify project creation and organization.
- Adding dates to undated tasks: Enhance task management by ensuring all tasks have due dates.

This project was designed to be used in conjunction with automation tools like Keyboard Maestro or AutoHotkey. These tools allow you to create custom workflows, enabling you to trigger relevant Python scripts with keyboard shortcuts or other triggers.


Here is an image of what notion tables are required, and what a working system would look like.
![image](https://github.com/AlexShen101/notion_task_scripts/assets/85968705/ddf73638-afcd-4a05-b040-716e3b63d6fe)

## Built With
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

## Getting Started (For Informational Purposes Only)
Note: Due to API updates, the following instructions might not result in a fully functional application. They are provided for reference purposes only.
- Install dependencies: Run `pip install -r requirements.txt` in your terminal.
- Set up Notion pages: Create three Notion pages:
  - Master Projects Database
  - Projects Database
  - Tasks Database
- Obtain database IDs: Retrieve the unique IDs for each Notion database and place them in the corresponding configuration files within the "setup" folder.
- Acquire Notion developer key: Generate a developer key from the Notion API and add it to the "setup.py" file within the "setup" folder.
