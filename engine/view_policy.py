"""Resolve character views without silently inventing missing artwork."""

from __future__ import annotations

from pathlib import Path

from .character_assets import CharacterAssetResolver


class ViewResolution:
    def __init__(self, requested: str, resolved: str, path: Path, fallback: bool):
        self.requested = requested
        self.resolved = resolved
        self.path = path
        self.fallback = fallback


def resolve_view(repo_root: str | Path, character_id: str, requested: str = "front") -> ViewResolution:
    resolver = CharacterAssetResolver(repo_root)
    requested_art = resolver.resolve(character_id, requested)
    if requested_art.has_master:
        return ViewResolution(requested, requested, requested_art.master, False)
    front = resolver.resolve(character_id, "front")
    if not front.has_master:
        raise FileNotFoundError(f"No artwork master for {character_id}")
    return ViewResolution(requested, "front", front.master, True)
