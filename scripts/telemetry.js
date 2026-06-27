import { supabase, insertarTelemetria } from './supabaseClient.js';

let productViewStart     = null;
let currentViewProductId = null;

function esFinDeSemana() {
  const d = new Date().getDay();
  return d === 0 || d === 6;
}

async function getUserId() {
  if (!supabase) return null;
  const { data: { session } } = await supabase.auth.getSession();
  return session?.user?.id ?? null;
}

export async function trackView(productoId) {
  productViewStart     = Date.now();
  currentViewProductId = productoId;
  const usuario_id     = await getUserId();
  insertarTelemetria({
    usuario_id,
    producto_id:          productoId,
    tipo_evento:          'view',
    dwell_time_segundos:  null,
    precio_pagado:        null,
    metodo_pago:          null,
    es_fin_de_semana:     esFinDeSemana()
  });
}

export async function trackAddToCart(productoId, precio) {
  const dwell = productViewStart && currentViewProductId === productoId
    ? parseFloat(((Date.now() - productViewStart) / 1000).toFixed(2))
    : null;
  productViewStart     = null;
  currentViewProductId = null;
  const usuario_id     = await getUserId();
  insertarTelemetria({
    usuario_id,
    producto_id:         productoId,
    tipo_evento:         'add_to_cart',
    dwell_time_segundos: dwell,
    precio_pagado:       precio,
    metodo_pago:         null,
    es_fin_de_semana:    esFinDeSemana()
  });
}

export async function trackPurchase(items, metodoPago) {
  const usuario_id = await getUserId();
  items.forEach(item => {
    const precioFinal = parseFloat((item.price * (1 - (item.porcentaje_descuento ?? 0))).toFixed(2));
    insertarTelemetria({
      usuario_id,
      producto_id:         item.id,
      tipo_evento:         'purchase',
      dwell_time_segundos: null,
      precio_pagado:       precioFinal,
      metodo_pago:         metodoPago,
      es_fin_de_semana:    esFinDeSemana()
    });
  });
}
