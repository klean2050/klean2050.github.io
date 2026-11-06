// Show the first five Updates; the button reveals the rest.
const newsToggle = document.getElementById('news-toggle');
const olderNews = [...document.querySelectorAll('.news-item')].slice(5);
olderNews.forEach(item => { item.hidden = true; });
if (!olderNews.length) newsToggle.remove();
newsToggle.addEventListener('click', () => {
  const expanded = newsToggle.getAttribute('aria-expanded') === 'true';
  olderNews.forEach(item => { item.hidden = expanded; });
  newsToggle.setAttribute('aria-expanded', String(!expanded));
  newsToggle.innerHTML = expanded
    ? 'More updates <span aria-hidden="true">＋</span>'
    : 'Fewer updates <span aria-hidden="true">−</span>';
});
