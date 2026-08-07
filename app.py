import os
import io
import time
import pypdf
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

HARDCODED_DICT = [
    "AMIT", "ANIL", "KUMA", "MISH", "SING", "VIKA", "PATE", "GUPT", "YADA", "VERM",
    "SHAR", "RAME", "SURE", "RAJE", "DINE", "MANT", "JOSH", "ROHI", "RAHU", "GAUR"
]

def generate_mode1_prefixes(hint):
    prefixes = []
    if hint and len(hint) >= 4:
        for i in range(len(hint) - 3):
            chunk = hint[i:i+4]
            prefixes.extend([chunk, chunk.upper(), chunk.lower()])
    for d in HARDCODED_DICT:
        prefixes.extend([d.upper(), d.lower()])
    
    seen = set()
    return [x for x in prefixes if not (x in seen or seen.add(x))]

def check_pdf_password(pdf_bytes, password):
    try:
        reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
        if reader.is_encrypted:
            # decrypt returns True (or 1/2) if password is correct
            if reader.decrypt(password):
                writer = pypdf.PdfWriter()
                for page in reader.pages:
                    writer.add_page(page)
                out = io.BytesIO()
                writer.write(out)
                out.seek(0)
                return True, out.getvalue()
            return False, None
        else:
            return True, pdf_bytes
    except Exception:
        return False, None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/crack', methods=['POST'])
def crack_pdf():
    if 'pdf' not in request.files:
        return jsonify({"status": "error", "message": "No file uploaded"}), 400
    
    file = request.files['pdf']
    mode = request.form.get('mode', 'mode1')
    hint = request.form.get('hint', '').strip()

    if file.filename == '':
        return jsonify({"status": "error", "message": "No file selected"}), 400

    pdf_bytes = file.read()
    matched_password = None
    start_time = time.time()
    
    if mode == 'mode1':
        prefixes = generate_mode1_prefixes(hint)
        for prefix in prefixes:
            for i in range(10000):
                if time.time() - start_time > 110:
                    return jsonify({"status": "error", "message": "Execution time limit reached."}), 408
                
                pwd = f"{prefix}{i:04d}"
                success, _ = check_pdf_password(pdf_bytes, pwd)
                if success:
                    matched_password = pwd
                    break
            if matched_password:
                break
                
    elif mode == 'mode2':
        for i in range(1000000): 
            if time.time() - start_time > 110:
                return jsonify({"status": "error", "message": "Execution time limit reached."}), 408
                
            pwd = f"{i:08d}"
            success, _ = check_pdf_password(pdf_bytes, pwd)
            if success:
                matched_password = pwd
                break

    if matched_password:
        return jsonify({
            "status": "success",
            "password": matched_password,
            "message": "Password recovered successfully!"
        })
    else:
        return jsonify({"status": "failed", "message": "Password not found in search space"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
