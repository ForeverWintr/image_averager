import pathlib
import argparse

import pytest

from src import image_averager


def test_existing_directory(tmpdir):
    assert image_averager.existing_directory(str(tmpdir)) == pathlib.Path(tmpdir)
    with pytest.raises(argparse.ArgumentTypeError):
        image_averager.existing_directory('/not/a/path')
