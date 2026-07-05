// api.js - Frontend wrapper for Flask Backend

const API_BASE = '/api';

const api = {
    async request(endpoint, method = 'GET', body = null) {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json'
            }
        };
        if (body) {
            options.body = JSON.stringify(body);
        }

        const response = await fetch(`${API_BASE}${endpoint}`, options);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'API Request Failed');
        }
        return data;
    },

    async status() {
        return this.request('/status');
    },

    async createVault(password) {
        return this.request('/create', 'POST', { password });
    },

    async unlockVault(password) {
        return this.request('/unlock', 'POST', { password });
    },

    async lockVault() {
        return this.request('/lock', 'POST');
    },

    async getEntries() {
        return this.request('/entries');
    },

    async addEntry(entryData) {
        return this.request('/entries', 'POST', entryData);
    },

    async updateEntry(id, entryData) {
        return this.request(`/entries/${id}`, 'PUT', entryData);
    },

    async deleteEntry(id) {
        return this.request(`/entries/${id}`, 'DELETE');
    }
};
