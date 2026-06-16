import { getUserProfile } from './onboarding.js';
import { insertTelemetry } from './supabaseClient.js';

// Stores the timestamp used to calculate dwell time for the current page.
let pageEnterTimestamp = Date.now();

export function trackClickEvent(target) {
  const telemetryPayload = {
    event_type: 'click',
    target: target?.dataset?.productId || target?.id || 'unknown',
    category: target?.dataset?.category || null,
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

function initTelemetryTracking() {
  document.querySelectorAll('.product-action').forEach((button) => {
    button.addEventListener('click', () => {
      trackClickEvent(button);
    });
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initTelemetryTracking, { once: true });
} else {
  initTelemetryTracking();
}

window.addEventListener('pageshow', () => {
  pageEnterTimestamp = Date.now();
});

window.addEventListener('beforeunload', () => {
  trackDwellTime();
});
