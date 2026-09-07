"""Apply AFRITOON performance state to canonical character artwork."""
from __future__ import annotations
from dataclasses import dataclass
import math
from PIL import Image, ImageDraw
from .acting import acting_expression
from .acting_timing import acting_motion
from .cast_scene import CastScene
from .mouth_timing import mouth_cues
from .performance import PerformanceState
from .story_performance import cue_at, cues_for

@dataclass(frozen=True)
class CharacterPerformanceProfile:
    skin: str
    face_center: tuple[float,float] = (300.0,335.0)
    eye_y: float = 330.0
    left_eye_x: float = 245.0
    right_eye_x: float = 355.0
    mouth_y: float = 435.0

PROFILES={"tunde":CharacterPerformanceProfile("#8b5a3c"),"seyi":CharacterPerformanceProfile("#6b3e24"),"mama":CharacterPerformanceProfile("#8b5a3c")}
CHARACTER_MOTION={"tunde":{"idle":(0,0,1),"talk":(0,-2,1),"shock":(-6,-10,1.04),"shocked":(-6,-10,1.04),"freeze":(0,0,1),"dance":(4,-6,1.03),"vibe":(-2,-3,1.02),"check_pocket":(3,4,1),"look_at_camera":(0,0,1.01),"laugh":(2,-4,1.02),"stand":(0,0,1)},"seyi":{"idle":(0,0,1),"talk":(.8,-1,1),"look":(2.5,0,1),"turn":(5,0,1),"look_at_camera":(1.5,0,1.01),"laugh":(2,-2,1.01),"freeze":(0,0,1)},"mama":{"idle":(0,0,1),"stand":(0,0,1),"talk":(-1,1,1.01),"turn":(-4,0,1),"look_at_camera":(-1.5,0,1.02),"angry":(0,2,1.01),"freeze":(0,0,1)}}

def _face_scale(image): return image.width/600.0
def _cover_face(draw,profile,s,box): draw.ellipse(tuple(int(v*s) for v in box),fill=profile.skin)

def _draw_expression(image,character,expression,mouth):
    profile=PROFILES.get(character,PROFILES["tunde"]); s=_face_scale(image); draw=ImageDraw.Draw(image); stroke=max(2,round(8*s)); black="#171717"; white="#ffffff"
    _cover_face(draw,profile,s,(202,235,288,305)); _cover_face(draw,profile,s,(312,235,398,305)); _cover_face(draw,profile,s,(235,395,365,480))
    eye_y=profile.eye_y*s; eye_h=34*s; eye_w=30*s; centers=(profile.left_eye_x*s,profile.right_eye_x*s)
    if expression in {"shocked","surprised"}: eye_w,eye_h=37*s,43*s
    elif expression=="angry": eye_h=27*s
    elif expression=="deadpan": eye_h=25*s
    for cx in centers:
        draw.ellipse((cx-eye_w,eye_y-eye_h,cx+eye_w,eye_y+eye_h),fill=white,outline=black,width=stroke); pupil=13*s if expression in {"shocked","surprised"} else 10*s; draw.ellipse((cx-pupil,eye_y-pupil,cx+pupil,eye_y+pupil),fill=black)
    brow_y=275*s
    if expression=="angry": draw.line((210*s,285*s,275*s,260*s),fill=black,width=stroke); draw.line((325*s,260*s,390*s,285*s),fill=black,width=stroke)
    elif expression=="deadpan": draw.line((210*s,brow_y,275*s,brow_y),fill=black,width=stroke); draw.line((325*s,brow_y,390*s,brow_y),fill=black,width=stroke)
    elif expression in {"shocked","surprised","curious"}: draw.line((210*s,260*s,275*s,250*s),fill=black,width=stroke); draw.line((325*s,250*s,390*s,260*s),fill=black,width=stroke)
    else: draw.line((210*s,270*s,275*s,258*s),fill=black,width=stroke); draw.line((325*s,258*s,390*s,270*s),fill=black,width=stroke)
    mx,my=300*s,profile.mouth_y*s
    if mouth in {"open","talk_o"}: draw.ellipse((mx-31*s,my-27*s,mx+31*s,my+27*s),fill=black)
    elif mouth in {"small_open","talk_e"}: draw.ellipse((mx-23*s,my-17*s,mx+23*s,my+17*s),fill=black)
    elif mouth in {"talk_a","talk_rest"}: draw.ellipse((mx-27*s,my-20*s,mx+27*s,my+20*s),fill=black)
    elif mouth=="talk_m": draw.line((275*s,my,325*s,my),fill=black,width=stroke)
    elif mouth in {"smile","wide_smile","happy","laughing"}: draw.arc((255*s,405*s,345*s,465*s),10,165,fill=black,width=stroke)
    elif mouth in {"sad","tight"}: draw.arc((255*s,420*s,345*s,470*s),195,345,fill=black,width=stroke)
    else: draw.line((270*s,my,330*s,my),fill=black,width=stroke)

def apply_face_performance(image,state,character):
    image=image.convert("RGBA"); _draw_expression(image,character,state.expression,state.mouth); return image

def apply_performance(image,state,character):
    image=apply_face_performance(image,state,character); rotation,y_shift,scale=CHARACTER_MOTION.get(character,CHARACTER_MOTION["tunde"]).get(state.pose,(0,0,1))
    if state.pose=="dance": rotation*=math.sin(1.0)
    if scale!=1: image=image.resize((max(1,round(image.width*scale)),max(1,round(image.height*scale))),Image.Resampling.LANCZOS)
    if rotation: image=image.rotate(rotation,resample=Image.Resampling.BICUBIC,expand=True)
    if y_shift:
        shifted=Image.new("RGBA",image.size,(0,0,0,0)); shifted.alpha_composite(image,(0,round(y_shift*image.width/600.0))); image=shifted
    return image

def _action_start_at(scene,character,frame_time,action):
    candidates=[float(c.time) for c in scene.cues() if c.character==character and c.time<=frame_time and c.pose==action]
    if scene.story_plan is not None: candidates.extend(float(c.at) for c in cues_for(scene.story_plan,character) if c.at<=frame_time and c.action==action)
    return max(candidates) if candidates else None

def _conversation_focus(scene,character,frame_time):
    line=scene.dialogue_at(frame_time)
    if line is None: return None
    speaker=line.character.strip().lower()
    if speaker==character: return None
    state=scene.state_at(frame_time); speaker_state=state.characters.get(speaker); listener_state=state.characters.get(character)
    if speaker_state is None or listener_state is None or not speaker_state.visible or not listener_state.visible: return None
    return speaker

def performance_for_character(scene,character,frame_time):
    state=scene.state_at(frame_time)
    if character not in state.characters: raise ValueError(f"Character not present in scene: {character}")
    instance=state.characters[character]; line=scene.dialogue_at(frame_time); mouth=()
    if line is not None and line.character.strip().lower()==character: mouth=mouth_cues(line.text,line.at,line.duration)
    active="closed"
    for cue in mouth:
        if cue.at<=frame_time<cue.at+cue.duration: active=cue.state.name; break

    # Dialogue is an explicit performance action: while a character is
    # speaking, their body should talk unless a stronger authored action is
    # currently active (shock/freeze/dance/etc.).
    pose=instance.pose
    if line is not None and line.character.strip().lower()==character:
        pose="talk"

    resolved_expression=acting_expression(character,pose,instance.expression)
    start=_action_start_at(scene,character,frame_time,pose)
    if start is not None: phase,_,motion_progress=acting_motion(character,pose,frame_time-start)
    else: phase,motion_progress="hold",1.0

    focus=None
    if scene.story_plan is not None:
        story_cue=cue_at(cues_for(scene.story_plan,character),frame_time)
        if story_cue is not None and story_cue.action==instance.pose: focus=story_cue.focus
    if pose=="look_at_camera": focus="camera"
    if focus is None: focus=_conversation_focus(scene,character,frame_time)
    return PerformanceState(pose=pose,action=pose,expression=resolved_expression,mouth=active,phase=phase,motion_progress=motion_progress,focus=focus)
