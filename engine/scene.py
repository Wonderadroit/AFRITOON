from PIL import Image, ImageDraw
from .character import draw_background, draw_character
from .scene import Scene, CharacterState


class Renderer:
    def __init__(self, scene: Scene):
        self.scene = scene

    def state_at(self, name: str, t: float) -> CharacterState:
        base = self.scene.characters[name]
        state = CharacterState(base.x, base.y, base.expression, "idle", base.facing)
        for action in self.scene.actions.get(name, []):
            if action.time > t:
                break
            state.action = action.name
            if action.name in {"shock", "shocked", "surprise"}:
                state.expression = "shock"
            elif action.name in {"laugh", "happy"}:
                state.expression = "happy"
            elif action.name in {"sad", "cry"}:
                state.expression = "sad"
            elif action.name in {"angry"}:
                state.expression = "angry"
            elif action.name in {"idle", "vibe", "dance", "walk", "run", "check_pocket", "look_at_camera", "shrug"}:
                if action.params.get("expression"):
                    state.expression = action.params["expression"]
        return state

    def frame(self, t: float) -> Image.Image:
        img = Image.new("RGB", (self.scene.width, self.scene.height), "white")
        draw_background(img, self.scene.background)
        # Render farther characters first.
        for name in self.scene.characters:
            state = self.state_at(name, t)
            draw_character(img, state, name, t)
        d = ImageDraw.Draw(img)
        d.text((40, 40), "AFRITOON", fill=(20,20,20))
        return img
