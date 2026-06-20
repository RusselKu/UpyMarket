const SUPABASE_URL = window.UPYSTORE_SUPABASE_URL || '';
const SUPABASE_ANON_KEY = window.UPYSTORE_SUPABASE_ANON_KEY || '';

export const supabase =
  SUPABASE_URL && SUPABASE_ANON_KEY && window.supabase
    ? window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY)
    : null;

if (!supabase) {
  console.warn('[UpyMarket] Supabase no configurado. Edita config.js con tus credenciales.');
}

export async function insertarUsuario(carrera, genero) {
  if (!supabase) return null;
  const { data, error } = await supabase
    .from('usuarios_sesion')
    .insert({ carrera, genero })
    .select('id')
    .single();
  if (error) { console.warn('[UpyMarket] Error al insertar usuario:', error.message); return null; }
  return data?.id ?? null;
}

export async function insertarTelemetria(payload) {
  if (!supabase) return;
  const { error } = await supabase.from('interacciones_telemetria').insert(payload);
  if (error) console.warn('[UpyMarket] Error telemetría:', error.message);
}
