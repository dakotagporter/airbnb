import os
from skimage import io, img_as_ubyte, color
from skimage.transform import resize

def wrangle_image(orig_dir, new_dir):
    image = resize(io.imread(orig_dir), (180,240), mode='constant', anti_aliasing=True)

    if len(image.shape) < 3:
        image = color.grey2rgb(image)
    elif image.shape[2] == 4:
        image = color.rgba2rgb(image)

    io.imsave(os.path.join(new_dir, 'test.jpg'), img_as_ubyte(image))
    # io.imsave(f'{new_dir}/test.jpg', img_as_ubyte(image))