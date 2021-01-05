import os
from time import time
import numpy as np
from skimage import io, img_as_ubyte, color
from skimage.transform import resize
from tensorflow.keras.models import load_model

from .stuff import AMENITIES

model_path = 'savedmodel/savedmodel'
model = load_model(model_path)

def wrangle_image(orig_dir, new_dir):
    image = resize(io.imread(orig_dir), (180, 240), mode='constant',
                   anti_aliasing=True)

    if len(image.shape) < 3:
        image = color.grey2rgb(image)
    elif image.shape[2] == 4:
        image = color.rgba2rgb(image)

    new_name = 'im' + str(int(time()))[-5:] + '.jpg'
    new_path = os.path.join(new_dir, new_name)
    io.imsave(new_path, img_as_ubyte(image))
    os.remove(orig_dir)

    return new_path


def encode_amens(input_amens):
    encoded = []
    for amen in AMENITIES:
        encoded.append(1 if amen in input_amens else 0)
    return np.array(encoded)

def encode_im(path):
    image = io.imread(path)
    return np.array(image)/255


def predict(im_path, amens):
    im = np.expand_dims(encode_im(im_path), axis=0)
    am = np.expand_dims(encode_amens(amens), axis=0)

    pred = model.predict([im, am])
    return '$' + str(pred[0][0].round(2))