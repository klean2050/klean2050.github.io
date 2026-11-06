const search=document.getElementById('search');
const papers=[...document.querySelectorAll('.paper')];
const years=[...document.querySelectorAll('.publication-year')];
const yearLinks=[...document.querySelectorAll('.year-index a')];
const clearSearch=document.querySelector('.clear-search');
const status=document.getElementById('result-status');
const normalize=value=>value.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
const searchable=papers.map(p=>normalize(p.querySelector('h3').textContent+' '+p.querySelector('.authors').textContent+' '+p.querySelector('.venue').textContent+' '+p.closest('section').id+' '+[...p.querySelectorAll('.paper-actions a')].map(a=>a.href).join(' ')));
function filterPapers(){
  const terms=normalize(search.value.trim()).split(/\s+/).filter(Boolean);
  let count=0;
  papers.forEach((paper,i)=>{paper.hidden=!terms.every(term=>searchable[i].includes(term));if(!paper.hidden)count++});
  years.forEach(year=>{const empty=![...year.querySelectorAll('.paper')].some(p=>!p.hidden);year.hidden=empty;const link=yearLinks.find(a=>a.hash==='#'+year.id);if(link)link.hidden=empty});
  clearSearch.hidden=!search.value;
  document.querySelector('.no-results').hidden=count!==0;
  status.textContent=terms.length?count+' publication'+(count===1?'':'s')+' found.':'';
  updateYear();
}
function resetSearch(){search.value='';filterPapers();search.focus()}
search.addEventListener('input',filterPapers);
search.addEventListener('keydown',event=>{if(event.key==='Escape')resetSearch()});
document.querySelector('.publication-search').addEventListener('submit',event=>event.preventDefault());
clearSearch.addEventListener('click',resetSearch);
document.querySelector('.reset-search').addEventListener('click',resetSearch);
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
function updateYear(){
  const visible=years.filter(section=>!section.hidden);
  let current=visible[0];
  visible.forEach(section=>{if(section.getBoundingClientRect().top<150)current=section});
  if(visible.length&&window.innerHeight+window.scrollY>=document.documentElement.scrollHeight-3)current=visible[visible.length-1];
  yearLinks.forEach(link=>{const active=current&&link.hash==='#'+current.id;link.classList.toggle('current',Boolean(active));if(active)link.setAttribute('aria-current','location');else link.removeAttribute('aria-current')});
}
window.addEventListener('scroll',updateYear,{passive:true});
updateYear();
