
(function(){
  function debounce(fn, delay){
    let t;
    return function(...args){
      clearTimeout(t);
      t = setTimeout(()=> fn.apply(this, args), delay);
    }
  }

  function createSearchModal(){
    const modal = document.createElement('div');
    modal.className = 'search-modal';
    modal.innerHTML = `
      <div class="search-modal-backdrop"></div>
      <div class="search-modal-panel">
        <div class="search-modal-header">
          <input type="search" class="search-live-input" placeholder="Search products, brands and categories" aria-label="Search">
          <button class="search-modal-close" aria-label="Close">&times;</button>
        </div>
        <div class="search-results"></div>
      </div>
    `;
    document.body.appendChild(modal);
    return modal;
  }

  function renderResults(container, data){
    const { products = [], categories = [] } = data;
    if(!products.length && !categories.length){
      container.innerHTML = '<div class="no-results">No results</div>';
      return;
    }
    const list = document.createElement('div');
    list.className = 'search-results-list';

    
    if(categories.length){
      const catHeader = document.createElement('div');
      catHeader.className = 'search-section-header';
      catHeader.textContent = 'Categories';
      list.appendChild(catHeader);
      
      categories.forEach(c => {
        const item = document.createElement('a');
        item.className = 'search-result-item category-item';
        item.href = '/product/category/' + encodeURIComponent(c.slug) + '/';
        item.innerHTML = `<i class="fa fa-folder"></i> ${c.name}`;
        list.appendChild(item);
      });
    }
    
    // Render products
    if(products.length){
      const prodHeader = document.createElement('div');
      prodHeader.className = 'search-section-header';
      prodHeader.textContent = 'Products';
      list.appendChild(prodHeader);
      
      products.forEach(p => {
        const item = document.createElement('a');
        item.className = 'search-result-item product-item';
        item.href = '/product/' + encodeURIComponent(p.slug) + '/';
        item.innerHTML = `
          <div class="sr-image">${p.image ? '<img src="'+p.image+'" alt="'+p.name+'">' : ''}</div>
          <div class="sr-body">
            <div class="sr-title">${p.name}</div>
            <div class="sr-price">${p.price}</div>
          </div>
        `;
        list.appendChild(item);
      });
    }
    container.innerHTML = '';
    container.appendChild(list);
  }

  document.addEventListener('DOMContentLoaded', function(){
    // ========== MOBILE SEARCH ==========
    const mobileToggle = document.getElementById('mobileSearchToggle');
    if(mobileToggle){
      const modal = createSearchModal();
      const input = modal.querySelector('.search-live-input');
      const resultsContainer = modal.querySelector('.search-results');
      const backdrop = modal.querySelector('.search-modal-backdrop');
      const closeBtn = modal.querySelector('.search-modal-close');

      function open(){
        modal.classList.add('open');
        input.value = '';
        resultsContainer.innerHTML = '';
        setTimeout(()=> input.focus(), 50);
        document.documentElement.style.overflow = 'hidden';
      }
      function close(){
        modal.classList.remove('open');
        document.documentElement.style.overflow = '';
      }

      mobileToggle.addEventListener('click', open);
      closeBtn.addEventListener('click', close);
      backdrop.addEventListener('click', close);
      document.addEventListener('keydown', function(e){ if(e.key === 'Escape') close(); });

      const doSearch = debounce(function(){
        const q = input.value.trim();
        if(!q){
          resultsContainer.innerHTML = '';
          return;
        }
        fetch('/product/search-live/?q=' + encodeURIComponent(q))
          .then(r => r.json())
          .then(data => {
            renderResults(resultsContainer, data);
          })
          .catch(err => {
            console.error('search error', err);
          });
      }, 300);

      input.addEventListener('input', doSearch);
    }

    // ========== DESKTOP SEARCH ==========
    const desktopInput = document.querySelector('.desktop-search-input');
    const desktopBtn = document.querySelector('.desktop-search-btn');
    const desktopResults = document.querySelector('.desktop-search-results');
    
    if(desktopInput && desktopResults){
      const doDesktopSearch = debounce(function(){
        const q = desktopInput.value.trim();
        if(!q){
          desktopResults.innerHTML = '';
          return;
        }
        fetch('/product/search-live/?q=' + encodeURIComponent(q))
          .then(r => r.json())
          .then(data => {
            renderResults(desktopResults, data);
          })
          .catch(err => {
            console.error('search error', err);
          });
      }, 300);

      desktopInput.addEventListener('input', doDesktopSearch);
      
      // Submit on button click: navigate to product list with query
      desktopBtn.addEventListener('click', function(e){
        e.preventDefault();
        const q = desktopInput.value.trim();
        if(q){
          window.location.href = '/?q=' + encodeURIComponent(q);
        }
      });
      
      // Close results when clicking outside
      document.addEventListener('click', function(e){
        if(!e.target.closest('.search-container')){
          desktopResults.innerHTML = '';
        }
      });
    }
  });
})();