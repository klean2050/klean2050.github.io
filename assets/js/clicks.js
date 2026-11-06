(() => {
  const dialog = document.getElementById('photo-viewer');
  if (!dialog || typeof dialog.showModal !== 'function') return;
  const image = dialog.querySelector('img');
  const caption = dialog.querySelector('.photo-viewer-caption');
  const close = dialog.querySelector('.photo-viewer-close');
  let previousFocus;

  document.querySelectorAll('.photo-link').forEach(link => {
    link.addEventListener('click', event => {
      if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      previousFocus = link;
      image.src = link.href;
      image.alt = link.querySelector('img').alt;
      caption.textContent = link.closest('.occasion').querySelector('h2').textContent;
      dialog.showModal();
      document.documentElement.classList.add('photo-viewer-open');
      close.focus();
    });
  });

  close.addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    if (event.target === dialog) {
      const box = dialog.getBoundingClientRect();
      if (event.clientX < box.left || event.clientX > box.right ||
          event.clientY < box.top || event.clientY > box.bottom) dialog.close();
    }
  });
  dialog.addEventListener('close', () => {
    document.documentElement.classList.remove('photo-viewer-open');
    image.removeAttribute('src');
    previousFocus?.focus();
  });
})();
