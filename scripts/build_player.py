"""Generate the interactive HTML demo player with embedded audio."""
import html as html_mod
import json
import base64
import os
from pathlib import Path

DIM_COLORS = {
    'solidarite': '#2ecc71', 'empathie': '#3498db', 'urgence': '#e74c3c',
    'chaleur': '#f39c12', 'tristesse': '#9b59b6', 'espoir': '#1abc9c',
    'determination': '#e67e22', 'indignation': '#c0392b',
}
DIM_LABELS = {
    'solidarite': 'Solidarité', 'empathie': 'Empathie', 'urgence': 'Urgence',
    'chaleur': 'Chaleur', 'tristesse': 'Tristesse', 'espoir': 'Espoir',
    'determination': 'Détermination', 'indignation': 'Indignation',
}
DIM_EMOJIS = {
    'solidarite': '🤝', 'empathie': '💙', 'urgence': '⚡',
    'chaleur': '🏠', 'tristesse': '😢', 'espoir': '🌟',
    'determination': '💪', 'indignation': '😤',
}

demo_dir = Path('data/audio/demo')

with open(demo_dir / 'generation_log.json') as f:
    gen_log = json.load(f)
with open(demo_dir / 'messages.json') as f:
    messages = json.load(f)

msg_map = {m['id']: m for m in messages}

cards = []
for gen in gen_log:
    if gen['status'] != 'ok':
        continue

    msg = msg_map[gen['id']]
    dim = msg['dominant_dim']
    params = msg['voice_params']
    color = DIM_COLORS.get(dim, '#666')
    label = DIM_LABELS.get(dim, dim)
    emoji = DIM_EMOJIS.get(dim, '')

    audio_path = gen['output_path']
    with open(audio_path, 'rb') as af:
        audio_b64 = base64.b64encode(af.read()).decode('utf-8')

    text_display = html_mod.escape(msg['text']).replace('\n', '<br>')
    speaker_gender = msg.get('speaker_gender', 'unknown')
    gender_icon = {'female': '♀', 'male': '♂'}.get(speaker_gender, '')
    gender_label = {'female': 'Locutrice', 'male': 'Locuteur'}.get(speaker_gender, '')

    def param_bar(val, lo, hi, color='#3498db'):
        pct = max(0, min(100, (val - lo) / (hi - lo) * 100))
        return f'<div class="pbar"><div class="pfill" style="width:{pct:.0f}%;background:{color}"></div></div><span class="pval">{val:.2f}</span>'

    gender_badge = f'<span class="gender-badge">{gender_icon} {gender_label}</span>' if gender_icon else ''

    card = f'''<div class="card" data-dim="{dim}" onclick="playCard(this)">
  <div class="card-head">
    <span class="badge" style="background:{color}">{emoji} {label}</span>
    <div class="card-meta"><span class="voice">{gen['voice_name']} · {gen['voice_gender']}</span>{gender_badge}</div>
  </div>
  <div class="card-text">❝ {text_display} ❞</div>
  <div class="params">
    <div class="pgrid">
      <span class="plbl">Speed</span>{param_bar(params['voice_speed'], 0.5, 1.5, '#2ecc71')}
      <span class="plbl">Pitch</span>{param_bar(params['voice_pitch'], -1, 1, '#3498db')}
      <span class="plbl">Energy</span>{param_bar(params['voice_energy'], 0, 1, '#e67e22')}
      <span class="plbl">Warmth</span>{param_bar(params['voice_warmth'], 0, 1, '#e74c3c')}
    </div>
  </div>
  <audio preload="none"><source src="data:audio/mpeg;base64,{audio_b64}" type="audio/mpeg"></audio>
  <button class="play-btn" onclick="event.stopPropagation();playCard(this.parentElement)">▶ Écouter</button>
</div>'''
    cards.append(card)

# Build filter buttons
dims_in_data = sorted(set(msg_map[g['id']]['dominant_dim'] for g in gen_log if g['status'] == 'ok'))
filters = '<button class="filter active" data-dim="all">Tous</button>'
for d in dims_in_data:
    filters += f'<button class="filter" data-dim="{d}" style="--fc:{DIM_COLORS[d]}">{DIM_EMOJIS.get(d,"")} {DIM_LABELS.get(d,d)}</button>'

html = f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>A Face to a Message — TTS Demo</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#0f0f13;color:#e0e0e0;min-height:100vh}}
.header{{text-align:center;padding:50px 20px 30px;background:linear-gradient(135deg,#1a1a2e,#16213e,#0f3460);border-bottom:1px solid rgba(255,255,255,0.05)}}
.header h1{{font-size:32px;margin-bottom:8px;background:linear-gradient(135deg,#e0e0e0,#a0a0ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.header p{{font-size:14px;opacity:0.6;max-width:600px;margin:0 auto}}
.header .stats{{margin-top:12px;font-size:12px;opacity:0.4}}
.filters{{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;padding:20px;max-width:1200px;margin:0 auto}}
.filter{{background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);color:#ccc;padding:6px 14px;border-radius:20px;cursor:pointer;font-size:12px;transition:all .2s}}
.filter:hover{{background:rgba(255,255,255,0.12)}}
.filter.active{{background:rgba(255,255,255,0.15);border-color:rgba(255,255,255,0.3);color:white}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:16px;padding:0 20px 40px;max-width:1200px;margin:0 auto}}
.card{{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:20px;cursor:pointer;transition:all .2s;position:relative;overflow:hidden}}
.card::before{{content:'';position:absolute;top:0;left:0;width:4px;height:100%;border-radius:12px 0 0 12px}}
.card:hover{{background:rgba(255,255,255,0.07);transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,0.3)}}
.card.playing{{border-color:rgba(255,255,255,0.2);box-shadow:0 0 20px rgba(100,100,255,0.1)}}
.card-head{{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}}
.badge{{color:white;padding:4px 12px;border-radius:16px;font-size:12px;font-weight:600}}
.voice{{font-size:11px;color:#666;background:rgba(255,255,255,0.06);padding:3px 10px;border-radius:10px}}
.card-meta{{display:flex;gap:6px;align-items:center}}
.gender-badge{{font-size:10px;color:#999;background:rgba(255,255,255,0.06);padding:2px 8px;border-radius:10px}}
.card-text{{font-style:italic;color:#b0b0b0;line-height:1.6;font-size:13px;padding:12px;background:rgba(255,255,255,0.03);border-radius:8px;margin:8px 0;border-left:2px solid rgba(255,255,255,0.08)}}
.params{{margin-top:12px}}
.pgrid{{display:grid;grid-template-columns:55px 1fr 40px;gap:4px 8px;align-items:center}}
.plbl{{font-size:11px;color:#666;text-align:right}}
.pbar{{height:4px;background:rgba(255,255,255,0.08);border-radius:2px}}
.pfill{{height:4px;border-radius:2px;transition:width .3s}}
.pval{{font-size:10px;color:#555}}
.play-btn{{width:100%;margin-top:14px;padding:8px;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.12);color:#ccc;border-radius:8px;cursor:pointer;font-size:12px;transition:all .2s}}
.play-btn:hover{{background:rgba(255,255,255,0.14);color:white}}
.card.playing .play-btn{{background:rgba(100,100,255,0.15);border-color:rgba(100,100,255,0.3);color:white}}
audio{{display:none}}
.footer{{text-align:center;padding:30px;color:#444;font-size:11px;border-top:1px solid rgba(255,255,255,0.05)}}
.hidden{{display:none}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.5}}}}
.card.playing .play-btn::before{{content:'';display:inline-block;width:8px;height:8px;background:#6c6cff;border-radius:50%;margin-right:6px;animation:pulse 1s infinite}}
</style>
</head>
<body>
<div class="header">
  <h1>🎭 A Face to a Message</h1>
  <p>Donner un visage aux messages — chaque témoignage parle avec sa propre voix émotionnelle</p>
  <div class="stats">{len(cards)} témoignages · 8 dimensions émotionnelles · 4 voix françaises · prosodie adaptative</div>
</div>
<div class="filters">{filters}</div>
<div class="grid">{''.join(cards)}</div>
<div class="footer">
  A Face to a Message · Télécom Paris · HI Paris! · Musée de l'immigration<br>
  Pipeline : Texte → Analyse émotionnelle → Sélection de voix → Prosodie SSML → Audio
</div>
<script>
let currentAudio=null;
let currentCard=null;
function playCard(card){{
  const audio=card.querySelector('audio');
  if(currentAudio&&currentAudio!==audio){{currentAudio.pause();currentAudio.currentTime=0;currentCard?.classList.remove('playing');currentCard.querySelector('.play-btn').textContent='▶ Écouter'}}
  if(audio.paused){{audio.play();card.classList.add('playing');card.querySelector('.play-btn').textContent='⏸ En cours...';currentAudio=audio;currentCard=card;audio.onended=()=>{{card.classList.remove('playing');card.querySelector('.play-btn').textContent='▶ Écouter';currentAudio=null;currentCard=null}}}}
  else{{audio.pause();audio.currentTime=0;card.classList.remove('playing');card.querySelector('.play-btn').textContent='▶ Écouter';currentAudio=null;currentCard=null}}
}}
document.querySelectorAll('.filter').forEach(btn=>{{
  btn.addEventListener('click',()=>{{
    document.querySelectorAll('.filter').forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
    const dim=btn.dataset.dim;
    document.querySelectorAll('.card').forEach(c=>{{
      c.classList.toggle('hidden',dim!=='all'&&c.dataset.dim!==dim)
    }})
  }})
}})
</script>
</body>
</html>'''

out = demo_dir / 'player.html'
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'✓ Player generated: {out}')
print(f'  {len(cards)} cards with embedded audio')
print(f'  File size: {os.path.getsize(out)/1024:.0f} KB')
