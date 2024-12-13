# Lozano_FinalProject
Overview

This project is a Task Manager Application built using Python's Tkinter library. It allows users to add, view, manage, and track tasks with the following features:

Add Tasks: Create tasks with a name, priority (High, Medium, Low), and a deadline including date and time.

View Reminders: See tasks categorized as pending, due, or overdue.

Mark as Complete: Mark tasks as completed.

View Completed Tasks: Track and delete tasks marked as complete.

Features

Interactive UI: Built using Tkinter for a user-friendly interface.

Calendar Integration: Uses the tkcalendar module for date selection.

Task Priority: Tasks can be assigned priorities (High, Medium, Low) which determine their sorting.

Real-Time Reminders: Tasks are categorized based on their current status (Pending, Due, Overdue) with automatic updates.

Requirements

Python 3.x

Required Python libraries:

tkinter (Standard library for GUI)

tkcalendar (Install using pip install tkcalendar)

Installation

Clone or download the repository.

Ensure Python 3.x is installed on your machine.

Install the tkcalendar library:

pip install tkcalendar

Run the program:

python <filename>.py

Usage

Adding a Task

Click the "Add Task" button in the main application window.

Enter the task details:

Task Name

Priority: Select between High, Medium, or Low.

Deadline: Select the date from the calendar and set the time.

Click the "Add Task" button to save the task.

Viewing Reminders

Click the "Check Reminders" button to open the reminders window.

Tasks are categorized as:

Pending: Tasks with time remaining.

Due: Tasks due within the next 60 seconds.

Overdue: Tasks past their deadline.

Marking Tasks as Complete

In the reminders window, find the task you want to complete.

Click the "Mark as Complete" button next to the task.

Viewing Completed Tasks

Click the "View Completed Tasks" button.

Completed tasks are listed in a separate window with options to delete them.

Code Overview

Core Components

Add Task UI:

Creates a popup window for entering task details.

Combines date and time into a deadline using datetime.

Reminder System:

Categorizes tasks into Pending, Due, and Overdue.

Updates reminders in real-time using after method in Tkinter.

Completed Tasks:

Tracks tasks marked as complete.

Provides options to view and delete completed tasks.

Key Libraries

Tkinter: For GUI elements such as windows, buttons, and labels.

Tkcalendar: For date selection in the task deadline.

Datetime: To handle deadlines and calculate task status.

Future Enhancements

Notifications: Add desktop notifications for reminders.

Data Persistence: Save tasks to a file or database for retrieval after restarting the app.

Search and Filter: Allow users to search or filter tasks by name, priority, or status.

Theme Customization: Add options for customizing the application's appearance.
