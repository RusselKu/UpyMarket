import { productos } from '../assets/catalog.js';
import { trackView, trackAddToCart, trackPurchase } from './telemetry.js';

// ── Estado ────────────────────────────────────────────────────────────────────
let activeFilter = 'all';
let searchValue  = '';
let cart = JSON.parse(sessionStorage.getItem('upymarket_cart')) || [];

// ── Nodos estáticos ───────────────────────────────────────────────────────────
const catalogGrid       = document.querySelector('#catalog-grid');
const searchInput       = document.querySelector('#product-search');
const filterButtons     = document.querySelectorAll('.filter-chip[data-filter]');

const cartPanel         = document.querySelector('#cart-panel');
const cartToggle        = document.querySelector('#cart-toggle');
const cartClose         = document.querySelector('#cart-close');
const cartCount         = document.querySelector('#cart-count');
const cartItems         = document.querySelector('#cart-items');
const cartEmpty         = document.querySelector('#cart-empty');
const cartTotalEl       = document.querySelector('#cart-total');
const paymentSelect     = document.querySelector('#payment-method');
const checkoutBtn       = document.querySelector('.checkout-button');

const notifToggle       = document.querySelector('#notification-toggle');
const notifClose        = document.querySelector('#notification-close');
const notifPanel        = document.querySelector('#notification-panel');

const detailModal       = document.querySelector('#product-detail-modal');
const detailClose       = document.querySelector('#product-detail-close');
const detailIcon        = document.querySelector('#product-detail-icon');
const detailTitle       = document.querySelector('#product-detail-title');
const detailCategory    = document.querySelector('#product-detail-category');
const detailDescription = document.querySelector('#product-detail-description');
const detailFeatures    = document.querySelector('#product-detail-features');
const detailPrice       = document.querySelector('#product-detail-price');
const detailPriceOrig   = document.querySelector('#product-detail-price-original');
const detailAdd         = document.querySelector('#product-detail-add');

const cartToast         = document.querySelector('#cart-toast');

// ── Helpers ───────────────────────────────────────────────────────────────────
function precioConDescuento(producto) {
  return producto.precio_original * (1 - producto.porcentaje_descuento);
}

function formatPrice(amount) {
  return `$${amount.toFixed(2)}`;
}

function categoryClass(categoria) {
  if (categoria === 'Académico')       return 'academic';
  if (categoria === 'Entretenimiento') return 'leisure';
  if (categoria === 'Laptop')          return 'tech';
  return 'tech';
}

function iconClass(categoria) {
  if (categoria === 'Académico')       return 'academic-icon';
  if (categoria === 'Entretenimiento') return 'leisure-icon';
  if (categoria === 'Laptop')          return 'tech-icon';
  return 'tech-icon';
}

// ── Renderizado del catálogo ──────────────────────────────────────────────────
function buildCard(p) {
  const precioFinal = precioConDescuento(p);
  const tieneDescuento = p.porcentaje_descuento > 0;
  const pct = Math.round(p.porcentaje_descuento * 100);
  const carreraTag = p.carrera_objetivo !== 'Todas'
    ? `<span class="career-tag">🎓 ${p.carrera_objetivo}</span>`
    : '';
  const discountBadge = tieneDescuento
    ? `<span class="discount-badge">-${pct}%</span>`
    : '';
  const priceHTML = tieneDescuento
    ? `<div class="price-wrapper">
         <span class="price-original">${formatPrice(p.precio_original)}</span>
         <span class="price">${formatPrice(precioFinal)}</span>
       </div>`
    : `<span class="price">${formatPrice(p.precio_original)}</span>`;

  const gpuBadge = p.tiene_gpu_dedicada
    ? `<span class="gpu-badge">GPU</span>`
    : '';

  const article = document.createElement('article');
  article.className = 'product-card glass-card';
  article.dataset.productId = p.id;
  article.dataset.category  = p.categoria;
  article.innerHTML = `
    ${discountBadge}${gpuBadge}
    <div class="product-icon ${iconClass(p.categoria)}">${p.icono}</div>
    <div class="product-topline">
      <span class="category-badge ${categoryClass(p.categoria)}">${p.categoria}</span>
      ${priceHTML}
    </div>
    <h3>${p.nombre}</h3>
    ${carreraTag}
    <p>${p.descripcion}</p>
    <div class="product-buttons">
      <button type="button" class="product-action" data-action="view_product">Ver Producto</button>
      <button type="button" class="product-action add-cart-action" data-action="add_to_cart">Agregar al Carrito</button>
    </div>
  `;
  return article;
}

function filteredProducts() {
  return productos.filter(p => {
    const matchCat = activeFilter === 'all' || p.categoria === activeFilter;
    const q = searchValue.toLowerCase();
    const matchSearch = !q
      || p.nombre.toLowerCase().includes(q)
      || p.categoria.toLowerCase().includes(q)
      || p.descripcion.toLowerCase().includes(q)
      || p.carrera_objetivo.toLowerCase().includes(q);
    return matchCat && matchSearch;
  });
}

function renderCatalog() {
  if (!catalogGrid) return;
  catalogGrid.innerHTML = '';
  const list = filteredProducts();
  if (list.length === 0) {
    catalogGrid.innerHTML = '<p class="no-results">No se encontraron productos.</p>';
    return;
  }
  list.forEach(p => catalogGrid.appendChild(buildCard(p)));
}

// ── Carrito ───────────────────────────────────────────────────────────────────
function saveCart() {
  sessionStorage.setItem('upymarket_cart', JSON.stringify(cart));
}

function renderCart() {
  if (!cartItems || !cartCount || !cartTotalEl || !cartEmpty) return;
  cartItems.innerHTML = '';
  const totalQty    = cart.reduce((s, i) => s + i.quantity, 0);
  const totalAmount = cart.reduce((s, i) => s + i.price * i.quantity, 0);
  cartCount.textContent  = totalQty;
  cartTotalEl.textContent = formatPrice(totalAmount);
  cartEmpty.hidden = cart.length > 0;

  cart.forEach(item => {
    const div = document.createElement('div');
    div.className = 'cart-item';
    div.innerHTML = `
      <div>
        <h3>${item.name}</h3>
        <p>${item.category} · ${formatPrice(item.price)}</p>
      </div>
      <div class="cart-item-actions">
        <span>Cant: ${item.quantity}</span>
        <button type="button" data-remove-id="${item.id}">Quitar</button>
      </div>`;
    cartItems.appendChild(div);
  });

  document.querySelectorAll('[data-remove-id]').forEach(btn => {
    btn.addEventListener('click', () => {
      cart = cart.filter(i => i.id !== btn.dataset.removeId);
      saveCart();
      renderCart();
    });
  });
}

function addToCart(product) {
  const existing = cart.find(i => i.id === product.id);
  if (existing) { existing.quantity += 1; }
  else { cart.push({ ...product, quantity: 1 }); }
  saveCart();
  renderCart();
  openCart();
  showToast(`${product.name} agregado al carrito`);
}

// ── Paneles ───────────────────────────────────────────────────────────────────
function openCart() {
  closeNotif();
  cartPanel?.classList.add('is-open');
}
function closeCart() { cartPanel?.classList.remove('is-open'); }

function openNotif() {
  closeCart();
  notifPanel?.classList.add('is-open');
}
function closeNotif() { notifPanel?.classList.remove('is-open'); }

function showToast(msg) {
  if (!cartToast) return;
  cartToast.textContent = msg;
  cartToast.classList.add('is-visible');
  setTimeout(() => cartToast.classList.remove('is-visible'), 2400);
}

// ── Modal de detalle ──────────────────────────────────────────────────────────
function openDetail(productId) {
  const p = productos.find(x => x.id === productId);
  if (!p || !detailModal) return;

  trackView(p.id);

  const tieneDescuento = p.porcentaje_descuento > 0;
  const pct = Math.round(p.porcentaje_descuento * 100);
  const precioFinal = precioConDescuento(p);

  detailIcon.textContent = p.icono;
  detailTitle.textContent = p.nombre;
  detailCategory.textContent = p.categoria;
  detailCategory.className = `category-badge ${categoryClass(p.categoria)}`;
  detailDescription.textContent = p.descripcion;

  if (detailPrice) detailPrice.textContent = formatPrice(precioFinal);
  if (detailPriceOrig) {
    detailPriceOrig.textContent = tieneDescuento ? `${formatPrice(p.precio_original)} (-${pct}%)` : '';
    detailPriceOrig.hidden = !tieneDescuento;
  }

  detailFeatures.innerHTML = '';
  (p.caracteristicas || []).forEach(f => {
    const li = document.createElement('li');
    li.textContent = f;
    detailFeatures.appendChild(li);
  });

  if (detailAdd) {
    detailAdd.dataset.productId = p.id;
    detailAdd.dataset.price     = precioFinal.toFixed(2);
    detailAdd.dataset.name      = p.nombre;
    detailAdd.dataset.category  = p.categoria;
  }

  closeCart();
  closeNotif();
  detailModal.classList.add('is-open');
}

function closeDetail() { detailModal?.classList.remove('is-open'); }

// ── Delegación de eventos sobre el catálogo ───────────────────────────────────
catalogGrid?.addEventListener('click', event => {
  const btn = event.target.closest('[data-action]');
  if (!btn) return;
  const card = btn.closest('.product-card');
  const productId = card?.dataset.productId;
  if (!productId) return;

  if (btn.dataset.action === 'view_product') {
    openDetail(productId);
  }
  if (btn.dataset.action === 'add_to_cart') {
    const p = productos.find(x => x.id === productId);
    if (!p) return;
    const precio = precioConDescuento(p);
    trackAddToCart(p.id, precio);
    addToCart({ id: p.id, name: p.nombre, category: p.categoria, price: precio, porcentaje_descuento: p.porcentaje_descuento });
  }
});

// Botón "Agregar" dentro del modal de detalle
detailAdd?.addEventListener('click', () => {
  const id    = detailAdd.dataset.productId;
  const price = parseFloat(detailAdd.dataset.price) || 0;
  const name  = detailAdd.dataset.name  || 'Producto';
  const cat   = detailAdd.dataset.category || '';
  const p     = productos.find(x => x.id === id);
  trackAddToCart(id, price);
  addToCart({ id, name, category: cat, price, porcentaje_descuento: p?.porcentaje_descuento ?? 0 });
  closeDetail();
});

// ── Filtros y búsqueda ────────────────────────────────────────────────────────
filterButtons.forEach(btn => {
  btn.addEventListener('click', () => {
    activeFilter = btn.dataset.filter;
    filterButtons.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    renderCatalog();
  });
});

searchInput?.addEventListener('input', () => {
  searchValue = searchInput.value.trim();
  renderCatalog();
});

// ── Checkout ──────────────────────────────────────────────────────────────────
checkoutBtn?.addEventListener('click', () => {
  if (cart.length === 0) { showToast('Tu carrito está vacío'); return; }
  const metodo = paymentSelect?.value || 'No especificado';
  if (!metodo || metodo === '') { showToast('Selecciona un método de pago'); return; }
  trackPurchase(cart, metodo);
  cart = [];
  saveCart();
  renderCart();
  closeCart();
  showToast('¡Compra registrada! Gracias por tu pedido');
});

// ── Controles de paneles ──────────────────────────────────────────────────────
cartToggle?.addEventListener('click', () => cartPanel?.classList.contains('is-open') ? closeCart() : openCart());
cartClose?.addEventListener('click', closeCart);
notifToggle?.addEventListener('click', () => notifPanel?.classList.contains('is-open') ? closeNotif() : openNotif());
notifClose?.addEventListener('click', closeNotif);
detailClose?.addEventListener('click', closeDetail);
detailModal?.addEventListener('click', e => { if (e.target === detailModal) closeDetail(); });

document.addEventListener('click', e => {
  if (!notifPanel?.contains(e.target) && !notifToggle?.contains(e.target)) closeNotif();
});

document.addEventListener('keydown', e => {
  if (e.key === 'Escape') { closeCart(); closeDetail(); closeNotif(); }
});

// ── Init ──────────────────────────────────────────────────────────────────────
renderCatalog();
renderCart();

// "Ver Ofertas" muestra solo productos con descuento activo
document.querySelector('#offers-link')?.addEventListener('click', () => {
  activeFilter = 'all';
  searchValue  = '';
  if (searchInput) searchInput.value = '';
  filterButtons.forEach(b => b.classList.remove('active'));
  filterButtons[0]?.classList.add('active');
  catalogGrid.innerHTML = '';
  productos
    .filter(p => p.porcentaje_descuento > 0)
    .forEach(p => catalogGrid.appendChild(buildCard(p)));
});
