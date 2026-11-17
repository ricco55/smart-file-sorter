from pypdf import PdfReader
from datetime import date
import ollama
import os

def read_text(file):
    reader = PdfReader(file)

    text = ""
    for page in reader.pages:
        text = text + page.extract_text()

    return text

def classify(file):
    text = read_text(file)

    instruction = "What type of document is this? Answer with one word only: CV, Attestation, Bill, Contract, Form, or Other."
    prompt = "Document: " + text + " " + instruction

    response = ollama.chat(
        model="qwen3.5:4b",
        messages=[{"role": "user", "content": prompt}],
        think=False,
    )
    print(response.message.content)

    categories = ["CV", "Attestation", "Bill", "Contract", "Form", "Other"]
    answer = response.message.content.strip()

    if answer in categories:
        return answer
    else:
        return "Unsure"

def get_date(file):
    text = read_text(file)

    instruction = "When was this document signed or issued? Answer only with the date as YYYY-MM-DD, or None if there is no date."
    prompt = "Document: " + text + " " + instruction

    response = ollama.chat(
        model="qwen3.5:4b",
        messages=[{"role": "user", "content": prompt}],
        think=False,
    )
    return response.message.content.strip()

folder_path = "C:/Users/HP/Documents/Test"
names = os.listdir(folder_path)
for name in names:
    if not name.endswith(".pdf"):
        continue
    full_path = folder_path + "/" + name
    folder = classify(full_path)
    category_folder = folder_path + "/" + folder
    os.makedirs(category_folder, exist_ok=True)
    seconds = os.path.getmtime(full_path)
    file_date = date.fromtimestamp(seconds)
    date_1 = get_date(full_path)
    date_2 = get_date(full_path)
    print("   Date modified:", file_date, "| Answer 1:", date_1, "| Answer 2:", date_2)
    # if date_1 == date_2 and len(date_1) == 10 and date_1[4] == "-" and date_1[7] == "-":
    #     chosen_date = date_1
    # else:
    #     chosen_date = str(file_date)
    chosen_date = str(file_date)
    new_name = chosen_date + "_" + name
    new_path = category_folder + "/" + new_name
    os.rename(full_path, new_path)
    print(name, "→", folder + "/" + new_name)