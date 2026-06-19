import { getUserProfile } from './onboarding.js';
import { insertTelemetry } from './supabaseClient.js';

// Stores the timestamp used to calculate dwell time for the current page.
let pageEnterTimestamp = Date.now();

function getProductTelemetryData(target) {
  const productCard = target.closest('.product-card');

  return {
    productId:
      target?.dataset?.productId ||
      productCard?.dataset?.productId ||
      target?.id ||
      'unknown',

    category:
      target?.dataset?.category ||
      productCard?.dataset?.category ||
      null,

    action:
      target?.dataset?.action ||
      'click'
  };
}

export function trackClickEvent(target) {
  const { productId, category, action } = getProductTelemetryData(target);

  const telemetryPayload = {
    event_type: action,
    target: productId,
    category: category,
    user_profile: getUserProfile(),
    created_at: new Date().toISOString()
  };

  return insertTelemetry(telemetryPayload);
}

export function trackDwellTime(pageName = 'catalog') {
  const dwellSeconds = Math.round((Date.now() - pageEnterTimestamp) / 1000);

  const telemetryPayload = {
    event_type: 'dwell',
    page: pageName,
    dwell_seconds: dwellSeconds,
    user_profile: getUserProfile(),
    created_at: new Date().toISOString()
  };

  return insertTelemetry(telemetryPayload);
}

document.querySelectorAll('.product-action').forEach((button) => {
  button.addEventListener('click', () => {
    trackClickEvent(button);
  });
});

window.addEventListener('pageshow', () => {
  pageEnterTimestamp = Date.now();
});

window.addEventListener('beforeunload', () => {
  trackDwellTime();
});