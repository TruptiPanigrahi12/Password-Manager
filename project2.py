import tkinter as tk
from tkinter import messagebox
import csv
import os

# File to store expenses
FILE_NAME = "expenses.csv"

# Create CSV file if not exists
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Category", "Amount", "Date"])

# Function to load expenses
def load_expenses():
    expenses_list.delete(0, tk.END)  # Clear list
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                expenses_list.insert(tk.END, f"{row[0]} - ₹{row[1]} on {row[2]}")

# Function to add an expense
def add_expense():
    category = category_entry.get()
    amount = amount_entry.get()
    date = date_entry.get()

    if category and amount and date:
        with open(FILE_NAME, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([category, amount, date])

        messagebox.showinfo("Success", "Expense added successfully!")
        category_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)
        load_expenses()
    else:
        messagebox.showwarning("Warning", "All fields are required!")

# Function to delete an expense
def delete_expense():
    try:
        selected_index = expenses_list.curselection()[0]
        expenses_list.delete(selected_index)

        # Remove from CSV file
        with open(FILE_NAME, "r") as file:
            lines = file.readlines()
        with open(FILE_NAME, "w") as file:
            for i, line in enumerate(lines):
                if i != selected_index + 1:
                    file.write(line)

        messagebox.showinfo("Success", "Expense deleted!")
    except IndexError:
        messagebox.showwarning("Warning", "Please select an expense!")

# Create GUI
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("400x400")

# Input fields
tk.Label(root, text="Category").pack()
category_entry = tk.Entry(root, width=30)
category_entry.pack(pady=5)

tk.Label(root, text="Amount (₹)").pack()
amount_entry = tk.Entry(root, width=30)
amount_entry.pack(pady=5)

tk.Label(root, text="Date (DD/MM/YYYY)").pack()
date_entry = tk.Entry(root, width=30)
date_entry.pack(pady=5)

# Buttons
tk.Button(root, text="Add Expense", command=add_expense).pack(pady=5)
tk.Button(root, text="Delete Expense", command=delete_expense).pack(pady=5)

# Expense List
expenses_list = tk.Listbox(root, width=50, height=10)
expenses_list.pack(pady=10)

load_expenses()

root.mainloop()
