import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# -----------------------------
# DATABASE SETUP
# -----------------------------
conn = sqlite3.connect("college_admission.db")
cursor = conn.cursor()

# Create table with UNIQUE name
cursor.execute("""
CREATE TABLE IF NOT EXISTS admissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    roll_no TEXT,
    course TEXT,
    email TEXT,
    phone TEXT,
    status TEXT
)
""")
conn.commit()

# Insert sample records (only once)
sample_data = [
    ("Aarav Sharma", "25MCA1001", "MCA", "aarav@example.com", "9876543210", "Approved"),
    ("Priya Patel", "25MCA1002", "MCA", "priya@example.com", "9876501234", "Pending"),
    ("Rohan Mehta", "25BTECH1003", "B.Tech", "rohan@example.com", "9988776655", "Approved"),
    ("Isha Gupta", "25BBA1004", "BBA", "isha@example.com", "9090909090", "Rejected"),
    ("Karan Singh", "25BSC1005", "B.Sc", "karan@example.com", "9123456789", "Pending"),
    ("Neha Verma", "25MBA1006", "MBA", "neha@example.com", "9876123450", "Approved"),
    ("Vikram Das", "25BCA1007", "BCA", "vikram@example.com", "9988001122", "Pending"),
    ("Sneha Reddy", "25MCOM1008", "M.Com", "sneha@example.com", "9001122334", "Approved"),
    ("Aditya Rao", "25MSC1009", "M.Sc", "aditya@example.com", "9123459000", "Rejected"),
    ("Simran Kaur", "25BA1010", "B.A", "simran@example.com", "9900887766", "Pending")
]

for data in sample_data:
    try:
        cursor.execute("INSERT INTO admissions (name, roll_no, course, email, phone, status) VALUES (?, ?, ?, ?, ?, ?)", data)
    except sqlite3.IntegrityError:
        pass  # Ignore duplicates
conn.commit()

# -----------------------------
# MAIN APPLICATION
# -----------------------------
root = tk.Tk()
root.title("College Admission System")
root.geometry("950x600")
root.config(bg="#E8F0F2")

# -----------------------------
# FUNCTIONS
# -----------------------------
def clear_fields():
    name_var.set("")
    roll_var.set("")
    course_var.set("")
    email_var.set("")
    phone_var.set("")
    status_var.set("Pending")

def add_record():
    name = name_var.get().strip()
    roll = roll_var.get().strip()
    course = course_var.get().strip()
    email = email_var.get().strip()
    phone = phone_var.get().strip()
    status = status_var.get()

    if name == "" or roll == "" or course == "":
        messagebox.showwarning("Input Error", "Name, Roll No, and Course are required!")
        return

    try:
        cursor.execute("INSERT INTO admissions (name, roll_no, course, email, phone, status) VALUES (?, ?, ?, ?, ?, ?)",
                       (name, roll, course, email, phone, status))
        conn.commit()
        fetch_data()
        clear_fields()
        messagebox.showinfo("Success", f"Student '{name}' added successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Duplicate Name", f"Student '{name}' already exists! Names must be unique.")

def fetch_data():
    cursor.execute("SELECT * FROM admissions")
    rows = cursor.fetchall()
    admission_table.delete(*admission_table.get_children())
    for row in rows:
        admission_table.insert("", tk.END, values=row)

def search_record():
    query = search_var.get()
    cursor.execute("SELECT * FROM admissions WHERE name LIKE ? OR roll_no LIKE ?", ('%' + query + '%', '%' + query + '%'))
    rows = cursor.fetchall()
    admission_table.delete(*admission_table.get_children())
    for row in rows:
        admission_table.insert("", tk.END, values=row)

def update_status():
    selected = admission_table.focus()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a record to update!")
        return
    data = admission_table.item(selected, 'values')
    new_status = status_var.get()
    cursor.execute("UPDATE admissions SET status=? WHERE id=?", (new_status, data[0]))
    conn.commit()
    fetch_data()
    messagebox.showinfo("Updated", f"Status updated to '{new_status}'")

def delete_record():
    selected = admission_table.focus()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a record to delete!")
        return
    data = admission_table.item(selected, 'values')
    confirm = messagebox.askyesno("Confirm Delete", f"Delete record for {data[1]}?")
    if confirm:
        cursor.execute("DELETE FROM admissions WHERE id=?", (data[0],))
        conn.commit()
        fetch_data()
        messagebox.showinfo("Deleted", "Record deleted successfully")

# -----------------------------
# GUI COMPONENTS
# -----------------------------
title = tk.Label(root, text="🎓 College Admission System", font=("Arial", 22, "bold"), bg="#E8F0F2", fg="#2E4F4F")
title.pack(pady=15)

frame = tk.Frame(root, bg="#E8F0F2")
frame.pack(pady=5)

# Input fields
name_var = tk.StringVar()
roll_var = tk.StringVar()
course_var = tk.StringVar()
email_var = tk.StringVar()
phone_var = tk.StringVar()
status_var = tk.StringVar(value="Pending")
search_var = tk.StringVar()

labels = ["Name", "Roll No", "Course", "Email", "Phone", "Status"]
vars = [name_var, roll_var, course_var, email_var, phone_var, status_var]

for i, text in enumerate(labels):
    tk.Label(frame, text=text + ":", font=("Arial", 11), bg="#E8F0F2").grid(row=i, column=0, sticky="w", padx=10, pady=5)
    if text == "Status":
        ttk.Combobox(frame, textvariable=status_var, values=["Pending", "Approved", "Rejected"], width=27).grid(row=i, column=1, padx=10, pady=5)
    else:
        tk.Entry(frame, textvariable=vars[i], width=30).grid(row=i, column=1, padx=10, pady=5)

# Buttons
btn_frame = tk.Frame(root, bg="#E8F0F2")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add Record", command=add_record, width=15, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Update Status", command=update_status, width=15, bg="#2196F3", fg="white").grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Delete Record", command=delete_record, width=15, bg="#F44336", fg="white").grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Clear Fields", command=clear_fields, width=15, bg="#9E9E9E", fg="white").grid(row=0, column=3, padx=5)

# Search bar
search_frame = tk.Frame(root, bg="#E8F0F2")
search_frame.pack(pady=10)
tk.Entry(search_frame, textvariable=search_var, width=30).grid(row=0, column=0, padx=10)
tk.Button(search_frame, text="Search", command=search_record, width=10, bg="#607D8B", fg="white").grid(row=0, column=1, padx=5)
tk.Button(search_frame, text="Show All", command=fetch_data, width=10, bg="#795548", fg="white").grid(row=0, column=2, padx=5)

# Table
table_frame = tk.Frame(root)
table_frame.pack(pady=10, fill="both", expand=True)

columns = ("ID", "Name", "Roll No", "Course", "Email", "Phone", "Status")
admission_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

for col in columns:
    admission_table.heading(col, text=col)
    admission_table.column(col, width=120, anchor="center")

admission_table.pack(fill="both", expand=True)

# Fetch initial data
fetch_data()

root.mainloop()
