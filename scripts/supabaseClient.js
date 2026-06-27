const SUPABASE_URL      = window.UPYSTORE_SUPABASE_URL      || '';
const SUPABASE_ANON_KEY = window.UPYSTORE_SUPABASE_ANON_KEY || '';

export const supabase =
  SUPABASE_URL && SUPABASE_ANON_KEY && window.supabase
    ? window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY)
    : null;

if (!supabase) {
  console.warn('[UpyMarket] Supabase no configurado. Edita config.js con tus credenciales.');
}

export async function cargarProductos() {
  if (!supabase) return [];
  const { data, error } = await supabase
    .from('catalogo_productos')
    .select('*')
    .order('id');
  if (error) { console.warn('[UpyMarket] Error cargando productos:', error.message); return []; }
  return (data || []).map(p => ({ ...p, categoria: p.categoria_general }));
}

export async function insertarPerfil(userId, carrera, genero) {
  if (!supabase) return null;
  const { data, error } = await supabase
    .from('usuarios_sesion')
    .insert({ id: userId, carrera, genero })
    .select('id')
    .single();
  if (error) { console.warn('[UpyMarket] Error al insertar perfil:', error.message); return null; }
  return data?.id ?? null;
}

export async function insertarTelemetria(payload) {
  if (!supabase) return;
  const { error } = await supabase.from('interacciones_telemetria').insert(payload);
  if (error) console.warn('[UpyMarket] Error telemetría:', error.message);
}
