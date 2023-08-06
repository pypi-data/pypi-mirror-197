from collections.abc import Sequence
from enum import Enum
import logging
import math
from pathlib import Path
from typing import Mapping
from PIL import Image, ImageDraw, ImageFont
from skit._types import Real, LayoutDef, Color, FreeTypeFont, Alignment, Scale
from abc import ABC, abstractmethod


logger = logging.getLogger(__file__)


# some defaults for fallback
_DEFAULT_FONT = ImageFont.truetype('Helvetica', 16)
_DEFAULT_COLOR = 'black'
_DEFAULT_THICKNESS = 1

class _DrawCommand(Enum):
    TEXT = 'text'
    RECTANGLE = 'rect'
    IMAGE = 'image'


class CardManipulation(ABC):
    @abstractmethod
    def background(self, color: str): pass

    @abstractmethod
    def layout(self, name: str, layoutdef: LayoutDef): pass

    @abstractmethod
    def layouts(self, names: Sequence[str], layoutdefs: Sequence[LayoutDef]): pass

    @abstractmethod
    def layouts_map(self, layouts: Mapping[str, LayoutDef]): pass

    @abstractmethod
    def text(
        self, text: str,
        layout: str,
        font: FreeTypeFont | None,
        color: Color | None,
    ): pass

    @abstractmethod
    def rectangle(
        self,
        layout: str,
        color: Color | None,
        thickness: Real | None,
    ): pass

    @abstractmethod
    def filled_rectangle(
        self,
        layout: str,
        color: Color,
    ): pass

    @abstractmethod
    def image(
        self,
        image: Path,
        layout: str,
    ): pass

    @abstractmethod
    def render_png(self, filename: str): pass


class Card(CardManipulation):
    "A single card."
    def __init__(self, width: int = 750, height: int = 1050):
        self._width = width
        self._height = height
        self._layouts = {}
        self._background = '#ffffff00'
        self._commands = []

    def background(self, color: str):
        "Set the background color for this card."
        assert type(color) is str

        logger.debug(f"setting background to {color}")
        self._background = color

    def layout(self, name: str, layoutdef: LayoutDef):
        "Create a new layout for this card."
        assert Alignment(layoutdef.h_align)
        assert Alignment(layoutdef.v_align)

        logger.debug(f"creating layout area {name}")
        self._layouts[name] = {
            'x': layoutdef.x,
            'y': layoutdef.y,
            'width': layoutdef.width,
            'height': layoutdef.height,
            'h_align': layoutdef.h_align,
            'v_align': layoutdef.v_align,
            'scale': layoutdef.scale,
        }
    
    def layouts(self, names: Sequence[str], layoutdefs: Sequence[LayoutDef]):
        "Create multiple layouts for this card."
        assert len(names) == len(layoutdefs), "mismatched names/layoutdefs arguments"
        
        for name, layoutdef in zip(names, layoutdefs):
            self.layout(name, layoutdef)

    def layouts_map(self, layouts: Mapping[str, LayoutDef]):
        "Create multiple layouts from a dictionary."
        for name, layoutdef in layouts.items():
            self.layout(name, layoutdef)

    def text(self, text: str, layout: str, font: FreeTypeFont | None = None, color: Color | None = None):
        "Add text to this card."
        assert type(text) is str

        if layout in self._layouts:
            logger.debug(f"adding '{text}' in {layout}")
            self._commands.append({
                'op': _DrawCommand.TEXT,
                'layout': layout,
                'text': text,
                'font': font,
                'color': color,
            })
        else:
            raise KeyError(f"missing layout '{layout}'")

    def rectangle(self, layout: str, color: Color | None = None, thickness: Real | None = None):
        "Draw a rectangle on this card."
        if layout in self._layouts:
            logger.debug(f"adding rectangle for {layout}")
            self._commands.append({
                'op': _DrawCommand.RECTANGLE,
                'layout': layout,
                'color': color,
                'thickness': thickness,
                'filled': False,
            })
        else:
            raise KeyError(f"missing layout '{layout}'")

    def filled_rectangle(self, layout: str, color: Color):
        "Draw a filled rectangle on this card."
        if layout in self._layouts:
            logger.debug(f"adding rectangle for {layout}")
            self._commands.append({
                'op': _DrawCommand.RECTANGLE,
                'layout': layout,
                'color': color,
                'thickness': 1,
                'filled': True,
            })
        else:
            raise KeyError(f"missing layout '{layout}'")

    def image(self, image: Path, layout: str):
        "Draw an external image on this card."
        if layout in self._layouts:
            logger.debug(f"adding image for {layout}")
            self._commands.append({
                'op': _DrawCommand.IMAGE,
                'layout': layout,
                'image': image,
            })
        else:
            raise KeyError(f"missing layout '{layout}'")

    def render_png(self, filename: str):
        "Render this card as a PNG."
        logger.debug(f"rendering {filename}")

        with Image.new('RGBA', (self._width, self._height), self._background) as im:
            d = ImageDraw.Draw(im)

            for cmd in self._commands:
                op = cmd.pop('op')
                match op:
                    case _DrawCommand.TEXT:
                        self._render_png_text(d, **cmd)
                    case _DrawCommand.RECTANGLE:
                        self._render_png_rectangle(d, **cmd)
                    case _DrawCommand.IMAGE:
                        self._render_png_image(im, **cmd)
                    case _:
                        raise ValueError(cmd)

            im.save(filename)

    def _render_png_text(self, d, layout, text, color, font):
        logger.debug(f"rendering text '{text}' at {layout}")
        layout = self._layouts[layout]

        match layout['h_align']:
            case Alignment.BEGIN:
                anchor_h = 'l'
                x = layout['x']
            case Alignment.MIDDLE:
                anchor_h = 'm'
                x = layout['x'] + (layout['width'] // 2)
            case Alignment.END:
                anchor_h = 'r'
                x = layout['x'] + layout['width']
            case _:
                raise ValueError(f"h_align value '{layout['h_align']}' unrecognized")

        match layout['v_align']:
            case Alignment.BEGIN:
                y = layout['y']
                anchor_v = 'a'
            case Alignment.MIDDLE:
                y = layout['y'] + (layout['height'] // 2)
                anchor_v = 'm'
            case Alignment.END:
                y = layout['y'] + layout['height']
                anchor_v = 'd'
            case _:
                raise ValueError(f"v_align value '{layout['v_align']}' unrecognized")

        d.text(
            [x, y],
            text,
            fill=color if color else _DEFAULT_COLOR,
            font=font if font else _DEFAULT_FONT,
            anchor=f"{anchor_h}{anchor_v}",
        )
    
    def _render_png_rectangle(self, d, layout, color, thickness, filled):
        logger.debug(f"rendering rectangle on {layout}")
        layout = self._layouts[layout]
        d.rectangle(
            [
                layout['x'],
                layout['y'],
                layout['x'] + layout['width'],
                layout['y'] + layout['height'],
            ],
            fill=color if filled and color else None,
            outline=color if color else _DEFAULT_COLOR,
            width=thickness if thickness else _DEFAULT_THICKNESS,
        )

    def _render_png_image(self, im, layout, image):
        logger.debug(f"rendering image at {layout}")
        layout = self._layouts[layout]
        with Image.open(image) as art:
            # compute new image scale
            proposed_scale = self._pick_image_size(art.width, art.height, layout['width'], layout['height'])
            match layout['scale']:
                case Scale.FIT:
                    art = art.resize(proposed_scale)
                case Scale.UP:
                    if art.width < proposed_scale[0] or art.height < proposed_scale[1]:
                        art = art.resize(proposed_scale)
                case Scale.DOWN:
                    if art.width > proposed_scale[0] or art.height > proposed_scale[1]:
                        art = art.resize(proposed_scale)
                case Scale.NONE:
                    pass    # there is nothing to do
                case _:
                    raise ValueError(f"scale value '{layout['scale']}' unrecognized")

            match layout['h_align']:
                case Alignment.BEGIN:
                    left = layout['x']
                case Alignment.MIDDLE:
                    left = layout['x'] + (layout['width'] - art.width) // 2
                case Alignment.END:
                    left = layout['x'] + layout['width'] - art.width
                case _:
                    raise ValueError(f"h_align value '{layout['h_align']}' unrecognized")

            match layout['v_align']:
                case Alignment.BEGIN:
                    top = layout['y']
                case Alignment.MIDDLE:
                    top = layout['y'] + (layout['height'] - art.height) // 2
                case Alignment.END:
                    top = layout['y'] + layout['height'] - art.height
                case _:
                    raise ValueError(f"v_align value '{layout['v_align']}' unrecognized")

            im.alpha_composite(art, (left, top))

    def _pick_image_size(self, img_width, img_height, layout_width, layout_height):
        if img_width == layout_width and img_height == layout_height:
            return img_width, img_height
        
        # unpacking the logic below...
        #   ratio_width = image.width / layout.width
        #   ratio_height = image.height / layout.height
        #   if either ratio is > 1, we are shrinking, so pick the larger one to make sure we fit
        #   if both ratios are < 1, we are growing, so pick the one closer to 1 to maximally fill
        #   either way, we're picking the largest number to use as a scale factor

        scale_factor = max(img_width / layout_width, img_height / layout_height)
        new_width = math.floor(img_width / scale_factor)
        new_height = math.floor(img_height / scale_factor)
        
        return new_width, new_height
