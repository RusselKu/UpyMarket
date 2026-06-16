const STORAGE_KEY = 'upyStoreUserProfile';
const modal = document.getElementById('onboarding-modal');
const form = document.getElementById('onboarding-form');

// Reads profile metadata that will be attached to telemetry events.
export function getUserProfile() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null');
  } catch {
    return null;
  }
}

export function saveUserProfile(profile) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(profile));
  sessionStorage.setItem(STORAGE_KEY, JSON.stringify(profile));
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
