import os
import json
import uuid
import struct
from datetime import datetime
from flask import Flask, request, jsonify, render_template

from crypto_utils import generate_salt, derive_key, encrypt_data, decrypt_data

# Set up Flask to serve static files and templates from the UI folder
UI_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '02 UI Implementation'))
app = Flask(__name__, template_folder=UI_FOLDER, static_folder=UI_FOLDER, static_url_path='')

# Vault file location
APPDATA_DIR = os.getenv('APPDATA')
if not APPDATA_DIR:
    # Fallback if APPDATA is not found (e.g. Linux/Mac testing)
    APPDATA_DIR = os.path.expanduser('~')
    
VAULT_DIR = os.path.join(APPDATA_DIR, 'CipherVault')
VAULT_PATH = os.path.join(VAULT_DIR, 'vault.cvlt')

# In-memory state (only holds data when unlocked)
app_state = {
    'unlocked': False,
    'key': None,
    'salt': None,
    'vault_data': None
}

MAGIC = b"CVLT"
VERSION = 1

def write_vault_to_disk():
    """Serializes, encrypts, and atomically writes the vault to disk."""
    if not app_state['unlocked']:
        raise Exception("Vault is locked")
        
    plaintext_json = json.dumps(app_state['vault_data']).encode('utf-8')
    nonce, ciphertext = encrypt_data(app_state['key'], plaintext_json)
    
    # Binary Format: MAGIC(4) + Version(2) + ArgonParams(4+2+1) + Salt(16) + Nonce(12) + Ciphertext
    header = struct.pack('<4sHIHB', MAGIC, VERSION, 65536, 3, 4)
    file_data = header + app_state['salt'] + nonce + ciphertext
    
    os.makedirs(VAULT_DIR, exist_ok=True)
    temp_path = VAULT_PATH + '.tmp'
    
    with open(temp_path, 'wb') as f:
        f.write(file_data)
        
    # Atomic replace
    os.replace(temp_path, VAULT_PATH)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({
        'vault_exists': os.path.exists(VAULT_PATH),
        'unlocked': app_state['unlocked']
    })

@app.route('/api/create', methods=['POST'])
def create_vault():
    if os.path.exists(VAULT_PATH):
        return jsonify({'error': 'Vault already exists'}), 400
        
    data = request.json
    password = data.get('password')
    if not password:
        return jsonify({'error': 'Password required'}), 400
        
    salt = generate_salt()
    key = derive_key(password, salt)
    
    now = datetime.utcnow().isoformat() + 'Z'
    initial_data = {
        'version': VERSION,
        'created_at': now,
        'updated_at': now,
        'entries': []
    }
    
    app_state['unlocked'] = True
    app_state['key'] = key
    app_state['salt'] = salt
    app_state['vault_data'] = initial_data
    
    try:
        write_vault_to_disk()
        return jsonify({'success': True})
    except Exception as e:
        app_state['unlocked'] = False
        return jsonify({'error': str(e)}), 500

@app.route('/api/unlock', methods=['POST'])
def unlock_vault():
    if not os.path.exists(VAULT_PATH):
        return jsonify({'error': 'Vault not found'}), 404
        
    password = request.json.get('password')
    if not password:
        return jsonify({'error': 'Password required'}), 400
        
    try:
        with open(VAULT_PATH, 'rb') as f:
            data = f.read()
            
        if data[:4] != MAGIC:
            return jsonify({'error': 'Invalid vault file'}), 400
            
        salt = data[13:29]
        nonce = data[29:41]
        ciphertext = data[41:]
        
        key = derive_key(password, salt)
        
        try:
            plaintext = decrypt_data(key, nonce, ciphertext)
            vault_data = json.loads(plaintext.decode('utf-8'))
            
            app_state['unlocked'] = True
            app_state['key'] = key
            app_state['salt'] = salt
            app_state['vault_data'] = vault_data
            
            return jsonify({'success': True})
        except Exception:
            # Cryptography raises an exception on bad tag (wrong password)
            return jsonify({'error': 'Incorrect password or corrupted vault'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/lock', methods=['POST'])
def lock_vault():
    # In Python we can't easily securely zero out memory like Rust's zeroize, 
    # but we drop the references to let the GC clean it up.
    app_state['unlocked'] = False
    app_state['key'] = None
    app_state['salt'] = None
    app_state['vault_data'] = None
    return jsonify({'success': True})

@app.route('/api/entries', methods=['GET', 'POST'])
def handle_entries():
    if not app_state['unlocked']:
        return jsonify({'error': 'Vault is locked'}), 401
        
    if request.method == 'GET':
        return jsonify(app_state['vault_data']['entries'])
        
    if request.method == 'POST':
        entry = request.json
        now = datetime.utcnow().isoformat() + 'Z'
        entry['id'] = str(uuid.uuid4())
        entry['created_at'] = now
        entry['updated_at'] = now
        
        app_state['vault_data']['entries'].append(entry)
        app_state['vault_data']['updated_at'] = now
        write_vault_to_disk()
        return jsonify(entry), 201

@app.route('/api/entries/<entry_id>', methods=['PUT', 'DELETE'])
def handle_single_entry(entry_id):
    if not app_state['unlocked']:
        return jsonify({'error': 'Vault is locked'}), 401
        
    entries = app_state['vault_data']['entries']
    
    if request.method == 'DELETE':
        app_state['vault_data']['entries'] = [e for e in entries if e.get('id') != entry_id]
        app_state['vault_data']['updated_at'] = datetime.utcnow().isoformat() + 'Z'
        write_vault_to_disk()
        return jsonify({'success': True})
        
    if request.method == 'PUT':
        for i, e in enumerate(entries):
            if e.get('id') == entry_id:
                updated_entry = request.json
                updated_entry['id'] = entry_id
                updated_entry['created_at'] = e.get('created_at')
                updated_entry['updated_at'] = datetime.utcnow().isoformat() + 'Z'
                entries[i] = updated_entry
                app_state['vault_data']['updated_at'] = updated_entry['updated_at']
                write_vault_to_disk()
                return jsonify(updated_entry)
        return jsonify({'error': 'Entry not found'}), 404

if __name__ == '__main__':
    # When running locally, ensure the UI folder exists
    os.makedirs(UI_FOLDER, exist_ok=True)
    # Create a simple placeholder index.html if it doesn't exist
    index_path = os.path.join(UI_FOLDER, 'index.html')
    if not os.path.exists(index_path):
        with open(index_path, 'w') as f:
            f.write("<h1>CipherVault Web UI Loading...</h1>")
            
    debug_mode = os.getenv('CIPHERVAULT_DEBUG', '').lower() in ('1', 'true', 'yes')
    print(f"Starting CipherVault server on http://127.0.0.1:5000")
    print(f"Vault location: {VAULT_PATH}")
    app.run(host='127.0.0.1', port=5000, debug=debug_mode)
