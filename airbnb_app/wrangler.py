import os
from time import time
from skimage import io, img_as_ubyte, color
from skimage.transform import resize


def wrangle_image(orig_dir, new_dir):
    image = resize(io.imread(orig_dir), (180, 240), mode='constant',
                   anti_aliasing=True)

    if len(image.shape) < 3:
        image = color.grey2rgb(image)
    elif image.shape[2] == 4:
        image = color.rgba2rgb(image)

    new_name = 'im' + str(int(time()))[-5:] + '.jpg'
    io.imsave(os.path.join(new_dir, new_name), img_as_ubyte(image))
    os.remove(orig_dir)

    return new_name, image
