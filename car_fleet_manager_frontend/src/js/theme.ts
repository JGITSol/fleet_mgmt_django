// Theme management with system preference and local storage
const theme = {
  init() {
    // Check for saved user preference, if any, on load
    const savedTheme = localStorage.getItem('theme');
    
    if (savedTheme) {
      document.documentElement.classList.add(savedTheme);
      this.isDark = savedTheme === 'dark';
    } else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
      document.documentElement.classList.add('dark');
      this.isDark = true;
    }
    
    // Watch for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
      if (!localStorage.getItem('theme')) {
        this.isDark = e.matches;
        document.documentElement.classList.toggle('dark', e.matches);
      }
    });
  },
  
  isDark: false,
  
  toggle() {
    this.isDark = !this.isDark;
    if (this.isDark) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  }
};

// Initialize theme when the script loads
document.addEventListener('DOMContentLoaded', () => {
  theme.init();
});

// Export for Alpine.js
window.theme = theme;
