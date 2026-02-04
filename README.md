# 📘 PDF Ledger Split Automation Tool

> A **secure, Windows-based Python automation tool** to split large ledger / statement PDFs into **party-wise PDFs** with **smart naming rules** and **strong security protection**.

---

## 👨‍💻 Developer

- **Name:** Abhijit Das  
- **Contact:** +91-9476378707  
- **Email:** one94community@gmail.com  

---

## 🚀 Features

- ✅ Bulk PDF processing
- ✅ Party-wise PDF split using `To:` keyword
- ✅ Automatic & clean file naming
- ✅ Company short code detection (SSIL / SSML / SSWPL)
- ✅ Month–Year auto detection from filename  
  *(e.g. `Sep 25 → SEPTEMBER-2025`)*
- ✅ Blank / `x` pages skipped
- ✅ Duplicate processing protection
- 🔐 Password protected execution
- 🔴 Danger Mode on 2nd wrong password
- 💣 Self-destruct on 3rd wrong password

---

## 🧠 How It Works

1. Tool starts and shows developer credit
2. Asks user confirmation (Y/N)
3. Requests password
4. Password logic:
   - 1st wrong → normal warning
   - 2nd wrong → 🔴 Danger Mode + developer contact
   - 3rd wrong → 💣 script deletes itself
5. Reads PDFs from input folder
6. Detects `To:` sections
7. Extracts and cleans party names
8. Detects company and assigns short code
9. Extracts Month–Year from PDF filename
10. Splits and saves PDFs in organized folders

---

## 📁 Project Structure

```text
PDF_Ledger_Split_Tool/
│
├── split_by_to.py
│
├── INPUT_STATEMENT_PDF/
│   ├── Ledger_Sep 25.pdf
│   ├── Ledger_Oct 25.pdf
│
└── OUTPUT_SPLIT_PDF/
```

⚠️ **Folder names must not be changed.**

---

## 🏷 Output File Naming Format

```text
PARTY-NAME-COMPANYCODE-MONTH-YEAR.pdf
```

### Example

```text
A. J. HARDWARE ENTERPRISE-SSIL-SEPTEMBER-2025.pdf
```

---

## ⚙️ Installation Guide

### 1️⃣ Install Python

- Download from: https://www.python.org/downloads/
- Install **Python 3.9 or higher**
- ✔️ Enable **Add Python to PATH**

---

### 2️⃣ Install Required Libraries

Open Command Prompt (CMD) and run:

```bash
pip install pdfplumber PyPDF2
```

---

### 3️⃣ Enable ANSI Colors (Required for Danger Mode)

Run once in CMD:

```bash
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1
```

Restart CMD after this.

---

## ▶ How to Run

```bash
python split_by_to.py
```

---

## 🔐 Security Warning

⚠️ On **3 consecutive wrong password attempts**,  
the script will **delete itself permanently**.

👉 Always keep a **backup copy** of the script.

---

## 🛠 Customization

- Change password in code:
```python
CORRECT_PASSWORD = "1234"
```

- Add new company mappings:
```python
COMPANY_CODE_MAP["new company name"] = "CODE"
```

---

## 📄 License

This project is for **internal / office automation use**.  
Redistribution or modification should retain developer credit.

---

## 📬 Contact

For support or customization:

**Abhijit Das**  
📱 +91-9476378707  
✉️ one94community@gmail.com
