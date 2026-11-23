"""Generate the Three.js 3D face wall — 8 realistic faces with lip sync.

Uses a GLB model (FaceCap) with 52 ARKit morph targets for realistic
facial animation, lip sync via Web Audio API, and eye gaze tracking.
Grid: 2 rows × 4 columns. Click a face to hear the testimony.
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
MODEL_PATH = Path('data/models/facecap.glb')
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

with open(MODEL_PATH, 'rb') as mf:
    model_b64 = base64.b64encode(mf.read()).decode('utf-8')

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
<script src="https://cdn.jsdelivr.net/gh/mrdoob/three.js@r128/examples/js/loaders/GLTFLoader.js"></script>
<script>
"use strict";

const FACES = {faces_json};
const MODEL_B64 = "{model_b64}";

// ─── Scene ───
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 100);
camera.position.set(0, 0, 14);

const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: false }});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setClearColor(0x000000, 1);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.4;
document.body.appendChild(renderer.domElement);

// ─── Lighting ───
scene.add(new THREE.AmbientLight(0x2a2a3e, 0.8));
const keyLight = new THREE.DirectionalLight(0xddeeff, 0.7);
keyLight.position.set(2, 4, 6);
scene.add(keyLight);
const fillLight = new THREE.DirectionalLight(0x445566, 0.3);
fillLight.position.set(-3, 1, 4);
scene.add(fillLight);
const rimLight = new THREE.DirectionalLight(0x667788, 0.2);
rimLight.position.set(0, -2, -3);
scene.add(rimLight);

// ─── Layout ───
const COLS = 4, ROWS = 2;
const SPACING_X = 3.2, SPACING_Y = 3.6;
const OFFSET_X = -(COLS - 1) * SPACING_X / 2;
const OFFSET_Y = (ROWS - 1) * SPACING_Y / 2 - 0.3;

const faceGroups = [];
const faceLights = [];
const faceMeshes = [];
const hoverTargets = [];
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2(0, 0);
const mouseWorld = new THREE.Vector3(0, 0, 0);

function lerp(a, b, t) {{ return a + (b - a) * t; }}

// ─── Web Audio lip sync ───
let audioCtx = null;
let analyser = null;
let freqData = null;
let activeSource = null;

function initAudio() {{
  if (audioCtx) return;
  audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  analyser = audioCtx.createAnalyser();
  analyser.fftSize = 256;
  analyser.smoothingTimeConstant = 0.6;
  freqData = new Uint8Array(analyser.frequencyBinCount);
  analyser.connect(audioCtx.destination);
}}

function connectAudio(audioEl) {{
  initAudio();
  if (activeSource) {{
    try {{ activeSource.disconnect(); }} catch(e) {{}}
  }}
  if (!audioEl._sourceNode) {{
    audioEl._sourceNode = audioCtx.createMediaElementSource(audioEl);
  }}
  audioEl._sourceNode.connect(analyser);
  activeSource = audioEl._sourceNode;
}}

function getAmplitude() {{
  if (!analyser) return 0;
  analyser.getByteFrequencyData(freqData);
  let sum = 0;
  const lo = 2, hi = 24;
  for (let i = lo; i < hi; i++) sum += freqData[i];
  return Math.min(1.0, (sum / ((hi - lo) * 255)) * 3.0);
}}

// ─── Apply emotion to morph targets ───
function applyEmotion(mesh, fp, restingInfluences) {{
  const d = mesh.morphTargetDictionary;
  if (!d) return;

  const r = new Float32Array(mesh.morphTargetInfluences.length);

  if (fp.eyebrows > 0) {{
    if (d['browOuterUp_L'] !== undefined) r[d['browOuterUp_L']] = fp.eyebrows * 0.6;
    if (d['browOuterUp_R'] !== undefined) r[d['browOuterUp_R']] = fp.eyebrows * 0.6;
  }} else {{
    if (d['browDown_L'] !== undefined) r[d['browDown_L']] = -fp.eyebrows * 0.5;
    if (d['browDown_R'] !== undefined) r[d['browDown_R']] = -fp.eyebrows * 0.5;
    if (d['browInnerUp'] !== undefined) r[d['browInnerUp']] = -fp.eyebrows * 0.3;
  }}

  if (fp.mouth > 0) {{
    if (d['mouthSmile_L'] !== undefined) r[d['mouthSmile_L']] = fp.mouth * 0.5;
    if (d['mouthSmile_R'] !== undefined) r[d['mouthSmile_R']] = fp.mouth * 0.5;
  }} else {{
    if (d['mouthFrown_L'] !== undefined) r[d['mouthFrown_L']] = -fp.mouth * 0.5;
    if (d['mouthFrown_R'] !== undefined) r[d['mouthFrown_R']] = -fp.mouth * 0.5;
  }}

  if (fp.eyes < 0.4) {{
    if (d['eyeSquint_L'] !== undefined) r[d['eyeSquint_L']] = (0.4 - fp.eyes) * 1.5;
    if (d['eyeSquint_R'] !== undefined) r[d['eyeSquint_R']] = (0.4 - fp.eyes) * 1.5;
  }} else if (fp.eyes > 0.7) {{
    if (d['eyeWide_L'] !== undefined) r[d['eyeWide_L']] = (fp.eyes - 0.7) * 2.0;
    if (d['eyeWide_R'] !== undefined) r[d['eyeWide_R']] = (fp.eyes - 0.7) * 2.0;
  }}

  for (let i = 0; i < r.length; i++) restingInfluences[i] = r[i];
}}

// ─── Decode base64 GLB model ───
function b64ToArrayBuffer(b64) {{
  const bin = atob(b64);
  const buf = new ArrayBuffer(bin.length);
  const view = new Uint8Array(buf);
  for (let i = 0; i < bin.length; i++) view[i] = bin.charCodeAt(i);
  return buf;
}}

const loader = new THREE.GLTFLoader();

const loadingDiv = document.createElement('div');
loadingDiv.style.cssText = 'position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);color:rgba(255,255,255,0.3);font:16px sans-serif;z-index:100';
loadingDiv.textContent = 'Chargement des visages...';
document.body.appendChild(loadingDiv);

const modelBuffer = b64ToArrayBuffer(MODEL_B64);
loader.parse(modelBuffer, '', (gltf) => {{
  loadingDiv.remove();

  const templateScene = gltf.scene;
  templateScene.updateMatrixWorld(true);

  FACES.forEach((data, index) => {{
    const col = index % COLS;
    const row = Math.floor(index / COLS);
    const x = OFFSET_X + col * SPACING_X;
    const y = OFFSET_Y - row * SPACING_Y;

    const group = new THREE.Group();
    group.position.set(x, y, 0);
    group.userData = {{ dim: data.dim, index, data, baseX: x, baseY: y }};

    const color = new THREE.Color(data.color);

    const clone = templateScene.clone(true);
    clone.scale.setScalar(1.4);
    clone.rotation.x = 0.05;

    const meshInfo = {{ head: null, teeth: null, eyes: [], restingInfluences: null }};

    clone.traverse((child) => {{
      if (child.isMesh) {{
        child.material = child.material.clone();
        child.material.emissive = color.clone();
        child.material.emissiveIntensity = 0.03;

        if (child.morphTargetDictionary) {{
          meshInfo.head = child;
          meshInfo.restingInfluences = new Float32Array(child.morphTargetInfluences.length);
          applyEmotion(child, data.face, meshInfo.restingInfluences);
          for (let i = 0; i < meshInfo.restingInfluences.length; i++) {{
            child.morphTargetInfluences[i] = meshInfo.restingInfluences[i];
          }}
        }}

        const name = (child.name || '').toLowerCase();
        if (name.includes('teeth') || name.includes('tooth')) {{
          meshInfo.teeth = child;
        }}
      }}

      if (child.name === 'eyeLeft' || child.name === 'eyeRight') {{
        meshInfo.eyes.push(child);
      }}
    }});

    group.add(clone);

    // Hit target for raycasting
    const hitGeo = new THREE.SphereGeometry(1.2, 16, 16);
    const hitMat = new THREE.MeshBasicMaterial({{ visible: false }});
    const hitMesh = new THREE.Mesh(hitGeo, hitMat);
    hitMesh.userData = {{ dim: data.dim, index }};
    group.add(hitMesh);
    hoverTargets.push(hitMesh);

    // Halo light
    const haloLight = new THREE.PointLight(color, 0.5, 6);
    haloLight.position.set(x, y, -2.5);
    scene.add(haloLight);
    faceLights.push(haloLight);

    // Rim accent light
    const accent = new THREE.PointLight(color, 0.15, 3);
    accent.position.set(x, y + 0.6, -1);
    scene.add(accent);

    scene.add(group);
    faceGroups.push(group);
    faceMeshes.push(meshInfo);
  }});

  // ─── Interaction ───
  let currentDim = null;
  let activeIndex = -1;

  function onMouseMove(e) {{
    mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;

    const v = new THREE.Vector3(mouse.x, mouse.y, 0.5);
    v.unproject(camera);
    const dir = v.sub(camera.position).normalize();
    const dist = -camera.position.z / dir.z;
    mouseWorld.copy(camera.position).add(dir.multiplyScalar(dist));

    camera.position.x = mouse.x * 0.25;
    camera.position.y = mouse.y * 0.15;
    camera.lookAt(0, 0, 0);
  }}

  window.stopAll = function() {{
    if (currentDim) {{
      const audio = document.getElementById('audio-' + currentDim);
      if (audio) {{ audio.pause(); audio.currentTime = 0; }}
    }}
    document.getElementById('textPanel').classList.remove('visible');
    document.getElementById('hint').style.opacity = '1';
    faceLights.forEach(l => {{ l.intensity = 0.5; }});
    currentDim = null;
    activeIndex = -1;
  }};

  function playFace(data, idx) {{
    window.stopAll();
    currentDim = data.dim;
    activeIndex = idx;

    document.getElementById('panelBadge').style.background = data.color;
    document.getElementById('panelBadge').textContent = data.label;
    document.getElementById('panelText').innerHTML = '\\u275D ' + data.text + ' \\u275E';
    document.getElementById('panelMeta').textContent = 'Voix : ' + data.voice;
    document.getElementById('textPanel').classList.add('visible');
    document.getElementById('hint').style.opacity = '0';

    faceLights[idx].intensity = 1.5;

    const audio = document.getElementById('audio-' + data.dim);
    connectAudio(audio);
    audio.currentTime = 0;
    audio.play();
    audio.onended = () => window.stopAll();
  }}

  function onClick(e) {{
    raycaster.setFromCamera(mouse, camera);
    const hits = raycaster.intersectObjects(hoverTargets);
    if (hits.length > 0) {{
      const dim = hits[0].object.userData.dim;
      const idx = hits[0].object.userData.index;
      if (currentDim === dim) window.stopAll();
      else playFace(FACES[idx], idx);
    }}
  }}

  window.addEventListener('mousemove', onMouseMove);
  window.addEventListener('click', onClick);
  window.addEventListener('resize', () => {{
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  }});

  // ─── Animation ───
  const clock = new THREE.Clock();

  function animate() {{
    requestAnimationFrame(animate);
    const t = clock.getElapsedTime();

    let speakerPos = null;
    if (activeIndex >= 0) {{
      speakerPos = new THREE.Vector3();
      faceGroups[activeIndex].getWorldPosition(speakerPos);
    }}

    const amplitude = activeIndex >= 0 ? getAmplitude() : 0;

    faceGroups.forEach((group, i) => {{
      const isActive = i === activeIndex;
      const info = faceMeshes[i];
      const baseX = group.userData.baseX;
      const baseY = group.userData.baseY;

      // ── Breathing ──
      const breathe = Math.sin(t * 0.8 + i * 0.7) * 0.01;
      group.scale.setScalar(1 + breathe);

      // ── Float ──
      group.position.y = baseY + Math.sin(t * 0.5 + i * 1.1) * 0.025;

      // ── Morph target animation ──
      if (info.head && info.head.morphTargetDictionary) {{
        const d = info.head.morphTargetDictionary;
        const inf = info.head.morphTargetInfluences;
        const rest = info.restingInfluences;

        // Reset to resting pose
        for (let j = 0; j < inf.length; j++) {{
          inf[j] = lerp(inf[j], rest[j], 0.08);
        }}

        // ── Blinking (~4s cycle) ──
        const blinkPhase = ((t + i * 1.3) % 4.0) / 4.0;
        if (blinkPhase > 0.94) {{
          const blinkAmt = Math.sin((blinkPhase - 0.94) / 0.06 * Math.PI);
          if (d['eyeBlink_L'] !== undefined) inf[d['eyeBlink_L']] = blinkAmt;
          if (d['eyeBlink_R'] !== undefined) inf[d['eyeBlink_R']] = blinkAmt;
        }}

        // ── Eye gaze via morph targets ──
        let gazeX = 0, gazeY = 0;
        if (!isActive && speakerPos) {{
          const dx = speakerPos.x - baseX;
          const dy = speakerPos.y - baseY;
          gazeX = Math.max(-1, Math.min(1, dx * 0.15));
          gazeY = Math.max(-1, Math.min(1, dy * 0.15));
        }} else {{
          gazeX = Math.max(-1, Math.min(1, (mouseWorld.x - baseX) * 0.1));
          gazeY = Math.max(-1, Math.min(1, (mouseWorld.y - baseY) * 0.1));
        }}

        if (gazeX > 0) {{
          if (d['eyeLookOut_L'] !== undefined) inf[d['eyeLookOut_L']] = gazeX * 0.6;
          if (d['eyeLookIn_R'] !== undefined) inf[d['eyeLookIn_R']] = gazeX * 0.6;
        }} else {{
          if (d['eyeLookIn_L'] !== undefined) inf[d['eyeLookIn_L']] = -gazeX * 0.6;
          if (d['eyeLookOut_R'] !== undefined) inf[d['eyeLookOut_R']] = -gazeX * 0.6;
        }}
        if (gazeY > 0) {{
          if (d['eyeLookUp_L'] !== undefined) inf[d['eyeLookUp_L']] = gazeY * 0.5;
          if (d['eyeLookUp_R'] !== undefined) inf[d['eyeLookUp_R']] = gazeY * 0.5;
        }} else {{
          if (d['eyeLookDown_L'] !== undefined) inf[d['eyeLookDown_L']] = -gazeY * 0.5;
          if (d['eyeLookDown_R'] !== undefined) inf[d['eyeLookDown_R']] = -gazeY * 0.5;
        }}

        if (isActive) {{
          // ── Lip sync from audio amplitude ──
          const a = amplitude;
          if (d['jawOpen'] !== undefined) inf[d['jawOpen']] = a * 0.6;
          if (d['mouthOpen'] !== undefined) inf[d['mouthOpen']] = a * 0.4;
          if (d['mouthFunnel'] !== undefined) inf[d['mouthFunnel']] = a * 0.15 + Math.sin(t * 5) * 0.05;
          if (d['mouthPucker'] !== undefined) inf[d['mouthPucker']] = Math.sin(t * 7) * a * 0.1;
          if (d['mouthStretch_L'] !== undefined) inf[d['mouthStretch_L']] = a * 0.1;
          if (d['mouthStretch_R'] !== undefined) inf[d['mouthStretch_R']] = a * 0.1;

          // Speaking micro-expressions
          if (d['browInnerUp'] !== undefined) inf[d['browInnerUp']] = rest[d['browInnerUp']] + a * 0.15;
          if (d['cheekSquint_L'] !== undefined) inf[d['cheekSquint_L']] = a * 0.1;
          if (d['cheekSquint_R'] !== undefined) inf[d['cheekSquint_R']] = a * 0.1;
          if (d['noseSneer_L'] !== undefined) inf[d['noseSneer_L']] = a * 0.05;
          if (d['noseSneer_R'] !== undefined) inf[d['noseSneer_R']] = a * 0.05;
        }} else {{
          // Idle micro-expressions
          const micro = Math.sin(t * 0.4 + i * 2.1) * 0.03;
          if (d['mouthSmile_L'] !== undefined) inf[d['mouthSmile_L']] += micro;
          if (d['mouthSmile_R'] !== undefined) inf[d['mouthSmile_R']] += micro;
        }}
      }}

      // ── Eye object rotation (if model has eye bones) ──
      if (info.eyes.length > 0) {{
        let lookTarget;
        if (!isActive && speakerPos) {{
          lookTarget = speakerPos;
        }} else {{
          lookTarget = mouseWorld;
        }}
        info.eyes.forEach(eye => {{
          const local = eye.parent.worldToLocal(lookTarget.clone());
          const maxAngle = 0.25;
          const targetRotY = Math.max(-maxAngle, Math.min(maxAngle, Math.atan2(local.x, local.z)));
          const targetRotX = Math.max(-maxAngle, Math.min(maxAngle, -Math.atan2(local.y, local.z)));
          eye.rotation.y = lerp(eye.rotation.y, targetRotY, 0.06);
          eye.rotation.x = lerp(eye.rotation.x, targetRotX, 0.06);
        }});
      }}

      // ── Head rotation ──
      if (isActive) {{
        group.rotation.x = lerp(group.rotation.x, Math.sin(t * 0.7) * 0.04, 0.04);
        group.rotation.y = lerp(group.rotation.y, Math.sin(t * 0.5) * 0.03, 0.04);
        faceLights[i].intensity = 1.3 + Math.sin(t * 2) * 0.4;
      }} else if (speakerPos) {{
        const dx = speakerPos.x - baseX;
        const dy = speakerPos.y - baseY;
        group.rotation.y = lerp(group.rotation.y, Math.atan2(dx, 10) * 0.5, 0.025);
        group.rotation.x = lerp(group.rotation.x, Math.atan2(-dy, 10) * 0.25, 0.025);
        faceLights[i].intensity = lerp(faceLights[i].intensity, 0.2, 0.03);
      }} else {{
        group.rotation.y = lerp(group.rotation.y, Math.sin(t * 0.3 + i * 0.8) * 0.04, 0.03);
        group.rotation.x = lerp(group.rotation.x, Math.sin(t * 0.4 + i * 1.2) * 0.02, 0.03);
        faceLights[i].intensity = lerp(faceLights[i].intensity, 0.5, 0.03);
      }}
    }});

    // ── Hover detection ──
    raycaster.setFromCamera(mouse, camera);
    const hits = raycaster.intersectObjects(hoverTargets);
    document.body.style.cursor = hits.length > 0 ? 'pointer' : 'default';

    hoverTargets.forEach(target => {{
      const idx = target.userData.index;
      const isHovered = hits.length > 0 && hits[0].object.userData.index === idx;
      const isAct = idx === activeIndex;
      const info = faceMeshes[idx];
      if (info.head) {{
        const goal = isAct ? 0.08 : (isHovered ? 0.06 : 0.03);
        info.head.material.emissiveIntensity = lerp(info.head.material.emissiveIntensity, goal, 0.08);
      }}
    }});

    renderer.render(scene, camera);
  }}

  animate();
}},
(error) => {{
  loadingDiv.textContent = 'Erreur de chargement du modèle 3D';
  console.error(error);
}});
</script>
</body>
</html>'''

with open(OUT_PATH, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f'3D Wall generated: {OUT_PATH}')
print(f'  {len(faces_data)} faces')
print(f'  File size: {os.path.getsize(OUT_PATH)/1024:.0f} KB')
