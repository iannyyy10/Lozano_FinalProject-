import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import datetime

# List to store tasks
tasks = []

def add_task_ui():
    def add_task():
        try:
            name = task_name_entry.get()
            selected_date = calendar.get_date()
            selected_hour = int(hour_var.get())
            selected_minute = int(minute_var.get())
            selected_period = period_var.get()

            # Combine date and time
            time = f"{selected_hour:02d}:{selected_minute:02d} {selected_period}"
            deadline = datetime.datetime.strptime(f"{selected_date} {time}", "%m/%d/%Y %I:%M %p")

            tasks.append({"name": name, "priority": selected_priority.get(), "deadline": deadline, "completed": False})
            tasks.sort(key=lambda x: (x["priority"], x["deadline"]))  # Sort by priority and deadline
            messagebox.showinfo("Success", "Task added successfully!")
            add_task_window.destroy()
        except ValueError:
            messagebox.showerror(
                "Invalid Time Entry", 
                "The time you entered is invalid. Please make sure you enter a valid time."
            )

    # Create Add Task Window
    add_task_window = tk.Toplevel(root)
    add_task_window.title("Add Task")
    add_task_window.geometry("400x600")
    add_task_window.resizable(False, False)  # Disable maximize for this window
    add_task_window.config(bg="#dceff7")  # Light blue background

    # Title
    tk.Label(add_task_window, text="Add Task", font=("Arial", 18, "bold"), bg="#dceff7", fg="#333").pack(pady=(10, 20))

    # Task Name Section
    frame_task_name = tk.Frame(add_task_window, bg="#dceff7")  # Use the same background color as the window
    frame_task_name.pack(pady=10)
    tk.Label(frame_task_name, text="Task Name:", font=("Arial", 12), bg="#dceff7").grid(row=0, column=0, sticky="w", padx=10)
    task_name_entry = tk.Entry(frame_task_name, width=30, font=("Arial", 12))
    task_name_entry.grid(row=0, column=1, padx=10, pady=5)

    frame_priority = tk.Frame(add_task_window, bg="#dceff7")  # Same background color
    frame_priority.pack(pady=10)
    tk.Label(frame_priority, text="Priority:", font=("Arial", 12), bg="#dceff7").grid(row=0, column=0, sticky="w", padx=10)

    # Variable to store selected priority
    selected_priority = tk.StringVar(value="Medium")  # Default is Medium

    # Create priority buttons with dynamic color updates
    priority_colors = {"High": "#FF0000", "Medium": "#FFA500", "Low": "#008000"}
    buttons = {}

    def select_priority(priority):
        selected_priority.set(priority)
        for prio, button in buttons.items():
            if prio == priority:
                button.config(relief="sunken", bg=priority_colors[priority], fg="white")
            else:
                button.config(relief="raised", bg=priority_colors[prio], fg="white")

    priorities_order = ["Low", "Medium", "High"]

    for idx, priority in enumerate(priorities_order):
        button = tk.Button(
            frame_priority,
            text=priority,
            bg=priority_colors[priority],
            fg="white",
            font=("Arial", 10),
            width=10,
            command=lambda p=priority: select_priority(p),
        )
        button.grid(row=0, column=idx + 1, padx=5)
        buttons[priority] = button

    # Deadline Section
    frame_deadline = tk.Frame(add_task_window, bg="#dceff7")  # Same background color
    frame_deadline.pack(pady=10)
    tk.Label(frame_deadline, text="Deadline:", font=("Arial", 12), bg="#dceff7").grid(row=0, column=0, sticky="w", padx=10)
    calendar = Calendar(frame_deadline, date_pattern="mm/dd/yyyy")
    calendar.grid(row=0, column=1, padx=10, pady=10)

    # Time Selection
    time_frame = tk.Frame(add_task_window, bg="#dceff7")  # Same background color
    time_frame.pack(pady=10)

    tk.Label(time_frame, text="Time:", font=("Arial", 12), bg="#dceff7").grid(row=0, column=0, sticky="w", padx=10)

    hour_var = tk.StringVar(value="12")
    minute_var = tk.StringVar(value="00")  # Default to 00
    period_var = tk.StringVar(value="AM")

    # Hour Spinbox with leading zero
    hour_spinbox = tk.Spinbox(
        time_frame,
        from_=1,
        to=12,
        textvariable=hour_var,
        format="%02.0f",  # Display two digits
        width=5,
        font=("Arial", 10),
    )
    hour_spinbox.grid(row=0, column=1, padx=5)

    tk.Label(time_frame, text=":", font=("Arial", 12), bg="#dceff7").grid(row=0, column=2)

    # Minute Spinbox with leading zero
    minute_spinbox = tk.Spinbox(
        time_frame,
        from_=0,
        to=59,
        textvariable=minute_var,
        format="%02.0f",  # Display two digits
        width=5,
        font=("Arial", 10),
    )
    minute_spinbox.grid(row=0, column=3, padx=5)

    tk.OptionMenu(time_frame, period_var, "AM", "PM").grid(row=0, column=4, padx=10)
    
    # Add Task Button
    tk.Button(add_task_window, text="Add Task", command=add_task, bg="#007BFF", fg="white", font=("Arial", 14), width=15).pack(pady=30)

    # Adjust spacing for overall clarity
    tk.Label(add_task_window, text="Fill out the task details and click 'Add Task'.", font=("Arial", 10), bg="#dceff7", fg="#555").pack(pady=(0, 20))


    # Global variable to track the reminders window
reminder_window = None

# For check reminder
def check_reminders_ui():
    global reminder_window

    # Check if the window already exists and is open
    if reminder_window is not None and reminder_window.winfo_exists():
        reminder_window.deiconify()  # Bring the existing window to the front
        return

    # Create Check Reminders Window
    reminder_window = tk.Toplevel(root)
    reminder_window.title("Reminders")
    reminder_window.geometry("800x400")  # Increased width for better layout
    reminder_window.resizable(False, False)  # Disable maximize for this window
    reminder_window.config(bg="#f4f4f4")

    tk.Label(reminder_window, text="Shishable Reminder", font=("Poppins", 16, "bold"), bg="#f4f4f4", fg="#333").pack(pady=10)

    # Create a canvas widget and a scrollbar
    canvas = tk.Canvas(reminder_window, bg="#f4f4f4")
    scrollbar = tk.Scrollbar(reminder_window, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Frame inside the canvas where tasks will be displayed
    reminder_frame = tk.Frame(canvas, bg="#f4f4f4")

    # Create a window inside the canvas to display the reminder frame
    canvas.create_window((0, 0), window=reminder_frame, anchor="nw")
    
    # Place the canvas and scrollbar in the window
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def update_reminders():
        now = datetime.datetime.now()
        reminder_texts = {"Pending": [], "Due": [], "Overdue": []}  # Separate dictionaries for each task status

        # Categorize tasks by their status: Pending, Due, Overdue
        for task in tasks:
            if not task["completed"]:
                time_left = task["deadline"] - now
                if time_left.total_seconds() <= 0:  # Task time has run out (overdue)
                    task["status"] = "Overdue"
                    reminder_texts["Overdue"].append((task["name"], task["priority"], task["status"], None, task["deadline"], task))
                elif time_left.total_seconds() <= 60:  # Task is due now
                    task["status"] = "Due"
                    reminder_texts["Due"].append((task["name"], task["priority"], task["status"], time_left, task["deadline"], task))
                else:  # Task is still pending
                    task["status"] = "Pending"
                    reminder_texts["Pending"].append((task["name"], task["priority"], task["status"], time_left, task["deadline"], task))

        # Clear previous reminders
        for widget in reminder_frame.winfo_children():
            widget.destroy()

        # If there are no upcoming or pending tasks, display the "No upcoming tasks" label
        if not any(reminder_texts["Pending"]) and not any(reminder_texts["Due"]):
            no_upcoming_task_label = tk.Label(
                reminder_frame,
                text="No upcoming tasks or reminders.",
                anchor="w",
                bg="#fbe4e4",
                font=("Quicksand", 12),
                fg="#555"
            )
            no_upcoming_task_label.pack(fill="x", pady=10)

        # Sort and display tasks: Pending -> Due -> Overdue
        for status in ["Pending", "Due", "Overdue"]:
            # Add section labels and separators
            if status == "Pending" and reminder_texts["Pending"]:
                tk.Label(reminder_frame, text="Pending Tasks", bg="#e9f7ef", font=("Poppins", 14, "bold"), anchor="w").pack(fill="x", pady=5)
                tk.Frame(reminder_frame, height=2, bg="#008000").pack(fill="x", pady=2)  # Green separator line
            elif status == "Due" and reminder_texts["Due"]:
                tk.Label(reminder_frame, text="Due Tasks", bg="#ffeb3b", font=("Poppins", 14, "bold"), anchor="w").pack(fill="x", pady=5)
                tk.Frame(reminder_frame, height=2, bg="#FFA500").pack(fill="x", pady=2)  # Yellow separator line
            elif status == "Overdue" and reminder_texts["Overdue"]:
                tk.Label(reminder_frame, text="Overdue Tasks", bg="#d3d3d3", font=("Poppins", 14, "bold"), anchor="w").pack(fill="x", pady=5)
                tk.Frame(reminder_frame, height=2, bg="#FF0000").pack(fill="x", pady=2)  # Red separator line

            # Sort tasks within each category by priority first, then by deadline
            if status == "Pending":
                reminder_texts["Pending"].sort(key=lambda x: (x[1], x[4]))  # Sort by priority and deadline
            elif status == "Due":
                reminder_texts["Due"].sort(key=lambda x: (x[1], x[4]))  # Sort by priority and deadline
            else:
                reminder_texts["Overdue"].sort(key=lambda x: x[4])  # Sort overdue tasks by deadline    

            # Display tasks in the respective status category
            for name, priority, status, time_left, deadline, task in reminder_texts[status]:
                time_left_str = str(time_left).split(".")[0]  # Removing microseconds for clarity
                deadline_str = deadline.strftime("%b. %d, %Y %I:%M %p")  # Month abbreviation, day, year, time

                # Prepare task text with colored priority
                task_text = f"{name} | Time left: {time_left_str} | Deadline: {deadline_str}"

                # Create a frame to hold both task text and priority side by side
                task_frame = tk.Frame(reminder_frame, bg="#e0e0e0")  # Darker gray background for each task frame

                task_label = tk.Label(
                    task_frame,
                    text=task_text,
                    anchor="w",
                    bg="#e0e0e0",  # Darker gray background for each task
                    font=("Arial", 10),
                    fg="black",  # Text color to contrast with background
                    width=60  # Adjusted width for better visibility
                )

                priority_label = tk.Label(
                    task_frame,
                    text=f"Priority: {priority}",
                    anchor="w",
                    bg="#e0e0e0",  # Darker gray background for priority as well
                    font=("Arial", 10),
                    fg={"High": "#FF0000", "Medium": "#FFA500", "Low": "#008000"}.get(priority, "black"),
                )

                task_label.pack(side="left", fill="x", padx=10, pady=2)
                priority_label.pack(side="left", padx=10, pady=2)  # Priority moved to the left

                # Mark as complete button moved to the right
                complete_button = tk.Button(
                    task_frame,
                    text="Mark as Complete",
                    bg="#28a745",
                    fg="white",
                    font=("Arial", 10),
                    command=lambda t=task: mark_as_complete(t)
                )
                complete_button.pack(side="right", padx=10, pady=2)

                task_frame.pack(fill="x", pady=5)

        # Update the scroll region of the canvas
        reminder_frame.update_idletasks()  # Make sure the frame's size is updated
        canvas.config(scrollregion=canvas.bbox("all"))

        # Call update_reminders every second
        reminder_window.after(1000, update_reminders)

    def mark_as_complete(task):
        task["completed"] = True  # Simply mark as complete, don't remove from tasks list
        messagebox.showinfo("Task Completed", f"Task '{task['name']}' has been marked as completed.")
    
    # When the window is closed, reset the variable
    def on_close():
        global reminder_window
        reminder_window.destroy()  # Destroy the window
        reminder_window = None  # Reset the variable

    reminder_window.protocol("WM_DELETE_WINDOW", on_close)

    update_reminders()

# New button to view completed tasks
# Global variable to track the completed tasks window
completed_task_window = None

def view_completed_tasks():
    global completed_task_window

    # Check if the window already exists and is open
    if completed_task_window is not None and completed_task_window.winfo_exists():
        completed_task_window.destroy()  # Destroy the existing window to refresh
        completed_task_window = None

    # Filter completed tasks
    completed_tasks = [task for task in tasks if task["completed"]]  
    if not completed_tasks:
        messagebox.showinfo("No Completed Tasks", "There are no completed tasks yet.")
        return

    # Create a new window for completed tasks
    completed_task_window = tk.Toplevel(root)
    completed_task_window.title("Completed Tasks")
    completed_task_window.geometry("500x300")
    completed_task_window.config(bg="#dceff7")  # Set background color similar to main window
    completed_task_window.resizable(False, False)  # Disable maximize for this window

    # Create a canvas widget and a scrollbar
    canvas = tk.Canvas(completed_task_window, bg="#dceff7")
    scrollbar = tk.Scrollbar(completed_task_window, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Frame inside the canvas where tasks will be displayed
    completed_task_frame = tk.Frame(canvas, bg="#dceff7")

    # Create a window inside the canvas to display the task frame
    canvas.create_window((0, 0), window=completed_task_frame, anchor="nw")

    # Place the canvas and scrollbar in the window
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Add a title label with a custom font
    tk.Label(completed_task_frame, text="Completed Tasks", font=("Arial", 16, "bold"), anchor="center", bg="#dceff7", fg="#333").pack(pady=10, fill="x")

    # Loop through completed tasks and display them with a custom background color
    for task in completed_tasks:
        task_frame = tk.Frame(completed_task_frame, bg="#dceff7", relief="raised", padx=10, pady=5)
        task_frame.pack(fill="x", pady=5)

        task_label = tk.Label(
            task_frame,
            text=f"Task: {task['name']} | Deadline: {task['deadline'].strftime('%b %d, %Y %I:%M %p')}",
            anchor="w",
            bg="#dceff7",  # Same background color as window but still distinguishable
            font=("Arial", 12),
            fg="black",  # Text color
            width=40,  # Set the width for the task label
            wraplength=360  # Allow wrapping text within the label
        )
        
        task_label.pack(side="left", fill="x")  # Text aligned to the left

        # Trash can icon to delete the task
        trash_icon = tk.Label(task_frame, text="🗑", font=("Arial", 14), fg="red", cursor="hand2", bg="#dceff7")
        trash_icon.pack(side="right", padx=80)  # Move it to the right with some padding

        # Bind the trash icon to the delete task function
        trash_icon.bind("<Button-1>", lambda event, task=task: delete_task_from_completed(task))

        # Change appearance on hover to enhance button-like feel
        def on_enter(event, label=trash_icon):
            label.config(fg="darkred")  # Darker red when hovered

        def on_leave(event, label=trash_icon):
            label.config(fg="red")  # Revert to original color

        trash_icon.bind("<Enter>", on_enter)  # Change color on hover
        trash_icon.bind("<Leave>", on_leave)  # Revert color when hover ends

    # Update the scroll region of the canvas
    completed_task_frame.update_idletasks()  # Make sure the frame's size is updated
    canvas.config(scrollregion=canvas.bbox("all"))

    # When the window is closed, reset the variable
    def on_close():
        global completed_task_window
        completed_task_window.destroy()  # Destroy the window
        completed_task_window = None  # Reset the variable

    completed_task_window.protocol("WM_DELETE_WINDOW", on_close)

def delete_task_from_completed(task):
    """Delete a task from the global list and refresh the completed tasks window."""
    tasks.remove(task)  # Remove the task from the global task list
    view_completed_tasks()  # Refresh the completed task window
    messagebox.showinfo("Task Deleted", f"Task '{task['name']}' has been deleted.")

# Main Tkinter UI
root = tk.Tk()
root.resizable(False, False)  # Disable maximize for the main window
root.title("SHISH: Simple Handy Intelligent Schedule Helper")
root.geometry("300x350")  # Smaller main window size
root.config(bg="#dceff7")  # Apply the selected background color

tk.Label(root, text="SHISH", font=("Baloo", 28, "bold"), bg="#dceff7", fg="#607D8B").pack(pady=20)

tk.Button(root, text="Add Task", command=add_task_ui, bg="#007BFF", fg="white", font=("Arial", 14), width=20).pack(pady=10)
tk.Button(root, text="Check Reminders", command=check_reminders_ui, bg="#28a745", fg="white", font=("Arial", 14), width=20).pack(pady=10)
tk.Button(root, text="View Completed Tasks", command=view_completed_tasks, bg="#FFC107", fg="black", font=("Arial", 14), width=20).pack(pady=10)

root.mainloop()