"""Deterministic character entrances and exits for scene blocking."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping

@dataclass(frozen=True)
class EntryExitCue:
    at: float
    character: str
    action: str
    position: tuple[float,float] | None = None
    duration: float = 0.0
    def __post_init__(self):
        if str(self.action).strip().lower() not in {"enter","exit"}: raise ValueError("EntryExitCue.action must be 'enter' or 'exit'")
        if self.at < 0 or self.duration < 0: raise ValueError("EntryExitCue.at/duration must be non-negative")
        if self.position is not None and len(self.position) != 2: raise ValueError("EntryExitCue.position must contain x and y")

def _smoothstep(a):
    x=max(0.0,min(1.0,float(a))); return x*x*(3.0-2.0*x)

def _lerp(a,b,p):
    p=_smoothstep(p); return (a[0]+(b[0]-a[0])*p,a[1]+(b[1]-a[1])*p)

def _default_offscreen(character: str, action: str, authored: tuple[float,float]) -> tuple[float,float]:
    # With no explicit staging point, enter from the left and exit to the right.
    return (-180.0, authored[1]) if action == "enter" else (1260.0, authored[1])

def resolve_entry_exit(character: str, now: float, base: Mapping[str,tuple[float,float]], cues: tuple[EntryExitCue,...]=()):
    cid=character.strip().lower(); authored=tuple(map(float,base.get(cid,(540.0,1150.0))))
    current=authored; visible=True
    for cue in sorted((c for c in cues if c.character.strip().lower()==cid),key=lambda c:c.at):
        if now < cue.at: continue
        if cue.action == "enter":
            start=tuple(map(float,cue.position)) if cue.position is not None else _default_offscreen(cid,"enter",authored)
            if cue.duration <= 0 or now >= cue.at+cue.duration: current=authored
            else: current=_lerp(start,authored,(now-cue.at)/cue.duration)
            visible=True
        else:
            start=current; target=tuple(map(float,cue.position)) if cue.position is not None else _default_offscreen(cid,"exit",authored)
            if cue.duration <= 0 or now >= cue.at+cue.duration: current=target; visible=False
            else: current=_lerp(start,target,(now-cue.at)/cue.duration); visible=True
    return current,visible

def resolve_entry_exit_states(now, base: Mapping[str,tuple[float,float,float]], cues=()):
    xy={cid:(v[0],v[1]) for cid,v in base.items()}; result={}
    for cid,(x,y,scale) in base.items():
        (px,py),visible=resolve_entry_exit(cid,now,xy,tuple(cues)); result[cid]=(px,py,scale,visible)
    return result
