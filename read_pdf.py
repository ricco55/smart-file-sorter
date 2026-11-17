from pypdf import PdfReader
import ollama

reader = PdfReader("test.pdf")

text = ""
for page in reader.pages:
    text = text + page.extract_text()

instruction = "What type of document is this? Answer with one word only: CV, Attestation, Bill, or Other."
prompt = instruction + " Document: " + text

response = ollama.chat(
    model="qwen3.5:4b",
    messages=[{"role": "user", "content": prompt}],
    think=False,
)
print(response.message.content)

categories = ["CV", "Attestation", "Bill", "Other"]
answer = "Bill."


if answer in categories:
    print("Move to folder:", answer)
else:
    print("Move to folder: Unsure")