// assets/js/theme-switcher.js
document.addEventListener('DOMContentLoaded', function() {
  const themeSwitcher = document.getElementById('theme-switcher');
  const currentTheme = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', currentTheme);

  themeSwitcher.checked = currentTheme === 'dark';

  themeSwitcher.addEventListener('change', function() {
    if (this.checked) {
      document.documentElement.setAttribute('data-theme', 'dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.setAttribute('data-theme', 'light');
      localStorage.setItem('theme', 'light');
    }
  });
});