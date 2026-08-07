import os
import io
import time
import pikepdf
from flask import Flask, request, jsonify, render_template, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit uploads to 16MB

# Common surnames dictionary for Mode 1
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
    
    # Deduplicate preserving order
    seen = set()
    return [x for x in prefixes if not (x in seen or seen.add(x))]

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
    
    # Brute-force execution logic
    matched_password = None
    unlocked_stream = None
    
    start_time = time.time()
    
    if mode == 'mode1':
        prefixes = generate_mode1_prefixes(hint)
        for prefix in prefixes:
            for i in range(10000):
                # Timeout safeguard for Render web workers
                if time.time() - start_time > 110:
                    return jsonify({"status": "error", "message": "Execution limit reached. Try a specific hint."}), 408
                
                pwd = f"{prefix}{i:04d}"
                try:
                    with pikepdf.open(io.BytesIO(pdf_bytes), password=pwd) as pdf:
                        out = io.BytesIO()
                        pdf.save(out)
                        out.seek(0)
                        matched_password = pwd
                        unlocked_stream = out.getvalue()
                        break
                except pikepdf.PasswordError:
                    continue
            if matched_password:
                break
                
    elif mode == 'mode2':
        # Limited numeric loop to prevent Web Service timeout
        for i in range(1000000): 
            if time.time() - start_time > 110:
                return jsonify({"status": "error", "message": "Time limit exceeded"}), 408
                
            pwd = f"{i:08d}"
            try:
                with pikepdf.open(io.BytesIO(pdf_bytes), password=pwd) as pdf:
                    out = io.BytesIO()
                    pdf.save(out)
                    out.seek(0)
                    matched_password = pwd
                    unlocked_stream = out.getvalue()
                    break
            except pikepdf.PasswordError:
                continue

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
