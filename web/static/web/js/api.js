// API Utility Functions for Django Bookstore

class BookstoreAPI {
    constructor() {
        this.baseURL = '/api';
        this.authToken = localStorage.getItem('accessToken');
    }

    // Set authentication token
    setAuthToken(token) {
        this.authToken = token;
        localStorage.setItem('accessToken', token);
        // Also set as cookie for middleware (60 minutes = 3600 seconds)
        document.cookie = `access_token=${token}; path=/; max-age=3600; SameSite=Lax`;
    }

    // Clear authentication token
    clearAuthToken() {
        this.authToken = null;
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        // Clear cookie
        document.cookie = 'access_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
    }

    // Get CSRF token from cookie
    getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        return null;
    }

    // Make API request
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            }
        };
        
        // Add JWT authentication
        if (this.authToken) {
            defaultOptions.headers['Authorization'] = `Bearer ${this.authToken}`;
        }
        
        // Add CSRF token for non-GET requests
        if (options.method && options.method !== 'GET') {
            const csrfToken = this.getCSRFToken();
            if (csrfToken) {
                defaultOptions.headers['X-CSRFToken'] = csrfToken;
            }
        }
        
        const response = await fetch(url, { ...defaultOptions, ...options });
        
        if (!response.ok) {
            if (response.status === 401) {
                // Token expired or invalid
                this.clearAuthToken();
                window.location.href = '/login/';
                throw new Error('Authentication required');
            }
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        // Handle empty responses (like 204 No Content for DELETE operations)
        if (response.status === 204 || response.headers.get('content-length') === '0') {
            return null;
        }
        
        // Check if response has content to parse
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            return await response.json();
        }
        
        // For non-JSON responses, return text
        return await response.text();
    }

    // Special request method for FormData (file uploads)
    async requestFormData(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        
        const defaultOptions = {
            headers: {}
        };
        
        // Add JWT authentication
        if (this.authToken) {
            defaultOptions.headers['Authorization'] = `Bearer ${this.authToken}`;
        }
        
        // Add CSRF token for non-GET requests
        if (options.method && options.method !== 'GET') {
            const csrfToken = this.getCSRFToken();
            if (csrfToken) {
                defaultOptions.headers['X-CSRFToken'] = csrfToken;
            }
        }
        
        // Don't set Content-Type for FormData - let browser set it with boundary
        const response = await fetch(url, { ...defaultOptions, ...options });
        
        if (!response.ok) {
            if (response.status === 401) {
                // Token expired or invalid
                this.clearAuthToken();
                window.location.href = '/login/';
                throw new Error('Authentication required');
            }
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        // Handle empty responses (like 204 No Content for DELETE operations)
        if (response.status === 204 || response.headers.get('content-length') === '0') {
            return null;
        }
        
        // Check if response has content to parse
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            return await response.json();
        }
        
        // For non-JSON responses, return text
        return await response.text();
    }

    // Authentication methods
    async login(username, password) {
        const response = await this.request('/auth/login/', {
            method: 'POST',
            body: JSON.stringify({ username, password })
        });
        
        // Store tokens
        this.setAuthToken(response.access);
        localStorage.setItem('refreshToken', response.refresh);
        
        return response;
    }

    async register(userData) {
        const response = await this.request('/auth/user/', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
        return response;
    }

    async logout() {
        try {
            const refreshToken = localStorage.getItem('refreshToken');
            if (refreshToken) {
                await this.request('/auth/logout/', {
                    method: 'POST',
                    body: JSON.stringify({ refresh: refreshToken })
                });
            }
        } catch (error) {
            console.error('Logout error:', error);
        } finally {
            this.clearAuthToken();
            localStorage.removeItem('refreshToken');
        }
    }

    async refreshToken() {
        const refreshToken = localStorage.getItem('refreshToken');
        if (!refreshToken) {
            throw new Error('No refresh token available');
        }
        
        const response = await this.request('/auth/token/refresh/', {
            method: 'POST',
            body: JSON.stringify({ refresh: refreshToken })
        });
        
        this.setAuthToken(response.access);
        return response;
    }

    // User methods
    async getCurrentUser() {
        return await this.request('/auth/user/');
    }

    async updateUser(userData) {
        return await this.request('/auth/user/', {
            method: 'PATCH',
            body: JSON.stringify(userData)
        });
    }

    // Book methods
    async getBooks(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const endpoint = queryString ? `/books/?${queryString}` : '/books/';
        return await this.request(endpoint);
    }

    async getBook(id) {
        return await this.request(`/books/${id}/`);
    }

    async createBook(bookData) {
        return await this.request('/books/', {
            method: 'POST',
            body: JSON.stringify(bookData)
        });
    }

    async updateBook(id, bookData) {
        return await this.request(`/books/${id}/`, {
            method: 'PATCH',
            body: JSON.stringify(bookData)
        });
    }

    async deleteBook(id) {
        return await this.request(`/books/${id}/`, {
            method: 'DELETE'
        });
    }

    // Book methods with image upload support
    async createBookWithImage(formData) {
        return await this.requestFormData('/books/', {
            method: 'POST',
            body: formData
        });
    }

    async updateBookWithImage(id, formData) {
        return await this.requestFormData(`/books/${id}/`, {
            method: 'PATCH',
            body: formData
        });
    }

    async searchBooks(params) {
        const queryString = new URLSearchParams(params).toString();
        const endpoint = queryString ? `/books/search/?${queryString}` : '/books/search/';
        return await this.request(endpoint);
    }

    async bulkDeleteBooks(bookIds) {
        return await this.request('/books/bulk_delete/', {
            method: 'POST',
            body: JSON.stringify({ book_ids: bookIds })
        });
    }

    async bulkDeleteFilteredBooks(params) {
        const queryString = new URLSearchParams(params).toString();
        const endpoint = queryString ? `/books/bulk_delete_filtered/?${queryString}` : '/books/bulk_delete_filtered/';
        return await this.request(endpoint, {
            method: 'POST'
        });
    }

    // Category methods
    async getCategories() {
        return await this.request('/categories/');
    }

    async getCategory(id) {
        return await this.request(`/categories/${id}/`);
    }

    async createCategory(categoryData) {
        return await this.request('/categories/', {
            method: 'POST',
            body: JSON.stringify(categoryData)
        });
    }

    async updateCategory(id, categoryData) {
        return await this.request(`/categories/${id}/`, {
            method: 'PATCH',
            body: JSON.stringify(categoryData)
        });
    }

    async deleteCategory(id) {
        return await this.request(`/categories/${id}/`, {
            method: 'DELETE'
        });
    }

    // Author methods
    async getAuthors() {
        return await this.request('/authors/');
    }

    async getAuthor(id) {
        return await this.request(`/authors/${id}/`);
    }

    async createAuthor(authorData) {
        return await this.request('/authors/', {
            method: 'POST',
            body: JSON.stringify(authorData)
        });
    }

    async updateAuthor(id, authorData) {
        return await this.request(`/authors/${id}/`, {
            method: 'PATCH',
            body: JSON.stringify(authorData)
        });
    }

    async deleteAuthor(id) {
        return await this.request(`/authors/${id}/`, {
            method: 'DELETE'
        });
    }

    // Favorite methods
    async getFavorites() {
        return await this.request('/favorites/');
    }

    async addFavorite(bookId) {
        return await this.request('/favorites/', {
            method: 'POST',
            body: JSON.stringify({ book_id: bookId })
        });
    }

    async removeFavorite(favoriteId) {
        return await this.request(`/favorites/${favoriteId}/`, {
            method: 'DELETE'
        });
    }

    async toggleFavorite(bookId) {
        return await this.request('/favorites/toggle/', {
            method: 'POST',
            body: JSON.stringify({ book_id: bookId })
        });
    }

    // Enhanced search method with all new filters
    async searchBooksEnhanced(params) {
        const queryString = new URLSearchParams(params).toString();
        const endpoint = queryString ? `/books/search/?${queryString}` : '/books/search/';
        return await this.request(endpoint);
    }

    // Genre methods
    async getGenres() {
        return await this.request('/genres/');
    }

    async getGenre(id) {
        return await this.request(`/genres/${id}/`);
    }

    async createGenre(genreData) {
        return await this.request('/genres/', {
            method: 'POST',
            body: JSON.stringify(genreData)
        });
    }

    async updateGenre(id, genreData) {
        return await this.request(`/genres/${id}/`, {
            method: 'PATCH',
            body: JSON.stringify(genreData)
        });
    }

    async deleteGenre(id) {
        return await this.request(`/genres/${id}/`, {
            method: 'DELETE'
        });
    }

    // Character methods
    async getCharacters() {
        return await this.request('/characters/');
    }

    async getCharacter(id) {
        return await this.request(`/characters/${id}/`);
    }

    async createCharacter(characterData) {
        return await this.request('/characters/', {
            method: 'POST',
            body: JSON.stringify(characterData)
        });
    }

    async updateCharacter(id, characterData) {
        return await this.request(`/characters/${id}/`, {
            method: 'PATCH',
            body: JSON.stringify(characterData)
        });
    }

    async deleteCharacter(id) {
        return await this.request(`/characters/${id}/`, {
            method: 'DELETE'
        });
    }

    // Award methods
    async getAwards() {
        return await this.request('/awards/');
    }

    async getAward(id) {
        return await this.request(`/awards/${id}/`);
    }

    async createAward(awardData) {
        return await this.request('/awards/', {
            method: 'POST',
            body: JSON.stringify(awardData)
        });
    }

    async updateAward(id, awardData) {
        return await this.request(`/awards/${id}/`, {
            method: 'PATCH',
            body: JSON.stringify(awardData)
        });
    }

    async deleteAward(id) {
        return await this.request(`/awards/${id}/`, {
            method: 'DELETE'
        });
    }

    // Publisher methods
    async getPublishers() {
        return await this.request('/publishers/');
    }

    async getPublisher(id) {
        return await this.request(`/publishers/${id}/`);
    }

    async createPublisher(publisherData) {
        return await this.request('/publishers/', {
            method: 'POST',
            body: JSON.stringify(publisherData)
        });
    }

    async updatePublisher(id, publisherData) {
        return await this.request(`/publishers/${id}/`, {
            method: 'PATCH',
            body: JSON.stringify(publisherData)
        });
    }

    async deletePublisher(id) {
        return await this.request(`/publishers/${id}/`, {
            method: 'DELETE'
        });
    }

    // Language methods
    async getLanguages() {
        return await this.request('/languages/');
    }

    async getLanguage(id) {
        return await this.request(`/languages/${id}/`);
    }

    async createLanguage(languageData) {
        return await this.request('/languages/', {
            method: 'POST',
            body: JSON.stringify(languageData)
        });
    }

    async updateLanguage(id, languageData) {
        return await this.request(`/languages/${id}/`, {
            method: 'PATCH',
            body: JSON.stringify(languageData)
        });
    }

    async deleteLanguage(id) {
        return await this.request(`/languages/${id}/`, {
            method: 'DELETE'
        });
    }

    // Series methods
    async getSeries() {
        return await this.request('/series/');
    }

    async getSeriesById(id) {
        return await this.request(`/series/${id}/`);
    }

    async createSeries(seriesData) {
        return await this.request('/series/', {
            method: 'POST',
            body: JSON.stringify(seriesData)
        });
    }

    async updateSeries(id, seriesData) {
        return await this.request(`/series/${id}/`, {
            method: 'PATCH',
            body: JSON.stringify(seriesData)
        });
    }

    async deleteSeries(id) {
        return await this.request(`/series/${id}/`, {
            method: 'DELETE'
        });
    }

    // Utility methods for dropdowns and selections
    async getAllDropdownData() {
        try {
            const [categories, authors, publishers, languages, series, genres] = await Promise.all([
                this.getCategories(),
                this.getAuthors(),
                this.getPublishers(),
                this.getLanguages(),
                this.getSeries(),
                this.getGenres()
            ]);

            return {
                categories: categories.results || categories,
                authors: authors.results || authors,
                publishers: publishers.results || publishers,
                languages: languages.results || languages,
                series: series.results || series,
                genres: genres.results || genres
            };
        } catch (error) {
            console.error('Error loading dropdown data:', error);
            throw error;
        }
    }

    // Enhanced book search with all new parameters
    async searchBooksWithFilters(filters = {}) {
        const params = new URLSearchParams();
        
        // Text search
        if (filters.search) params.append('search', filters.search);
        
        // Basic filters
        if (filters.category) params.append('category', filters.category);
        if (filters.author) params.append('author', filters.author);
        if (filters.publisher) params.append('publisher', filters.publisher);
        if (filters.language) params.append('language', filters.language);
        if (filters.series) params.append('series', filters.series);
        if (filters.book_format) params.append('book_format', filters.book_format);
        
        // Genre filter (multiple)
        if (filters.genres && Array.isArray(filters.genres)) {
            filters.genres.forEach(genre => params.append('genres', genre));
        }
        
        // Price range
        if (filters.min_price) params.append('min_price', filters.min_price);
        if (filters.max_price) params.append('max_price', filters.max_price);
        
        // Rating range
        if (filters.min_rating) params.append('min_rating', filters.min_rating);
        if (filters.max_rating) params.append('max_rating', filters.max_rating);
        
        // Date range
        if (filters.min_publication_date) params.append('min_publication_date', filters.min_publication_date);
        if (filters.max_publication_date) params.append('max_publication_date', filters.max_publication_date);
        
        // Boolean filters
        if (filters.favorites_only) params.append('favorites_only', filters.favorites_only);
        if (filters.has_cover_image) params.append('has_cover_image', filters.has_cover_image);
        
        // Ordering
        if (filters.ordering) params.append('ordering', filters.ordering);
        
        // Pagination
        if (filters.page) params.append('page', filters.page);
        
        const endpoint = `/books/search/?${params.toString()}`;
        return await this.request(endpoint);
    }
}

// Create global API instance
window.api = new BookstoreAPI();

// Utility functions
window.showNotification = function(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg max-w-sm ${
        type === 'success' ? 'bg-green-500 text-white' :
        type === 'error' ? 'bg-red-500 text-white' :
        type === 'warning' ? 'bg-yellow-500 text-white' :
        'bg-blue-500 text-white'
    }`;
    
    notification.innerHTML = `
        <div class="flex items-center justify-between">
            <span>${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" class="ml-4 text-white hover:text-gray-200">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
};

window.showError = function(message) {
    showNotification(message, 'error');
};

window.showSuccess = function(message) {
    showNotification(message, 'success');
};

window.showWarning = function(message) {
    showNotification(message, 'warning');
};

// Check authentication status on page load
document.addEventListener('DOMContentLoaded', function() {
    const authToken = localStorage.getItem('accessToken'); // Fixed: was 'authToken'
    if (authToken) {
        // Verify token is still valid
        api.getCurrentUser().catch(() => {
            api.clearAuthToken();
        });
    }
});
