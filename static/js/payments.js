// payments.js — small theme toggle: light, dark, ios
function initPaymentsTheme(){
  const btn = document.getElementById('theme-toggle');
  const body = document.body;
  // load
  const saved = localStorage.getItem('mz_theme') || 'light';
  applyTheme(saved);

  if(!btn) return;
  btn.addEventListener('click', ()=>{
    // cycle: light -> dark -> ios
    let cur = localStorage.getItem('mz_theme') || 'light';
    let next = (cur === 'light') ? 'dark' : (cur === 'dark') ? 'ios' : 'light';
    localStorage.setItem('mz_theme', next);
    applyTheme(next);
  });

  function applyTheme(name){
    body.classList.remove('theme-dark','theme-ios');
    if(name === 'dark') body.classList.add('theme-dark');
    if(name === 'ios') body.classList.add('theme-ios');
  }
}