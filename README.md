# smart-file-sorter

My first AI agent: it reads the PDFs in a folder, asks a local AI what type each one is, and moves it into a folder for that type with a date in front of its name.

Example: `contract.pdf` → `Other/2026-10-02_contract.pdf`

## How it works

1. Reads the text of every page of each PDF (`pypdf`).
2. Sends the text to a local model (`qwen3.5:4b` via Ollama) and asks: CV, Attestation, Bill, Contract, Form or Other?
3. Safety net: if the answer isn't exactly one of those words, the file goes to `Unsure`.
4. Adds the file's **Date modified** (from Windows) to the start of the name.
5. Creates the category folder and moves the file.

## Why the date comes from Windows, not the AI

I tested asking qwen for the date the document was signed. It often gave different dates for the same file on different runs, and sometimes the same wrong date twice. A wrong date in a filename is worse than no date, so the filename uses Date modified, which is always correct.

qwen's date answers are still printed on screen as a suggestion, so I can compare models later.

## Safety

- Never deletes anything.
- Never overwrites a file (Windows refuses).
- Only touches PDFs; everything else is skipped.
- Dry run: put `#` in front of the `os.makedirs` and `os.rename` lines to see what it *would* do without moving anything.
- Make a backup copy of the folder before the first real run.

## Requirements

- Windows, Python 3.14
- [Ollama](https://ollama.com) running, with `qwen3.5:4b` pulled
- `pip install ollama pypdf`

## How to use

1. Change `folder_path` in `read_pdf.py` to your folder (use `/` slashes).
2. Run a dry run first and check the output.
3. Then run it for real.

## Known limitations

- **Tested on 9 PDFs: 8 correct, 1 Unsure, 0 wrong.** Each file is classified twice; if the answers differ, it goes to `Unsure` for a human to check. Document_de_Synthese (an Attestation) is too hard for a 4b model: across runs it got Form, Attestation and Other. A file can still be wrong if the model gives the same wrong answer twice.
- Slow: about 4 AI calls per file (category twice, date twice).
