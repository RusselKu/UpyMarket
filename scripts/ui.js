import { cargarProductos } from './supabaseClient.js';
import { trackView, trackAddToCart, trackPurchase } from './telemetry.js';

let productos = [];
let activeFilter = 'all';
let searchValue = '';
let cart = JSON.parse(sessionStorage.getItem('upymarket_cart')) || [];

const catalogGrid = document.querySelector('#catalog-grid');
const searchInput = document.querySelector('#product-search');
const filterButtons = document.querySelectorAll('.filter-chip[data-filter]');

const cartPanel = document.querySelector('#cart-panel');
const cartToggle = document.querySelector('#cart-toggle');
const cartClose = document.querySelector('#cart-close');
const cartCount = document.querySelector('#cart-count');
const cartItems = document.querySelector('#cart-items');
const cartEmpty = document.querySelector('#cart-empty');
const cartTotalEl = document.querySelector('#cart-total');
const paymentSelect = document.querySelector('#payment-method');
const checkoutBtn = document.querySelector('.checkout-button');

const notifToggle = document.querySelector('#notification-toggle');
const notifClose = document.querySelector('#notification-close');
const notifPanel = document.querySelector('#notification-panel');

const detailModal = document.querySelector('#product-detail-modal');
const detailClose = document.querySelector('#product-detail-close');
const detailIcon = document.querySelector('#product-detail-icon');
const detailTitle = document.querySelector('#product-detail-title');
const detailCategory = document.querySelector('#product-detail-category');
const detailDescription = document.querySelector('#product-detail-description');
const detailFeatures = document.querySelector('#product-detail-features');
const detailPrice = document.querySelector('#product-detail-price');
const detailPriceOrig = document.querySelector('#product-detail-price-original');
const detailAdd = document.querySelector('#product-detail-add');

const cartToast = document.querySelector('#cart-toast');

function precioConDescuento(producto) {
  return producto.precio_original * (1 - producto.porcentaje_descuento);
}

function formatPrice(amount) {
  return `$${amount.toFixed(2)}`;
}

function categoryClass(categoria) {
  if (categoria === 'Académico') return 'academic';
  if (categoria === 'Books') return 'books';
  if (categoria === 'Food') return 'food';
  if (categoria === 'Services') return 'services';
  if (categoria === 'Entretenimiento') return 'leisure';
  if (categoria === 'Sports') return 'sports';
  if (categoria === 'Other') return 'other';
  if (categoria === 'Laptop') return 'tech';
  return 'tech';
}

function iconClass(categoria) {
  if (categoria === 'Académico') return 'academic-icon';
  if (categoria === 'Books') return 'books-icon';
  if (categoria === 'Food') return 'food-icon';
  if (categoria === 'Services') return 'services-icon';
  if (categoria === 'Entretenimiento') return 'leisure-icon';
  if (categoria === 'Sports') return 'sports-icon';
  if (categoria === 'Other') return 'other-icon';
  if (categoria === 'Laptop') return 'tech-icon';
  return 'tech-icon';
}

function displayCategory(categoria) {
  if (categoria === 'Académico') return 'Academic';
  if (categoria === 'Entretenimiento') return 'Entertainment';
  if (categoria === 'Laptop') return 'Technology';
  return categoria;
}

function productImage(producto) {
  const text = `${producto.nombre} ${producto.descripcion}`.toLowerCase();

  if (producto.categoria === 'Laptop') {
    return producto.tiene_gpu_dedicada
      ? 'assets/product-images/laptop-gpu.svg'
      : 'assets/product-images/laptop.svg';
  }

  if (producto.categoria === 'Académico') {
    if (text.includes('curso') || text.includes('tutoria') || text.includes('certific')) {
      return 'assets/product-images/services.svg';
    }
    return 'assets/product-images/academic.svg';
  }

  if (producto.categoria === 'Books') return 'assets/product-images/books.svg';
  if (producto.categoria === 'Food') return 'assets/product-images/food.svg';
  if (producto.categoria === 'Services') return 'assets/product-images/services.svg';
  if (producto.categoria === 'Sports') return 'assets/product-images/sports.svg';
  if (producto.categoria === 'Other') return 'assets/product-images/other.svg';
  return 'assets/product-images/entertainment.svg';
}

function sellerLabel(producto) {
  if (producto.carrera_objetivo && producto.carrera_objetivo !== 'Todas') {
    return `Seller: ${producto.carrera_objetivo}`;
  }
  if (producto.categoria === 'Laptop') return 'Seller: UPY Tech Circle';
  if (producto.categoria === 'Académico') return 'Seller: Student Academic Hub';
  return 'Seller: UPY Community';
}

function conditionLabel(producto) {
  if (producto.categoria === 'Laptop') return 'Condition: Verified listing';
  if (producto.porcentaje_descuento > 0) return 'Condition: Featured offer';
  return 'Condition: Active listing';
}

function buildCard(producto) {
  const precioFinal = precioConDescuento(producto);
  const tieneDescuento = producto.porcentaje_descuento > 0;
  const pct = Math.round(producto.porcentaje_descuento * 100);
  const carreraTag = producto.carrera_objetivo !== 'Todas'
    ? `<span class="career-tag">Career: ${producto.carrera_objetivo}</span>`
    : '';
  const discountBadge = tieneDescuento
    ? `<span class="discount-badge">-${pct}%</span>`
    : '';
  const priceHTML = tieneDescuento
    ? `<div class="price-wrapper">
         <span class="price-original">${formatPrice(producto.precio_original)}</span>
         <span class="price">${formatPrice(precioFinal)}</span>
       </div>`
    : `<span class="price">${formatPrice(producto.precio_original)}</span>`;

  const gpuBadge = producto.tiene_gpu_dedicada
    ? '<span class="gpu-badge">GPU</span>'
    : '';

  const article = document.createElement('article');
  article.className = 'product-card glass-card';
  article.dataset.productId = producto.id;
  article.dataset.category = producto.categoria;
  article.innerHTML = `
    ${discountBadge}${gpuBadge}
    <div class="product-icon ${iconClass(producto.categoria)}">
      <img src="${productImage(producto)}" alt="${producto.nombre}" loading="lazy" />
    </div>
    <div class="product-topline">
      <span class="category-badge ${categoryClass(producto.categoria)}">${displayCategory(producto.categoria)}</span>
      ${priceHTML}
    </div>
    <h3>${producto.nombre}</h3>
    ${carreraTag}
    <p>${producto.descripcion}</p>
    <div class="product-meta">
      <span class="product-seller">${sellerLabel(producto)}</span>
      <span class="product-state">${conditionLabel(producto)}</span>
    </div>
    <div class="product-buttons">
      <button type="button" class="product-action" data-action="view_product">View details</button>
      <button type="button" class="product-action add-cart-action" data-action="add_to_cart">Add to cart</button>
    </div>
  `;
  return article;
}

function filteredProducts() {
  return productos.filter((producto) => {
    const matchCat = activeFilter === 'all' || producto.categoria === activeFilter;
    const q = searchValue.toLowerCase();
    const matchSearch = !q
      || producto.nombre.toLowerCase().includes(q)
      || producto.categoria.toLowerCase().includes(q)
      || producto.descripcion.toLowerCase().includes(q)
      || producto.carrera_objetivo.toLowerCase().includes(q);
    return matchCat && matchSearch;
  });
}

function renderCatalog() {
  if (!catalogGrid) return;
  catalogGrid.innerHTML = '';
  const list = filteredProducts();
  if (list.length === 0) {
    catalogGrid.innerHTML = '<p class="no-results">No products matched your search.</p>';
    return;
  }
  list.forEach((producto) => catalogGrid.appendChild(buildCard(producto)));
}

function saveCart() {
  sessionStorage.setItem('upymarket_cart', JSON.stringify(cart));
}

function renderCart() {
  if (!cartItems || !cartCount || !cartTotalEl || !cartEmpty) return;
  cartItems.innerHTML = '';
  const totalQty = cart.reduce((sum, item) => sum + item.quantity, 0);
  const totalAmount = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
  cartCount.textContent = totalQty;
  cartTotalEl.textContent = formatPrice(totalAmount);
  cartEmpty.hidden = cart.length > 0;

  cart.forEach((item) => {
    const div = document.createElement('div');
    div.className = 'cart-item';
    div.innerHTML = `
      <div>
        <h3>${item.name}</h3>
        <p>${item.category} · ${formatPrice(item.price)}</p>
      </div>
      <div class="cart-item-actions">
        <span>Qty: ${item.quantity}</span>
        <button type="button" data-remove-id="${item.id}">Remove</button>
      </div>`;
    cartItems.appendChild(div);
  });

  document.querySelectorAll('[data-remove-id]').forEach((btn) => {
    btn.addEventListener('click', () => {
      cart = cart.filter((item) => item.id !== btn.dataset.removeId);
      saveCart();
      renderCart();
    });
  });
}

function addToCart(producto) {
  const existing = cart.find((item) => item.id === producto.id);
  if (existing) {
    existing.quantity += 1;
  } else {
    cart.push({ ...producto, quantity: 1 });
  }
  saveCart();
  renderCart();
  openCart();
  showToast(`${producto.name || producto.nombre || 'Product'} added to cart`);
}

function openCart() {
  closeNotif();
  cartPanel?.classList.add('is-open');
}

function closeCart() {
  cartPanel?.classList.remove('is-open');
}

function openNotif() {
  closeCart();
  notifPanel?.classList.add('is-open');
}

function closeNotif() {
  notifPanel?.classList.remove('is-open');
}

function showToast(msg) {
  if (!cartToast) return;
  cartToast.textContent = msg;
  cartToast.classList.add('is-visible');
  setTimeout(() => cartToast.classList.remove('is-visible'), 2400);
}

function openDetail(productId) {
  const producto = productos.find((item) => item.id === productId);
  if (!producto || !detailModal) return;

  trackView(producto.id);

  const tieneDescuento = producto.porcentaje_descuento > 0;
  const pct = Math.round(producto.porcentaje_descuento * 100);
  const precioFinal = precioConDescuento(producto);

  detailIcon.innerHTML = `<img src="${productImage(producto)}" alt="${producto.nombre}" />`;
  detailTitle.textContent = producto.nombre;
  detailCategory.textContent = displayCategory(producto.categoria);
  detailCategory.className = `category-badge ${categoryClass(producto.categoria)}`;
  detailDescription.textContent = producto.descripcion;

  if (detailPrice) detailPrice.textContent = formatPrice(precioFinal);
  if (detailPriceOrig) {
    detailPriceOrig.textContent = tieneDescuento
      ? `${formatPrice(producto.precio_original)} (-${pct}%)`
      : '';
    detailPriceOrig.hidden = !tieneDescuento;
  }

  detailFeatures.innerHTML = '';
  (producto.caracteristicas || []).forEach((feature) => {
    const li = document.createElement('li');
    li.textContent = feature;
    detailFeatures.appendChild(li);
  });

  if (detailAdd) {
    detailAdd.dataset.productId = producto.id;
    detailAdd.dataset.price = precioFinal.toFixed(2);
    detailAdd.dataset.name = producto.nombre;
    detailAdd.dataset.category = producto.categoria;
  }

  closeCart();
  closeNotif();
  detailModal.classList.add('is-open');
}

function closeDetail() {
  detailModal?.classList.remove('is-open');
}

catalogGrid?.addEventListener('click', (event) => {
  const btn = event.target.closest('[data-action]');
  if (!btn) return;
  const card = btn.closest('.product-card');
  const productId = card?.dataset.productId;
  if (!productId) return;

  if (btn.dataset.action === 'view_product') {
    openDetail(productId);
  }

  if (btn.dataset.action === 'add_to_cart') {
    const producto = productos.find((item) => item.id === productId);
    if (!producto) return;
    const precio = precioConDescuento(producto);
    trackAddToCart(producto.id, precio);
    addToCart({
      id: producto.id,
      name: producto.nombre,
      category: producto.categoria,
      price: precio,
      porcentaje_descuento: producto.porcentaje_descuento
    });
  }
});

detailAdd?.addEventListener('click', () => {
  const id = detailAdd.dataset.productId;
  const price = parseFloat(detailAdd.dataset.price) || 0;
  const name = detailAdd.dataset.name || 'Producto';
  const category = detailAdd.dataset.category || '';
  const producto = productos.find((item) => item.id === id);
  trackAddToCart(id, price);
  addToCart({
    id,
    name,
    category,
    price,
    porcentaje_descuento: producto?.porcentaje_descuento ?? 0
  });
  closeDetail();
});

filterButtons.forEach((btn) => {
  btn.addEventListener('click', () => {
    activeFilter = btn.dataset.filter;
    filterButtons.forEach((item) => item.classList.remove('active'));
    btn.classList.add('active');
    renderCatalog();
  });
});

searchInput?.addEventListener('input', () => {
  searchValue = searchInput.value.trim();
  renderCatalog();
});

checkoutBtn?.addEventListener('click', () => {
  if (cart.length === 0) {
    showToast('Your cart is empty');
    return;
  }

  const metodo = paymentSelect?.value || 'No especificado';
  if (!metodo || metodo === '') {
    showToast('Select a payment method');
    return;
  }

  trackPurchase(cart, metodo);
  cart = [];
  saveCart();
  renderCart();
  closeCart();
  showToast('Purchase recorded successfully');
});

cartToggle?.addEventListener('click', () => (
  cartPanel?.classList.contains('is-open') ? closeCart() : openCart()
));
cartClose?.addEventListener('click', closeCart);
notifToggle?.addEventListener('click', () => (
  notifPanel?.classList.contains('is-open') ? closeNotif() : openNotif()
));
notifClose?.addEventListener('click', closeNotif);
detailClose?.addEventListener('click', closeDetail);
detailModal?.addEventListener('click', (event) => {
  if (event.target === detailModal) closeDetail();
});

document.addEventListener('click', (event) => {
  if (!notifPanel?.contains(event.target) && !notifToggle?.contains(event.target)) {
    closeNotif();
  }
});

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') {
    closeCart();
    closeDetail();
    closeNotif();
  }
});

if (catalogGrid) {
  catalogGrid.innerHTML = '<p class="no-results" style="grid-column:1/-1;text-align:center;padding:3rem 1rem">Cargando productos...</p>';
}
(async () => {
  productos = await cargarProductos();
  renderCatalog();
  renderCart();
})();
