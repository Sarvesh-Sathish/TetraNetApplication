import requests
from PIL import Image
import numpy as np


def get_mask(image_dir, name='mask_frame', testing=False):

    image_dir = ''

    if (not testing):
        image_dir = 'uploads/images/test.png'
    else:
        image_dir = 'image_dir'

    img = Image.open(image_dir)
    original_size = img.size

    files = {'image': open(image_dir, 'rb').read()}

    requests.get('http://67515655-f00a-44a0-a447-22a76351d991.eastus.azurecontainer.io/score')
    response = requests.post('http://67515655-f00a-44a0-a447-22a76351d991.eastus.azurecontainer.io/score', files=files)

    new_img = response.json()
    new_img = np.array(new_img, dtype='uint8')
    new_img = new_img * 255
    new_img = Image.fromarray(new_img)

    saved_file_dir = 'uploads/images/' + name + '.png'

    new_img.save(saved_file_dir)

    return saved_file_dir, original_size



