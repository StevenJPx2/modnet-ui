import argparse
import os
import sys
from io import BytesIO

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
from PIL import Image

from .modnet.src.models.modnet import MODNet

REF_SIZE = 512


def setup_modnet(ckpt_path: str):

    # define image to tensor transform
    im_transform = transforms.Compose(
        [transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]
    )

    # create MODNet and load the pre-trained ckpt
    modnet = MODNet(backbone_pretrained=False)
    modnet = nn.DataParallel(modnet)

    if torch.cuda.is_available():
        modnet = modnet.cuda()
        weights = torch.load(ckpt_path)
    else:
        weights = torch.load(ckpt_path, map_location=torch.device("cpu"))
    modnet.load_state_dict(weights)
    modnet.eval()

    return im_transform, modnet


def generate_foreground(image_io: Image.Image, matte_io: Image.Image):
    # obtain predicted foreground
    image = np.asarray(image_io)
    if len(image.shape) == 2:
        image = image[:, :, None]
    if image.shape[2] == 1:
        image = np.repeat(image, 3, axis=2)
    elif image.shape[2] == 4:
        image = image[:, :, 0:3]
    matte = np.repeat(np.asarray(matte_io)[:, :, None], 3, axis=2) / 255
    return image * matte + np.full(image.shape, 255) * (1 - matte)


def process_image(
    buffer: bytes,
    im_transform: transforms.Compose,
    modnet: MODNet | nn.DataParallel,
):

    # read image
    image = Image.open(BytesIO(buffer))

    # unify image channels to 3
    im = np.asarray(image)
    if len(im.shape) == 2:
        im = im[:, :, None]
    if im.shape[2] == 1:
        im = np.repeat(im, 3, axis=2)
    elif im.shape[2] == 4:
        im = im[:, :, 0:3]

    # convert image to PyTorch tensor
    im = Image.fromarray(im)
    im = im_transform(im)

    # add mini-batch dim
    im = im[None, :, :, :]

    # resize image for input
    im_b, im_c, im_h, im_w = im.shape
    if max(im_h, im_w) < REF_SIZE or min(im_h, im_w) > REF_SIZE:
        if im_w >= im_h:
            im_rh = REF_SIZE
            im_rw = int(im_w / im_h * REF_SIZE)
        elif im_w < im_h:
            im_rw = REF_SIZE
            im_rh = int(im_h / im_w * REF_SIZE)
    else:
        im_rh = im_h
        im_rw = im_w

    im_rw = im_rw - im_rw % 32
    im_rh = im_rh - im_rh % 32
    im = F.interpolate(im, size=(im_rh, im_rw), mode="area")

    # inference
    _, _, matte = modnet(im.cuda() if torch.cuda.is_available() else im, True)

    # resize and save matte
    matte = F.interpolate(matte, size=(im_h, im_w), mode="area")
    matte = matte[0][0].data.cpu().numpy()
    matte = Image.fromarray(((matte * 255).astype("uint8")), mode="L")

    return Image.fromarray(np.uint8(generate_foreground(image, matte)))


def process_images_from_path(
    input_path: str,
    output_path: str,
    ckpt_path: str = "modnet/modnet/pretrained/modnet_photographic_portrait_matting.ckpt",
):

    input_path = os.path.expanduser(input_path)
    output_path = os.path.expanduser(output_path)
    ckpt_path = os.path.abspath(ckpt_path)

    # check input arguments
    if not os.path.exists(input_path):
        print("Cannot find input path: {0}".format(input_path))
        exit()
    if not os.path.exists(output_path):
        print("Cannot find output path: {0}".format(output_path))
        exit()
    if not os.path.exists(ckpt_path):
        print("Cannot find ckpt path: {0}".format(ckpt_path))
        exit()

    im_transform, modnet = setup_modnet(ckpt_path)

    # inference images
    im_names = os.listdir(input_path)
    for im_name in im_names:
        file = open(os.path.join(input_path, im_name), "rb").read()
        output_name = im_name.split(".")[0] + ".png"
        print(f"Processing image {im_name}")
        process_image(file, im_transform, modnet).save(
            os.path.join(output_path, output_name)
        )


if __name__ == "__main__":
    # define cmd arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-path", type=str, help="path of input images")
    parser.add_argument("--output-path", type=str, help="path of output images")
    parser.add_argument("--ckpt-path", type=str, help="path of pre-trained MODNet")
    args = parser.parse_args()

    process_images_from_path(args.input_path, args.output_path)
