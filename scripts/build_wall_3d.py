"""Generate the Three.js 3D face wall — 8 sculptural masks with embedded audio.

Style: abstract/sculptural ceramic masks on deep black, colored light halos.
Grid: 2 rows × 4 columns. Click a face to hear the testimony + animate.
"""

import json
import base64
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.analysis.emotion_v2 import score_dimensions_v2, compute_avatar_params_v2
import html as html_mod

DEMO_DIR = Path('data/audio/demo')
OUT_PATH = DEMO_DIR / 'wall_3d.html'

DIM_META = {
    'solidarite':    {'label': 'Solidarité',    'color': '#2ecc71'},
    'empathie':      {'label': 'Empathie',      'color': '#3498db'},
    'urgence':       {'label': 'Urgence',       'color': '#e74c3c'},
    'chaleur':       {'label': 'Chaleur',       'color': '#f39c12'},
    'tristesse':     {'label': 'Tristesse',     'color': '#9b59b6'},
    'espoir':        {'label': 'Espoir',        'color': '#1abc9c'},
    'determination': {'label': 'Détermination', 'color': '#e67e22'},
    'indignation':   {'label': 'Indignation',   'color': '#c0392b'},
}

DIM_ORDER = ['solidarite', 'empathie', 'urgence', 'chaleur',
             'tristesse', 'espoir', 'determination', 'indignation']

with open(DEMO_DIR / 'messages.json') as f:
    messages = json.load(f)
with open(DEMO_DIR / 'generation_log.json') as f:
    gen_log = json.load(f)

log_map = {r['id']: r for r in gen_log if r['status'] == 'ok'}

faces_data = []
audio_elements = []

for dim in DIM_ORDER:
    for m in messages:
        if m['dominant_dim'] == dim and m['id'] in log_map:
            scores = score_dimensions_v2(m['text'])
            params = compute_avatar_params_v2(scores)

            audio_path = log_map[m['id']]['output_path']
            with open(audio_path, 'rb') as af:
                audio_b64 = base64.b64encode(af.read()).decode('utf-8')

            faces_data.append({
                'dim': dim,
                'label': DIM_META[dim]['label'],
                'color': DIM_META[dim]['color'],
                'face': {
                    'eyebrows': round(params.get('face_eyebrows', 0.0), 3),
                    'mouth':    round(params.get('face_mouth', 0.0), 3),
                    'eyes':     round(params.get('face_eyes', 0.7), 3),
                    'gaze':     round(params.get('face_gaze', 0.5), 3),
                },
                'text': html_mod.escape(m['text']),
                'voice': log_map[m['id']]['voice_name'],
            })
            audio_elements.append(
                f'<audio id="audio-{dim}" preload="auto">'
                f'<source src="data:audio/mpeg;base64,{audio_b64}" type="audio/mpeg">'
                f'</audio>'
            )
            break

faces_json = json.dumps(faces_data, ensure_ascii=False)
audio_html = '\n'.join(audio_elements)

html_content = f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>A Face to a Message</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 100%; height: 100%; overflow: hidden; background: #000; }}
canvas {{ display: block; }}

#overlay {{
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  pointer-events: none;
  z-index: 10;
}}

#title {{
  position: fixed;
  top: 24px;
  width: 100%;
  text-align: center;
  font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
  font-size: 20px;
  font-weight: 300;
  letter-spacing: 6px;
  text-transform: uppercase;
  color: rgba(255,255,255,0.4);
  z-index: 11;
  pointer-events: none;
  transition: opacity 0.6s;
}}

#subtitle {{
  position: fixed;
  top: 54px;
  width: 100%;
  text-align: center;
  font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
  font-size: 11px;
  color: rgba(255,255,255,0.2);
  z-index: 11;
  pointer-events: none;
}}

#textPanel {{
  position: fixed;
  bottom: 0; left: 0; right: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.95) 60%, transparent);
  padding: 60px 40px 32px;
  transform: translateY(100%);
  transition: transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);
  z-index: 20;
  pointer-events: auto;
  max-height: 45vh;
  overflow-y: auto;
}}
#textPanel.visible {{ transform: translateY(0); }}

#textPanel .badge {{
  display: inline-block;
  padding: 5px 16px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  color: white;
  font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
  margin-bottom: 14px;
}}

#textPanel .testimony {{
  font-family: Georgia, 'Times New Roman', serif;
  font-style: italic;
  font-size: 16px;
  line-height: 1.9;
  color: rgba(255,255,255,0.75);
  max-width: 760px;
}}

#textPanel .meta {{
  margin-top: 12px;
  font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
  font-size: 11px;
  color: rgba(255,255,255,0.25);
}}

#textPanel .close {{
  position: absolute;
  top: 16px; right: 24px;
  background: none; border: none;
  color: rgba(255,255,255,0.4);
  font-size: 24px;
  cursor: pointer;
  pointer-events: auto;
}}
#textPanel .close:hover {{ color: white; }}

#hint {{
  position: fixed;
  bottom: 20px;
  width: 100%;
  text-align: center;
  font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
  font-size: 11px;
  color: rgba(255,255,255,0.15);
  z-index: 11;
  pointer-events: none;
  transition: opacity 0.6s;
}}

#footer {{
  position: fixed;
  bottom: 6px;
  width: 100%;
  text-align: center;
  font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
  font-size: 9px;
  color: rgba(255,255,255,0.08);
  z-index: 11;
  pointer-events: none;
}}
</style>
</head>
<body>

<div id="title">A Face to a Message</div>
<div id="subtitle">Donner un visage aux messages</div>

<div id="textPanel">
  <button class="close" onclick="stopAll()">&times;</button>
  <div class="badge" id="panelBadge"></div>
  <div class="testimony" id="panelText"></div>
  <div class="meta" id="panelMeta"></div>
</div>

<div id="hint">Cliquez sur un visage</div>
<div id="footer">T&eacute;l&eacute;com Paris &middot; Mus&eacute;e de l&#39;immigration</div>

{audio_html}

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
"use strict";

const FACES = {faces_json};

// ─── Scene setup ───
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 100);
camera.position.set(0, 0, 14);

const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: false }});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setClearColor(0x000000, 1);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0;
document.body.appendChild(renderer.domElement);

// ─── Lighting ───
const ambientLight = new THREE.AmbientLight(0x111122, 0.5);
scene.add(ambientLight);

const topLight = new THREE.DirectionalLight(0xffffff, 0.3);
topLight.position.set(0, 5, 5);
scene.add(topLight);

// ─── Face construction ───
const faceGroups = [];
const faceLights = [];
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
const hoverTargets = [];

const COLS = 4, ROWS = 2;
const SPACING_X = 3.2, SPACING_Y = 3.6;
const OFFSET_X = -(COLS - 1) * SPACING_X / 2;
const OFFSET_Y = (ROWS - 1) * SPACING_Y / 2 - 0.3;

function hexToThreeColor(hex) {{
  return new THREE.Color(hex);
}}

function createFace(data, index) {{
  const col = index % COLS;
  const row = Math.floor(index / COLS);
  const x = OFFSET_X + col * SPACING_X;
  const y = OFFSET_Y - row * SPACING_Y;

  const group = new THREE.Group();
  group.position.set(x, y, 0);
  group.userData = {{ dim: data.dim, index: index, data: data }};

  const color = hexToThreeColor(data.color);
  const matBase = new THREE.MeshStandardMaterial({{
    color: 0x1a1a1a,
    roughness: 0.65,
    metalness: 0.1,
    emissive: color,
    emissiveIntensity: 0.08,
  }});

  // Head — slightly flattened sphere
  const headGeo = new THREE.SphereGeometry(1.1, 48, 48);
  headGeo.scale(1, 1.2, 0.85);
  const head = new THREE.Mesh(headGeo, matBase.clone());
  group.add(head);
  hoverTargets.push(head);
  head.userData = {{ dim: data.dim, index: index }};

  const fp = data.face;

  // Eyes — recessed cavities + glowing pupils
  const eyeSocket = new THREE.MeshStandardMaterial({{
    color: 0x000000,
    roughness: 1.0,
    metalness: 0,
  }});
  const eyeGlow = new THREE.MeshStandardMaterial({{
    color: color,
    emissive: color,
    emissiveIntensity: 0.6,
    roughness: 0.3,
    metalness: 0,
  }});

  const eyeOpenness = 0.08 + fp.eyes * 0.14;

  [-1, 1].forEach(side => {{
    const socketGeo = new THREE.SphereGeometry(0.18, 24, 24);
    socketGeo.scale(1, eyeOpenness / 0.18, 0.5);
    const socket = new THREE.Mesh(socketGeo, eyeSocket);
    socket.position.set(side * 0.35, 0.15 + fp.gaze * 0.05, 0.85);
    group.add(socket);

    const pupilGeo = new THREE.SphereGeometry(0.06 + fp.eyes * 0.04, 16, 16);
    const pupil = new THREE.Mesh(pupilGeo, eyeGlow.clone());
    pupil.position.set(side * 0.35, 0.15 + fp.gaze * 0.05, 0.9);
    pupil.userData.type = 'pupil';
    group.add(pupil);
  }});

  // Eyebrows — thin ridges
  const browMat = new THREE.MeshStandardMaterial({{
    color: 0x222222,
    emissive: color,
    emissiveIntensity: 0.15,
    roughness: 0.8,
  }});

  [-1, 1].forEach(side => {{
    const browGeo = new THREE.BoxGeometry(0.28, 0.035, 0.08);
    const brow = new THREE.Mesh(browGeo, browMat);
    const browHeight = 0.38 + fp.eyebrows * 0.12;
    brow.position.set(side * 0.35, browHeight, 0.88);
    brow.rotation.z = side * (-fp.eyebrows * 0.2);
    brow.userData.type = 'brow';
    group.add(brow);
  }});

  // Mouth — curved line using tube geometry
  const mouthCurve = fp.mouth;
  const mouthPoints = [];
  for (let i = 0; i <= 20; i++) {{
    const t = (i / 20 - 0.5) * 2;
    const mx = t * 0.25;
    const my = -0.35 + mouthCurve * 0.08 * (1 - t * t);
    const mz = 0.88 - Math.abs(t) * 0.05;
    mouthPoints.push(new THREE.Vector3(mx, my, mz));
  }}
  const mouthPath = new THREE.CatmullRomCurve3(mouthPoints);
  const mouthGeo = new THREE.TubeGeometry(mouthPath, 20, 0.02, 8, false);
  const mouthMat = new THREE.MeshStandardMaterial({{
    color: 0x111111,
    emissive: color,
    emissiveIntensity: 0.3,
    roughness: 0.5,
  }});
  const mouthMesh = new THREE.Mesh(mouthGeo, mouthMat);
  mouthMesh.userData.type = 'mouth';
  mouthMesh.userData.baseCurve = mouthCurve;
  group.add(mouthMesh);

  // Nose — subtle ridge
  const noseGeo = new THREE.ConeGeometry(0.06, 0.2, 8);
  const nose = new THREE.Mesh(noseGeo, matBase.clone());
  nose.position.set(0, -0.05, 0.95);
  nose.rotation.x = -0.3;
  group.add(nose);

  // Point light halo behind the face
  const haloLight = new THREE.PointLight(color, 0.4, 5);
  haloLight.position.set(x, y, -1.5);
  scene.add(haloLight);
  faceLights.push(haloLight);

  scene.add(group);
  faceGroups.push(group);
}}

FACES.forEach((f, i) => createFace(f, i));

// ─── Interaction ───
let currentDim = null;
let activeGroup = null;

function onMouseMove(e) {{
  mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;

  // Subtle camera parallax
  camera.position.x = mouse.x * 0.3;
  camera.position.y = mouse.y * 0.2;
  camera.lookAt(0, 0, 0);
}}

function onClick(e) {{
  raycaster.setFromCamera(mouse, camera);
  const hits = raycaster.intersectObjects(hoverTargets);
  if (hits.length > 0) {{
    const dim = hits[0].object.userData.dim;
    const idx = hits[0].object.userData.index;
    const data = FACES[idx];
    if (currentDim === dim) {{
      stopAll();
    }} else {{
      playFace(data, idx);
    }}
  }}
}}

function playFace(data, idx) {{
  stopAll();
  currentDim = data.dim;
  activeGroup = faceGroups[idx];

  // Show text panel
  const panel = document.getElementById('textPanel');
  const badge = document.getElementById('panelBadge');
  const text = document.getElementById('panelText');
  const meta = document.getElementById('panelMeta');
  badge.style.background = data.color;
  badge.textContent = data.label;
  text.innerHTML = '\\u275D ' + data.text + ' \\u275E';
  meta.textContent = 'Voix : ' + data.voice;
  panel.classList.add('visible');

  // Hide hint
  document.getElementById('hint').style.opacity = '0';

  // Boost halo light
  faceLights[idx].intensity = 1.5;

  // Play audio
  const audio = document.getElementById('audio-' + data.dim);
  audio.currentTime = 0;
  audio.play();
  audio.onended = () => stopAll();
}}

function stopAll() {{
  if (currentDim) {{
    const audio = document.getElementById('audio-' + currentDim);
    if (audio) {{ audio.pause(); audio.currentTime = 0; }}
  }}
  document.getElementById('textPanel').classList.remove('visible');
  document.getElementById('hint').style.opacity = '1';

  // Reset all halo lights
  faceLights.forEach((l, i) => {{ l.intensity = 0.4; }});

  currentDim = null;
  activeGroup = null;
}}

window.addEventListener('mousemove', onMouseMove);
window.addEventListener('click', onClick);
window.addEventListener('resize', () => {{
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}});

// ─── Animation loop ───
const clock = new THREE.Clock();

function animate() {{
  requestAnimationFrame(animate);
  const t = clock.getElapsedTime();

  faceGroups.forEach((group, i) => {{
    const isActive = activeGroup === group;

    // Idle breathing for all faces
    const breathe = Math.sin(t * 0.8 + i * 0.7) * 0.015;
    group.scale.setScalar(1 + breathe);

    // Subtle idle float
    group.position.y = (OFFSET_Y - Math.floor(i / COLS) * SPACING_Y) +
                       Math.sin(t * 0.5 + i * 1.1) * 0.04;

    if (isActive) {{
      // Active face: talking animation
      group.children.forEach(child => {{
        if (child.userData.type === 'mouth') {{
          // Regenerate mouth with speech oscillation
          const baseCurve = child.userData.baseCurve;
          const talk = Math.sin(t * 12) * 0.3 + Math.sin(t * 17) * 0.15 + Math.sin(t * 7) * 0.2;
          const pts = [];
          for (let j = 0; j <= 20; j++) {{
            const s = (j / 20 - 0.5) * 2;
            const mx = s * 0.25;
            const my = -0.35 + (baseCurve + talk * 0.3) * 0.08 * (1 - s * s);
            const mz = 0.88 - Math.abs(s) * 0.05;
            pts.push(new THREE.Vector3(mx, my, mz));
          }}
          const curve = new THREE.CatmullRomCurve3(pts);
          const newGeo = new THREE.TubeGeometry(curve, 20, 0.02 + Math.abs(talk) * 0.008, 8, false);
          child.geometry.dispose();
          child.geometry = newGeo;
        }}

        if (child.userData.type === 'pupil') {{
          // Pupils dilate slightly when speaking
          const s = 1 + Math.sin(t * 3) * 0.1;
          child.scale.setScalar(s);
        }}

        if (child.userData.type === 'brow') {{
          // Subtle brow movement while speaking
          const shift = Math.sin(t * 2.5 + (child.position.x > 0 ? 0.5 : 0)) * 0.02;
          child.position.y += shift;
        }}
      }});

      // Pulse halo
      faceLights[i].intensity = 1.2 + Math.sin(t * 2) * 0.4;

      // Slight forward lean
      group.rotation.x = Math.sin(t * 0.7) * 0.03;
      group.rotation.y = Math.sin(t * 0.5) * 0.02;
    }} else {{
      // Idle: very subtle rotation
      group.rotation.y = Math.sin(t * 0.3 + i * 0.8) * 0.05;
      group.rotation.x = Math.sin(t * 0.4 + i * 1.2) * 0.02;
    }}
  }});

  // Hover glow
  raycaster.setFromCamera(mouse, camera);
  const hits = raycaster.intersectObjects(hoverTargets);
  document.body.style.cursor = hits.length > 0 ? 'pointer' : 'default';

  hoverTargets.forEach(target => {{
    const idx = target.userData.index;
    const isHovered = hits.length > 0 && hits[0].object.userData.index === idx;
    const isActive = activeGroup === faceGroups[idx];
    const targetIntensity = isActive ? 0.2 : (isHovered ? 0.15 : 0.08);
    const mat = target.material;
    mat.emissiveIntensity += (targetIntensity - mat.emissiveIntensity) * 0.1;
  }});

  renderer.render(scene, camera);
}}

animate();
</script>
</body>
</html>'''

with open(OUT_PATH, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f'3D Wall generated: {OUT_PATH}')
print(f'  {len(faces_data)} faces')
print(f'  File size: {os.path.getsize(OUT_PATH)/1024:.0f} KB')
