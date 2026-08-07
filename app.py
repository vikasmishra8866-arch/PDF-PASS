import streamlit as st
import pikepdf
import io

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Deep Ocean Hydro | PDF Recovery",
    page_icon="🔑",
    layout="centered"
)

# --- DEEP OCEAN HYDRO STYLING (NEW DESIGN SYSTEM) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    /* Primary Background Hydro Pulse */
    .stApp {
        background: linear-gradient(135deg, #031329 0%, #082247 50%, #031329 100%) !important;
        background-size: 200% 200% !important;
        animation: hydroPulse 10s ease infinite !important;
        color: #f8fafc !important;
    }

    @keyframes hydroPulse {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }

    /* Card Containers */
    div.stMarkdownContainer > div, .hydro-card {
        animation: fadeInUp 0.5s ease-out forwards;
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(12px) scale(0.98); }
        to { opacity: 1; transform: translateY(0) scale(1); }
    }

    .hydro-header {
        background-color: #0b1d3a;
        border: 1px solid rgba(6, 182, 212, 0.3);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(3, 19, 41, 0.7);
    }

    .hydro-header-title {
        color: #f8fafc;
        font-size: 32px;
        font-weight: 900;
        letter-spacing: 2px;
        margin: 0;
    }

    .hydro-header-sub {
        color: #06b6d4;
        font-weight: 600;
        font-size: 14px;
        margin-top: 6px;
    }

    .hydro-container {
        background-color: #0b1d3a;
        border: 1px solid rgba(6, 182, 212, 0.2);
        border-radius: 16px;
        padding: 16px 20px;
        margin-bottom: 20px;
        color: #94a3b8;
        font-weight: 600;
        font-size: 14px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }

    /* Inputs Styling */
    .stTextInput input {
        background-color: #031329 !important;
        color: #22d3ee !important;
        border: 1px solid #1e3a8a !important;
        border-radius: 12px !important;
        height: 48px !important;
        font-size: 18px !important;
        font-weight: 800 !important;
        letter-spacing: 1px !important;
        padding-left: 14px !important;
    }

    .stTextInput input:focus {
        border-color: #06b6d4 !important;
        box-shadow: 0 0 0 2px rgba(6, 182, 212, 0.4) !important;
    }

    /* Radio Buttons */
    div[data-testid="stRadio"] label {
        color: #22d3ee !important;
        font-size: 16px !important;
        font-weight: 800 !important;
        cursor: pointer;
    }
    
    div[data-testid="stRadio"] p {
        color: #94a3b8 !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }

    /* Primary Button */
    div.stButton > button:first-child {
        background: #06b6d4 !important;
        color: #031329 !important;
        border: none !important;
        font-weight: 900 !important;
        font-size: 18px !important;
        height: 52px !important;
        border-radius: 12px !important;
        width: 100% !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 0 15px rgba(6, 182, 212, 0.3) !important;
    }

    div.stButton > button:first-child:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 0 22px rgba(6, 182, 212, 0.6) !important;
        background: #22d3ee !important;
    }

    /* Print Protocol */
    @media print {
        .stButton, div[data-testid="stRadio"], .stFileUploader {
            display: none !important;
        }
        .stApp {
            background: #ffffff !important;
            color: #000000 !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER COMPONENT ---
st.markdown("""
    <div class="hydro-header">
        <div class="hydro-header-title">PDF ULTRA RECOVERY</div>
        <div class="hydro-header-sub">⚡ DEEP OCEAN HYDRO ENGINE</div>
    </div>
""", unsafe_allow_html=True)

# --- RECOVERY MODE SELECTION ---
st.markdown('<div class="hydro-container">⚙️ RECOVERY SCAN PATTERN</div>', unsafe_allow_html=True)
recovery_mode = st.radio("", ["Name + 4 Digits", "8-Digit Numbers Only"], horizontal=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- UPLOADER COMPONENT ---
st.markdown('<div class="hydro-container">🛰️ SATELLITE SCANNER ACTIVE</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["pdf"], label_visibility="collapsed")

custom_hint = ""
if recovery_mode == "Name + 4 Digits":
    st.markdown('<div class="hydro-container">💡 NAME HINT ENGINE</div>', unsafe_allow_html=True)
    custom_hint = st.text_input("hint_input", placeholder="ENTER NAME HINT (E.G. VIKAS)", label_visibility="collapsed").strip()

# --- HARDCODED DICTIONARY ARRAY ---
COMMON_NAMES = [
    "AMIT", "ANIL", "ARUN", "AJAY", "ABHI", "AKAS", "AMAN", "ANSH", "ANUP", "ASHU", 
    "DEEP", "DEVA", "DINE", "GAUR", "GURU", "HARI", "HEMA", "INDU", "JAYA", "JAYE", 
    "JYOT", "KAMA", "KAPI", "KIRA", "KUNA", "LALU", "MADH", "MANO", "MEEN", "MOHA", 
    "MUKA", "NEER", "NITI", "PANK", "PAWA", "PIYU", "POOJ", "PRAD", "PRAK", "PRAM", 
    "RAHU", "RAJA", "RAJE", "RAKE", "RAMA", "RANI", "RAVI", "RISH", "ROHA", "ROHI", 
    "SACH", "SAME", "SANJ", "SANT", "SARA", "SATI", "SHIV", "SHYA", "SONU", "SUMI", 
    "SUNI", "SURA", "TARA", "UMES", "VIKA", "VIMA", "VINA", "VINO", "VIVE", "YOGE", 
    "KUMA", "SING", "MISH", "SHAR", "VERM", "GUPT", "YADA", "PATE", "CHAU", "KHAN",
    "RAWA", "NEGI", "BISH", "SAIN", "DHIL", "SIDD", "KAUR", "BALA", "ALOK", "ASIF",
    "BABU", "BALI", "BINK", "CHET", "DAKS", "ESHA", "FAIZ", "GOPL", "HARS", "ISHA",
    "JNAT", "KAVS", "LOKS", "MAHE", "NARE", "OMPR", "PRAT", "QASH", "RASH", "SUDH"
]

# --- EXECUTION PIPELINE ---
if uploaded_file and st.button("🚀 EXECUTE RECOVERY ENGINE"):
    pdf_bytes = uploaded_file.read()
    found = False
    status_box = st.empty()
    
    try:
        if recovery_mode == "Name + 4 Digits":
            search_list = []
            if custom_hint and len(custom_hint) >= 4:
                for i in range(len(custom_hint) - 3):
                    chunk = custom_hint[i:i+4]
                    search_list.extend([chunk, chunk.upper(), chunk.lower()])
            
            for name in COMMON_NAMES:
                if name not in search_list:
                    search_list.extend([name, name.lower()])
            
            search_list = list(dict.fromkeys(search_list))
            bar = st.progress(0)
            
            for idx, prefix in enumerate(search_list):
                status_box.markdown(f"📡 **Scanning:** `{prefix}XXXX`...")
                bar.progress((idx + 1) / len(search_list))
                
                for n in range(10000):
                    password = f"{prefix}{n:04d}"
                    try:
                        with pikepdf.open(io.BytesIO(pdf_bytes), password=password) as pdf:
                            test_output = io.BytesIO()
                            pdf.save(test_output)
                            
                            st.balloons()
                            st.success(f"🔓 VERIFIED MATCH FOUND: {password}")
                            found = True
                            st.download_button(
                                "📥 DOWNLOAD UNLOCKED PDF",
                                test_output.getvalue(),
                                f"Unlocked_{password}.pdf"
                            )
                            break
                    except:
                        continue
                if found:
                    break

        else: # 8-Digit Mode
            status_box.info("📡 Running 8-Digit Scan...")
            for n in range(100000000):
                password = f"{n:08d}"
                if n % 2000 == 0:
                    status_box.markdown(f"📡 **Testing:** `{password}`...")
                try:
                    with pikepdf.open(io.BytesIO(pdf_bytes), password=password) as pdf:
                        test_output = io.BytesIO()
                        pdf.save(test_output)
                        
                        st.balloons()
                        st.success(f"🔓 VERIFIED MATCH FOUND: {password}")
                        found = True
                        st.download_button(
                            "📥 DOWNLOAD UNLOCKED PDF",
                            test_output.getvalue(),
                            f"Unlocked_{password}.pdf"
                        )
                        break
                except:
                    continue
                if found:
                    break

        if not found:
            st.error("❌ Password not found or scan failed.")

    except Exception as e:
        st.error(f"Execution Error: {e}")

st.markdown("""
    <script>
    function sendHeight() {
        var height = document.body.scrollHeight;
        parent.postMessage({ type: 'resize', height: height }, '*');
    }
    window.addEventListener('load', sendHeight);
    window.addEventListener('resize', sendHeight);
    </script>
""", unsafe_allow_html=True)
