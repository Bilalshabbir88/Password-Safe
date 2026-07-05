# CipherVault v1 — Architecture (Python Revision)

> **Decisions Locked:** 2026-06-25
> - Stack Pivot: Switched from Rust/Tauri to Python/Flask + Vanilla Web UI for frictionless development
> - Vault file location: `%APPDATA%/CipherVault/`
> - V1 scope: Password manager only (no credit cards, secure notes, TOTP, security health)
> - Encryption: Argon2id KDF → AES-256-GCM
> - Frontend: Dark emerald theme from DESIGN.md reference
> - V2 features removed entirely from sidebar

## Tech Stack
| Layer | Technology | Why |
|-------|-----------|-----|
| Backend | **Python (Flask)** | Simple, fast to develop, handles local file I/O easily |
| Frontend | **HTML/CSS/JS** (vanilla) | Matches the existing mockup; served by Flask |
| Encryption | **cryptography (AESGCM) + argon2-cffi** | Industry-standard crypto for Python |
| Storage | **Single encrypted `.vault` file** | Simple, portable, easy to backup |

## Encryption Architecture

### Flow
```
Master Password → Argon2id(salt, m=64MB, t=3, p=4) → 256-bit Key
Key + Nonce → AES-256-GCM Encrypt/Decrypt → JSON vault data
```

### Security Properties
- Memory-hard KDF prevents GPU brute-force
- Authenticated encryption prevents tampering
- Fresh nonce on every save
- Atomic file writes prevent corruption

## API Endpoints (Python → JS)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/status` | Check if vault exists |
| POST | `/api/create` | First-time vault setup |
| POST | `/api/unlock` | Decrypt and load vault into memory |
| POST | `/api/lock` | Clear decrypted data from memory |
| GET | `/api/entries` | Get all entries (requires unlock) |
| POST | `/api/entries` | Add new password |
| PUT | `/api/entries/<id>` | Edit existing entry |
| DELETE | `/api/entries/<id>` | Remove entry |

## Project Structure
```
Password Safe/
├── 01 Brainstorming & Architecture/
│   └── (C) Architecture.md
├── 02 UI Implementation/
│   ├── index.html
│   ├── style.css
│   └── app.js
└── 03 Backend Building/
    ├── app.py
    ├── crypto_utils.py
    └── requirements.txt
```
