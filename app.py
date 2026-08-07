import io
import time
import pikepdf
import streamlit as st

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="ULTRA RECOVERY - PDF Password Recovery",
    page_icon="🔓",
    layout="centered"
)

# ==========================================
# CUSTOM CSS (EXACT MANDATED STYLING)
# ==========================================
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: radial-gradient(circle, #1e213a 0%, #050505 100%) !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
    }

    /* Header Box */
    .header-box {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid rgba(212, 175, 55, 0.4);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 25px;
    }

    .header-title {
        color: #d4af37;
        font-size: 40px;
        font-weight: 800;
        margin: 0;
        letter-spacing: 2px;
        text-transform: uppercase;
        text-shadow: 0 0 10px rgba(212, 175, 55, 0.3);
    }

    .header-subtext {
        color: #e0e0e0;
        font-size: 16px;
        margin-top: 8px;
        font-weight: 500;
    }

    /* RGB Animated Border Container */
    @keyframes rgb-border {
        0% { box-shadow: 0 0 15px #ff0000; border-color: #ff0000; }
        33% { box-shadow: 0 0 15px #00ff00; border-color: #00ff00; }
        66% { box-shadow: 0 0 15px #0000ff; border-color: #0000ff; }
        100% { box-shadow: 0 0 15px #ff0000; border-color: #ff0000; }
    }

    .rgb-container {
        border: 2px solid #ff0000;
        border-radius: 16px;
        padding: 20px;
        background: rgba(10, 10, 20, 0.6);
        animation: rgb-border 4s infinite linear;
        margin-bottom: 25px;
    }

    /* Radio Buttons */
    .stRadio > label {
        color: #FFFFFF !important;
        font-size: 18px !important;
        font-weight: 700 !important;
    }

    div[role="radiogroup"] label {
        color: #FFFF00 !important;
        font-size: 22px !important;
        font-weight: 900 !important;
    }

    /* Input Boxes Styling */
    .stTextInput > div > div > input {
        color: #FF0000 !important;
        font-size: 24px !important;
        font-weight: 900 !important;
        border: 2px solid #FF0000 !important;
        box-shadow: 0 0 10px rgba(255, 0, 0, 0.5) !important;
        background-color: #0d0d1a !important;
        border-radius: 10px !important;
        text-align: center;
    }

    .stTextInput > label {
        color: #FFFFFF !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }

    /* File Uploader Customization */
    .stFileUploader > label {
        color: #FFFFFF !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }

    /* Primary Start Button */
    .stButton > button {
        width: 100% !important;
        background: linear-gradient(90deg, #FF1493 0%, #00BFFF 100%) !important;
        color: #FFFFFF !important;
        font-size: 22px !important;
        font-weight: 800 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        box-shadow: 0 4px 15px rgba(255, 20, 147, 0.4) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }

    .stButton > button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 6px 20px rgba(0, 191, 255, 0.6) !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER SECTION
# ==========================================
st.markdown("""
<div class="header-box">
    <div class="header-title">ULTRA RECOVERY</div>
    <div class="header-subtext">💎 Managed by: VIKAS MISHRA</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# HARDCODED INDIAN NAMES DATABASE
# ==========================================
COMMON_INDIAN_PREFIXES = [
    "AMIT", "ANIL", "KUMA", "MISH", "SING", "VIKA", "RAHU", "ROHI",
    "RAJE", "POOJ", "NEHA", "PANK", "MANO", "SURA", "DEEP", "VIJA",
    "AJAY", "SANT", "ALOK", "RAME", "SURE", "DINE", "MOKE", "RAKESH",
    "NEER", "SUNI", "ANUP", "VIVE", "GAUR", "SACH", "AKAS", "ROHO",
    "RITU", "PRIY", "KAPO", "SHAR", "VERM", "PATI", "YADA", "GUPT",
    "JAIN", "CHAU", "AGAR", "TIWA", "DUBI", "SAHA", "MEHT", "JOSH",
    "NAIR", "MENO", "PILL", "REDD", "RAO", "ROYA", "KHAN", "SHAH",
    "DAS", "BOSE", "DUTT", "SEN", "PAL", "ROY", "MALH", "SETI",
    "KHUR", "BAJA", "AROR", "BHAT", "CHAW", "KALA", "KAUR", "SING",
    "PATE", "DESA", "JOSH", "KULK", "PATI", "PAWA", "THAK", "RANE",
    "SHIN", "KADAM", "CHAV", "INGA", "MORE", "JADH", "GAIK", "SANT",
    "BARR", "SARK", "MUKH", "BANER", "CHAT", "GANG", "GHOS", "BIHO",
    "TIWA", "PANDE", "SHUK", "TRIP", "CRAV", "DWIV", "AVAS", "CHAT"
]

# ==========================================
# RECOVERY CORE FUNCTIONS
# ==========================================
def verify_and_unlock(pdf_bytes: bytes, password: str):
    """Verifies password validity with double saving check."""
    try:
        pdf = pikepdf.open(io.BytesIO(pdf_bytes), password=password)
        test_output = io.BytesIO()
        pdf.save(test_output)
        test_output.seek(0)
        return test_output
    except Exception:
        return None

def generate_name_prefixes(name_hint: str):
    """Generates 4-character sliding window prefixes."""
    prefixes = set()
    clean_name = name_hint.strip()
    
    if len(clean_name) >= 4:
        for i in range(len(clean_name) - 3):
            chunk = clean_name[i:i+4]
            prefixes.add(chunk.upper())
            prefixes.add(chunk.lower())
            prefixes.add(chunk.capitalize())
    elif len(clean_name) > 0:
        prefixes.add(clean_name.upper())
        prefixes.add(clean_name.lower())
        prefixes.add(clean_name.capitalize())
        
    for p in COMMON_INDIAN_PREFIXES:
        prefixes.add(p)
        prefixes.add(p.lower())

    return list(prefixes)

# ==========================================
# UI & MAIN APPLICATON LAYOUT
# ==========================================
st.markdown('<div class="rgb-container">', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload Password Protected PDF File", type=["pdf"])

mode = st.radio(
    "SELECT RECOVERY MODE:",
    options=["Name + 4 Digits", "8-Digit Numbers Only"]
)

name_hint = ""
if mode == "Name + 4 Digits":
    name_hint = st.text_input("ENTER NAME HINT (e.g. Vikas):", value="")

st.markdown('</div>', unsafe_allow_html=True)

start_recovery = st.button("🚀 START ULTRA RECOVERY PROCESS")

# ==========================================
# RECOVERY EXECUTION CONTROLLER
# ==========================================
if start_recovery:
    if not uploaded_file:
        st.error("❌ Please upload a protected PDF file first.")
    else:
        pdf_bytes = uploaded_file.read()
        status_box = st.empty()
        progress_bar = st.progress(0)
        
        found_password = None
        unlocked_pdf_stream = None
        start_time = time.time()

        if mode == "Name + 4 Digits":
            prefixes = generate_name_prefixes(name_hint)
            total_prefixes = len(prefixes)
            total_combinations = total_prefixes * 10000
            tested_count = 0

            status_box.info(f"🔍 Starting scan with {total_prefixes} prefix patterns (~{total_combinations:,} combinations)...")

            for prefix in prefixes:
                for num in range(10000):
                    tested_count += 1
                    pwd = f"{prefix}{num:04d}"

                    if tested_count % 2000 == 0:
                        elapsed = time.time() - start_time
                        speed = int(tested_count / elapsed) if elapsed > 0 else 0
                        progress_bar.progress(min(tested_count / total_combinations, 1.0))
                        status_box.text(f"⏳ Testing: {pwd} | Tested: {tested_count:,} / {total_combinations:,} | Speed: {speed} pwd/s")

                    unlocked_stream = verify_and_unlock(pdf_bytes, pwd)
                    if unlocked_stream:
                        found_password = pwd
                        unlocked_pdf_stream = unlocked_stream
                        break
                if found_password:
                    break

        elif mode == "8-Digit Numbers Only":
            total_combinations = 100000000
            status_box.info("🔢 Starting 8-Digit Sequential Brute-Force (00000000 to 99999999)...")

            for num in range(total_combinations):
                pwd = f"{num:08d}"

                if num % 2000 == 0:
                    elapsed = time.time() - start_time
                    speed = int(num / elapsed) if elapsed > 0 else 0
                    progress_bar.progress(min(num / total_combinations, 1.0))
                    status_box.text(f"⏳ Testing: {pwd} | Tested: {num:,} / {total_combinations:,} | Speed: {speed} pwd/s")

                unlocked_stream = verify_and_unlock(pdf_bytes, pwd)
                if unlocked_stream:
                    found_password = pwd
                    unlocked_pdf_stream = unlocked_stream
                    break

        progress_bar.progress(1.0)

        if found_password and unlocked_pdf_stream:
            status_box.empty()
            st.balloons()
            st.success(f"🎉 **PASSWORD FOUND SUCCESSFULLY!**\n\nVerified Password: `{found_password}`")
            
            st.download_button(
                label="📥 DOWNLOAD UNLOCKED PDF",
                data=unlocked_pdf_stream.getvalue(),
                file_name=f"unlocked_{uploaded_file.name}",
                mime="application/pdf"
            )
        else:
            status_box.empty()
            st.error("❌ Recovery Failed. Password not found within the selected mode criteria.")
