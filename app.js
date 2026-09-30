const KEY = 'chatbot-ai-history';
const themeKey = 'chatbot-ai-theme';
const input = document.querySelector('#messageInput');
const conversation = document.querySelector('#conversation');
const welcome = document.querySelector('#welcome');
const sendButton = document.querySelector('#sendButton');
let messages = JSON.parse(localStorage.getItem(KEY) || '[]');

function save() { localStorage.setItem(KEY, JSON.stringify(messages)); }
function scrollDown() { conversation.scrollTo({ top: conversation.scrollHeight, behavior: 'smooth' }); }
function addMessage(role, text, persist = true) {
  if (welcome) welcome.style.display = 'none';
  const row = document.createElement('div'); row.className = `message ${role}`;
  const avatar = document.createElement('div'); avatar.className = 'avatar'; avatar.textContent = role === 'ai' ? '✦' : 'Vy';
  const bubble = document.createElement('div'); bubble.className = 'bubble'; bubble.textContent = text;
  if (role === 'user') row.append(bubble, avatar); else row.append(avatar, bubble);
  conversation.appendChild(row); if (persist) { messages.push({ role, text }); save(); } scrollDown();
}
function showTyping() { const row = document.createElement('div'); row.className = 'message ai'; row.id = 'typing'; row.innerHTML = '<div class="avatar">✦</div><div class="bubble typing"><i></i><i></i><i></i></div>'; conversation.appendChild(row); scrollDown(); }
function generateReply(text) {
  const t = text.toLowerCase();
  if (t.includes('projekt') || t.includes('nápad')) return 'Pojďme na to s lehkostí. Navrhuji začít malým experimentem: vyberte jedno téma, jednu cílovou osobu a jeden konkrétní výsledek, který může vzniknout během týdne. Jaké téma vás právě nejvíc přitahuje?';
  if (t.includes('slož') || t.includes('vysvět')) return 'Rád to přeložím do jednoduchého jazyka. Pošlete mi pojem nebo otázku a vysvětlím ji ve třech vrstvách: jednou větou, příkladem a praktickým použitím.';
  if (t.includes('den') || t.includes('plán')) return 'Začněme realisticky: vyberte jednu důležitou věc, dvě menší a prostor na odpočinek. Co je dnes váš nejdůležitější výsledek? Pomohu vám z něj sestavit konkrétní plán.';
  if (t.includes('ahoj') || t.includes('čau')) return 'Ahoj! Jsem rád, že jste tady. Co dnes společně vytvoříme nebo vyřešíme?';
  return 'To je zajímavá myšlenka. Abych vám odpověděl co nejlépe, můžeme ji rozdělit na menší kroky. Co je pro vás na této otázce nejdůležitější — porozumět jí, něco naplánovat, nebo vytvořit konkrétní výsledek?';
}
function send() { const text = input.value.trim(); if (!text) return; addMessage('user', text); input.value = ''; input.style.height = 'auto'; showTyping(); setTimeout(() => { document.querySelector('#typing')?.remove(); addMessage('ai', generateReply(text)); }, 650); }
function renderHistory() { messages.forEach(m => addMessage(m.role, m.text, false)); }
input.addEventListener('input', () => { input.style.height = 'auto'; input.style.height = `${Math.min(input.scrollHeight, 140)}px`; });
input.addEventListener('keydown', e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); } });
sendButton.addEventListener('click', send);
document.querySelectorAll('.suggestion').forEach(btn => btn.addEventListener('click', () => { input.value = btn.dataset.prompt; input.focus(); }));
document.querySelector('#newChat').addEventListener('click', () => { messages = []; save(); conversation.querySelectorAll('.message').forEach(el => el.remove()); welcome.style.display = ''; input.focus(); });
document.querySelector('#exportChat').addEventListener('click', () => { const text = messages.map(m => `${m.role === 'user' ? 'Vy' : 'ChatBot-AI'}:\n${m.text}`).join('\n\n'); const blob = new Blob([text || 'Konverzace je zatím prázdná.'], { type: 'text/plain;charset=utf-8' }); const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'chatbot-ai-konverzace.txt'; a.click(); URL.revokeObjectURL(a.href); });
const toggle = document.querySelector('#themeToggle'); const label = document.querySelector('#themeLabel');
function setTheme(dark) { document.body.classList.toggle('dark', dark); label.textContent = dark ? 'Světlý vzhled' : 'Tmavý vzhled'; localStorage.setItem(themeKey, dark ? 'dark' : 'light'); }
toggle.addEventListener('click', () => setTheme(!document.body.classList.contains('dark')));
if (localStorage.getItem(themeKey) === 'dark') setTheme(true);
renderHistory();
