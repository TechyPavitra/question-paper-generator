import sys
import subprocess

# Auto-install missing packages
required_packages = ["PyQt6", "reportlab"]
for pkg in required_packages:
    try:
        __import__(pkg.lower() if pkg != "PyQt6" else "PyQt6.QtWidgets")
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

# --- Now that dependencies are installed, import everything ---
import csv
import random
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)

# Constants
DATA_FOLDER = "data"
NUM_QUESTIONS = 50

def load_questions(subject):
    filepath = os.path.join(DATA_FOLDER, f"{subject.lower()}.csv")
    with open(filepath, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def generate_paper(questions, count):
    return random.sample(questions, min(count, len(questions)))

def split_text(text, max_length):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        if len(current) + len(word) + 1 <= max_length:
            current += " " + word if current else word
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

def export_pdf(paper, subject, filename=None):
    filename = filename or f"Class12_{subject}_Paper.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    x_margin = 50
    y = height - 50

    c.setFont("Helvetica-Bold", 14)
    c.drawString(x_margin, y, f"ધોરણ ૧૨ – {subject.capitalize()} (MCQ Only)")
    y -= 30
    c.setFont("Helvetica", 12)
    c.drawString(x_margin, y, "Most Important Question Paper")
    y -= 20
    c.drawString(x_margin, y, f"Generated on: {datetime.now().strftime('%d-%m-%Y %I:%M %p')}")
    y -= 40

    c.setFont("Helvetica", 11)

    for i, q in enumerate(paper, 1):
        question_text = f"{i}. {q['question']} ({q['rarity']})"
        lines = split_text(question_text, 90)
        for line in lines:
            c.drawString(x_margin, y, line)
            y -= 16
            if y < 60:
                c.showPage()
                y = height - 50

        if q['type'] == 'mcq':
            options = q['options'].split(',')
            for idx, opt in enumerate(options):
                c.drawString(x_margin + 20, y, f"({chr(65 + idx)}) {opt.strip()}")
                y -= 16
                if y < 60:
                    c.showPage()
                    y = height - 50
        elif q['type'] == 'diagram':
            c.drawString(x_margin + 20, y, "(આ પ્રશ્ન માટે આંકડો દોરવો જરૂરી છે)")
            y -= 16

        y -= 10

    c.save()
    return filename

class QuestionPaperGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Class 12 Question Paper Generator")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Enter Subject Name:")
        layout.addWidget(self.label)

        self.subject_input = QLineEdit()
        layout.addWidget(self.subject_input)

        self.generate_button = QPushButton("Generate Question Paper")
        self.generate_button.clicked.connect(self.generate_paper)
        layout.addWidget(self.generate_button)

        self.setLayout(layout)

    def generate_paper(self):
        subject = self.subject_input.text().strip().lower()
        if not subject:
            QMessageBox.critical(self, "Error", "Please enter a subject.")
            return

        try:
            questions = load_questions(subject)
            paper = generate_paper(questions, NUM_QUESTIONS)
            filename = export_pdf(paper, subject)
            QMessageBox.information(self, "Success", f"PDF saved as '{filename}'")
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", f"Subject file '{subject}.csv' not found in 'data/' folder.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuestionPaperGenerator()
    window.show()
    sys.exit(app.exec())
