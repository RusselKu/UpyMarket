const STORAGE_KEY = 'upyStoreUserProfile';
const modal = document.getElementById('onboarding-modal');
const form = document.getElementById('onboarding-form');

function encodeProfile(profile) {
  return window.btoa(unescape(encodeURIComponent(JSON.stringify(profile))));
}

function decodeProfile(value) {
  return JSON.parse(decodeURIComponent(escape(window.atob(value))));
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

if (modal && form) {
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
