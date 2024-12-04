# TDL
Manage your to do list in one place.

This project is a Task Management API built using Flask and SQLite that allows users to create, read, update, and delete (CRUD) tasks. The application provides endpoints to manage tasks with properties such as title and status. The status of each task can be updated, and new tasks can be added. The tasks are stored in an SQLite database, and the API exposes these functionalities as HTTP endpoints that can be tested with tools like Postman.


If you wish to clone the repository, you need to run the database creation command in your local environment to recreate the database using this python code:

from app import db
db.create_all()
