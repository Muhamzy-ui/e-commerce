// sidebar-mobile.js
// Mobile sidebar: clones existing sidebar or creates a default one for all pages

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

  function getSidebarContent() {
    let sidebar = document.querySelector('.sidebar');
    if (sidebar) return sidebar.cloneNode(true);

    // fallback default sidebar if none exists
    const defaultSidebar = document.createElement('div');
    defaultSidebar.className = 'sidebar';
    defaultSidebar.innerHTML = `
      <ul class="list-unstyled mb-0">
        <li><a href="/">Home</a></li>
        <li><a href="/products/">Products</a></li>
        <li><a href="/account/dashboard/">Dashboard</a></li>
        <li><a href="/wishlist/">Wishlist</a></li>
        <li><a href="/orders/">Orders</a></li>
        <li><a href="/help/">Help Center</a></li>
        <li><a href="/account/register_vendor/">Become a Vendor</a></li>
      </ul>
    `;
    return defaultSidebar;
  }

  document.addEventListener('DOMContentLoaded', function(){
    const toggle = document.getElementById('sidebarToggle');
    if(!toggle) return;

    const modal = createModal();
    const modalBody = modal.querySelector('.sidebar-modal-body');
    const clonedSidebar = getSidebarContent();

    // Reset styles for mobile
    clonedSidebar.style.width = '100%';
    clonedSidebar.style.display = 'block';
    clonedSidebar.style.border = 'none';
    clonedSidebar.style.borderRadius = '0';
    clonedSidebar.style.padding = '16px';

    modalBody.appendChild(clonedSidebar);

    // Toggle events
    toggle.addEventListener('click', () => openModal(modal));
    modal.querySelector('.sidebar-modal-close').addEventListener('click', () => closeModal(modal));
    modal.querySelector('.sidebar-modal-backdrop').addEventListener('click', () => closeModal(modal));

    // Close on ESC
    document.addEventListener('keydown', function(e){
      if(e.key === 'Escape') closeModal(modal);
    });
  });

  // Desktop account dropdown hover
  document.addEventListener('DOMContentLoaded', function(){
    if(window.innerWidth >= 768){
      const dropdown = document.querySelector('.nav-item.dropdown');
      if(dropdown){
        dropdown.addEventListener('mouseenter', () => dropdown.classList.add('show'));
        dropdown.addEventListener('mouseleave', () => dropdown.classList.remove('show'));
      }
    }
  });
})();
