function toggleHint() {
    const mode = document.getElementById('mode').value;
    const container = document.getElementById('hintContainer');
    if (mode === 'mode1') {
        container.classList.remove('hidden');
    } else {
        container.classList.add('hidden');
    }
}

document.getElementById('crackForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const pdfInput = document.getElementById('pdfFile');
    const mode = document.getElementById('mode').value;
    const hint = document.getElementById('hint').value;
    const submitBtn = document.getElementById('submitBtn');
    const tvContainer = document.getElementById('tvContainer');
    const terminal = document.getElementById('terminalLog');
    const resultBox = document.getElementById('resultBox');
    const passResult = document.getElementById('passResult');

    if (!pdfInput.files[0]) return;

    // UI State Updating
    submitBtn.disabled = true;
    tvContainer.classList.remove('hidden');
    resultBox.classList.add('hidden');
    terminal.innerHTML = '<div>> STARTING BRUTE FORCE SEQUENCE...</div>';

    // Matrix TV Visual FX Stream
    let streamInterval = setInterval(() => {
        let fakeCand = mode === 'mode1' 
            ? (hint || 'VIKA').toUpperCase() + Math.floor(1000 + Math.random() * 9000)
            : Math.floor(10000000 + Math.random() * 90000000);
            
        let line = document.createElement('div');
        line.textContent = `> TESTING CANDIDATE: [ ${fakeCand} ] ... FAIL`;
        terminal.appendChild(line);
        terminal.scrollTop = terminal.scrollHeight;
    }, 80);

    // Call Render Flask Backend API
    const formData = new FormData();
    formData.append('pdf', pdfInput.files[0]);
    formData.append('mode', mode);
    formData.append('hint', hint);

    try {
        const response = await fetch('/api/crack', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        clearInterval(streamInterval);

        if (response.ok && data.status === 'success') {
            let successLine = document.createElement('div');
            successLine.className = 'text-emerald-400 font-bold';
            successLine.textContent = `> SUCCESS! MATCH VERIFIED: ${data.password}`;
            terminal.appendChild(successLine);

            passResult.textContent = data.password;
            resultBox.classList.remove('hidden');
        } else {
            let failLine = document.createElement('div');
            failLine.className = 'text-red-400 font-bold';
            failLine.textContent = `> ERROR: ${data.message || 'PASSWORD NOT FOUND'}`;
            terminal.appendChild(failLine);
        }
    } catch (error) {
        clearInterval(streamInterval);
        let errLine = document.createElement('div');
        errLine.className = 'text-red-400 font-bold';
        errLine.textContent = `> SYSTEM ERROR: CONNECTION TIMED OUT`;
        terminal.appendChild(errLine);
    } finally {
        submitBtn.disabled = false;
        terminal.scrollTop = terminal.scrollHeight;
    }
});

// Dynamic iFrame Resize Handler
function sendIframeHeight() {
    if (window.parent && window.parent !== window) {
        window.parent.postMessage({ type: 'resize', height: document.body.scrollHeight }, '*');
    }
}
window.addEventListener('load', sendIframeHeight);
window.addEventListener('resize', sendIframeHeight);
