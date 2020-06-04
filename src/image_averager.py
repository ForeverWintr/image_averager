import argparse
import pathlib

from PIL import Image
import numpy as np


def existing_directory(path: str):
    fullpath = pathlib.Path(path).absolute()
    if not fullpath.exists() or not fullpath.is_dir():
        raise argparse.ArgumentTypeError(fullpath)
    return fullpath


def get_arg_parser():
    p = argparse.ArgumentParser(description='Averages images in a directory')
    p.add_argument(
        '-s',
        '--src_directory',
        help='src directory containing images',
        type=existing_directory,
        default='.',
        required=False,
    )
    return p


def iter_image_arrays(src_directory, glob):
    '''Yield numpy arrays of images'''
    for p in src_directory.glob(glob):
        image = Image.open(p)
        yield np.array(image)


def build_average_image(src_directory: pathlib.Path, glob='*.png') -> Image:
    # Using a python tuple here, because I'm not sure if there's a benefit to fitting these all in
    # a numpy array
    all_arrays = tuple(iter_image_arrays(src_directory, glob))
    average = np.mean(all_arrays, axis=0)
    result = Image.fromarray(average.astype(np.uint8))
    return result


def main(argv=None):
    p = get_arg_parser()
    p.parse_args(argv)


if __name__ == '__main__':
    main()
