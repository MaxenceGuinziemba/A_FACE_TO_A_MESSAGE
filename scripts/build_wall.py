"""Generate the interactive wall of 8 animated SVG faces with embedded audio.

Each face represents one emotional dimension. Click to play the testimony
audio — the face animates while the voice speaks.
"""

import json
import base64
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.analysis.emotion_v2 import score_dimensions_v2, compute_avatar_params_v2

DEMO_DIR = Path('data/audio/demo')
OUT_PATH = DEMO_DIR / 'wall.html'

DIM_META = {
    'solidarite':    {'label': 'Solidarité',     'color': '#2ecc71', 'emoji': '🤝'},
    'empathie':      {'label': 'Empathie',       'color': '#3498db', 'emoji': '💙'},
    'urgence':       {'label': 'Urgence',        'color': '#e74c3c', 'emoji': '⚡'},
    'chaleur':       {'label': 'Chaleur',        'color': '#f39c12', 'emoji': '🏠'},
    'tristesse':     {'label': 'Tristesse',      'color': '#9b59b6', 'emoji': '😢'},
    'espoir':        {'label': 'Espoir',         'color': '#1abc9c', 'emoji': '🌟'},
    'determination': {'label': 'Détermination',  'color': '#e67e22', 'emoji': '💪'},
    'indignation':   {'label': 'Indignation',    'color': '#c0392b', 'emoji': '😤'},
}

DIM_ORDER = ['solidarite', 'empathie', 'urgence', 'chaleur',
             'tristesse', 'espoir', 'determination', 'indignation']

with open(DEMO_DIR / 'messages.json') as f:
    messages = json.load(f)
with open(DEMO_DIR / 'generation_log.json') as f:
    gen_log = json.load(f)

log_map = {r['id']: r for r in gen_log if r['status'] == 'ok'}

# Pick one message per dimension, recompute face params
faces = []
used_dims = set()
for dim in DIM_ORDER:
    for m in messages:
        if m['dominant_dim'] == dim and dim not in used_dims and m['id'] in log_map:
            scores = score_dimensions_v2(m['text'])
            params = compute_avatar_params_v2(scores)
            face = {
                'eyebrows': round(params.get('face_eyebrows', 0.0), 2),
                'mouth':    round(params.get('face_mouth', 0.0), 2),
                'eyes':     round(params.get('face_eyes', 0.7), 2),
                'gaze':     round(params.get('face_gaze', 0.5), 2),
            }

            audio_path = log_map[m['id']]['output_path']
            with open(audio_path, 'rb') as af:
                audio_b64 = base64.b64encode(af.read()).decode('utf-8')

            import html as html_mod
            faces.append({
                'dim': dim,
                'label': DIM_META[dim]['label'],
                'color': DIM_META[dim]['color'],
                'emoji': DIM_META[dim]['emoji'],
                'face': face,
                'text': html_mod.escape(m['text']),
                'audio_b64': audio_b64,
                'voice': log_map[m['id']]['voice_name'],
            })
            used_dims.add(dim)
            break

# Build JSON data for JS (without audio to keep it clean)
faces_js = json.dumps([{
    'dim': f['dim'], 'label': f['label'], 'color': f['color'],
    'emoji': f['emoji'], 'face': f['face'], 'text': f['text'],
    'voice': f['voice'],
} for f in faces], ensure_ascii=False)

# Build audio sources
audio_tags = '\n'.join(
    f'<audio id="audio-{f["dim"]}" preload="auto">'
    f'<source src="data:audio/mpeg;base64,{f["audio_b64"]}" type="audio/mpeg">'
    f'</audio>'
    for f in faces
)

html = f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>A Face to a Message — Le Mur</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #0a0a0f;
  color: #e0e0e0;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
}}
.header {{
  text-align: center;
  padding: 40px 20px 20px;
}}
.header h1 {{
  font-size: 28px;
  font-weight: 300;
  letter-spacing: 4px;
  text-transform: uppercase;
  color: #ccc;
}}
.header p {{
  font-size: 13px;
  color: #666;
  margin-top: 8px;
}}
.wall {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  padding: 30px;
  max-width: 1100px;
  width: 100%;
}}
.face-cell {{
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: transform 0.3s;
}}
.face-cell:hover {{
  transform: scale(1.05);
}}
.face-cell.active {{
  transform: scale(1.08);
}}
.face-container {{
  width: 180px;
  height: 180px;
  position: relative;
}}
.face-container svg {{
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 4px 20px rgba(0,0,0,0.5));
}}
.face-label {{
  margin-top: 10px;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 1px;
  text-align: center;
  opacity: 0.7;
  transition: opacity 0.3s;
}}
.face-cell:hover .face-label,
.face-cell.active .face-label {{
  opacity: 1;
}}

/* Text panel */
.text-panel {{
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, rgba(10,10,15,0.98), rgba(10,10,15,0.9));
  backdrop-filter: blur(20px);
  padding: 24px 40px;
  transform: translateY(100%);
  transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  border-top: 1px solid rgba(255,255,255,0.08);
  max-height: 40vh;
  overflow-y: auto;
}}
.text-panel.visible {{
  transform: translateY(0);
}}
.text-panel .dim-badge {{
  display: inline-block;
  padding: 4px 14px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  color: white;
  margin-bottom: 12px;
}}
.text-panel .testimony {{
  font-style: italic;
  font-size: 15px;
  line-height: 1.8;
  color: #bbb;
  max-width: 800px;
}}
.text-panel .voice-info {{
  margin-top: 10px;
  font-size: 11px;
  color: #555;
}}
.text-panel .close-btn {{
  position: absolute;
  top: 12px;
  right: 20px;
  background: none;
  border: none;
  color: #666;
  font-size: 20px;
  cursor: pointer;
}}
.text-panel .close-btn:hover {{
  color: #fff;
}}

/* Pulse ring for active face */
@keyframes pulse-ring {{
  0% {{ transform: scale(1); opacity: 0.6; }}
  100% {{ transform: scale(1.3); opacity: 0; }}
}}
.pulse {{
  position: absolute;
  top: 0; left: 0;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 2px solid currentColor;
  animation: pulse-ring 1.5s ease-out infinite;
  pointer-events: none;
  opacity: 0;
}}
.face-cell.active .pulse {{
  opacity: 1;
}}

/* Breathing animation for idle faces */
@keyframes breathe {{
  0%, 100% {{ transform: scaleY(1); }}
  50% {{ transform: scaleY(1.02); }}
}}
.face-container svg {{
  animation: breathe 4s ease-in-out infinite;
}}

.footer {{
  padding: 20px;
  color: #333;
  font-size: 11px;
  text-align: center;
  margin-top: auto;
}}
</style>
</head>
<body>

<div class="header">
  <h1>A Face to a Message</h1>
  <p>Cliquez sur un visage pour entendre son t&eacute;moignage</p>
</div>

<div class="wall" id="wall"></div>

<div class="text-panel" id="textPanel">
  <button class="close-btn" onclick="stopAll()">&times;</button>
  <div class="dim-badge" id="panelBadge"></div>
  <div class="testimony" id="panelText"></div>
  <div class="voice-info" id="panelVoice"></div>
</div>

{audio_tags}

<div class="footer">
  A Face to a Message &middot; T&eacute;l&eacute;com Paris &middot; Mus&eacute;e de l&#39;immigration
</div>

<script>
const FACES = {faces_js};
let currentDim = null;
let animFrame = null;

function buildSVGFace(face, color, dim) {{
  const ey = face.eyebrows;  // -1..1 (sad to raised)
  const mo = face.mouth;     // -1..1 (frown to smile)
  const ez = face.eyes;      // 0..1  (closed to wide)
  const gz = face.gaze;      // -1..1 (down to up)

  const headColor = color + '20';
  const strokeColor = color;

  // Eye geometry
  const eyeOpenness = 3 + ez * 10;      // 3..13 height
  const pupilY = 70 - gz * 6;           // gaze shifts pupil
  const pupilR = 2.5 + ez * 1.5;        // bigger when open

  // Eyebrow geometry
  const browY = 52 - ey * 10;           // raised = higher
  const browTilt = ey * 5;              // tilt for expression

  // Mouth geometry
  const mouthCurve = mo * 12;           // positive = smile
  const mouthWidth = 16 + Math.abs(mo) * 4;
  const mouthOpen = Math.max(0, -mo * 3); // opens on frown

  return `
    <svg viewBox="0 0 160 160" xmlns="http://www.w3.org/2000/svg">
      <!-- Head -->
      <circle cx="80" cy="80" r="70" fill="${{headColor}}" stroke="${{strokeColor}}" stroke-width="1.5" opacity="0.8"/>

      <!-- Left eyebrow -->
      <line x1="50" y1="${{browY + browTilt}}" x2="70" y2="${{browY - browTilt}}"
            stroke="${{strokeColor}}" stroke-width="2.5" stroke-linecap="round" class="brow-l" opacity="0.9"/>
      <!-- Right eyebrow -->
      <line x1="90" y1="${{browY - browTilt}}" x2="110" y2="${{browY + browTilt}}"
            stroke="${{strokeColor}}" stroke-width="2.5" stroke-linecap="round" class="brow-r" opacity="0.9"/>

      <!-- Left eye -->
      <ellipse cx="62" cy="70" rx="9" ry="${{eyeOpenness}}"
               fill="none" stroke="${{strokeColor}}" stroke-width="1.5" class="eye-l"/>
      <circle cx="62" cy="${{pupilY}}" r="${{pupilR}}"
              fill="${{strokeColor}}" class="pupil-l" opacity="0.9"/>

      <!-- Right eye -->
      <ellipse cx="98" cy="70" rx="9" ry="${{eyeOpenness}}"
               fill="none" stroke="${{strokeColor}}" stroke-width="1.5" class="eye-r"/>
      <circle cx="98" cy="${{pupilY}}" r="${{pupilR}}"
              fill="${{strokeColor}}" class="pupil-r" opacity="0.9"/>

      <!-- Mouth -->
      <path d="M${{80 - mouthWidth}},100 Q80,${{100 + mouthCurve}} ${{80 + mouthWidth}},100"
            fill="none" stroke="${{strokeColor}}" stroke-width="2" stroke-linecap="round" class="mouth" opacity="0.8"/>
      ${{mouthOpen > 0.5 ? `<ellipse cx="80" cy="${{102 + mouthOpen}}" rx="${{mouthWidth * 0.4}}" ry="${{mouthOpen * 2}}"
            fill="${{strokeColor}}" opacity="0.15" class="mouth-open"/>` : ''}}

      <!-- Nose hint -->
      <line x1="80" y1="78" x2="80" y2="88" stroke="${{strokeColor}}" stroke-width="1" opacity="0.3"/>
    </svg>`;
}}

function buildWall() {{
  const wall = document.getElementById('wall');
  FACES.forEach(f => {{
    const cell = document.createElement('div');
    cell.className = 'face-cell';
    cell.dataset.dim = f.dim;
    cell.innerHTML = `
      <div class="face-container" id="face-${{f.dim}}">
        <div class="pulse" style="color:${{f.color}}"></div>
        ${{buildSVGFace(f.face, f.color, f.dim)}}
      </div>
      <div class="face-label" style="color:${{f.color}}">${{f.emoji}} ${{f.label}}</div>
    `;
    cell.addEventListener('click', () => toggleFace(f));
    wall.appendChild(cell);
  }});
}}

function toggleFace(f) {{
  if (currentDim === f.dim) {{
    stopAll();
    return;
  }}
  stopAll();
  currentDim = f.dim;

  const audio = document.getElementById('audio-' + f.dim);
  const cell = document.querySelector(`.face-cell[data-dim="${{f.dim}}"]`);
  const panel = document.getElementById('textPanel');
  const badge = document.getElementById('panelBadge');
  const text = document.getElementById('panelText');
  const voice = document.getElementById('panelVoice');

  cell.classList.add('active');
  badge.style.background = f.color;
  badge.textContent = f.emoji + ' ' + f.label;
  text.innerHTML = '\\u275D ' + f.text + ' \\u275E';
  voice.textContent = 'Voix : ' + f.voice;
  panel.classList.add('visible');

  audio.currentTime = 0;
  audio.play();

  startAnimation(f);

  audio.onended = () => stopAll();
}}

function stopAll() {{
  if (currentDim) {{
    const audio = document.getElementById('audio-' + currentDim);
    if (audio) {{ audio.pause(); audio.currentTime = 0; }}
  }}
  document.querySelectorAll('.face-cell').forEach(c => c.classList.remove('active'));
  document.getElementById('textPanel').classList.remove('visible');
  currentDim = null;
  if (animFrame) {{ cancelAnimationFrame(animFrame); animFrame = null; }}
}}

function startAnimation(f) {{
  const container = document.getElementById('face-' + f.dim);
  const svg = container.querySelector('svg');
  const mouth = svg.querySelector('.mouth');
  const browL = svg.querySelector('.brow-l');
  const browR = svg.querySelector('.brow-r');
  const eyeL = svg.querySelector('.eye-l');
  const eyeR = svg.querySelector('.eye-r');
  const pupilL = svg.querySelector('.pupil-l');
  const pupilR = svg.querySelector('.pupil-r');

  const base = f.face;
  const baseEyeOpen = 3 + base.eyes * 10;
  const baseBrowY = 52 - base.eyebrows * 10;
  const baseBrowTilt = base.eyebrows * 5;
  const baseMouthWidth = 16 + Math.abs(base.mouth) * 4;
  const baseMouthCurve = base.mouth * 12;
  const basePupilY = 70 - base.gaze * 6;

  function animate(t) {{
    if (!currentDim || currentDim !== f.dim) return;

    // Subtle oscillations simulating speech
    const s1 = Math.sin(t * 0.008) * 0.5;
    const s2 = Math.sin(t * 0.012) * 0.3;
    const s3 = Math.sin(t * 0.006) * 0.4;
    const talk = Math.sin(t * 0.025) * 0.5 + Math.sin(t * 0.037) * 0.3;

    // Mouth moves with "speech" rhythm
    const mCurve = baseMouthCurve + talk * 4;
    const mW = baseMouthWidth;
    mouth.setAttribute('d', `M${{80-mW}},100 Q80,${{100+mCurve}} ${{80+mW}},100`);

    // Eyebrows micro-movement
    const browShift = s1 * 1.5;
    browL.setAttribute('y1', baseBrowY + baseBrowTilt + browShift);
    browL.setAttribute('y2', baseBrowY - baseBrowTilt + browShift);
    browR.setAttribute('y1', baseBrowY - baseBrowTilt + browShift);
    browR.setAttribute('y2', baseBrowY + baseBrowTilt + browShift);

    // Eyes subtle blink every ~4s
    const blinkPhase = (t % 4000) / 4000;
    let eyeScale = 1;
    if (blinkPhase > 0.95) {{
      eyeScale = 1 - Math.sin((blinkPhase - 0.95) / 0.05 * Math.PI) * 0.8;
    }}
    const eyeH = baseEyeOpen * eyeScale;
    eyeL.setAttribute('ry', eyeH);
    eyeR.setAttribute('ry', eyeH);

    // Pupils slight drift
    const pDrift = s3 * 2;
    pupilL.setAttribute('cy', basePupilY + pDrift);
    pupilR.setAttribute('cy', basePupilY + pDrift);

    animFrame = requestAnimationFrame(animate);
  }}

  animFrame = requestAnimationFrame(animate);
}}

buildWall();
</script>
</body>
</html>'''

with open(OUT_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'Wall generated: {OUT_PATH}')
print(f'  {len(faces)} faces')
print(f'  File size: {os.path.getsize(OUT_PATH)/1024:.0f} KB')
