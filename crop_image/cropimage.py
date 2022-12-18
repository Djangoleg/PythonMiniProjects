import os
from pathlib import Path

from PIL import Image

if __name__ == '__main__':
    image_path = Path(os.path.join('img', "dog_photo.jpg"))
    image = Image.open(image_path.absolute())

    width, height = image.size  # Get dimensions
    new_width = 600
    new_height = 600

    left = (width - new_width) / 2
    top = (height - new_height) / 2
    right = (width + new_width) / 2
    bottom = (height + new_height) / 2

    area = (left, top, right, bottom)
    img = image.crop(area)

    new_img = os.path.join(os.path.dirname(image_path), image_path.stem + '_crop' + image_path.suffix)
    img.save(Path(new_img).absolute())
