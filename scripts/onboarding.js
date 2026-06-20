import { insertarUsuario } from './supabaseClient.js';

const STORAGE_KEY = 'upyMarketPerfil';
const modal = document.getElementById('onboarding-modal');
const form  = document.getElementById('onboarding-form');
const avatarEl = document.querySelector('.user-avatar');

function encodeProfile(profile) {
  return window.btoa(unescape(encodeURIComponent(JSON.stringify(profile))));
}

function decodeProfile(value) {
  return JSON.parse(decodeURIComponent(escape(window.atob(value))));
}

export function getUserProfile() {
  try {
    const val = sessionStorage.getItem(STORAGE_KEY) || localStorage.getItem(STORAGE_KEY);
    return val ? decodeProfile(val) : null;
  } catch {
    return null;
  }
}

export function saveUserProfile(profile) {
  const encoded = encodeProfile(profile);
  localStorage.setItem(STORAGE_KEY, encoded);
  sessionStorage.setItem(STORAGE_KEY, encoded);
}

function updateAvatar(carrera) {
  if (!avatarEl) return;
  const initials = carrera
    .split(' ')
    .slice(0, 2)
    .map(w => w[0]?.toUpperCase() ?? '')
    .join('');
  avatarEl.textContent = initials || 'ES';
  avatarEl.title = carrera;
}

if (modal && form) {
  const profile = getUserProfile();
  if (profile) {
    updateAvatar(profile.carrera);
  } else {
    modal.classList.add('is-open');
  }

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const fd = new FormData(form);
    const carrera = String(fd.get('carrera') || '').trim();
    const genero  = String(fd.get('genero')  || '').trim();
    if (!carrera || !genero) return;

    const submitBtn = form.querySelector('button[type="submit"]');
    if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = 'Guardando...'; }

    const userId = await insertarUsuario(carrera, genero);

    const profile = { carrera, genero, userId, capturedAt: new Date().toISOString() };
    saveUserProfile(profile);
    updateAvatar(carrera);
    modal.classList.remove('is-open');
  });
}
