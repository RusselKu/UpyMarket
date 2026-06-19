const searchInput = document.querySelector('#product-search');
const filterButtons = document.querySelectorAll('.filter-chip[data-filter]');
const productCards = document.querySelectorAll('.product-card');

const cartToast = document.querySelector('#cart-toast');
const cartToggle = document.querySelector('#cart-toggle');
const cartClose = document.querySelector('#cart-close');
const cartPanel = document.querySelector('#cart-panel');
const cartCount = document.querySelector('#cart-count');
const cartItems = document.querySelector('#cart-items');
const cartEmpty = document.querySelector('#cart-empty');
const cartTotal = document.querySelector('#cart-total');

const notificationToggle = document.querySelector('#notification-toggle');
const notificationClose = document.querySelector('#notification-close');
const notificationPanel = document.querySelector('#notification-panel');

const productDetailModal = document.querySelector('#product-detail-modal');
const productDetailClose = document.querySelector('#product-detail-close');
const productDetailIcon = document.querySelector('#product-detail-icon');
const productDetailTitle = document.querySelector('#product-detail-title');
const productDetailCategory = document.querySelector('#product-detail-category');
const productDetailDescription = document.querySelector('#product-detail-description');
const productDetailFeatures = document.querySelector('#product-detail-features');
const productDetailPrice = document.querySelector('#product-detail-price');
const productDetailAdd = document.querySelector('#product-detail-add');

let activeFilter = 'all';
let cart = JSON.parse(sessionStorage.getItem('upystore_cart')) || [];

const productExtraDetails = {
  p1: {
    icon: '📘',
    description:
      'Study Planner Pro helps students organize assignments, exams, projects, and weekly academic goals in one simple tool.',
    features: ['Academic planning', 'Weekly organization', 'Exam tracking']
  },
  p2: {
    icon: '🎧',
    description:
      'Campus Headphones are designed for online classes, focus sessions, campus breaks, and everyday entertainment.',
    features: ['Lightweight design', 'Online class ready', 'Portable audio']
  },
  p3: {
    icon: '💻',
    description:
      'NovaBook G15 is a GPU-powered laptop for programming, data projects, design work, and high-performance student tasks.',
    features: ['Dedicated GPU', 'Data workload support', 'High-performance projects']
  }
};

function normalizeText(text) {
  return text.toLowerCase().trim();
}

function updateCatalogVisibility() {
  const searchValue = normalizeText(searchInput?.value || '');

  productCards.forEach((card) => {
    const productName = normalizeText(card.querySelector('h3')?.textContent || '');
    const productCategory = card.dataset.category || '';
    const productDescription = normalizeText(card.querySelector('p')?.textContent || '');

    const matchesSearch =
      productName.includes(searchValue) ||
      normalizeText(productCategory).includes(searchValue) ||
      productDescription.includes(searchValue);

    const matchesFilter = activeFilter === 'all' || productCategory === activeFilter;

    card.hidden = !(matchesSearch && matchesFilter);
  });
}

filterButtons.forEach((button) => {
  button.addEventListener('click', () => {
    activeFilter = button.dataset.filter;

    filterButtons.forEach((item) => item.classList.remove('active'));
    button.classList.add('active');

    updateCatalogVisibility();
  });
});

searchInput?.addEventListener('input', updateCatalogVisibility);

function getProductData(button) {
  const productCard = button.closest('.product-card');

  const id =
    productCard?.dataset.productId ||
    button.dataset.productId ||
    'unknown';

  const category =
    productCard?.dataset.category ||
    button.dataset.category ||
    'Unknown';

  const name =
    productCard?.querySelector('h3')?.textContent ||
    button.dataset.productName ||
    'Product';

  const priceText =
    productCard?.querySelector('.price')?.textContent ||
    button.dataset.price ||
    '$0';

  const price = Number(priceText.replace('$', '').trim()) || 0;

  return {
    id,
    name,
    category,
    price
  };
}

function saveCart() {
  sessionStorage.setItem('upystore_cart', JSON.stringify(cart));
}

function renderCart() {
  if (!cartItems || !cartCount || !cartTotal || !cartEmpty) return;

  cartItems.innerHTML = '';

  const totalQuantity = cart.reduce((sum, item) => sum + item.quantity, 0);
  const totalAmount = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);

  cartCount.textContent = totalQuantity;
  cartTotal.textContent = `$${totalAmount.toFixed(2)}`;

  cartEmpty.hidden = cart.length > 0;

  cart.forEach((item) => {
    const cartItem = document.createElement('div');
    cartItem.className = 'cart-item';

    cartItem.innerHTML = `
      <div>
        <h3>${item.name}</h3>
        <p>${item.category} · $${item.price.toFixed(2)}</p>
      </div>

      <div class="cart-item-actions">
        <span>Qty: ${item.quantity}</span>
        <button type="button" data-remove-id="${item.id}">Remove</button>
      </div>
    `;

    cartItems.appendChild(cartItem);
  });

  document.querySelectorAll('[data-remove-id]').forEach((button) => {
    button.addEventListener('click', () => {
      const productId = button.dataset.removeId;
      cart = cart.filter((item) => item.id !== productId);
      saveCart();
      renderCart();
    });
  });
}

function openCart() {
  closeNotifications();
  cartPanel?.classList.add('is-open');
}

function closeCart() {
  cartPanel?.classList.remove('is-open');
}

function openNotifications() {
  closeCart();
  notificationPanel?.classList.add('is-open');
}

function closeNotifications() {
  notificationPanel?.classList.remove('is-open');
}

function showToast(message) {
  if (!cartToast) return;

  cartToast.textContent = message;
  cartToast.classList.add('is-visible');

  setTimeout(() => {
    cartToast.classList.remove('is-visible');
  }, 2200);
}

function addProductToCart(product) {
  const existingProduct = cart.find((item) => item.id === product.id);

  if (existingProduct) {
    existingProduct.quantity += 1;
  } else {
    cart.push({
      ...product,
      quantity: 1
    });
  }

  saveCart();
  renderCart();
  openCart();
  showToast(`${product.name} added to cart`);
}

function setCategoryBadgeStyle(category) {
  if (!productDetailCategory) return;

  productDetailCategory.className = 'category-badge';

  if (category === 'Academic') {
    productDetailCategory.classList.add('academic');
  } else if (category === 'Leisure') {
    productDetailCategory.classList.add('leisure');
  } else {
    productDetailCategory.classList.add('tech');
  }
}

function openProductDetail(button) {
  const product = getProductData(button);
  const details = productExtraDetails[product.id] || {
    icon: '📦',
    description: 'Detailed information for this product.',
    features: ['Student-focused product', 'Useful interaction data', 'Marketplace item']
  };

  if (
    !productDetailModal ||
    !productDetailIcon ||
    !productDetailTitle ||
    !productDetailCategory ||
    !productDetailDescription ||
    !productDetailFeatures ||
    !productDetailPrice ||
    !productDetailAdd
  ) {
    return;
  }

  productDetailIcon.textContent = details.icon;
  productDetailTitle.textContent = product.name;
  productDetailCategory.textContent = product.category;
  productDetailDescription.textContent = details.description;
  productDetailPrice.textContent = `$${product.price.toFixed(2)}`;

  setCategoryBadgeStyle(product.category);

  productDetailFeatures.innerHTML = '';

  details.features.forEach((feature) => {
    const item = document.createElement('li');
    item.textContent = feature;
    productDetailFeatures.appendChild(item);
  });

  productDetailAdd.dataset.productId = product.id;
  productDetailAdd.dataset.category = product.category;
  productDetailAdd.dataset.productName = product.name;
  productDetailAdd.dataset.price = `$${product.price.toFixed(2)}`;

  closeCart();
  closeNotifications();
  productDetailModal.classList.add('is-open');
}

function closeProductDetail() {
  productDetailModal?.classList.remove('is-open');
}

document.querySelectorAll('[data-action="view_product"]').forEach((button) => {
  button.addEventListener('click', () => {
    openProductDetail(button);
  });
});

document.querySelectorAll('[data-action="add_to_cart"]').forEach((button) => {
  button.addEventListener('click', () => {
    const product = getProductData(button);
    addProductToCart(product);

    if (button.id === 'product-detail-add') {
      closeProductDetail();
    }
  });
});

cartToggle?.addEventListener('click', () => {
  const isOpen = cartPanel?.classList.contains('is-open');

  if (isOpen) {
    closeCart();
  } else {
    openCart();
  }
});

cartClose?.addEventListener('click', closeCart);

notificationToggle?.addEventListener('click', () => {
  const isOpen = notificationPanel?.classList.contains('is-open');

  if (isOpen) {
    closeNotifications();
  } else {
    openNotifications();
  }
});

notificationClose?.addEventListener('click', closeNotifications);

productDetailClose?.addEventListener('click', closeProductDetail);

productDetailModal?.addEventListener('click', (event) => {
  if (event.target === productDetailModal) {
    closeProductDetail();
  }
});

document.addEventListener('click', (event) => {
  const clickedInsideNotifications = notificationPanel?.contains(event.target);
  const clickedNotificationButton = notificationToggle?.contains(event.target);

  if (!clickedInsideNotifications && !clickedNotificationButton) {
    closeNotifications();
  }
});

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') {
    closeCart();
    closeProductDetail();
    closeNotifications();
  }
});

renderCart();