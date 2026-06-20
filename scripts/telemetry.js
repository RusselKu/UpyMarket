import { getUserProfile } from './onboarding.js';
import { insertarTelemetria } from './supabaseClient.js';

let productViewStart = null;
let currentViewProductId = null;

function esFinDeSemana() {
  const d = new Date().getDay();
  return d === 0 || d === 6;
}

function basePayload(productoId) {
  const profile = getUserProfile();
  return {
    usuario_id:    profile?.userId ?? null,
    producto_id:   productoId,
    es_fin_de_semana: esFinDeSemana()
  };
}

export function trackView(productoId) {
  productViewStart = Date.now();
  currentViewProductId = productoId;
  insertarTelemetria({ ...basePayload(productoId), tipo_evento: 'view', dwell_time_segundos: null, precio_pagado: null, metodo_pago: null });
}

export function trackAddToCart(productoId, precio) {
  const dwell = productViewStart && currentViewProductId === productoId
    ? parseFloat(((Date.now() - productViewStart) / 1000).toFixed(2))
    : null;
  productViewStart = null;
  currentViewProductId = null;
  insertarTelemetria({ ...basePayload(productoId), tipo_evento: 'add_to_cart', dwell_time_segundos: dwell, precio_pagado: precio, metodo_pago: null });
}

export function trackPurchase(items, metodoPago) {
  items.forEach(item => {
    const precioFinal = parseFloat((item.price * (1 - (item.porcentaje_descuento ?? 0))).toFixed(2));
    insertarTelemetria({ ...basePayload(item.id), tipo_evento: 'purchase', dwell_time_segundos: null, precio_pagado: precioFinal, metodo_pago: metodoPago });
  });
}
