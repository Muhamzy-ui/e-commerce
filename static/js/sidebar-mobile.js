// sidebar-mobile.js
// Finds the first .sidebar on the page, clones it into a mobile modal overlay,
// and toggles it when the #sidebarToggle button is clicked.

(function(){
  function createModal() {
    const modal = document.createElement('div');
    modal.className = 'sidebar-modal';
    modal.innerHTML = `
      <div class="sidebar-modal-backdrop" tabindex="-1"></div>
      <div class="sidebar-modal-panel">
        <button class="sidebar-modal-close" aria-label="Close">&times;</button>
        <div class="sidebar-modal-body"></div>
      </div>
    `;
    document.body.appendChild(modal);
    return modal;
  }

  function openModal(modal){
    modal.classList.add('open');
    document.documentElement.style.overflow = 'hidden';
  }
  function closeModal(modal){
    modal.classList.remove('open');
    document.documentElement.style.overflow = '';
  }

  document.addEventListener('DOMContentLoaded', function(){
    const toggle = document.getElementById('sidebarToggle');
    if(!toggle) return;

    const existingSidebar = document.querySelector('.sidebar');
    if(!existingSidebar) return;

    const modal = createModal();
    const modalBody = modal.querySelector('.sidebar-modal-body');
    const cloned = existingSidebar.cloneNode(true);
    
    // Remove/reset width constraints and display properties
    cloned.style.width = '100%';
    cloned.style.display = 'block';
    cloned.style.border = 'none';
    cloned.style.borderRadius = '0';
    cloned.style.padding = '16px';
    
    modalBody.appendChild(cloned);

    // events
    toggle.addEventListener('click', function(){ openModal(modal); });
    modal.querySelector('.sidebar-modal-close').addEventListener('click', function(){ closeModal(modal); });
    modal.querySelector('.sidebar-modal-backdrop').addEventListener('click', function(){ closeModal(modal); });

    // close on esc
    document.addEventListener('keydown', function(e){ if(e.key === 'Escape') closeModal(modal); });
  });
})();
