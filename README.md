# Class 12 Question Paper Generator (MCQ only with GUI)

📚 Supports: Economics, Psychology, Philosophy, Gujarati, English, Sanskrit, Computer...

## Folder Structure
- `data/`: Store all CSVs for subjects.
- `generator.py`: Main script with GUI using Tkinter.

## Required Modules
- customtkinter
- csv
- random
- os
- reportlab

## CSV Format
Each row should look like:
```
question,type,options
"સૂર્ય કયા દિશામાં ઉગે છે?","mcq","ઉત્તર,દક્ષિણ,પૂર્વ,પશ્ચિમ"
```

## How to Use
1. Add your questions in subject CSV file inside `data/`.
2. Run:
```bash
python generator.py
```
3. Enter the subject name and click generate.

Enjoy!


---

## Rarity Field (NEW)
You must use one of:
- `most` = Most Important
- `sometimes` = Occasionally asked
- `rarely` = Rarely asked

## Question Types
- `"mcq"`: Multiple choice question (requires `options`)
- `"diagram"`: Diagram-based question (options should be empty)
- `"normal"`: Normal question (open-ended, options should be empty)

## Example File
Use `example.csv` in `/data/` to understand formatting. You can open in Excel or Google Sheets for easier editing.
