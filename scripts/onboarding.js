const STORAGE_KEY = 'upyStoreUserProfile';

function encodeProfile(profile) {
  const utf8Binary = encodeURIComponent(JSON.stringify(profile)).replace(/%([0-9A-F]{2})/g, (_, hex) =>
    String.fromCharCode(Number.parseInt(hex, 16))
  );
  return window.btoa(utf8Binary);
}

function decodeProfile(value) {
  const binary = window.atob(value);
  const percentEncoded = Array.from(binary, (char) => `%${char.charCodeAt(0).toString(16).padStart(2, '0')}`).join('');
  return JSON.parse(decodeURIComponent(percentEncoded));
}

// Reads profile metadata that will be attached to telemetry events.
export function getUserProfile() {
  try {
    const sessionValue = sessionStorage.getItem(STORAGE_KEY);
    const localValue = localStorage.getItem(STORAGE_KEY);
    const storedValue = sessionValue || localValue;
    return storedValue ? decodeProfile(storedValue) : null;
  } catch {
    return null;
  }
}

export function saveUserProfile(profile) {
  const encoded = encodeProfile(profile);
  localStorage.setItem(STORAGE_KEY, encoded);
  sessionStorage.setItem(STORAGE_KEY, encoded);
}

function initOnboarding() {
  const modal = document.getElementById('onboarding-modal');
  const form = document.getElementById('onboarding-form');
  if (!modal || !form) {
    return;
  }

  if (!getUserProfile()) {
    modal.classList.add('is-open');
  }

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    const profile = {
      career: String(formData.get('career') || '').trim(),
      gender: String(formData.get('gender') || '').trim(),
      capturedAt: new Date().toISOString()
    };

    if (!profile.career || !profile.gender) {
      return;
    }

    saveUserProfile(profile);
    modal.classList.remove('is-open');
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initOnboarding, { once: true });
} else {
  initOnboarding();
}
