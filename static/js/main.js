function toggleTheme() {
  const html = document.documentElement;
  const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  html.setAttribute('data-theme', next);
  try { localStorage.setItem('theme', next); } catch(e) {}
}

// Modal open/close
function openModal(id) {
  const el = document.getElementById(id);
  if (el) el.hidden = false;
}
function closeModal(id) {
  const el = document.getElementById(id);
  if (el) el.hidden = true;
}

// Delegated events
document.addEventListener('click', (e) => {
  const openId = e.target?.dataset?.open;
  const closeId = e.target?.dataset?.close;
  if (openId) { openModal(openId); }
  if (closeId) { closeModal(closeId); }
});
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeModal('message-modal');
});

// Send anonymous message
async function sendAnonMessage(e) {
  e.preventDefault();
  const form = e.target;
  const btn = document.getElementById('send-btn');
  const fb = document.getElementById('form-feedback');
  const data = new FormData(form);

  const payload = {
    name: data.get('name') || '',
    message: (data.get('message') || '').toString(),
    _hp: data.get('_hp') || ''
  };

  if (!payload.message || payload.message.trim().length < 10) {
    fb.textContent = 'Please write at least 10 characters.';
    return;
  }

  btn.disabled = true;
  fb.textContent = 'Sending...';

  try {
    const res = await fetch('/api/message', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const json = await res.json().catch(() => ({}));
    if (!res.ok || !json.ok) {
      fb.textContent = json.error || 'Could not send message now.';
      btn.disabled = false;
      return;
    }
    fb.textContent = 'Message sent. Thank you!';
    setTimeout(() => {
      form.reset();
      btn.disabled = false;
      fb.textContent = '';
      closeModal('message-modal');
    }, 700);
  } catch (err) {
    fb.textContent = 'Network error. Please try again.';
    btn.disabled = false;
  }
}

// Attach submit handler
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('message-form');
  if (form) form.addEventListener('submit', sendAnonMessage);
});