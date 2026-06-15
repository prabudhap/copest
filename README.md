# 📝 Copest: Collaborative Real-Time Text Pad

A lightweight, collaborative, real-time scratchpad server built in Python using **Flask** and **Server-Sent Events (SSE)**. It allows multiple devices on the same local network to view and edit a shared text document simultaneously without page refreshes. It also generates a QR code on the homepage, making it incredibly simple for mobile devices to join in.

---

## ✨ Features

- **Real-Time Synchronization:** Updates are pushed instantly to all connected clients using Server-Sent Events (`EventSource`).
- **Cursor Focus Protection:** The textarea only updates when you are not actively typing in it, preventing the cursor from jumping and disrupting your edits.
- **Auto-Discovery & QR Code Sharing:** Automatically detects the host machine's local IP address and displays a QR code + URL so other devices on the same Wi-Fi network can scan and join.
- **Persistence:** All modifications are saved to a local file (`shared_document.txt`) automatically.

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7 or higher

### Step-by-Step Setup

1. **Clone or Navigate to the Directory:**
   ```bash
   cd "d:/vibhu/some stuff/vib/projects/copest"
   ```

2. **Create and Activate a Virtual Environment (Optional but Recommended):**
   - **On Windows (PowerShell):**
     ```powershell
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```
   - **On macOS/Linux:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install Dependencies:**
   Install the required packages using the generated `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 How to Run

Start the application by running:
```bash
python copest.py
```

Upon launching, the Flask app will run on port `5000` and bind to all network interfaces (`0.0.0.0`), allowing external access.

---

## 📱 How to Use

1. **Access Locally:** Open your browser and navigate to `http://localhost:5000`.
2. **Access on Other Devices (Mobile/Tablet):**
   - Ensure your other devices are connected to the same Wi-Fi / Local Area Network (LAN).
   - Click the **"Share via QR"** button on the page.
   - Scan the displayed QR code with your phone/tablet camera, or type the printed IP address (e.g., `http://192.168.x.x:5000`) into your mobile browser.
3. **Collaborate:** Start typing! Your changes will be synced to all other connected browsers when you click **"Save Changes"**.

---

## 🗂️ File Directory structure
- [copest.py](file:///d:/vibhu/some%20stuff/vib/projects/copest/copest.py) - Main application file (backend and frontend UI template).
- [requirements.txt](file:///d:/vibhu/some%20stuff/vib/projects/copest/requirements.txt) - List of dependency libraries.
- [shared_document.txt](file:///d:/vibhu/some%20stuff/vib/projects/copest/shared_document.txt) - The file where the shared text content is persisted.
