# Python To-Do List Application

A simple yet powerful to-do list application built with Python and Tkinter.

## Features

- Add new tasks with priority levels (Low, Medium, High)
- Mark tasks as complete/incomplete
- Edit existing tasks
- Delete tasks
- Tasks are color-coded based on priority and completion status
- Persistent storage (tasks are saved to a JSON file)
- Clean and intuitive graphical user interface

## Installation

1. Ensure you have Python 3.6 or higher installed on your system
2. Download or clone this repository
3. No additional dependencies are required (uses only standard library modules)

## Usage

1. Run the application:
python todo_app.py


2. To add a task:
- Type your task in the input field
- Select a priority level (default is Medium)
- Press Enter or click the "Add Task" button

3. To modify a task:
- Select a task from the list
- Use the appropriate button:
  - "Mark Complete": Toggle completion status
  - "Edit": Modify the task text or priority
  - "Delete": Remove the task (with confirmation)

## Data Storage

Tasks are automatically saved to a `tasks.json` file in the same directory as the application. This file will be created automatically when you add your first task.

## Keyboard Shortcuts

- Enter: Add a new task
- Mouse click: Select a task for operations

## Customization

You can modify the application by editing the source code:

- Change colors and styling in the `update_task_list()` method
- Modify the window size in the `__init__` method
- Adjust the task data structure in the `add_task()` method

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
