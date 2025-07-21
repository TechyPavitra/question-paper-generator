
import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox

DATA_FOLDER = "data"
RARITY_OPTIONS = ["most", "sometimes", "rarely"]
QUESTION_TYPES = ["mcq", "paragraph", "diagram"]

# Function to save question to the correct subject CSV
def save_question():
    subject = subject_var.get().strip().lower()
    q_type = type_var.get()
    rarity = rarity_var.get()
    question = question_entry.get("1.0", "end").strip()
    options = options_entry.get().strip()

    if not subject or not q_type or not rarity or not question:
        messagebox.showerror("Error", "Please fill in all required fields.")
        return

    filename = os.path.join(DATA_FOLDER, f"{subject}.csv")

    # Create file if it doesn't exist
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["question", "type", "options", "rarity"])

    # Write the question row
    with open(filename, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([question, q_type, options if q_type == "mcq" else "", rarity])

    messagebox.showinfo("Success", f"Question saved to '{subject}.csv'")
    question_entry.delete("1.0", "end")
    options_entry.delete(0, "end")

# GUI layout
root = tk.Tk()
root.title("Add Question to Subject CSV")

tk.Label(root, text="Subject (e.g. english, gujarati):").pack(pady=2)
subject_var = tk.StringVar()
tk.Entry(root, textvariable=subject_var).pack(pady=2)

tk.Label(root, text="Question Type:").pack(pady=2)
type_var = tk.StringVar(value="mcq")
ttk.Combobox(root, textvariable=type_var, values=QUESTION_TYPES, state="readonly").pack(pady=2)

tk.Label(root, text="Rarity:").pack(pady=2)
rarity_var = tk.StringVar(value="most")
ttk.Combobox(root, textvariable=rarity_var, values=RARITY_OPTIONS, state="readonly").pack(pady=2)

tk.Label(root, text="Enter Question:").pack(pady=2)
question_entry = tk.Text(root, height=4, width=50)
question_entry.pack(pady=2)

tk.Label(root, text="Options (only for MCQ, comma separated):").pack(pady=2)
options_entry = tk.Entry(root, width=50)
options_entry.pack(pady=2)

tk.Button(root, text="Save Question", command=save_question).pack(pady=10)

root.mainloop()
