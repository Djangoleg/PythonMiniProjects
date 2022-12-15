import os
from pathlib import Path

from PIL import Image


def crop_image(image_path, area):
    image_file = Path(image_path)
    image = Image.open(image_file.absolute())
    img = image.crop(area)
    new_img = os.path.join(os.path.dirname(image_file), image_file.stem + '_crop' + image_file.suffix)
    img.save(Path(new_img).absolute())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    area = (300, 300, 700, 700)
    image_path = os.path.join('img', "dog_photo2.jpg")
    crop_image(image_path, area)


