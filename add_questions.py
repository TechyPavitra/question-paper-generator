import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

os.makedirs("data", exist_ok=True)

SUBJECTS = ["economics", "psychology", "philosophy", "gujarati", "english", "sanskrit", "computer"]

SECTIONS = ["A", "B", "C", "D", "E"]
RARITIES = ["most imp", "sometimes", "rarely"]

class QuestionEntryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Add Question to CSV")
        self.root.geometry("600x500")

        # Subject Dropdown
        tk.Label(root, text="Select Subject:").pack()
        self.subject_var = tk.StringVar()
        self.subject_menu = ttk.Combobox(root, textvariable=self.subject_var, values=SUBJECTS, state='readonly')
        self.subject_menu.pack()

        # Section Dropdown
        tk.Label(root, text="Select Section:").pack()
        self.section_var = tk.StringVar()
        self.section_menu = ttk.Combobox(root, textvariable=self.section_var, values=SECTIONS, state='readonly')
        self.section_menu.pack()

        # Question Type Dropdown
        tk.Label(root, text="Select Question Type:").pack()
        self.qtype_var = tk.StringVar()
        self.qtype_menu = ttk.Combobox(root, textvariable=self.qtype_var, values=["mcq", "paragraph", "diagram"], state='readonly')
        self.qtype_menu.pack()

        # Rarity Dropdown
        tk.Label(root, text="Select Rarity:").pack()
        self.rarity_var = tk.StringVar()
        self.rarity_menu = ttk.Combobox(root, textvariable=self.rarity_var, values=RARITIES, state='readonly')
        self.rarity_menu.pack()

        # Question Text Entry
        tk.Label(root, text="Enter Question:").pack()
        self.question_text = tk.Text(root, height=4)
        self.question_text.pack(pady=5)

        # MCQ Options Frame (only visible if type is mcq)
        self.mcq_frame = tk.Frame(root)
        tk.Label(self.mcq_frame, text="Enter MCQ options (comma separated):").pack()
        self.options_entry = tk.Entry(self.mcq_frame, width=50)
        self.options_entry.pack()
        self.mcq_frame.pack_forget()

        # Update MCQ field visibility on question type change
        self.qtype_menu.bind("<<ComboboxSelected>>", self.toggle_mcq_options)

        # Save Button
        tk.Button(root, text="Save Question", command=self.save_question).pack(pady=10)

    def toggle_mcq_options(self, event=None):
        if self.qtype_var.get() == "mcq":
            self.mcq_frame.pack()
        else:
            self.mcq_frame.pack_forget()

    def save_question(self):
        subject = self.subject_var.get().strip().lower()
        qtype = self.qtype_var.get()
        rarity = self.rarity_var.get()
        section = self.section_var.get()
        question = self.question_text.get("1.0", "end").strip()
        options = self.options_entry.get().strip() if qtype == "mcq" else ""

        if not subject or not qtype or not rarity or not question or not section:
            messagebox.showerror("Error", "Please fill all required fields.")
            return

        filepath = os.path.join("data", f"{subject}.csv")
        file_exists = os.path.isfile(filepath)

        with open(filepath, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["question", "type", "options", "rarity", "section"])
            if not file_exists:
                writer.writeheader()
            writer.writerow({
                "question": question,
                "type": qtype,
                "options": options,
                "rarity": rarity,
                "section": section
            })

        messagebox.showinfo("Success", f"Question saved to {filepath}")
        self.question_text.delete("1.0", "end")
        self.options_entry.delete(0, "end")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuestionEntryApp(root)
    root.mainloop()


