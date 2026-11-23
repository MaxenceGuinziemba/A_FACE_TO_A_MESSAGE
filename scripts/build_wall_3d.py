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

// ─── Scene ───
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 100);
camera.position.set(0, 0, 14);

const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: false }});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setClearColor(0x000000, 1);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
document.body.appendChild(renderer.domElement);

// ─── Lighting ───
scene.add(new THREE.AmbientLight(0x1a1a2e, 0.6));
const keyLight = new THREE.DirectionalLight(0xddeeff, 0.5);
keyLight.position.set(2, 4, 6);
scene.add(keyLight);
const fillLight = new THREE.DirectionalLight(0x334455, 0.25);
fillLight.position.set(-3, 1, 4);
scene.add(fillLight);

// ─── Layout ───
const faceGroups = [];
const faceLights = [];
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2(0, 0);
const mouseWorld = new THREE.Vector3(0, 0, 5);
const hoverTargets = [];

const COLS = 4, ROWS = 2;
const SPACING_X = 3.2, SPACING_Y = 3.6;
const OFFSET_X = -(COLS - 1) * SPACING_X / 2;
const OFFSET_Y = (ROWS - 1) * SPACING_Y / 2 - 0.3;

function hexColor(hex) {{ return new THREE.Color(hex); }}

// ─── Sculpt a human head from sphere ───
function sculptHead(geo) {{
  const pos = geo.attributes.position;
  const v = new THREE.Vector3();
  for (let i = 0; i < pos.count; i++) {{
    v.set(pos.getX(i), pos.getY(i), pos.getZ(i));
    const nx = v.x, ny = v.y, nz = v.z;
    const r = v.length();
    const theta = Math.atan2(ny, Math.sqrt(nx*nx + nz*nz));
    const phi = Math.atan2(nx, nz);

    // Narrow the chin
    if (ny < -0.3) {{
      const chinFactor = 1.0 - Math.pow(Math.max(0, (-ny - 0.3) / 0.7), 1.3) * 0.35;
      v.x *= chinFactor;
      v.z *= (1.0 - Math.pow(Math.max(0, (-ny - 0.3) / 0.7), 1.0) * 0.15);
    }}

    // Widen cheekbones
    if (ny > -0.15 && ny < 0.15 && Math.abs(nx) > 0.3) {{
      const cheekPush = Math.sin((ny + 0.15) / 0.3 * Math.PI) * 0.06;
      v.x += Math.sign(nx) * cheekPush;
    }}

    // Indent eye sockets
    const eyeY = 0.2;
    [-1, 1].forEach(side => {{
      const eyeX = side * 0.35;
      const dx = nx - eyeX, dy = ny - eyeY;
      const dist = Math.sqrt(dx*dx + dy*dy);
      if (dist < 0.2 && nz > 0) {{
        const indent = (1 - dist / 0.2) * 0.08;
        v.z -= indent;
      }}
    }});

    // Nose bridge bump
    if (Math.abs(nx) < 0.08 && ny > -0.1 && ny < 0.3 && nz > 0) {{
      const nosePush = (1 - Math.abs(nx) / 0.08) * 0.07 *
                       Math.sin((ny + 0.1) / 0.4 * Math.PI);
      v.z += nosePush;
    }}

    // Brow ridge
    if (ny > 0.25 && ny < 0.4 && nz > 0) {{
      const browPush = Math.sin((ny - 0.25) / 0.15 * Math.PI) * 0.04;
      v.z += browPush;
    }}

    // Slight forehead roundness
    if (ny > 0.5 && nz > 0) {{
      v.z += (ny - 0.5) * 0.03;
    }}

    pos.setXYZ(i, v.x, v.y, v.z);
  }}
  pos.needsUpdate = true;
  geo.computeVertexNormals();
}}

// ─── Build face ───
function createFace(data, index) {{
  const col = index % COLS;
  const row = Math.floor(index / COLS);
  const x = OFFSET_X + col * SPACING_X;
  const y = OFFSET_Y - row * SPACING_Y;

  const group = new THREE.Group();
  group.position.set(x, y, 0);
  group.userData = {{ dim: data.dim, index, data, baseX: x, baseY: y }};

  const color = hexColor(data.color);
  const fp = data.face;

  // ── Head ──
  const skinMat = new THREE.MeshStandardMaterial({{
    color: 0x1c1c22,
    roughness: 0.55,
    metalness: 0.08,
    emissive: color,
    emissiveIntensity: 0.04,
  }});
  const headGeo = new THREE.SphereGeometry(1.1, 64, 64);
  headGeo.scale(1, 1.25, 0.65);
  sculptHead(headGeo);
  const head = new THREE.Mesh(headGeo, skinMat.clone());
  group.add(head);
  hoverTargets.push(head);
  head.userData = {{ dim: data.dim, index }};

  // ── Eyes (sclera + iris + pupil) ──
  const eyeBaseY = 0.22;
  const eyeSpacing = 0.33;

  [-1, 1].forEach(side => {{
    // Sclera
    const scleraGeo = new THREE.SphereGeometry(0.11, 24, 16);
    scleraGeo.scale(1.2, 0.7 + fp.eyes * 0.4, 0.5);
    const scleraMat = new THREE.MeshStandardMaterial({{
      color: 0xf0f0f0, roughness: 0.3, metalness: 0,
    }});
    const sclera = new THREE.Mesh(scleraGeo, scleraMat);
    sclera.position.set(side * eyeSpacing, eyeBaseY, 0.58);
    group.add(sclera);

    // Iris
    const irisGeo = new THREE.SphereGeometry(0.055, 16, 16);
    const irisMat = new THREE.MeshStandardMaterial({{
      color: color.clone().multiplyScalar(0.7),
      emissive: color,
      emissiveIntensity: 0.4,
      roughness: 0.2,
    }});
    const iris = new THREE.Mesh(irisGeo, irisMat);
    iris.position.set(side * eyeSpacing, eyeBaseY, 0.64);
    iris.userData.type = 'iris';
    iris.userData.baseX = side * eyeSpacing;
    iris.userData.baseY = eyeBaseY;
    iris.userData.side = side;
    group.add(iris);

    // Pupil
    const pupilGeo = new THREE.SphereGeometry(0.025, 12, 12);
    const pupilMat = new THREE.MeshStandardMaterial({{
      color: 0x000000, emissive: color, emissiveIntensity: 0.15,
      roughness: 0.1,
    }});
    const pupil = new THREE.Mesh(pupilGeo, pupilMat);
    pupil.position.set(side * eyeSpacing, eyeBaseY, 0.67);
    pupil.userData.type = 'pupil';
    pupil.userData.baseX = side * eyeSpacing;
    pupil.userData.baseY = eyeBaseY;
    pupil.userData.side = side;
    group.add(pupil);

    // Upper eyelid (subtle shadow)
    const lidGeo = new THREE.PlaneGeometry(0.16, 0.04);
    const lidMat = new THREE.MeshStandardMaterial({{
      color: 0x111118, transparent: true, opacity: 0.5,
      roughness: 1, side: THREE.DoubleSide,
    }});
    const lid = new THREE.Mesh(lidGeo, lidMat);
    lid.position.set(side * eyeSpacing, eyeBaseY + 0.08, 0.63);
    lid.rotation.x = 0.3;
    group.add(lid);
  }});

  // ── Eyebrows ──
  const browMat = new THREE.MeshStandardMaterial({{
    color: 0x151518, emissive: color, emissiveIntensity: 0.12, roughness: 0.8,
  }});
  const browBaseY = 0.42 + fp.eyebrows * 0.1;

  [-1, 1].forEach(side => {{
    // Rounded brow shape
    const browShape = new THREE.Shape();
    browShape.moveTo(-0.14, 0);
    browShape.quadraticCurveTo(-0.07, 0.025, 0, 0.02);
    browShape.quadraticCurveTo(0.07, 0.015, 0.14, -0.005);
    browShape.quadraticCurveTo(0.07, -0.015, 0, -0.01);
    browShape.quadraticCurveTo(-0.07, -0.01, -0.14, 0);
    const browGeo = new THREE.ExtrudeGeometry(browShape, {{
      depth: 0.06, bevelEnabled: true, bevelThickness: 0.01,
      bevelSize: 0.01, bevelSegments: 3,
    }});
    const brow = new THREE.Mesh(browGeo, browMat.clone());
    brow.position.set(side * eyeSpacing, browBaseY, 0.56);
    brow.rotation.z = side * (-fp.eyebrows * 0.2);
    if (side < 0) brow.scale.x = -1;
    brow.userData.type = 'brow';
    brow.userData.baseY = browBaseY;
    group.add(brow);
  }});

  // ── Nose ──
  // Bridge
  const bridgePts = [
    new THREE.Vector3(0, 0.15, 0.62),
    new THREE.Vector3(0, 0.05, 0.68),
    new THREE.Vector3(0, -0.05, 0.72),
    new THREE.Vector3(0, -0.1, 0.68),
  ];
  const bridgeCurve = new THREE.CatmullRomCurve3(bridgePts);
  const bridgeGeo = new THREE.TubeGeometry(bridgeCurve, 12, 0.025, 8, false);
  const noseMat = skinMat.clone();
  noseMat.emissiveIntensity = 0.02;
  const bridge = new THREE.Mesh(bridgeGeo, noseMat);
  group.add(bridge);

  // Nostrils
  [-1, 1].forEach(side => {{
    const nostrilGeo = new THREE.SphereGeometry(0.025, 8, 8);
    const nostril = new THREE.Mesh(nostrilGeo, noseMat.clone());
    nostril.position.set(side * 0.03, -0.12, 0.67);
    group.add(nostril);
  }});

  // ── Lips ──
  const mouthCurve = fp.mouth;
  const lipColor = new THREE.MeshStandardMaterial({{
    color: 0x2a1a1a,
    emissive: color,
    emissiveIntensity: 0.15,
    roughness: 0.4,
  }});

  // Upper lip
  function buildLipGeo(yOffset, curve, thickness) {{
    const pts = [];
    for (let i = 0; i <= 24; i++) {{
      const s = (i / 24 - 0.5) * 2;
      const lx = s * 0.22;
      const ly = yOffset + curve * 0.08 * (1 - s * s);
      const lz = 0.62 - Math.abs(s) * 0.04;
      pts.push(new THREE.Vector3(lx, ly, lz));
    }}
    const path = new THREE.CatmullRomCurve3(pts);
    return new THREE.TubeGeometry(path, 24, thickness, 8, false);
  }}

  const upperLip = new THREE.Mesh(buildLipGeo(-0.28, mouthCurve * 0.5, 0.018), lipColor.clone());
  upperLip.userData.type = 'upperLip';
  upperLip.userData.baseCurve = mouthCurve;
  group.add(upperLip);

  const lowerLip = new THREE.Mesh(buildLipGeo(-0.32, mouthCurve * 0.3, 0.022), lipColor.clone());
  lowerLip.userData.type = 'lowerLip';
  lowerLip.userData.baseCurve = mouthCurve;
  group.add(lowerLip);

  // ── Halo + rim lights ──
  const haloLight = new THREE.PointLight(color, 0.5, 6);
  haloLight.position.set(x, y, -1.8);
  scene.add(haloLight);
  faceLights.push(haloLight);

  const rimLight = new THREE.PointLight(color, 0.15, 3);
  rimLight.position.set(x, y + 0.5, -0.8);
  scene.add(rimLight);

  scene.add(group);
  faceGroups.push(group);
}}

FACES.forEach((f, i) => createFace(f, i));

// ─── Interaction ───
let currentDim = null;
let activeGroup = null;
let activeIndex = -1;

function onMouseMove(e) {{
  mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;

  // Project mouse into world space on z=0 plane for eye tracking
  const v = new THREE.Vector3(mouse.x, mouse.y, 0.5);
  v.unproject(camera);
  const dir = v.sub(camera.position).normalize();
  const dist = -camera.position.z / dir.z;
  mouseWorld.copy(camera.position).add(dir.multiplyScalar(dist));

  // Subtle camera parallax
  camera.position.x = mouse.x * 0.25;
  camera.position.y = mouse.y * 0.15;
  camera.lookAt(0, 0, 0);
}}

function onClick(e) {{
  raycaster.setFromCamera(mouse, camera);
  const hits = raycaster.intersectObjects(hoverTargets);
  if (hits.length > 0) {{
    const dim = hits[0].object.userData.dim;
    const idx = hits[0].object.userData.index;
    if (currentDim === dim) stopAll();
    else playFace(FACES[idx], idx);
  }}
}}

function playFace(data, idx) {{
  stopAll();
  currentDim = data.dim;
  activeGroup = faceGroups[idx];
  activeIndex = idx;

  const panel = document.getElementById('textPanel');
  document.getElementById('panelBadge').style.background = data.color;
  document.getElementById('panelBadge').textContent = data.label;
  document.getElementById('panelText').innerHTML = '\\u275D ' + data.text + ' \\u275E';
  document.getElementById('panelMeta').textContent = 'Voix : ' + data.voice;
  panel.classList.add('visible');
  document.getElementById('hint').style.opacity = '0';

  faceLights[idx].intensity = 1.5;

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
  faceLights.forEach(l => {{ l.intensity = 0.5; }});
  currentDim = null;
  activeGroup = null;
  activeIndex = -1;
}}

window.addEventListener('mousemove', onMouseMove);
window.addEventListener('click', onClick);
window.addEventListener('resize', () => {{
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}});

// ─── Smooth value tracking ───
function lerp(a, b, t) {{ return a + (b - a) * t; }}

// ─── Animation ───
const clock = new THREE.Clock();

function animate() {{
  requestAnimationFrame(animate);
  const t = clock.getElapsedTime();
  const dt = Math.min(clock.getDelta(), 0.05);

  // Speaker world position (for idle faces to look at)
  let speakerPos = null;
  if (activeGroup) {{
    speakerPos = new THREE.Vector3();
    activeGroup.getWorldPosition(speakerPos);
  }}

  faceGroups.forEach((group, i) => {{
    const isActive = i === activeIndex;
    const fp = group.userData.data.face;
    const baseX = group.userData.baseX;
    const baseY = group.userData.baseY;

    // ── Breathing (all faces) ──
    const breathe = Math.sin(t * 0.8 + i * 0.7) * 0.012;
    group.scale.setScalar(1 + breathe);

    // ── Float ──
    group.position.y = baseY + Math.sin(t * 0.5 + i * 1.1) * 0.03;

    // ── Eye target: mouse (always) or speaker (idle while someone talks) ──
    let eyeTarget = mouseWorld.clone();
    let lookStrength = 0.6;

    if (!isActive && speakerPos) {{
      // Idle faces look toward the speaker
      eyeTarget = speakerPos.clone();
      lookStrength = 0.8;
    }}

    // Convert eye target to group-local coordinates
    const localTarget = group.worldToLocal(eyeTarget.clone());

    group.children.forEach(child => {{
      // ── Eyes follow target ──
      if (child.userData.type === 'iris' || child.userData.type === 'pupil') {{
        const bx = child.userData.baseX;
        const by = child.userData.baseY;
        const dx = (localTarget.x - bx) * 0.03 * lookStrength;
        const dy = (localTarget.y - by) * 0.03 * lookStrength;
        const maxShift = 0.035;
        const cx = Math.max(-maxShift, Math.min(maxShift, dx));
        const cy = Math.max(-maxShift, Math.min(maxShift, dy));
        child.position.x = lerp(child.position.x, bx + cx, 0.08);
        child.position.y = lerp(child.position.y, by + cy, 0.08);
      }}

      // ── Active face: talking ──
      if (isActive) {{
        if (child.userData.type === 'upperLip' || child.userData.type === 'lowerLip') {{
          const baseCurve = child.userData.baseCurve;
          const isUpper = child.userData.type === 'upperLip';
          const talk = Math.sin(t * 12) * 0.4 + Math.sin(t * 17) * 0.2 + Math.sin(t * 7) * 0.25;
          const yOff = isUpper ? -0.28 : (-0.32 - Math.abs(talk) * 0.025);
          const curve = baseCurve * (isUpper ? 0.5 : 0.3) + talk * 0.2;
          const thickness = (isUpper ? 0.018 : 0.022) + Math.abs(talk) * 0.005;
          const pts = [];
          for (let j = 0; j <= 24; j++) {{
            const s = (j / 24 - 0.5) * 2;
            pts.push(new THREE.Vector3(
              s * 0.22,
              yOff + curve * 0.08 * (1 - s * s),
              0.62 - Math.abs(s) * 0.04
            ));
          }}
          const path = new THREE.CatmullRomCurve3(pts);
          const newGeo = new THREE.TubeGeometry(path, 24, thickness, 8, false);
          child.geometry.dispose();
          child.geometry = newGeo;
        }}

        if (child.userData.type === 'pupil') {{
          child.scale.setScalar(1 + Math.sin(t * 3) * 0.1);
        }}

        if (child.userData.type === 'brow') {{
          const shift = Math.sin(t * 2.5 + (child.position.x > 0 ? 0.5 : 0)) * 0.02;
          child.position.y = lerp(child.position.y, child.userData.baseY + shift, 0.1);
        }}
      }} else {{
        // ── Idle face ──
        if (child.userData.type === 'brow') {{
          child.position.y = lerp(child.position.y, child.userData.baseY, 0.05);
        }}
      }}
    }});

    // ── Head rotation ──
    if (isActive) {{
      // Active: slight animated movement
      group.rotation.x = lerp(group.rotation.x, Math.sin(t * 0.7) * 0.04, 0.05);
      group.rotation.y = lerp(group.rotation.y, Math.sin(t * 0.5) * 0.03, 0.05);
      faceLights[i].intensity = 1.3 + Math.sin(t * 2) * 0.4;
    }} else if (speakerPos) {{
      // Idle while someone speaks: turn slightly toward speaker
      const dx = speakerPos.x - baseX;
      const dy = speakerPos.y - baseY;
      const targetRotY = Math.atan2(dx, 10) * 0.6;
      const targetRotX = Math.atan2(-dy, 10) * 0.3;
      group.rotation.y = lerp(group.rotation.y, targetRotY, 0.03);
      group.rotation.x = lerp(group.rotation.x, targetRotX, 0.03);
      // Dim idle faces slightly
      faceLights[i].intensity = lerp(faceLights[i].intensity, 0.25, 0.03);
    }} else {{
      // No one speaking: gentle idle sway
      const idleRotY = Math.sin(t * 0.3 + i * 0.8) * 0.05;
      const idleRotX = Math.sin(t * 0.4 + i * 1.2) * 0.02;
      group.rotation.y = lerp(group.rotation.y, idleRotY, 0.04);
      group.rotation.x = lerp(group.rotation.x, idleRotX, 0.04);
      faceLights[i].intensity = lerp(faceLights[i].intensity, 0.5, 0.03);
    }}

    // ── Blink ~~4s cycle ──
    const blinkPhase = ((t + i * 1.3) % 4.0) / 4.0;
    if (blinkPhase > 0.94) {{
      const blinkAmt = Math.sin((blinkPhase - 0.94) / 0.06 * Math.PI);
      group.children.forEach(child => {{
        if (child.geometry && child.geometry.parameters &&
            child.userData.type !== 'iris' && child.userData.type !== 'pupil' &&
            child.geometry.type === 'SphereGeometry' &&
            child.material.color && child.material.color.r > 0.8) {{
          child.scale.y = 1 - blinkAmt * 0.7;
        }}
      }});
    }}
  }});

  // Hover glow
  raycaster.setFromCamera(mouse, camera);
  const hits = raycaster.intersectObjects(hoverTargets);
  document.body.style.cursor = hits.length > 0 ? 'pointer' : 'default';

  hoverTargets.forEach(target => {{
    const idx = target.userData.index;
    const isHovered = hits.length > 0 && hits[0].object.userData.index === idx;
    const isAct = idx === activeIndex;
    const goalEmissive = isAct ? 0.15 : (isHovered ? 0.12 : 0.04);
    target.material.emissiveIntensity = lerp(target.material.emissiveIntensity, goalEmissive, 0.08);
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
