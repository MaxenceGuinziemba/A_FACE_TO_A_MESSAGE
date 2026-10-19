import pytest
import pandas as pd

from src.analysis.emotion import (
    FACE_MAP,
    LEXICON,
    NO_EVIDENCE,
    VOICE_MAP,
    compute_avatar_params,
    dominant_dimension,
    score_dimensions,
)


def test_scores_match_words_not_substrings():
    scores = score_dimensions("Une place importante pour les personnes déplacées.")

    assert scores["empathie"] == 0
    assert dominant_dimension(scores) == NO_EVIDENCE


def test_scores_are_accent_insensitive_and_ignore_local_negation():
    positive = score_dimensions("Nous sommes très SOLIDAIRES.")
    negated = score_dimensions("Nous ne sommes pas solidaires.")

    assert positive["solidarite"] > 0
    assert negated["solidarite"] == 0


def test_urgency_phrase_with_negation_words_is_not_discarded():
    scores = score_dimensions("Il ne faut plus attendre.")

    assert scores["urgence"] == pytest.approx(1 / 3)


def test_overlapping_phrases_count_as_one_piece_of_evidence():
    scores = score_dimensions("Je les accueille à leur place.")

    assert scores["empathie"] == pytest.approx(1 / 3)


def test_empty_or_unmatched_text_has_no_dominant_dimension():
    assert dominant_dimension(score_dimensions("")) == NO_EVIDENCE
    assert dominant_dimension(score_dimensions("Bonjour à toutes et à tous.")) == NO_EVIDENCE


def test_dominant_dimension_accepts_pandas_rows():
    row = pd.Series({"solidarite": 0.0, "empathie": 1 / 3})

    assert dominant_dimension(row) == "empathie"


def test_avatar_defaults_are_used_when_there_is_no_evidence():
    params = compute_avatar_params(score_dimensions(""))

    assert params == {
        "voice_pitch": 0.0,
        "voice_speed": 1.0,
        "voice_energy": 0.5,
        "voice_warmth": 0.5,
        "face_eyebrows": 0.0,
        "face_mouth": 0.0,
        "face_eyes": 0.5,
        "face_gaze": 0.5,
    }


def test_avatar_parameters_are_bounded_and_follow_the_weighted_map():
    params = compute_avatar_params({"solidarite": 1.0})

    assert params["voice_speed"] == VOICE_MAP["solidarite"]["speed"]
    assert params["face_mouth"] == FACE_MAP["solidarite"]["mouth"]
    assert 0.5 <= params["voice_speed"] <= 1.5
    for name in ("voice_energy", "voice_warmth", "face_eyes", "face_gaze"):
        assert 0 <= params[name] <= 1
    for name in ("voice_pitch", "face_eyebrows", "face_mouth"):
        assert -1 <= params[name] <= 1


def test_lexicon_and_maps_cover_the_same_dimensions():
    assert set(LEXICON) == set(VOICE_MAP) == set(FACE_MAP)
