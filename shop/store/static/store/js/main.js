/* ═══════════════════════════════════════════════════
   StyleHub — Main JavaScript
   - Cart AJAX (add / update / remove)
   - Toast notifications
   - Header scroll + hamburger
   - Newsletter subscribe
   ═══════════════════════════════════════════════════ */

// ── CSRF helper ──────────────────────────────────────
function getCookie(name) {
  let val = null;
  document.cookie.split(';').forEach(c => {
    const [k, v] = c.trim().split('=');
    if (k === name) val = decodeURIComponent(v);
  });
  return val;
}

// ── Toast ─────────────────────────────────────────────
function showToast(message, type = 'success') {
  const toast = document.getElementById('toast');
  if (!toast) return;
  toast.textContent = message;
  toast.className = `toast toast--${type} show`;
  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => {
    toast.classList.remove('show');
  }, 3200);
}

// ── Cart badge ────────────────────────────────────────
function updateCartBadge(count) {
  const badge = document.getElementById('cart-badge');
  if (!badge) return;
  badge.textContent = count;
  badge.style.display = count > 0 ? 'flex' : 'none';
  // Pulse animation
  badge.classList.remove('pulse');
  void badge.offsetWidth;
  badge.classList.add('pulse');
}

// ── Add to Cart (used site-wide) ──────────────────────
async function addToCart(productId, quantity = 1, size = '') {
  try {
    const res = await fetch('/api/cart/add/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({ product_id: productId, quantity, size }),
    });
    const data = await res.json();
    if (data.success) {
      showToast(data.message, 'success');
      updateCartBadge(data.cart_count);
    } else {
      showToast(data.error || 'Could not add to cart.', 'error');
    }
  } catch (err) {
    showToast('Network error. Please try again.', 'error');
    console.error('addToCart error:', err);
  }
}

// ── Product card "Add to Cart" buttons ────────────────
document.addEventListener('click', function (e) {
  const btn = e.target.closest('.add-to-cart-btn');
  if (!btn) return;
  const productId = btn.dataset.productId;
  if (!productId) return;

  // Visual feedback
  btn.disabled = true;
  const originalHTML = btn.innerHTML;
  btn.innerHTML = "<i class='bx bx-check'></i>";
  btn.style.background = 'var(--brand)';
  btn.style.color = '#fff';

  addToCart(productId, 1, '').finally(() => {
    setTimeout(() => {
      btn.innerHTML = originalHTML;
      btn.style.background = '';
      btn.style.color = '';
      btn.disabled = false;
    }, 1200);
  });
});

// ── Newsletter ─────────────────────────────────────────
async function subscribeNewsletter(e) {
  e.preventDefault();
  const emailInput = document.getElementById('newsletter-email');
  const email = emailInput?.value?.trim();
  if (!email) return;

  const btn = e.target.querySelector('button[type="submit"]');
  const originalText = btn.textContent;
  btn.textContent = 'Subscribing…';
  btn.disabled = true;

  try {
    const res = await fetch('/api/newsletter/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({ email }),
    });
    const data = await res.json();
    showToast(data.message || (data.success ? 'Subscribed!' : data.error), data.success ? 'success' : 'error');
    if (data.success) emailInput.value = '';
  } catch {
    showToast('Something went wrong. Try again.', 'error');
  } finally {
    btn.textContent = originalText;
    btn.disabled = false;
  }
}

// ── Sticky header shadow ──────────────────────────────
const header = document.getElementById('header');
if (header) {
  window.addEventListener('scroll', () => {
    header.style.boxShadow = window.scrollY > 10
      ? '0 2px 20px rgba(0,0,0,0.12)'
      : '0 1px 0 #e5e7eb';
  }, { passive: true });
}

// ── Hamburger / mobile nav ────────────────────────────
const hamburger = document.getElementById('hamburger');
const navbar = document.getElementById('navbar');
if (hamburger && navbar) {
  hamburger.addEventListener('click', () => {
    const isOpen = navbar.classList.toggle('open');
    hamburger.innerHTML = isOpen ? "<i class='bx bx-x'></i>" : "<i class='bx bx-menu'></i>";
    hamburger.setAttribute('aria-expanded', isOpen);
  });

  // Close on outside click
  document.addEventListener('click', (e) => {
    if (!header.contains(e.target)) {
      navbar.classList.remove('open');
      hamburger.innerHTML = "<i class='bx bx-menu'></i>";
    }
  });
}

// ── Cart badge pulse CSS injection ────────────────────
const style = document.createElement('style');
style.textContent = `
  @keyframes badgePulse {
    0%   { transform: scale(1); }
    50%  { transform: scale(1.4); }
    100% { transform: scale(1); }
  }
  .cart-badge.pulse { animation: badgePulse 0.4s ease; }
`;
document.head.appendChild(style);

// ── Lazy load polyfill (native already handles in modern browsers) ──
if ('loading' in HTMLImageElement.prototype === false) {
  const imgs = document.querySelectorAll('img[loading="lazy"]');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        img.src = img.dataset.src || img.src;
        observer.unobserve(img);
      }
    });
  });
  imgs.forEach(img => observer.observe(img));
}
