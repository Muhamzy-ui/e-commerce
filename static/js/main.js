function setupPasswordToggle(fieldID, toggleID) {
    const input = document.getElementById(fieldID);
    const toggle = document.getElementById(toggleID);
    if (toggle && input) {
        toggle.addEventListener('click', () => {
            const isPassword = input.type === 'password';
            input.type = isPassword ? 'text' : 'password';

            toggle.classList.toggle('fa-eye');
            toggle.classList.toggle('fa-eye-slash');
        });
    }
}

// Apply toggles
setupPasswordToggle('password', 'togglePassword');       // Login
setupPasswordToggle('password1', 'togglePassword1');     // Signup password
setupPasswordToggle('password2', 'togglePassword2');     // Signup confirm password

// Optional: Password strength for signup
const pass1 = document.getElementById('password1');
const strengthEl = document.getElementById('passwordStrength');
if(pass1 && strengthEl){
    pass1.addEventListener('input', () => {
        const val = pass1.value;
        let strength = 'Weak';
        let color = 'red';
        if (val.length >= 8 && /[A-Z]/.test(val) && /[0-9]/.test(val) && /[\W]/.test(val)) {
            strength = 'Strong';
            color = 'green';
        } else if (val.length >= 6) {
            strength = 'Medium';
            color = 'orange';
        }
        strengthEl.textContent = `Password Strength: ${strength}`;
        strengthEl.style.color = color;
    });
}




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


  const carouselElement = document.getElementById('productCarousel');
  const thumbs = document.querySelectorAll('.thumb-select');

  carouselElement.addEventListener('slide.bs.carousel', function (e) {
    thumbs.forEach(t => t.classList.remove('border-primary'));
    thumbs[e.to].classList.add('border-primary');
  });


  const accountToggle = document.getElementById("accountToggle");
const accountSheet = document.getElementById("accountSheet");
const closeAccountSheet = document.getElementById("closeAccountSheet");

if (accountToggle) {
    accountToggle.addEventListener("click", () => {
        accountSheet.classList.add("active");
    });
}

if (closeAccountSheet) {
    closeAccountSheet.addEventListener("click", () => {
        accountSheet.classList.remove("active");
    });
}



    // Mobile search toggle
    const toggleBtn = document.getElementById("mobileSearchToggle");
    const searchBar = document.getElementById("mobileSearchBar");

    if (toggleBtn) {
        toggleBtn.addEventListener("click", () => {
            searchBar.classList.toggle("show");
        });
    }

    function previewImages(files) {
    const previews = document.getElementById('previews');
    previews.innerHTML = '';
    Array.from(files).forEach(file => {
        const reader = new FileReader();
        reader.onload = e => {
            const img = document.createElement('img');
            img.src = e.target.result;
            img.classList.add('preview-image-thumb');
            img.style.width = '80px';
            img.style.height = '80px';
            img.style.objectFit = 'cover';
            img.style.borderRadius = '5px';
            previews.appendChild(img);
        };
        reader.readAsDataURL(file);
    });
}
