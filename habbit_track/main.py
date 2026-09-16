import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import json
import os
import threading
import time


# =========================================================
# FILE
# =========================================================

FILE_NAME = "habits.json"

habits_data = []


# =========================================================
# LOAD DATA FROM JSON
# =========================================================

def load_data():
    global habits_data

    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                habits_data = json.load(file)

        except:
            habits_data = []

    else:
        habits_data = []


# =========================================================
# SAVE DATA TO JSON
# =========================================================

def save_data():

    with open(FILE_NAME, "w") as file:
        json.dump(
            habits_data,
            file,
            indent=4
        )


# =========================================================
# CREATE TODAY'S RECURRING HABITS
# =========================================================

def create_today_habits():

    today = datetime.now().strftime("%Y-%m-%d")

    # Get unique habit names from previous records
    habit_names = set()

    for habit in habits_data:
        habit_names.add(habit["name"])

    # Create today's record if it doesn't exist
    for name in habit_names:

        already_exists = False

        for habit in habits_data:

            if (
                habit["name"] == name
                and
                habit["date"] == today
            ):
                already_exists = True
                break

        if not already_exists:

            previous_habit = None

            # Find latest record of this habit
            for habit in reversed(habits_data):

                if habit["name"] == name:
                    previous_habit = habit
                    break

            reminder = "18:00"

            if previous_habit:
                reminder = previous_habit.get(
                    "reminder",
                    "18:00"
                )

            new_habit = {
                "name": name,
                "completed": False,
                "reminder": reminder,
                "date": today
            }

            habits_data.append(
                new_habit
            )

    save_data()


# =========================================================
# SHOW TODAY'S HABITS
# =========================================================

def show_habits():

    habit_list.delete(
        0,
        tk.END
    )

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    today_habits = [
        habit
        for habit in habits_data
        if habit["date"] == today
    ]

    for habit in today_habits:

        if habit["completed"]:
            status = "✅"
        else:
            status = "⬜"

        reminder = habit.get(
            "reminder",
            "--:--"
        )

        habit_list.insert(
            tk.END,
            f"{status} {habit['name']}   ⏰ {reminder}"
        )

    update_progress()
    update_streak()


# =========================================================
# UPDATE DAILY PROGRESS
# =========================================================

def update_progress():

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    today_habits = [
        habit
        for habit in habits_data
        if habit["date"] == today
    ]

    total = len(today_habits)

    completed = sum(
        1
        for habit in today_habits
        if habit["completed"]
    )

    total_label.config(
        text=str(total)
    )

    completed_label.config(
        text=str(completed)
    )

    if total > 0:

        percentage = int(
            (completed / total) * 100
        )

    else:

        percentage = 0

    progress_label.config(
        text=f"Today's Progress: {percentage}%"
    )

    progress_bar.config(
        state="normal"
    )

    progress_bar.set(
        percentage
    )

    progress_bar.config(
        state="disabled"
    )


# =========================================================
# ADD HABIT
# =========================================================

def add_habit():

    name = habit_entry.get().strip()

    reminder = time_entry.get().strip()

    if name == "" or name == "Enter habit...":

        messagebox.showwarning(
            "Warning",
            "Please enter a habit."
        )

        return

    # Validate time

    try:

        datetime.strptime(
            reminder,
            "%H:%M"
        )

    except ValueError:

        messagebox.showwarning(
            "Invalid Time",
            "Please enter time in HH:MM format.\n\nExample: 18:30"
        )

        return

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    # Prevent duplicate habit for today

    for habit in habits_data:

        if (
            habit["name"].lower() == name.lower()
            and
            habit["date"] == today
        ):

            messagebox.showwarning(
                "Already Exists",
                "This habit is already added today."
            )

            return

    new_habit = {
        "name": name,
        "completed": False,
        "reminder": reminder,
        "date": today
    }

    habits_data.append(
        new_habit
    )

    save_data()

    habit_entry.delete(
        0,
        tk.END
    )

    show_habits()

    messagebox.showinfo(
        "Success",
        "Habit added successfully! 🎉"
    )


# =========================================================
# COMPLETE HABIT
# =========================================================

def complete_habit():

    selected = habit_list.curselection()

    if not selected:

        messagebox.showwarning(
            "Warning",
            "Please select a habit."
        )

        return

    index = selected[0]

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    today_habits = [
        habit
        for habit in habits_data
        if habit["date"] == today
    ]

    today_habits[index]["completed"] = True

    save_data()

    show_habits()


# =========================================================
# DELETE HABIT
# =========================================================

def delete_habit():

    selected = habit_list.curselection()

    if not selected:

        messagebox.showwarning(
            "Warning",
            "Please select a habit."
        )

        return

    index = selected[0]

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    today_habits = [
        habit
        for habit in habits_data
        if habit["date"] == today
    ]

    habit_to_delete = today_habits[index]

    confirm = messagebox.askyesno(
        "Delete Habit",
        f"Delete '{habit_to_delete['name']}'?"
    )

    if confirm:

        habits_data.remove(
            habit_to_delete
        )

        save_data()

        show_habits()


# =========================================================
# EDIT HABIT
# =========================================================

def edit_habit():

    selected = habit_list.curselection()

    if not selected:

        messagebox.showwarning(
            "Warning",
            "Please select a habit."
        )

        return

    index = selected[0]

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    today_habits = [
        habit
        for habit in habits_data
        if habit["date"] == today
    ]

    selected_habit = today_habits[index]

    # Edit window

    edit_window = tk.Toplevel(
        window
    )

    edit_window.title(
        "Edit Habit"
    )

    edit_window.geometry(
        "420x330"
    )

    edit_window.configure(
        bg="#f5f3ff"
    )

    edit_window.resizable(
        False,
        False
    )

    # Title

    tk.Label(
        edit_window,
        text="✏️ EDIT HABIT",
        font=("Arial", 20, "bold"),
        bg="#f5f3ff",
        fg="#5b21b6"
    ).pack(
        pady=20
    )

    # Habit name label

    tk.Label(
        edit_window,
        text="Habit Name",
        font=("Arial", 11, "bold"),
        bg="#f5f3ff"
    ).pack()

    # Habit name entry

    edit_name = tk.Entry(
        edit_window,
        width=30,
        font=("Arial", 12)
    )

    edit_name.pack(
        pady=8
    )

    edit_name.insert(
        0,
        selected_habit["name"]
    )

    # Reminder label

    tk.Label(
        edit_window,
        text="Reminder Time (HH:MM)",
        font=("Arial", 11, "bold"),
        bg="#f5f3ff"
    ).pack()

    # Reminder entry

    edit_time = tk.Entry(
        edit_window,
        width=15,
        font=("Arial", 12)
    )

    edit_time.pack(
        pady=8
    )

    edit_time.insert(
        0,
        selected_habit.get(
            "reminder",
            "18:00"
        )
    )

    # Save edit

    def save_edit():

        new_name = edit_name.get().strip()

        new_time = edit_time.get().strip()

        if new_name == "":

            messagebox.showwarning(
                "Warning",
                "Habit name cannot be empty."
            )

            return

        try:

            datetime.strptime(
                new_time,
                "%H:%M"
            )

        except ValueError:

            messagebox.showwarning(
                "Invalid Time",
                "Enter time like 18:30"
            )

            return

        selected_habit["name"] = new_name

        selected_habit["reminder"] = new_time

        save_data()

        show_habits()

        edit_window.destroy()

        messagebox.showinfo(
            "Updated",
            "Habit updated successfully! ✨"
        )

    tk.Button(
        edit_window,
        text="💾 Save Changes",
        command=save_edit,
        width=20,
        bg="#7c3aed",
        fg="white",
        font=("Arial", 11, "bold")
    ).pack(
        pady=20
    )


# =========================================================
# STREAK
# =========================================================

def update_streak():

    completed_dates = set()

    for habit in habits_data:

        if habit["completed"]:

            completed_dates.add(
                habit["date"]
            )

    streak = 0

    current_date = datetime.now().date()

    while True:

        date_string = current_date.strftime(
            "%Y-%m-%d"
        )

        if date_string in completed_dates:

            streak += 1

            current_date -= timedelta(
                days=1
            )

        else:

            break

    streak_label.config(
        text=f"🔥 Streak: {streak} days"
    )


# =========================================================
# SET REMINDER
# =========================================================

def set_reminder():

    selected = habit_list.curselection()

    if not selected:

        messagebox.showwarning(
            "Warning",
            "Please select a habit first."
        )

        return

    reminder = time_entry.get().strip()

    try:

        datetime.strptime(
            reminder,
            "%H:%M"
        )

    except ValueError:

        messagebox.showwarning(
            "Invalid Time",
            "Enter time like 18:30"
        )

        return

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    today_habits = [
        habit
        for habit in habits_data
        if habit["date"] == today
    ]

    index = selected[0]

    today_habits[index]["reminder"] = reminder

    save_data()

    show_habits()

    messagebox.showinfo(
        "Reminder Set",
        f"Reminder set for {reminder} ⏰"
    )


# =========================================================
# AUTOMATIC REMINDER CHECKER
# =========================================================

def reminder_checker():

    checked_reminders = set()

    while True:

        now = datetime.now()

        current_time = now.strftime(
            "%H:%M"
        )

        current_date = now.strftime(
            "%Y-%m-%d"
        )

        for habit in habits_data:

            if (
                habit["date"] == current_date
                and
                habit.get("reminder") == current_time
                and
                not habit["completed"]
            ):

                reminder_id = (
                    current_date,
                    habit["name"],
                    habit["reminder"]
                )

                if reminder_id not in checked_reminders:

                    checked_reminders.add(
                        reminder_id
                    )

                    window.after(
                        0,
                        lambda name=habit["name"],
                        reminder=habit["reminder"]:
                        show_reminder(
                            name,
                            reminder
                        )
                    )

        time.sleep(20)


# =========================================================
# SHOW REMINDER
# =========================================================

def show_reminder(
    name,
    reminder
):

    messagebox.showinfo(
        "⏰ Habit Reminder",
        f"Time: {reminder}\n\n"
        f"Don't forget your habit:\n\n"
        f"💜 {name}"
    )


# =========================================================
# WEEKLY VIEW
# =========================================================

def weekly_view():

    weekly_window = tk.Toplevel(
        window
    )

    weekly_window.title(
        "Weekly Habit Summary"
    )

    weekly_window.geometry(
        "700x620"
    )

    weekly_window.configure(
        bg="#f5f3ff"
    )

    # Title

    tk.Label(
        weekly_window,
        text="📅 WEEKLY HABIT SUMMARY",
        font=("Arial", 20, "bold"),
        bg="#f5f3ff",
        fg="#5b21b6"
    ).pack(
        pady=20
    )

    tk.Label(
        weekly_window,
        text="Your last 7 days performance",
        font=("Arial", 11),
        bg="#f5f3ff",
        fg="#555555"
    ).pack()

    today = datetime.now().date()

    for i in range(6, -1, -1):

        current_date = (
            today - timedelta(days=i)
        )

        date_string = current_date.strftime(
            "%Y-%m-%d"
        )

        day_name = current_date.strftime(
            "%A"
        )

        day_habits = [
            habit
            for habit in habits_data
            if habit["date"] == date_string
        ]

        total = len(day_habits)

        completed = sum(
            1
            for habit in day_habits
            if habit["completed"]
        )

        if total > 0:

            percentage = int(
                (completed / total) * 100
            )

        else:

            percentage = 0

        if total == 0:

            status = "⚪ No data"

        elif percentage == 100:

            status = "🟢 Complete"

        elif percentage > 0:

            status = "🟡 In Progress"

        else:

            status = "🔴 Not Started"

        # Day frame

        frame = tk.Frame(
            weekly_window,
            bg="white",
            bd=1,
            relief="solid"
        )

        frame.pack(
            fill="x",
            padx=30,
            pady=5
        )

        tk.Label(
            frame,
            text=day_name,
            font=("Arial", 12, "bold"),
            bg="white",
            width=12,
            anchor="w"
        ).pack(
            side="left",
            padx=10,
            pady=10
        )

        tk.Label(
            frame,
            text=date_string,
            font=("Arial", 10),
            bg="white",
            fg="#777777"
        ).pack(
            side="left",
            padx=10
        )

        tk.Label(
            frame,
            text=f"{completed}/{total} ({percentage}%)",
            font=("Arial", 11, "bold"),
            bg="white"
        ).pack(
            side="left",
            padx=10
        )

        tk.Label(
            frame,
            text=status,
            font=("Arial", 10),
            bg="white"
        ).pack(
            side="right",
            padx=10
        )


# =========================================================
# MAIN WINDOW
# =========================================================

window = tk.Tk()

window.title(
    "Smart Habit Tracker"
)

window.geometry(
    "850x800"
)

window.configure(
    bg="#f5f3ff"
)

window.resizable(
    True,
    True
)


# =========================================================
# HEADER
# =========================================================

tk.Label(
    window,
    text="💜 SMART HABIT TRACKER",
    font=("Arial", 24, "bold"),
    bg="#f5f3ff",
    fg="#5b21b6"
).pack(
    pady=(25, 5)
)


tk.Label(
    window,
    text=datetime.now().strftime(
        "%A, %d %B %Y"
    ),
    font=("Arial", 11),
    bg="#f5f3ff",
    fg="#666666"
).pack()


# =========================================================
# STREAK
# =========================================================

streak_label = tk.Label(
    window,
    text="🔥 Streak: 0 days",
    font=("Arial", 13, "bold"),
    bg="#f5f3ff",
    fg="#7c3aed"
)

streak_label.pack(
    pady=10
)


# =========================================================
# STAT CARDS
# =========================================================

stats_frame = tk.Frame(
    window,
    bg="#f5f3ff"
)

stats_frame.pack(
    pady=10
)


# TOTAL CARD

total_card = tk.Frame(
    stats_frame,
    bg="white",
    width=180,
    height=80,
    bd=1,
    relief="solid"
)

total_card.pack(
    side="left",
    padx=10
)

total_card.pack_propagate(
    False
)


tk.Label(
    total_card,
    text="TOTAL",
    font=("Arial", 10, "bold"),
    bg="white",
    fg="#777777"
).pack()


total_label = tk.Label(
    total_card,
    text="0",
    font=("Arial", 22, "bold"),
    bg="white",
    fg="#5b21b6"
)

total_label.pack()


# COMPLETED CARD

completed_card = tk.Frame(
    stats_frame,
    bg="white",
    width=180,
    height=80,
    bd=1,
    relief="solid"
)

completed_card.pack(
    side="left",
    padx=10
)

completed_card.pack_propagate(
    False
)


tk.Label(
    completed_card,
    text="COMPLETED",
    font=("Arial", 10, "bold"),
    bg="white",
    fg="#777777"
).pack()


completed_label = tk.Label(
    completed_card,
    text="0",
    font=("Arial", 22, "bold"),
    bg="white",
    fg="#16a34a"
)

completed_label.pack()


# =========================================================
# PROGRESS
# =========================================================

progress_label = tk.Label(
    window,
    text="Today's Progress: 0%",
    font=("Arial", 12, "bold"),
    bg="#f5f3ff",
    fg="#333333"
)

progress_label.pack(
    pady=(15, 5)
)


progress_bar = tk.Scale(
    window,
    from_=0,
    to=100,
    orient="horizontal",
    length=450,
    showvalue=False,
    state="disabled",
    bg="#f5f3ff",
    highlightthickness=0
)

progress_bar.pack()


# =========================================================
# INPUT AREA
# =========================================================

input_frame = tk.Frame(
    window,
    bg="#f5f3ff"
)

input_frame.pack(
    pady=20
)


habit_entry = tk.Entry(
    input_frame,
    width=25,
    font=("Arial", 12)
)

habit_entry.grid(
    row=0,
    column=0,
    padx=5
)

habit_entry.insert(
    0,
    "Enter habit..."
)


time_entry = tk.Entry(
    input_frame,
    width=10,
    font=("Arial", 12)
)

time_entry.grid(
    row=0,
    column=1,
    padx=5
)

time_entry.insert(
    0,
    "18:00"
)


# =========================================================
# HABIT LIST
# =========================================================

habit_list = tk.Listbox(
    window,
    width=65,
    height=10,
    font=("Arial", 12),
    bd=1,
    relief="solid"
)

habit_list.pack(
    pady=10
)


# =========================================================
# MAIN BUTTONS
# =========================================================

button_frame = tk.Frame(
    window,
    bg="#f5f3ff"
)

button_frame.pack(
    pady=10
)


# ADD

tk.Button(
    button_frame,
    text="➕ Add Habit",
    command=add_habit,
    width=15,
    bg="#7c3aed",
    fg="white",
    font=("Arial", 10, "bold")
).grid(
    row=0,
    column=0,
    padx=5
)


# COMPLETE

tk.Button(
    button_frame,
    text="✅ Complete",
    command=complete_habit,
    width=15,
    bg="#16a34a",
    fg="white",
    font=("Arial", 10, "bold")
).grid(
    row=0,
    column=1,
    padx=5
)


# DELETE

tk.Button(
    button_frame,
    text="🗑 Delete",
    command=delete_habit,
    width=15,
    bg="#dc2626",
    fg="white",
    font=("Arial", 10, "bold")
).grid(
    row=0,
    column=2,
    padx=5
)


# EDIT

tk.Button(
    button_frame,
    text="✏️ Edit",
    command=edit_habit,
    width=15,
    bg="#2563eb",
    fg="white",
    font=("Arial", 10, "bold")
).grid(
    row=0,
    column=3,
    padx=5
)


# =========================================================
# SECOND BUTTON ROW
# =========================================================

second_button_frame = tk.Frame(
    window,
    bg="#f5f3ff"
)

second_button_frame.pack(
    pady=5
)


# REMINDER

tk.Button(
    second_button_frame,
    text="⏰ Set Reminder",
    command=set_reminder,
    width=20,
    bg="#f59e0b",
    fg="white",
    font=("Arial", 10, "bold")
).grid(
    row=0,
    column=0,
    padx=5
)


# WEEKLY VIEW

tk.Button(
    second_button_frame,
    text="📅 Weekly View",
    command=weekly_view,
    width=20,
    bg="#5b21b6",
    fg="white",
    font=("Arial", 10, "bold")
).grid(
    row=0,
    column=1,
    padx=5
)


# =========================================================
# START APPLICATION
# =========================================================

load_data()

create_today_habits()

show_habits()


# =========================================================
# START REMINDER THREAD
# =========================================================

reminder_thread = threading.Thread(
    target=reminder_checker,
    daemon=True
)

reminder_thread.start()


# =========================================================
# RUN
# =========================================================

window.mainloop()