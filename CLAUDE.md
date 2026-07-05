# Password Safe — CipherVault

An encrypted password safe that stores all passwords on the local device, keeping each logically secure and easily accessible. Branded as **CipherVault**.

## Claude's Role

My role is to build and improve the Python (Flask) backend and frontend for this password manager, implementing encryption logic, file management, and connecting it to the UI.

## Process

1. `01 Brainstorming & Architecture/` — Architecture design and tech stack setup.
2. `02 UI Implementation/` — Frontend UI (HTML, CSS, JS).
3. `03 Backend Building/` — Python Flask backend with Argon2id + AES-256-GCM encryption.
4. `04 Testing & Security/` — Security reviews and testing to ensure production-grade safety.

## Key People

Bilal — Product Owner, UI Designer, and Developer

## Folder Structure

- `01 Brainstorming & Architecture/` — Ideas, system architecture, and technology planning.
- `02 UI Implementation/` — Frontend assets, styles, and UI code.
- `03 Backend Building/` — Python Flask backend (`app.py`, `crypto_utils.py`, `requirements.txt`), encryption logic, vault file management.
- `04 Testing & Security/` — Test suites, security audits, and QA notes.
- `05 System/` — Scripts, configs, reusable processes.
- `06 Skills/` — Skill markdown files for this specific project.
- `07 Attachments/` — Images, screenshots, PDFs.
- `08 Iteration Logs/` — Notes on improvements and future updates.
- `stitch_emerald_vault_dashboard/` — Design reference mockup and design system.

## Rules & Conventions

- **`(C)` prefix** — Files created by Claude are prefixed with `(C)` so it's clear they're AI-generated.
- **Editing rule** — Before editing any file without the `(C)` prefix, ask for permission first.
- **Skills** — All reusable scripts/automations are saved as markdown files in the Skills folder, NOT as Claude Code skills.
- **Tech Stack** — Python 3.11+, Flask, cryptography library, argon2-cffi. Frontend: vanilla HTML/CSS/JS served by Flask.

## Commands

```bash
pip install -r requirements.txt
python app.py
# Opens at http://127.0.0.1:5000
```

## Current Status

> **Last updated:** 2026-06-26
> **Status:** V1 functional — Flask backend with encryption + frontend UI working. No tests yet. `.gitignore` needed. See `01 Brainstorming & Architecture/(C) Architecture.md` for full spec.

<!-- TODO: Add unit tests for crypto_utils.py, add .gitignore, add run script -->
