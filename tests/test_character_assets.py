from pathlib import Path

from engine.assets import LAYER_NAMES
from engine.character_assets import CharacterAssetResolver


def test_all_core_characters_have_canonical_front_masters():
    resolver = CharacterAssetResolver(Path("."))
    for character_id in ("tunde", "seyi", "mama"):
        art = resolver.resolve(character_id, "front")
        assert art.has_master
        assert len(LAYER_NAMES) == 16


def test_character_layer_contract_is_stable():
    resolver = CharacterAssetResolver(".")
    assert resolver.resolve("tunde").layers.missing() == list(LAYER_NAMES)
