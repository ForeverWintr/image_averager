import argparse
import pathlib
import sys

from PIL import Image
import numpy as np
from loguru import logger

# don't set up logging on import...
logger.disable(__name__)

VALID_LEVELS = ('TRACE', 'DEBUG', 'INFO', 'SUCCESS', 'WARNING', 'ERROR', 'CRITICAL')


def existing_directory(path: str):
    fullpath = pathlib.Path(path).absolute()
    if not fullpath.exists() or not fullpath.is_dir():
        raise argparse.ArgumentTypeError(fullpath)
    return fullpath


def abspath(path: str):
    return pathlib.Path(path).absolute()


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
    p.add_argument(
        '-o',
        '--output_file',
        help='Path to a file to store the results',
        type=abspath,
        default='averaged.png',
    )
    p.add_argument(
        '-l', '--log_level', help='Log verbosity', choices=VALID_LEVELS, default='CRITICAL'
    )

    return p


def iter_image_arrays(src_directory, glob):
    '''Yield numpy arrays of images'''
    for p in src_directory.glob(glob):
        image = Image.open(p)
        yield np.array(image)


def build_average_image(src_directory: pathlib.Path, glob='*.png') -> Image:
    # Using a python tuple here, because I'm not sure if there's a benefit to fitting these all in
    # a numpy array.
    all_arrays = tuple(iter_image_arrays(src_directory, glob))
    logger.info(f'averaging {len(all_arrays)} images.')
    average = np.mean(all_arrays, axis=0)
    result = Image.fromarray(average.astype(np.uint8))
    return result


def configure_logging(level: str):
    logger.remove()
    logger.enable(__name__)
    logger.add(sys.stderr, format="{level} {message}", filter=__name__, level=level)


def main(argv=None):
    p = get_arg_parser()
    args = p.parse_args(argv)

    configure_logging(args.log_level)

    result = build_average_image(args.src_directory)
    result.save(args.output_file)
    return 0


if __name__ == '__main__':
    sys.exit(main())
