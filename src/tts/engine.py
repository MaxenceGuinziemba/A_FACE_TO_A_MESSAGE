"""
TTS Engine — Transform emotional profiles into expressive French speech.

Uses Edge TTS with subtle prosody adjustments. Sends full text in one pass
to avoid truncation issues from sentence-by-sentence concatenation.
"""

import asyncio
import re
from pathlib import Path
from dataclasses import dataclass

import edge_tts


@dataclass
class VoiceProfile:
    name: str
    voice_id: str
    gender: str
    character: str


VOICES = [
    VoiceProfile('Vivienne', 'fr-FR-VivienneMultilingualNeural', 'female', 'warm, empathetic'),
    VoiceProfile('Denise', 'fr-FR-DeniseNeural', 'female', 'soft, reflective'),
    VoiceProfile('Remy', 'fr-FR-RemyMultilingualNeural', 'male', 'engaged, determined'),
    VoiceProfile('Henri', 'fr-FR-HenriNeural', 'male', 'assertive, serious'),
]

# Dimension → preferred voice per gender
_DIM_VOICE = {
    'tristesse':     {'female': 'Denise',   'male': 'Henri'},
    'indignation':   {'female': 'Denise',   'male': 'Henri'},
    'urgence':       {'female': 'Vivienne', 'male': 'Henri'},
    'espoir':        {'female': 'Vivienne', 'male': 'Remy'},
    'chaleur':       {'female': 'Vivienne', 'male': 'Remy'},
    'empathie':      {'female': 'Vivienne', 'male': 'Remy'},
    'solidarite':    {'female': 'Vivienne', 'male': 'Remy'},
    'determination': {'female': 'Denise',   'male': 'Henri'},
}


def select_voice(
    voice_params: dict,
    dominant_dim: str = None,
    speaker_gender: str = 'unknown',
) -> VoiceProfile:
    """Select voice based on emotion and gender guard-rail.

    speaker_gender is a guard-rail: if 'female' detected, exclude male voices
    (and vice-versa) to avoid obvious incoherence. If 'unknown', all voices
    are eligible.
    """
    if speaker_gender == 'female':
        eligible = [v for v in VOICES if v.gender == 'female']
    elif speaker_gender == 'male':
        eligible = [v for v in VOICES if v.gender == 'male']
    else:
        eligible = list(VOICES)

    if not eligible:
        eligible = list(VOICES)

    # For unknown gender, use a hash of voice_params to distribute voices
    if speaker_gender == 'unknown':
        h = hash(str(sorted(voice_params.items()))) % 2
        gender_key = 'male' if h % 2 == 0 else 'female'
    else:
        gender_key = speaker_gender

    if dominant_dim and dominant_dim in _DIM_VOICE:
        name = _DIM_VOICE[dominant_dim][gender_key]
        match = next((v for v in eligible if v.name == name), None)
        if match:
            return match

    warmth = voice_params.get('voice_warmth', 0.5)
    energy = voice_params.get('voice_energy', 0.5)
    if energy > 0.6:
        prefer = 'Henri' if gender_key == 'male' else 'Vivienne'
    elif warmth > 0.6:
        prefer = 'Remy' if gender_key == 'male' else 'Vivienne'
    else:
        prefer = 'Henri' if gender_key == 'male' else 'Denise'

    match = next((v for v in eligible if v.name == prefer), None)
    return match or eligible[0]


def _rate_str(speed: float) -> str:
    """voice_speed [0.5, 1.5] → edge-tts rate string. Subtle: ±15% max."""
    pct = int((speed - 1.0) * 30)  # 0.5→-15%, 1.5→+15%
    pct = max(-15, min(15, pct))
    return f'{pct:+d}%'


def _pitch_str(pitch: float) -> str:
    """voice_pitch [-1, 1] → edge-tts pitch string. Subtle: ±10Hz max."""
    hz = int(pitch * 10)
    hz = max(-10, min(10, hz))
    return f'{hz:+d}Hz'


def _volume_str(energy: float) -> str:
    """voice_energy [0, 1] → edge-tts volume string. Subtle: ±15% max."""
    pct = int((energy - 0.5) * 30)  # 0→-15%, 1→+15%
    pct = max(-15, min(15, pct))
    return f'{pct:+d}%'


def _sanitize(text: str) -> str:
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'\S+@\S+\.\S+', '', text)
    text = re.sub(r'\b\w{40,}\b', '', text)
    text = text.strip()
    if not text or len(text) < 3:
        text = 'Un message.'
    return text


async def generate_audio(
    text: str,
    voice_params: dict,
    output_path: str | Path,
    dominant_dim: str = None,
    voice_override: str = None,
    speaker_gender: str = 'unknown',
) -> dict:
    """Generate MP3 from text with subtle emotional prosody.

    Sends the full text in one call to Edge TTS — no sentence splitting,
    no chunk concatenation. This avoids truncation and audio glitches.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    text = _sanitize(text)

    if voice_override:
        voice = next(
            (v for v in VOICES if v.voice_id == voice_override or v.name == voice_override),
            VOICES[0],
        )
    else:
        voice = select_voice(voice_params, dominant_dim, speaker_gender)

    pitch = voice_params.get('voice_pitch', 0.0)
    speed = voice_params.get('voice_speed', 1.0)
    energy = voice_params.get('voice_energy', 0.5)

    rate = _rate_str(speed)
    pitch_s = _pitch_str(pitch)
    volume = _volume_str(energy)

    for attempt in range(3):
        try:
            kwargs = dict(rate=rate, pitch=pitch_s, volume=volume)
            if attempt == 2:
                kwargs = {}
            comm = edge_tts.Communicate(text, voice.voice_id, **kwargs)
            await comm.save(str(output_path))
            break
        except edge_tts.exceptions.NoAudioReceived:
            if attempt == 2:
                comm = edge_tts.Communicate('Un message.', voice.voice_id)
                await comm.save(str(output_path))
            await asyncio.sleep(0.5)

    return {
        'output_path': str(output_path),
        'voice_name': voice.name,
        'voice_id': voice.voice_id,
        'voice_gender': voice.gender,
        'dominant_dim': dominant_dim,
        'params': voice_params,
    }


def generate_audio_sync(text, voice_params, output_path, **kwargs):
    return asyncio.run(generate_audio(text, voice_params, output_path, **kwargs))


async def generate_batch(
    messages: list[dict],
    output_dir: str | Path,
    max_concurrent: int = 5,
) -> list[dict]:
    """Generate audio for multiple messages concurrently."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    semaphore = asyncio.Semaphore(max_concurrent)
    results = []

    async def process_one(msg):
        async with semaphore:
            out_path = output_dir / f'{msg["id"]}.mp3'
            try:
                result = await generate_audio(
                    text=msg['text'],
                    voice_params=msg['voice_params'],
                    output_path=out_path,
                    dominant_dim=msg.get('dominant_dim'),
                    speaker_gender=msg.get('speaker_gender', 'unknown'),
                )
                result['id'] = msg['id']
                result['status'] = 'ok'
                return result
            except Exception as e:
                return {'id': msg['id'], 'status': 'error', 'error': str(e)}

    tasks = [process_one(msg) for msg in messages]
    results = await asyncio.gather(*tasks)
    return list(results)


def generate_batch_sync(messages, output_dir, **kwargs):
    return asyncio.run(generate_batch(messages, output_dir, **kwargs))
