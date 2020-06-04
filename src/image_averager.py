import argparse
import pathlib


def existing_directory(path: str):
    fullpath = pathlib.Path(path).absolute()
    if not fullpath.exists():
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


def main(argv=None):
    p = get_arg_parser()
    p.parse_args(argv)


if __name__ == '__main__':
    main()
