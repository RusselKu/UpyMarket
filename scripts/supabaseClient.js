// Configure public Supabase credentials via global variables for GitHub Pages deployments.
const SUPABASE_URL = window.UPYSTORE_SUPABASE_URL || 'https://YOUR_PROJECT.supabase.co';
const SUPABASE_ANON_KEY = window.UPYSTORE_SUPABASE_ANON_KEY || 'YOUR_PUBLIC_ANON_KEY';

export const supabase = window.supabase?.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

export async function insertTelemetry(payload) {
  if (!supabase) {
    console.warn('Supabase client not available. Configure credentials before production use.');
    return { error: 'Supabase client unavailable' };
  }

  return supabase.from('interacciones_crudas').insert(payload);
}
