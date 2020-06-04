import pathlib
import argparse
import shutil

import pytest

from src import image_averager


@pytest.fixture
def test_image_dir(tmpdir):
    test_images = pathlib.Path(__file__).parent / 'data' / 'test_images'
    target = pathlib.Path(tmpdir) / 'images'

    shutil.copytree(test_images, target)
    return target


def test_existing_directory(tmpdir):
    assert image_averager.existing_directory(str(tmpdir)) == pathlib.Path(tmpdir)
    with pytest.raises(argparse.ArgumentTypeError):
        image_averager.existing_directory('/not/a/path')


def test_build_average_image(test_image_dir, tmpdir):
    result = image_averager.build_average_image(test_image_dir)

    outpath = pathlib.Path(tmpdir) / 'result.png'
    result.save(outpath)
    assert 0
