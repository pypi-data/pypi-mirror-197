import os
import random
import logging

from PIL import Image, ImageDraw, ImageFont
from torchvision import transforms


logger = logging.getLogger(__name__)


class SimpleRandomWordGenerator:
    def __init__(self, word_sampler, font_dir, font_size_range=(64, 64),
                 bg_range=(240, 255), color_range=(0, 15), stroke_width_range=(0, 2),
                 stroke_fill_range=(0, 15), rotation_range=(0, 0), spaces_range=(0, 2)):
        self.sampler = word_sampler
        self.font_dir = font_dir
        self.font_files = [os.path.join(font_dir, font_file) for font_file in os.listdir(font_dir)
                           if font_file.endswith('.otf') or font_file.endswith('.ttf')]

        self.font_size_range = font_size_range
        self.bg_range = bg_range
        self.color_range = color_range
        self.stroke_width_range = stroke_width_range
        self.stroke_fill_range = stroke_fill_range
        self.rotation_range = rotation_range
        self.spaces_range = spaces_range

    def __iter__(self):
        while True:
            word = self.sampler()

            font_size = random.randint(*self.font_size_range)
            font_file = random.choice(self.font_files)
            font = ImageFont.truetype(font_file, size=font_size)

            background = random.randint(*self.bg_range)
            color = random.randint(*self.color_range)
            stroke_fill = random.randint(*self.stroke_fill_range)
            stroke_width = random.randint(*self.stroke_width_range)
            num_spaces = random.randint(*self.spaces_range)

            word_with_spaces = add_spacing(word, num_spaces)
            try:
                image = self.create_image(word_with_spaces, font, font_size,
                                          background=background, color=color,
                                          stroke_width=stroke_width, stroke_fill=stroke_fill)
                if image.height > 0 and image.width > 0:
                    yield image, word
            except Exception:
                msg = 'Failed to create image for "{}": font "{}", font size {}, ' \
                      'background {}, color {}, stroke width {}, stroke fill {}, # spaces {}'

                # todo: this is wrong when using extra worker processes in dataloader
                logger.exception(msg.format(
                    word, font_file, font_size, background, color,
                    stroke_width, stroke_fill, num_spaces
                ))

    def create_image(self, word, font, size=64, background=255, color=0,
                     stroke_width=1, stroke_fill=0):
        padding = stroke_width
        char_size = size
        num_chars = len(word)
        width = char_size * num_chars + padding * 2

        vertical_offset = 25
        height = size * 2 + 20 + padding * 2 + vertical_offset * 2

        min_degrees, max_degrees = self.rotation_range
        rotate = transforms.RandomRotation(degrees=[min_degrees, max_degrees], expand=True, fill=background)

        with Image.new("L", (width, height)) as image:
            draw = ImageDraw.Draw(image)

            # give extra vertical space (at least 25 pixels from top and bottom)
            bbox = draw.textbbox((padding, vertical_offset), word, font=font)
            draw.rectangle((0, 0, image.width, image.height), fill=background)
            draw.text((padding, vertical_offset), word, fill=color, font=font,
                      stroke_width=stroke_width, stroke_fill=stroke_fill)

            x0, y0, x, y = bbox
            padded_bbox = (max(0, x0 - padding),
                           max(0, y0 - padding),
                           min(width, x + padding),
                           min(height, y + padding))

            shear_x = transforms.RandomAffine(0, shear=(-10, 30), fill=background)

            image = image.crop(padded_bbox)
            image = shear_x(image)

            if self.rotation_range != (0, 0):
                image = rotate(image)
            return image


def add_spacing(s, n=0, space=0x202F):
    narrow_space = chr(space) * n
    return narrow_space.join(s)
