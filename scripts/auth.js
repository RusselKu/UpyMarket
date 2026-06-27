import { supabase, insertarPerfil } from './supabaseClient.js';

const DOMAIN = '@upy.edu.mx';

const modal        = document.getElementById('auth-modal');
const tabLogin     = document.getElementById('tab-login');
const tabRegister  = document.getElementById('tab-register');
const formLogin    = document.getElementById('form-login');
const formRegister = document.getElementById('form-register');

function validateDomain(email) {
  return email.toLowerCase().endsWith(DOMAIN);
}

function showMsg(form, msg, type = 'error') {
  const el = form.querySelector('.auth-message');
  if (!el) return;
  el.textContent = msg;
  el.className = `auth-message ${type}`;
}

function setLoading(form, on) {
  const btn = form.querySelector('button[type=submit]');
  if (!btn) return;
  btn.disabled = on;
  btn.textContent = on ? 'Cargando...' : (btn.dataset.label || btn.textContent);
}

function switchTab(tab) {
  const isLogin = tab === 'login';
  tabLogin.classList.toggle('active', isLogin);
  tabRegister.classList.toggle('active', !isLogin);
  formLogin.hidden = !isLogin;
  formRegister.hidden = isLogin;
  formLogin.querySelector('.auth-message').textContent = '';
  formRegister.querySelector('.auth-message').textContent = '';
}

tabLogin?.addEventListener('click', () => switchTab('login'));
tabRegister?.addEventListener('click', () => switchTab('register'));

// ── Login ─────────────────────────────────────────────────────────────────────
formLogin?.addEventListener('submit', async e => {
  e.preventDefault();
  const email    = formLogin.querySelector('[name=email]').value.trim();
  const password = formLogin.querySelector('[name=password]').value;

  if (!validateDomain(email)) {
    showMsg(formLogin, 'Solo se permiten correos @upy.edu.mx');
    return;
  }

  setLoading(formLogin, true);
  const { error } = await supabase.auth.signInWithPassword({ email, password });
  setLoading(formLogin, false);

  if (error) showMsg(formLogin, 'Correo o contraseña incorrectos');
});

// ── Register ──────────────────────────────────────────────────────────────────
formRegister?.addEventListener('submit', async e => {
  e.preventDefault();
  const email    = formRegister.querySelector('[name=email]').value.trim();
  const password = formRegister.querySelector('[name=password]').value;
  const carrera  = formRegister.querySelector('[name=carrera]').value;
  const genero   = formRegister.querySelector('[name=genero]').value;

  if (!validateDomain(email)) {
    showMsg(formRegister, 'Solo se permiten correos @upy.edu.mx');
    return;
  }

  setLoading(formRegister, true);
  const { error } = await supabase.auth.signUp({
    email,
    password,
    options: { data: { carrera, genero } }
  });
  setLoading(formRegister, false);

  if (error) {
    showMsg(formRegister, error.message);
  } else {
    showMsg(formRegister, '¡Revisa tu correo @upy.edu.mx y confirma tu cuenta!', 'success');
  }
});

// ── Auth state ────────────────────────────────────────────────────────────────
supabase?.auth.onAuthStateChange(async (event, session) => {
  if (event === 'SIGNED_IN' && session?.user) {
    const user = session.user;
    updateAvatar(user.email);
    modal?.classList.remove('is-open');
    window.dispatchEvent(new CustomEvent('upymarket:signed-in'));

    // Crear perfil en usuarios_sesion si es la primera vez
    const { data: existing } = await supabase
      .from('usuarios_sesion')
      .select('id')
      .eq('id', user.id)
      .single();

    if (!existing) {
      const { carrera, genero } = user.user_metadata || {};
      if (carrera && genero) {
        await insertarPerfil(user.id, carrera, genero);
      }
    }
  } else if (event === 'SIGNED_OUT') {
    updateAvatar(null);
    modal?.classList.add('is-open');
  }
});

function updateAvatar(email) {
  const el = document.querySelector('.user-avatar');
  if (!el) return;
  if (!email) { el.textContent = 'ES'; el.title = 'Perfil'; return; }
  const name = email.split('@')[0];
  el.textContent = name.slice(0, 2).toUpperCase();
  el.title = email;
}

// Logout al hacer click en el avatar
document.querySelector('.user-avatar')?.addEventListener('click', async () => {
  if (!supabase) return;
  const ok = confirm('¿Cerrar sesión?');
  if (ok) await supabase.auth.signOut();
});

// ── Init ──────────────────────────────────────────────────────────────────────
async function init() {
  if (!supabase) { modal?.classList.add('is-open'); return; }
  const { data: { session } } = await supabase.auth.getSession();
  if (session?.user) {
    updateAvatar(session.user.email);
  } else {
    modal?.classList.add('is-open');
  }
}

init();
