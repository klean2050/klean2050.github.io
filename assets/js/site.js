// Shared navigation and theme controls, loaded before page-specific scripts.
// The inline <head> script picks the saved or OS theme before first paint.
const themeButton = document.getElementById('theme-toggle');
function applyTheme(dark) {
  document.documentElement.dataset.theme = dark ? 'dark' : 'light';
  const label = dark ? 'Switch to light theme' : 'Switch to dark theme';
  themeButton.setAttribute('aria-label', label);
  themeButton.title = label;
  document.querySelector('meta[name="theme-color"]').content = dark ? '#16151c' : '#ffffff';
}
applyTheme(document.documentElement.dataset.theme === 'dark');
themeButton.addEventListener('click', () => {
  const dark = document.documentElement.dataset.theme !== 'dark';
  applyTheme(dark);
  try { localStorage.setItem('theme', dark ? 'dark' : 'light'); } catch {}
});

const menuButton = document.querySelector('.menu-toggle');
const links = document.getElementById('nav-links');
menuButton.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded', String(open));
  links.classList.toggle('open', open);
});
// GitHub Pages sends Last-Modified on every deploy, so the footer date never needs hand edits.
const lastUpdated = document.querySelector('.last-updated');
if (lastUpdated) {
  lastUpdated.textContent = ' · Last updated ' + new Date(document.lastModified)
    .toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
}

function closeMenu() {
  menuButton.setAttribute('aria-expanded', 'false');
  links.classList.remove('open');
}
links.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && links.classList.contains('open')) {
    closeMenu();
    menuButton.focus();
  }
});
