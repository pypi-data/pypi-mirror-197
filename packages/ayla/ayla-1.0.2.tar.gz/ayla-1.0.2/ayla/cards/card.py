"""
kuuhaku v1.0
Copyright (c) 2023 KuuhakuTeam

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


import uuid

from ..errors import InvalidCharacteres

from io import BytesIO
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

class RankCard:

    def __init__(
        self,
        pfp: str,
        background: str,
        nickname: str,
        level: int,
        current_xp: int,
        xp_max: int,
        text_color: str,
        bar_color: str
    ) -> None:
        self.pfp = pfp
        self.bg = background
        self.nickname = nickname
        self.level = level
        self.current_xp = current_xp
        self.xp_max = xp_max
        self.text_color = text_color
        self.bar_color = bar_color

    def card1(self):
        try:
            # things
            path = str(Path(__file__).parent)
            avatar = Image.open(self.pfp)
            avatar = avatar.resize((170, 170))
            bg = Image.open(self.bg)
            overlay = Image.open(path + "/assets/overlay1.png")
            background = Image.new("RGBA", overlay.size)
            backgroundover = bg.resize((638, 159))
            background.paste(backgroundover, (0, 0))
            bg = background.resize(overlay.size)
            bg.paste(overlay, (0, 0), overlay)
            myFont = ImageFont.truetype(path + "/assets/fonts/levelfont.otf", 40)            
            draw = ImageDraw.Draw(bg)

            # draw nickname
            draw.text((205, (327/2)+20), self.nickname, font=myFont,
                    fill=self.text_color, stroke_width=1, stroke_fill=(0, 0, 0))
            
            # draw xp
            bar_exp = (self.current_xp/self.xp_max)*420
            if bar_exp <= 50:
                bar_exp = 50
            current_exp = _convert_number(self.current_xp)
            max_exp = _convert_number(self.xp_max)
            myFont = ImageFont.truetype(path + "/assets/fonts/levelfont.otf", 30)

            # draw level
            draw.text((197, (327/2)+125), f"LEVEL - {self.level}",
                    font=myFont, fill=self.text_color, stroke_width=1, stroke_fill=(0, 0, 0))
            w, _ = draw.textsize(f"{current_exp}/{max_exp}", font=myFont)
            draw.text((638-w-50, (327/2)+125), f"{current_exp}/{max_exp}",
                    font=myFont, fill=self.text_color, stroke_width=1, stroke_fill=(0, 0, 0))
            
            # draw avatar
            mask_im = Image.open(
                path + "/assets/mask_circle.jpg").convert('L').resize((170, 170))
            new = Image.new("RGB", avatar.size, (0, 0, 0))
            try:
                new.paste(avatar, mask=avatar.convert("RGBA").split()[3])
            except Exception as e:
                print(e)
                new.paste(avatar, (0, 0))
            bg.paste(new, (13, 65), mask_im)

            im = Image.new("RGB", (490, 51), (0, 0, 0))
            draw = ImageDraw.Draw(im, "RGBA")
            draw.rounded_rectangle((0, 0, 420, 50), 30, fill=(255, 255, 255, 50))
            draw.rounded_rectangle((0, 0, bar_exp, 50), 30, fill=self.bar_color)
            bg.paste(im, (190, 235))
            new = Image.new("RGBA", bg.size)
            new.paste(bg, (0, 0), Image.open(path + "/assets/curvedoverlay.png").convert("L"))
            bg = new.resize((505, 259))

            final_img = str(uuid.uuid4()) + ".png"
            image = BytesIO()
            bg.save(final_img, 'png')
            image.seek(0)
            return final_img
        except UnicodeEncodeError:
            raise InvalidCharacteres("Failed to encode characters")

    def card2(self):
        try:
            # things
            path = str(Path(__file__).parent)
            avatar = Image.open(self.pfp)
            bg = Image.open(self.bg)

            # background
            W, H = (1000, 333)
            bg = bg.filter(ImageFilter.BLUR)
            background = bg.resize((1000, 333))
            position = (420, 30)
            avatar = avatar.resize((160, 160))
            mask = Image.open(path + "/assets/mask_circle.jpg").resize((160, 160))
            new = Image.new("RGBA", avatar.size, (0, 0, 0))
            try:
                new.paste(avatar, mask=avatar.convert("RGBA").split()[3])
            except:
                new.paste(avatar, (0, 0))
            background.paste(new, position, mask.convert("L"))

            # init
            draw = ImageDraw.Draw(background)
            myFont = ImageFont.truetype(path + "/assets/fonts/rabbit.ttf", 50)
            xp_level_font = ImageFont.truetype(path + "/assets/fonts/rabbit.ttf", 25)

            # draw level
            combined = f"LEVEL: {self.level}"
            draw.text((380, 250), combined, font=xp_level_font,
                    fill=self.text_color, stroke_width=1, stroke_fill=(0, 0, 0))

            # draw nickname
            w, h = draw.textsize(self.nickname)
            draw.text((((W-w)-w*2.5)/2, 180), f"{self.nickname}", font=myFont,
                    fill=self.text_color, stroke_width=1, stroke_fill=(0, 0, 0))

            # draw xp
            exp = f"{_convert_number(self.current_xp)}/{_convert_number(self.xp_max)}"
            draw.text((520, 250), exp, font=xp_level_font,
                    fill=self.text_color, stroke_width=1, stroke_fill=(0, 0, 0))

            bar_exp = (self.current_xp/self.xp_max) * 420
            if bar_exp <= 50:
                bar_exp = 50

            # draw xp bar
            im = Image.new("RGBA", (421, 26))
            draw = ImageDraw.Draw(im, "RGBA")
            draw.rounded_rectangle((0, 0, 420, 25), 30, fill=(255, 255, 255, 50))
            draw.rounded_rectangle((0, 0, bar_exp, 25), 30, fill=self.bar_color)
            background.paste(im, (290, 280), im)
            final_img = str(uuid.uuid4()) + ".png"
            image = BytesIO()
            background.save(final_img, 'png')
            image.seek(0)
            return final_img
        except UnicodeEncodeError:
            raise InvalidCharacteres("Failed to encode characters")


    def card3(self):
        try:
            # things
            path = str(Path(__file__).parent)
            avatar = Image.open(self.pfp)
            bg = Image.open(self.bg)

            # background
            background = bg.filter(ImageFilter.BLUR)
            background = bg.resize((1000, 333))
            avatar = avatar.resize((210, 210))
            mask = Image.open(path + "/assets/mask_circle.jpg").resize((210, 210))
            new = Image.new("RGBA", avatar.size, (0, 0, 0))
            try:
                new.paste(avatar, mask=avatar.convert("RGBA").split()[3])
            except:
                new.paste(avatar, (0, 0))
            background.paste(new, (655, 115//2), mask.convert("L"))

            # fonts
            myFont = ImageFont.truetype(path + "/assets/fonts/rabbit.ttf", 80)
            xp_level_font = ImageFont.truetype(path + "/assets/fonts/rabbit.ttf", 25)

            # init
            draw = ImageDraw.Draw(background)

            # draw level
            combined = f"LEVEL: {self.level}"
            w = draw.textlength(combined, font=xp_level_font)
            draw.text((515, 205), combined, font=xp_level_font,
                    fill=self.text_color, stroke_width=1, stroke_fill=(0, 0, 0))

            # draw nickname
            draw.text((70, 80), f"{self.nickname}", font=myFont,
                    fill=self.text_color, stroke_width=1, stroke_fill=(0, 0, 0))

            # draw xp
            exp = f"{_convert_number(self.current_xp)}/{_convert_number(self.xp_max)}"
            w = draw.textlength(exp, font=xp_level_font)
            draw.text((80, 205), exp, font=xp_level_font, fill=self.text_color,
                    stroke_width=1, stroke_fill=(0, 0, 0))
            bar_exp = (self.current_xp/self.xp_max) * 549
            if bar_exp <= 50:
                bar_exp = 50

            # draw xp bar
            im = Image.new("RGBA", (550, 26))
            draw = ImageDraw.Draw(im, "RGBA")
            draw.rectangle((0, 0, 549, 25), fill=(255, 255, 255, 225))
            draw.rectangle((0, 0, bar_exp, 35), fill=self.bar_color)
            background.paste(im, (80, 245))
            final_img = str(uuid.uuid4()) + ".png"
            image = BytesIO()
            background.save(final_img, 'png')
            image.seek(0)
            return final_img
        except UnicodeEncodeError:
            raise InvalidCharacteres("Failed to encode characters")


def _convert_number(number: int) -> str:
    if number >= 1000000000:
        return f"{number / 1000000000:.1f}B"
    elif number >= 1000000:
        return f"{number / 1000000:.1f}M"
    elif number >= 1000:
        return f"{number / 1000:.1f}K"
    else:
        return str(number)
