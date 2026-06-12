import socket
import io
import base64
import time
import qrcode,json
from flask import Flask, request, render_template_string, redirect, url_for, Response

app = Flask(__name__)
FILE_PATH = "shared_document.txt"

# A global variable to keep track of file version changes
file_version = 0

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shared Real-Time Pad</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f4f4f9; }
        .container { max-width: 800px; margin: auto; }
        textarea { width: 100%; height: 400px; padding: 10px; font-size: 16px; border: 1px solid #ccc; border-radius: 5px; box-sizing: border-box; }
        .btn { border: none; padding: 10px 20px; font-size: 16px; border-radius: 5px; cursor: pointer; margin-top: 10px; text-decoration: none; display: inline-block; }
        .btn-blue { background-color: #007bff; color: white; }
        .btn-blue:hover { background-color: #0056b3; }
        .btn-green { background-color: #28a745; color: white; margin-left: 10px; }
        .btn-green:hover { background-color: #218838; }
        .header-section { display: flex; justify-content: space-between; align-items: center; }
        .info { font-size: 12px; color: #28a745; font-weight: bold; margin-top: -10px; margin-bottom: 15px; }
        .modal { display: none; position: fixed; z-index: 1; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.5); }
        .modal-content { background-color: white; margin: 15% auto; padding: 20px; border-radius: 10px; width: 300px; text-align: center; position: relative; }
        .close { position: absolute; right: 15px; top: 10px; font-size: 24px; cursor: pointer; color: #aaa; }
        .close:hover { color: black; }
        .qr-img { width: 200px; height: 200px; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header-section">
            <h2>📝 Shared Real-Time Pad</h2>
            <button class="btn btn-green" onclick="openModal()">📱 Share via QR</button>
        </div>
        <p class="info">● Live sync active. No need to refresh!</p>
        
        <form method="POST" action="/save" id="padForm">
            <textarea name="content" id="padField">{{ content }}</textarea>
            <br>
            <input type="submit" class="btn btn-blue" value="Save Changes">
        </form>
    </div>

    <div id="qrModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeModal()">&times;</span>
            <h3>Scan to open on phone</h3>
            <img class="qr-img" src="data:image/png;base64,{{ qr_base64 }}" alt="QR Code">
            <p style="font-size: 11px; color: #999; word-break: break-all;">{{ network_url }}</p>
        </div>
    </div>

    <script>
        const padField = document.getElementById('padField');

        // Modal triggers
        function openModal() { document.getElementById("qrModal").style.display = "block"; }
        function closeModal() { document.getElementById("qrModal").style.display = "none"; }
        window.onclick = function(event) {
            let modal = document.getElementById("qrModal");
            if (event.target == modal) { modal.style.display = "none"; }
        }

        // ⚡ REAL-TIME STREAM LISTENER ⚡
        // This opens a continuous listener with the python backend
        const eventSource = new EventSource("/stream");
        
        eventSource.onmessage = function(event) {
            // Parse the data sent by python
            const data = JSON.parse(event.data);
            
            // Only update the textarea if the user isn't actively typing inside it
            // This prevents the cursor from jumping around while you type
            if (document.activeElement !== padField) {
                padField.value = data.content;
            }
        };
    </script>
</body>
</html>
"""

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def generate_qr_base64(url):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def read_file():
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Type anything here... All devices can see and edit this!"

@app.route('/')
def index():
    content = read_file()
    local_ip = get_local_ip()
    network_url = f"http://{local_ip}:5000"
    qr_base64 = generate_qr_base64(network_url)
    return render_template_string(HTML_TEMPLATE, content=content, qr_base64=qr_base64, network_url=network_url)

@app.route('/save', methods=['POST'])
def save():
    global file_version
    new_content = request.form.get('content', '')
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    # Increment the version so the stream loop knows it's time to broadcast an update
    file_version += 1
    return redirect(url_for('index'))

# ⚡ THE BACKEND STREAM ENDPOINT ⚡
@app.route('/stream')
def stream():
    def event_stream():
        global file_version
        last_seen_version = file_version
        
        while True:
            # Check if someone updated the version tracker
            if file_version > last_seen_version:
                last_seen_version = file_version
                content = read_file()
                
                # Safely convert the string to a JSON structure to handle newlines and quotes perfectly
                json_data = json.dumps({"content": content})
                
                # Format required by Server-Sent Events protocol
                yield f"data: {json_data}\n\n"
            
            time.sleep(0.5) # Sleep half a second before re-checking to keep CPU usage low
            
    return Response(event_stream(), mimetype="text/event-stream")
    
if __name__ == '__main__':
    local_ip = get_local_ip()
    port = 5000
    app.run(host='0.0.0.0', port=port, debug=True)