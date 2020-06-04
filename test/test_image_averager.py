import pathlib
import argparse
import shutil

import pytest
import numpy as np
from PIL import Image

from src import image_averager


@pytest.fixture
def test_image_dir(tmpdir):
    test_images = pathlib.Path(__file__).parent / 'data' / 'test_images'
    target = pathlib.Path(tmpdir) / 'images'

    shutil.copytree(test_images, target)
    return target


@pytest.fixture
def averaged_image():
    return pathlib.Path(__file__).parent / 'data' / 'expected_result.png'


def test_existing_directory(tmpdir):
    assert image_averager.existing_directory(str(tmpdir)) == pathlib.Path(tmpdir)
    with pytest.raises(argparse.ArgumentTypeError):
        image_averager.existing_directory('/not/a/path')


def test_build_average_image(test_image_dir, tmpdir, averaged_image):
    result = image_averager.build_average_image(test_image_dir)

    # outpath = pathlib.Path(tmpdir) / 'result.png'
    # result.save(outpath)

    expected = np.array(Image.open(averaged_image))
    np.testing.assert_array_equal(expected, np.array(result))


def test_cli(test_image_dir, tmpdir, capsys):
    outpath = pathlib.Path(tmpdir / "result.png")
    args = f'-s {test_image_dir} -o {outpath} -l{"DEBUG"}'
    image_averager.main(args.split())

    out, err = capsys.readouterr()
    assert not out
    assert err == 'INFO averaging 3 images.\n'
    assert outpath.exists()
