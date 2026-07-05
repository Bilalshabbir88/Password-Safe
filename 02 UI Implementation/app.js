// app.js - Main Application Logic

const app = {
    state: {
        entries: [],
        currentEntry: null,
        passVisible: false
    },

    async init() {
        try {
            const status = await api.status();
            if (status.unlocked) {
                this.loadDashboard();
            } else if (status.vault_exists) {
                this.showScreen('screen-unlock');
            } else {
                this.showScreen('screen-welcome');
            }
        } catch (e) {
            console.error("Init failed:", e);
        }
    },

    showScreen(id) {
        document.querySelectorAll('.screen').forEach(el => el.classList.remove('active'));
        document.getElementById(id).classList.add('active');
    },

    async createVault() {
        const pwd = document.getElementById('create-pwd').value;
        const confirm = document.getElementById('create-pwd-confirm').value;
        if (pwd !== confirm) return alert("Passwords don't match");
        if (pwd.length < 4) return alert("Password too short");

        try {
            await api.createVault(pwd);
            this.loadDashboard();
        } catch (e) {
            alert(e.message);
        }
    },

    async unlockVault() {
        const pwd = document.getElementById('unlock-pwd').value;
        try {
            await api.unlockVault(pwd);
            document.getElementById('unlock-pwd').value = '';
            this.loadDashboard();
        } catch (e) {
            alert(e.message);
        }
    },

    async lockVault() {
        await api.lockVault();
        this.state.entries = [];
        this.showScreen('screen-unlock');
    },

    async loadDashboard() {
        this.showScreen('screen-dashboard');
        await this.refreshEntries();
    },

    async refreshEntries() {
        try {
            this.state.entries = await api.getEntries();
            this.renderList();
        } catch(e) {
            console.error(e);
            this.showScreen('screen-unlock');
        }
    },

    renderList() {
        const listEl = document.getElementById('entries-list');
        listEl.innerHTML = '';
        
        const query = (document.getElementById('search-input')?.value || '').toLowerCase();
        const filtered = this.state.entries.filter(e => 
            e.name.toLowerCase().includes(query) || 
            e.username.toLowerCase().includes(query)
        );
        
        filtered.forEach(entry => {
            const el = document.createElement('div');
            el.className = 'entry-item' + (this.state.currentEntry?.id === entry.id ? ' active' : '');
            
            // Extract first letter for avatar
            const firstLetter = entry.name ? entry.name.charAt(0).toUpperCase() : '?';
            
            el.innerHTML = `
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="width: 32px; height: 32px; border-radius: 50%; background: var(--primary-dim); color: var(--primary); display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 14px;">${firstLetter}</div>
                    <div>
                        <div class="entry-name">${entry.name}</div>
                        <div class="entry-username">${entry.username}</div>
                    </div>
                </div>
            `;
            el.onclick = () => this.selectEntry(entry);
            listEl.appendChild(el);
        });
    },

    onSearch() {
        this.renderList();
    },

    generatePassword() {
        const chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+~`|}{[]:;?><,./-=";
        let password = "";
        for (let i = 0; i < 16; i++) {
            password += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        document.getElementById('new-pass').value = password;
    },

    selectEntry(entry) {
        this.state.currentEntry = entry;
        this.state.passVisible = false;
        this.renderList();
        
        document.getElementById('empty-state').classList.add('hidden');
        document.getElementById('new-entry-view').classList.add('hidden');
        document.getElementById('detail-view').classList.remove('hidden');

        document.getElementById('det-name').textContent = entry.name;
        document.getElementById('det-user').textContent = entry.username;
        this.updatePassMask();
    },

    showNewEntry() {
        this.state.currentEntry = null;
        this.renderList();
        document.getElementById('new-name').value = '';
        document.getElementById('new-user').value = '';
        document.getElementById('new-pass').value = '';

        document.getElementById('empty-state').classList.add('hidden');
        document.getElementById('detail-view').classList.add('hidden');
        document.getElementById('new-entry-view').classList.remove('hidden');
    },

    async saveNewEntry() {
        const entry = {
            name: document.getElementById('new-name').value,
            username: document.getElementById('new-user').value,
            password: document.getElementById('new-pass').value
        };
        if(!entry.name) return alert("Name is required");

        try {
            await api.addEntry(entry);
            await this.refreshEntries();
            this.selectEntry(this.state.entries[this.state.entries.length - 1]);
        } catch(e) {
            alert(e.message);
        }
    },

    async deleteCurrent() {
        if(!this.state.currentEntry) return;
        if(confirm("Are you sure you want to delete this entry?")) {
            await api.deleteEntry(this.state.currentEntry.id);
            this.state.currentEntry = null;
            document.getElementById('detail-view').classList.add('hidden');
            document.getElementById('empty-state').classList.remove('hidden');
            await this.refreshEntries();
        }
    },

    togglePassword() {
        this.state.passVisible = !this.state.passVisible;
        this.updatePassMask();
    },

    updatePassMask() {
        const passEl = document.getElementById('det-pass');
        const iconEl = document.getElementById('det-pass-toggle');
        if (this.state.passVisible) {
            passEl.textContent = this.state.currentEntry.password;
            iconEl.textContent = 'visibility_off';
        } else {
            passEl.textContent = '•'.repeat(Math.max(8, this.state.currentEntry.password.length));
            iconEl.textContent = 'visibility';
        }
    },

    copyToClipboard(source) {
        let text = '';
        if (source === 'det-user') text = this.state.currentEntry.username;
        if (source === 'det-pass-raw') text = this.state.currentEntry.password;
        
        navigator.clipboard.writeText(text).then(() => {
            const toast = document.getElementById('toast');
            toast.classList.add('show');
            setTimeout(() => toast.classList.remove('show'), 2000);
        });
    }
};

window.onload = () => app.init();
