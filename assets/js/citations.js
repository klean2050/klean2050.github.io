// BibTeX controls shared by the three research direction pages.
document.querySelectorAll('.bib-toggle').forEach(button=>button.addEventListener('click',()=>{
  const open=button.getAttribute('aria-expanded')!=='true';
  button.setAttribute('aria-expanded',String(open));
  button.querySelector('[aria-hidden]').textContent=open?'−':'＋';
  document.getElementById(button.getAttribute('aria-controls')).hidden=!open;
}));
document.querySelectorAll('.copy-citation').forEach(button=>button.addEventListener('click',async()=>{
  const citation=button.closest('.citation');
  try{await navigator.clipboard.writeText(citation.querySelector('code').textContent);button.textContent='Copied';citation.querySelector('.copy-status').textContent='Citation copied.';setTimeout(()=>{button.textContent='Copy';citation.querySelector('.copy-status').textContent=''},2000)}
  catch{citation.querySelector('.copy-status').textContent='Select the citation text to copy it.'}
}));
