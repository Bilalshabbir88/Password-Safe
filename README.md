# 🔐 CipherVault (Password Safe)

## 📌 Project Overview
CipherVault is a locally hosted, highly secure password manager designed to store your sensitive credentials directly on your own device. Built with military-grade encryption, this tool ensures your data never touches a remote server unless you explicitly choose to back it up.

## ⚙️ Tech Stack
- **Backend:** Python 3.11+, Flask
- **Frontend:** Vanilla HTML, CSS, JavaScript (Stitch Emerald Dashboard Design)
- **Encryption:** `AES-256-GCM` (Advanced Encryption Standard)
- **Key Derivation:** `Argon2id` (State-of-the-art password hashing)
- **Data Storage:** Local encrypted vault files (`.cvlt`)

## 🧠 Core Security Features
1. **Zero-Knowledge Architecture:** Your master password is never saved anywhere. If you lose it, the vault is mathematically impossible to decrypt.
2. **Argon2id Key Derivation:** Defends against GPU brute-force attacks and side-channel attacks by adjusting memory and CPU cost factors.
3. **AES-256-GCM Encryption:** Provides both confidentiality and authenticity. If a vault file is tampered with by a malicious actor, the system will reject it automatically.

## 🚀 How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/Bilalshabbir88/Password-Safe.git
cd Password-Safe/03\ Backend\ Building
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv .venv
# On Windows:
.\.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Start the Vault Server
```bash
python app.py
```
*The local server will start. Open your browser and navigate to `http://127.0.0.1:5000` to access your vault.*
