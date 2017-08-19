from .base import Base
from PIL import Image, ImageFont, ImageDraw


class Vzhuh(Base):
    name = 'vzhuh'
    path = 'storage/vzhuh.png'

    def execute(self, command):
        text = self.__format_text('вжух ' + ' '.join(command.args))
        self.__generate_image(text)

        self.send_photo(command, photo=open(self.path, 'rb'))

    def __format_text(self, text):
        result = []
        current_part = ''
        if len(text) > 8:
            parts = text.upper().split(' ')
            for part in parts:
                if len(current_part) + len(part) <= 10:
                    current_part += part + ' '
                else:
                    result.append(current_part)
                    result.append(part)
                    current_part = ''
            result.append(current_part)
        else:
            result.append(text)

        return '\n'.join(result)

    def __generate_image(self, text):
        img = Image.open("resources/vzhuh/sample.png")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('resources/vzhuh/Impact.ttf', 44, index=0)
        draw.text((222, 280), text, (0, 0, 0), font=font)
        img.save(self.path)
