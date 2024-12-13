import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import datetime

tasks = []

def add_task_ui():
    def add_task():
        try:
            name = task_name_entry.get()
            selected_date = calendar.get_date()
            selected_hour = int(hour_var.get())
            selected_minute = int(minute_var.get())
            selected_period = period_var.get()

            time = f"{selected_hour:02d}:{selected_minute:02d} {selected_period}"
            deadline = datetime.datetime.strptime(f"{selected_date} {time}", "%m/%d/%Y %I:%M %p")

            tasks.append({"name": name, "priority": selected_priority.get(), "deadline": deadline, "completed": False})
            tasks.sort(key=lambda x: (x["priority"], x["deadline"])) 
            messagebox.showinfo("Success", "Task added successfully!")
            add_task_window.destroy()
        except ValueError:
            messagebox.showerror(
                "Invalid Time Entry", 
                "The time you entered is invalid. Please make sure you enter a valid time."
            )

    add_task_window = tk.Toplevel(root)
    add_task_window.title("Add Task")
    add_task_window.geometry("400x600")
    add_task_window.resizable(False, False)  
    add_task_window.config(bg="#dceff7") 

    tk.Label(add_task_window, text="Add Task", font=("Arial", 18, "bold"), bg="#dceff7", fg="#333").pack(pady=(10, 20))

    frame_task_name = tk.Frame(add_task_window, bg="#dceff7") 
    frame_task_name.pack(pady=10)
    tk.Label(frame_task_name, text="Task Name:", font=("Arial", 12), bg="#dceff7").grid(row=0, column=0, sticky="w", padx=10)
    task_name_entry = tk.Entry(frame_task_name, width=30, font=("Arial", 12))
    task_name_entry.grid(row=0, column=1, padx=10, pady=5)

    frame_priority = tk.Frame(add_task_window, bg="#dceff7") 
    frame_priority.pack(pady=10)
    tk.Label(frame_priority, text="Priority:", font=("Arial", 12), bg="#dceff7").grid(row=0, column=0, sticky="w", padx=10)

    selected_priority = tk.StringVar(value="Medium")  

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

    frame_deadline = tk.Frame(add_task_window, bg="#dceff7") 
    frame_deadline.pack(pady=10)
    tk.Label(frame_deadline, text="Deadline:", font=("Arial", 12), bg="#dceff7").grid(row=0, column=0, sticky="w", padx=10)
    calendar = Calendar(frame_deadline, date_pattern="mm/dd/yyyy")
    calendar.grid(row=0, column=1, padx=10, pady=10)

    time_frame = tk.Frame(add_task_window, bg="#dceff7")
    time_frame.pack(pady=10)

    tk.Label(time_frame, text="Time:", font=("Arial", 12), bg="#dceff7").grid(row=0, column=0, sticky="w", padx=10)

    hour_var = tk.StringVar(value="12")
    minute_var = tk.StringVar(value="00")  
    period_var = tk.StringVar(value="AM")

    hour_spinbox = tk.Spinbox(
        time_frame,
        from_=1,
        to=12,
        textvariable=hour_var,
        format="%02.0f", 
        width=5,
        font=("Arial", 10),
    )
    hour_spinbox.grid(row=0, column=1, padx=5)

    tk.Label(time_frame, text=":", font=("Arial", 12), bg="#dceff7").grid(row=0, column=2)

    minute_spinbox = tk.Spinbox(
        time_frame,
        from_=0,
        to=59,
        textvariable=minute_var,
        format="%02.0f", 
        width=5,
        font=("Arial", 10),
    )
    minute_spinbox.grid(row=0, column=3, padx=5)

    tk.OptionMenu(time_frame, period_var, "AM", "PM").grid(row=0, column=4, padx=10)
    
    tk.Button(add_task_window, text="Add Task", command=add_task, bg="#007BFF", fg="white", font=("Arial", 14), width=15).pack(pady=30)

    tk.Label(add_task_window, text="Fill out the task details and click 'Add Task'.", font=("Arial", 10), bg="#dceff7", fg="#555").pack(pady=(0, 20))


reminder_window = None

def check_reminders_ui():
    global reminder_window

    if reminder_window is not None and reminder_window.winfo_exists():
        reminder_window.deiconify()  
        return

    reminder_window = tk.Toplevel(root)
    reminder_window.title("Reminders")
    reminder_window.geometry("800x400") 
    reminder_window.resizable(False, False)
    reminder_window.config(bg="#f4f4f4")

    tk.Label(reminder_window, text="Shishable Reminder", font=("Poppins", 16, "bold"), bg="#f4f4f4", fg="#333").pack(pady=10)

    canvas = tk.Canvas(reminder_window, bg="#f4f4f4")
    scrollbar = tk.Scrollbar(reminder_window, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    reminder_frame = tk.Frame(canvas, bg="#f4f4f4")

    canvas.create_window((0, 0), window=reminder_frame, anchor="nw")
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def update_reminders():
        now = datetime.datetime.now()
        reminder_texts = {"Pending": [], "Due": [], "Overdue": []} 

        for task in tasks:
            if not task["completed"]:
                time_left = task["deadline"] - now
                if time_left.total_seconds() <= 0:  
                    task["status"] = "Overdue"
                    reminder_texts["Overdue"].append((task["name"], task["priority"], task["status"], None, task["deadline"], task))
                elif time_left.total_seconds() <= 60:  
                    task["status"] = "Due"
                    reminder_texts["Due"].append((task["name"], task["priority"], task["status"], time_left, task["deadline"], task))
                else:  
                    task["status"] = "Pending"
                    reminder_texts["Pending"].append((task["name"], task["priority"], task["status"], time_left, task["deadline"], task))

        for widget in reminder_frame.winfo_children():
            widget.destroy()

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

        for status in ["Pending", "Due", "Overdue"]:
            if status == "Pending" and reminder_texts["Pending"]:
                tk.Label(reminder_frame, text="Pending Tasks", bg="#e9f7ef", font=("Poppins", 14, "bold"), anchor="w").pack(fill="x", pady=5)
                tk.Frame(reminder_frame, height=2, bg="#008000").pack(fill="x", pady=2) 
            elif status == "Due" and reminder_texts["Due"]:
                tk.Label(reminder_frame, text="Due Tasks", bg="#ffeb3b", font=("Poppins", 14, "bold"), anchor="w").pack(fill="x", pady=5)
                tk.Frame(reminder_frame, height=2, bg="#FFA500").pack(fill="x", pady=2)  
            elif status == "Overdue" and reminder_texts["Overdue"]:
                tk.Label(reminder_frame, text="Overdue Tasks", bg="#d3d3d3", font=("Poppins", 14, "bold"), anchor="w").pack(fill="x", pady=5)
                tk.Frame(reminder_frame, height=2, bg="#FF0000").pack(fill="x", pady=2)  

            if status == "Pending":
                reminder_texts["Pending"].sort(key=lambda x: (x[1], x[4]))  
            elif status == "Due":
                reminder_texts["Due"].sort(key=lambda x: (x[1], x[4])) 
            else:
                reminder_texts["Overdue"].sort(key=lambda x: x[4])     

            for name, priority, status, time_left, deadline, task in reminder_texts[status]:
                time_left_str = str(time_left).split(".")[0] 
                deadline_str = deadline.strftime("%b. %d, %Y %I:%M %p")  

                task_text = f"{name} | Time left: {time_left_str} | Deadline: {deadline_str}"

                task_frame = tk.Frame(reminder_frame, bg="#e0e0e0")  

                task_label = tk.Label(
                    task_frame,
                    text=task_text,
                    anchor="w",
                    bg="#e0e0e0",  
                    font=("Arial", 10),
                    fg="black",  
                    width=60  
                )

                priority_label = tk.Label(
                    task_frame,
                    text=f"Priority: {priority}",
                    anchor="w",
                    bg="#e0e0e0",  
                    font=("Arial", 10),
                    fg={"High": "#FF0000", "Medium": "#FFA500", "Low": "#008000"}.get(priority, "black"),
                )

                task_label.pack(side="left", fill="x", padx=10, pady=2)
                priority_label.pack(side="left", padx=10, pady=2)  

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

        reminder_frame.update_idletasks() 
        canvas.config(scrollregion=canvas.bbox("all"))

        reminder_window.after(1000, update_reminders)

    def mark_as_complete(task):
        task["completed"] = True  
        messagebox.showinfo("Task Completed", f"Task '{task['name']}' has been marked as completed.")
    
    def on_close():
        global reminder_window
        reminder_window.destroy() 
        reminder_window = None  

    reminder_window.protocol("WM_DELETE_WINDOW", on_close)

    update_reminders()

completed_task_window = None

def view_completed_tasks():
    global completed_task_window

    if completed_task_window is not None and completed_task_window.winfo_exists():
        completed_task_window.destroy()  
        completed_task_window = None

    completed_tasks = [task for task in tasks if task["completed"]]  
    if not completed_tasks:
        messagebox.showinfo("No Completed Tasks", "There are no completed tasks yet.")
        return

    completed_task_window = tk.Toplevel(root)
    completed_task_window.title("Completed Tasks")
    completed_task_window.geometry("500x300")
    completed_task_window.config(bg="#dceff7")  
    completed_task_window.resizable(False, False)  

    canvas = tk.Canvas(completed_task_window, bg="#dceff7")
    scrollbar = tk.Scrollbar(completed_task_window, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    completed_task_frame = tk.Frame(canvas, bg="#dceff7")

    canvas.create_window((0, 0), window=completed_task_frame, anchor="nw")

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    tk.Label(completed_task_frame, text="Completed Tasks", font=("Arial", 16, "bold"), anchor="center", bg="#dceff7", fg="#333").pack(pady=10, fill="x")

    for task in completed_tasks:
        task_frame = tk.Frame(completed_task_frame, bg="#dceff7", relief="raised", padx=10, pady=5)
        task_frame.pack(fill="x", pady=5)

        task_label = tk.Label(
            task_frame,
            text=f"Task: {task['name']} | Deadline: {task['deadline'].strftime('%b %d, %Y %I:%M %p')}",
            anchor="w",
            bg="#dceff7", 
            font=("Arial", 12),
            fg="black",  
            width=40, 
            wraplength=360 
        )
        
        task_label.pack(side="left", fill="x") 

        trash_icon = tk.Label(task_frame, text="🗑", font=("Arial", 14), fg="red", cursor="hand2", bg="#dceff7")
        trash_icon.pack(side="right", padx=80) 

        trash_icon.bind("<Button-1>", lambda event, task=task: delete_task_from_completed(task))

        def on_enter(event, label=trash_icon):
            label.config(fg="darkred")  

        def on_leave(event, label=trash_icon):
            label.config(fg="red")  

        trash_icon.bind("<Enter>", on_enter) 
        trash_icon.bind("<Leave>", on_leave) 

    completed_task_frame.update_idletasks()  
    canvas.config(scrollregion=canvas.bbox("all"))

    def on_close():
        global completed_task_window
        completed_task_window.destroy() 
        completed_task_window = None  

    completed_task_window.protocol("WM_DELETE_WINDOW", on_close)

def delete_task_from_completed(task):
    """Delete a task from the global list and refresh the completed tasks window."""
    tasks.remove(task) 
    view_completed_tasks()  
    messagebox.showinfo("Task Deleted", f"Task '{task['name']}' has been deleted.")

root = tk.Tk()
root.resizable(False, False)  
root.title("SHISH: Simple Handy Intelligent Schedule Helper")
root.geometry("300x350") 
root.config(bg="#dceff7") 

tk.Label(root, text="SHISH", font=("Baloo", 28, "bold"), bg="#dceff7", fg="#607D8B").pack(pady=20)

tk.Button(root, text="Add Task", command=add_task_ui, bg="#007BFF", fg="white", font=("Arial", 14), width=20).pack(pady=10)
tk.Button(root, text="Check Reminders", command=check_reminders_ui, bg="#28a745", fg="white", font=("Arial", 14), width=20).pack(pady=10)
tk.Button(root, text="View Completed Tasks", command=view_completed_tasks, bg="#FFC107", fg="black", font=("Arial", 14), width=20).pack(pady=10)

root.mainloop()
