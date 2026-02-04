import pdfplumber
from PyPDF2 import PdfReader, PdfWriter
import os, sys, re, time

# ================== CREDIT SCREEN ==================
print("=" * 60)
print("        PDF Ledger Split Automation Tool")
print("        Developed by: Abhijit Das")
print("        Contact: 91 - 9476378707")
print("        Email: one94community@gmail.com")
print("=" * 60)
print()
# ==================================================

# ================== YES / NO CONFIRMATION ==========
while True:
    ch = input("Do you want to split the PDFs? (Y/N): ").strip().lower()
    if ch == "y":
        break
    elif ch == "n":
        print("❌ Operation cancelled.")
        input("Press Enter to exit...")
        sys.exit()
    else:
        print("⚠️ Please type Y or N only.")
# ==================================================

# ================== SELF DESTRUCT ==================
def self_destruct():
    script = os.path.abspath(__file__)
    bat = script.replace(".py", "_destroy.bat")

    with open(bat, "w") as f:
        f.write(f"""
@echo off
timeout /t 2 >nul
del "{script}"
del "%~f0"
""")
    os.startfile(bat)
    sys.exit()
# ==================================================

# ================== PASSWORD CHECK =================
CORRECT_PASSWORD = "1234"
MAX_ATTEMPTS = 3

DEV_NAME = "Abhijit Das"
DEV_PHONE = "+91 - 9476378707"
DEV_EMAIL = "one94community@gmail.com"

attempts = 0

while attempts < MAX_ATTEMPTS:
    pwd = input("Enter password to continue: ").strip()

    if pwd == CORRECT_PASSWORD:
        print("\033[0m\n✅ Password verified. Starting...\n")
        break

    attempts += 1
    remaining = MAX_ATTEMPTS - attempts

    # 2nd wrong → DANGER MODE + CONTACT
    if remaining == 1:
        print("\033[41;97m")
        print("\n🚨🚨 DANGER MODE ACTIVATED 🚨🚨")
        print("❌ WRONG PASSWORD ENTERED 2 TIMES ❌")
        print("\n📞 CONTACT DEVELOPER")
        print(f"👤 Name   : {DEV_NAME}")
        print(f"📱 Phone  : {DEV_PHONE}")
        print(f"✉️ Email  : {DEV_EMAIL}")
        print("\n⚠️ ONE MORE WRONG ATTEMPT WILL DELETE THIS PROGRAM!")
        print("\033[0m")

    # 3rd wrong → SELF DESTRUCT
    elif remaining == 0:
        print("\033[41;97m")
        print("\n💣 SECURITY BREACH DETECTED 💣")
        print("🔥 PROGRAM WILL SELF-DESTRUCT 🔥")
        print("\033[0m")
        time.sleep(2)
        self_destruct()

    else:
        print(f"❌ Wrong password. Attempts left: {remaining}")
# ==================================================

INPUT_DIR = "INPUT_STATEMENT_PDF"
OUTPUT_ROOT = "OUTPUT_SPLIT_PDF"
os.makedirs(OUTPUT_ROOT, exist_ok=True)

COMPANY_CODE_MAP = {
    "shyam steel industries ltd": "SSIL",
    "shyam steel manufacturing ltd": "SSML",
    "shyam steel works pvt ltd": "SSWPL"
}

def clean_filename(n):
    for c in '<>:"/\\|?*':
        n = n.replace(c, "")
    return n.strip()

def clean_party_name(n):
    n = re.sub(r"[- ]?\d+$", "", n.strip())
    n = re.split(
        r"shyam steel industries ltd|"
        r"shyam steel manufacturing ltd|"
        r"shyam steel works pvt ltd",
        n,
        flags=re.I
    )[0]
    return n.strip()

def is_useless_page(t):
    return not t or t.strip().lower() == "x"

def extract_month_year(fname):
    m = {
        "jan":"JANUARY","feb":"FEBRUARY","mar":"MARCH","apr":"APRIL",
        "may":"MAY","jun":"JUNE","jul":"JULY","aug":"AUGUST",
        "sep":"SEPTEMBER","oct":"OCTOBER","nov":"NOVEMBER","dec":"DECEMBER"
    }
    x = re.search(r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[-_ ]?(\d{2,4})", fname.lower())
    if x:
        y = x.group(2)
        if len(y) == 2:
            y = "20" + y
        return f"{m[x.group(1)]}-{y}"
    return "UNKNOWN"

def get_company_code(text):
    t = text.lower()
    for k,v in COMPANY_CODE_MAP.items():
        if k in t:
            return v
    return "UNKNOWN"

# ================== MAIN PROCESS ===================
for pdf_file in os.listdir(INPUT_DIR):
    if not pdf_file.lower().endswith(".pdf"):
        continue

    base = os.path.splitext(pdf_file)[0]
    in_path = os.path.join(INPUT_DIR, pdf_file)
    out_dir = os.path.join(OUTPUT_ROOT, base)

    if os.path.exists(out_dir) and os.listdir(out_dir):
        print(f"⏭️ Skipped (already done): {pdf_file}")
        continue

    os.makedirs(out_dir, exist_ok=True)
    print(f"\n📄 Processing: {pdf_file}")

    sections = []

    with pdfplumber.open(in_path) as pdf:
        texts = []
        for i,p in enumerate(pdf.pages):
            t = p.extract_text()
            texts.append(t)
            if is_useless_page(t):
                continue
            lines = [l.strip() for l in t.split("\n") if l.strip()]
            for j,l in enumerate(lines):
                if l.lower().startswith("to:") and j+1 < len(lines):
                    sections.append({
                        "party": clean_party_name(lines[j+1]),
                        "start": i
                    })

    if not sections:
        continue

    for i in range(len(sections)):
        sections[i]["end"] = (sections[i+1]["start"]-1) if i+1<len(sections) else len(texts)-1

    reader = PdfReader(in_path)
    my = extract_month_year(pdf_file)

    for s in sections:
        w = PdfWriter()
        for p in range(s["start"], s["end"]+1):
            if not is_useless_page(texts[p]):
                w.add_page(reader.pages[p])

        if not w.pages:
            continue

        code = get_company_code(texts[s["start"]])
        fname = clean_filename(f"{s['party']}-{code}-{my}.pdf")
        out = os.path.join(out_dir, fname)

        if os.path.exists(out):
            continue

        with open(out,"wb") as f:
            w.write(f)

        print(f"✔ Created: {base}/{fname}")

print("\n✅ ALL DONE!")
input("Press Enter to exit...")
# ==================================================
