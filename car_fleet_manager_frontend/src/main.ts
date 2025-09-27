// Main entry point for the application
import 'alpinejs';
import { persist } from '@alpinejs/persist';
import intersect from '@alpinejs/intersect';
import 'htmx.org';
import './js/theme';

// Initialize Alpine.js with plugins
window.Alpine = Alpine;
Alpine.plugin(persist);
Alpine.plugin(intersect);

// Start Alpine when the page loads
document.addEventListener('DOMContentLoaded', () => {
  Alpine.start();
});

// HTMX configuration
document.body.addEventListener('htmx:beforeSwap', (event: any) => {
  // Handle 401 Unauthorized responses
  if (event.detail.xhr.status === 401) {
    window.location.href = '/accounts/login/?next=' + window.location.pathname;
  }
});
