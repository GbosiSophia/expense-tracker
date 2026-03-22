import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


root = tk.Tk()
root.title("Expense Tracker")
root.geometry("900x700")
root.configure(bg="#f9f9f9")  # light cream background

total_spent = 0


title_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="ridge")
title_frame.pack(pady=10, padx=20, fill="x")
tk.Label(title_frame, text="Expense Tracker", font=("Arial", 26, "bold"),
         bg="#ffffff", fg="#333333").pack(pady=10)


canvas = tk.Canvas(root, bg="#f9f9f9")
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#f9f9f9")

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


form_frame = tk.Frame(scrollable_frame, bg="#ffffff", bd=2, relief="ridge")
form_frame.pack(padx=20, pady=10, fill="x")

label_color = "#333333"
entry_bg = "#f4f4f4"

tk.Label(form_frame, text="Amount", font=("Arial", 15), bg="#ffffff", fg=label_color).grid(row=0, column=0, padx=10, pady=5, sticky="w")
tk.Label(form_frame, text="Category", font=("Arial", 15), bg="#ffffff", fg=label_color).grid(row=2, column=0, padx=10, pady=5, sticky="w")
tk.Label(form_frame, text="Description", font=("Arial", 15), bg="#ffffff", fg=label_color).grid(row=4, column=0, padx=10, pady=5, sticky="w")
tk.Label(form_frame, text="Date", font=("Arial", 15), bg="#ffffff", fg=label_color).grid(row=6, column=0, padx=10, pady=5, sticky="w")

amount_entry = tk.Entry(form_frame, bg=entry_bg, fg="#333333", relief="flat")
amount_entry.grid(row=1, column=0, padx=10, pady=5, sticky="we")

category_box = ttk.Combobox(form_frame, values=["Food", "Transport", "Clothes", "Savings", "School", "Other"], state="readonly")
category_box.grid(row=3, column=0, padx=10, pady=5, sticky="we")
category_box.current(0)

description_entry = tk.Entry(form_frame, width=30, bg=entry_bg, fg="#333333", relief="flat")
description_entry.grid(row=5, column=0, padx=10, pady=5, sticky="we")

date_entry = DateEntry(form_frame, width=17, background="#4ca1af", foreground="#ffffff", borderwidth=1)
date_entry.grid(row=7, column=0, padx=10, pady=5, sticky="we")


result_label = tk.Label(scrollable_frame, text="", fg="red", bg="#f9f9f9", font=("Arial", 11))
result_label.pack()


def add_expense():
    global total_spent

    amount_text = amount_entry.get()
    category = category_box.get()
    description = description_entry.get()
    date = date_entry.get()

    if amount_text == "":
        result_label.config(text="Please enter an amount.")
        return

    try:
        amount = float(amount_text)
    except ValueError:
        result_label.config(text="Amount must be a number")
        return

    tag = 'evenrow' if len(tree.get_children()) % 2 == 0 else 'oddrow'
    tree.insert("", "end", values=(date, category, description, f"{amount:.2f}"), tags=(tag,))

    total_spent += amount
    total_label.config(text=f"Total Spent: ₦{total_spent:.2f}")

    result_label.config(text=f"Added: {category} - {description} - ₦{amount:.2f}")

    amount_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    category_box.current(0)

    with open("expenses.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, category, description, amount])

def load_expenses():
    global total_spent
    try:
        with open("expenses.csv", "r", newline="") as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                if not row or len(row) != 4:
                    continue
                date, category, description, amount = row
                tag = 'evenrow' if len(tree.get_children()) % 2 == 0 else 'oddrow'
                tree.insert("", "end", values=(date, category, description, f"{float(amount):.2f}"), tags=(tag,))
                total_spent += float(amount)
        total_label.config(text=f"Total Spent: ₦{total_spent:.2f}")
    except FileNotFoundError:
        pass

def clear_fields():
    amount_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    category_box.current(0)

def delete_expense():
    global total_spent
    selected = tree.selection()
    if not selected:
        result_label.config(text="Select an expense to delete")
        return
    item = tree.item(selected)
    amount = float(item["values"][3])
    total_spent -= amount
    total_label.config(text=f"Total Spent: ₦{total_spent:.2f}")
    tree.delete(selected)

def summarize_by_category():
    category_totals = {}
    for widget in summary_output_frame.winfo_children():
        widget.destroy()
    for row in tree.get_children():
        values = tree.item(row)["values"]
        category = values[1]
        amount = float(values[3])
        category_totals[category] = category_totals.get(category, 0) + amount
    for category, total in category_totals.items():
        tk.Label(summary_output_frame, text=f"{category}: ₦{total:.2f}", font=("Arial", 11), bg="#f9f9f9").pack()

def show_category_chart():
    category_totals = {}
    for row in tree.get_children():
        values = tree.item(row)["values"]
        category = values[1]
        amount = float(values[3])
        category_totals[category] = category_totals.get(category, 0) + amount

    categories = list(category_totals.keys())
    amounts = list(category_totals.values())

    plt.close('all')
    fig = plt.Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=90)
    ax.set_title("Expenses by Category")

    for widget in chart_frame.winfo_children():
        widget.destroy()
    canvas_fig = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas_fig.draw()
    canvas_fig.get_tk_widget().pack()

def show_monthly_chart():
    monthly_totals = {}
    for row in tree.get_children():
        values = tree.item(row)["values"]
        date = values[0]
        amount = float(values[3])
        month = date[:7]
        monthly_totals[month] = monthly_totals.get(month, 0) + amount

    months = list(monthly_totals.keys())
    totals = list(monthly_totals.values())

    plt.close('all')
    fig = plt.Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(months, totals, marker="o", color="#4ca1af")
    ax.set_title("Monthly Spending")
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount (₦)")
    ax.grid(True)

    for widget in chart_frame.winfo_children():
        widget.destroy()
    canvas_fig = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas_fig.draw()
    canvas_fig.get_tk_widget().pack()


button_frame = tk.Frame(scrollable_frame, bg="#f9f9f9")
button_frame.pack(pady=10)

button_bg = "#4ca1af"
button_fg = "#ffffff"
button_params = {"bg": button_bg, "fg": button_fg, "relief":"flat", "padx":12, "pady":6, "font":("Arial", 11, "bold"), "bd":0}

tk.Button(button_frame, text="Add Expense", command=add_expense, **button_params).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Clear Fields", command=clear_fields, **button_params).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Delete", command=delete_expense, **button_params).grid(row=0, column=2, padx=5)
tk.Button(button_frame, text="Summarize", command=summarize_by_category, **button_params).grid(row=0, column=3, padx=5)
tk.Button(button_frame, text="Category Chart", command=show_category_chart, **button_params).grid(row=0, column=4, padx=5)
tk.Button(button_frame, text="Monthly Chart", command=show_monthly_chart, **button_params).grid(row=0, column=5, padx=5)


table_frame = tk.Frame(scrollable_frame, bg="#ffffff", bd=2, relief="ridge")
table_frame.pack(padx=20, pady=10, fill="both", expand=True)

columns = ("Date", "Category", "Description", "Amount")
tree = ttk.Treeview(table_frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.grid(row=0, column=0, sticky="nsew")

scrollbar_tree = tk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar_tree.set)
scrollbar_tree.grid(row=0, column=1, sticky="ns")

table_frame.grid_rowconfigure(0, weight=1)
table_frame.grid_columnconfigure(0, weight=1)


style = ttk.Style()
style.theme_use("default")
style.configure("Treeview",
                background="#ffffff",
                foreground="#333333",
                rowheight=25,
                fieldbackground="#ffffff",
                font=("Arial", 10))
style.map('Treeview', background=[('selected', '#4ca1af')], foreground=[('selected', '#ffffff')])
style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#e0e0e0", foreground="#333333")
tree.tag_configure('oddrow', background="#ffffff")
tree.tag_configure('evenrow', background="#f7f7f7")


summary_frame = tk.Frame(scrollable_frame, bg="#f9f9f9")
summary_frame.pack(pady=10, fill="x")
total_label = tk.Label(summary_frame, text="Total Spent: ₦0", font=("Arial", 12, "bold"), bg="#f9f9f9")
total_label.pack()

summary_output_frame = tk.Frame(summary_frame, bg="#f9f9f9")
summary_output_frame.pack()

chart_frame = tk.Frame(scrollable_frame, bg="#f9f9f9")
chart_frame.pack(pady=10)

load_expenses()

root.mainloop()