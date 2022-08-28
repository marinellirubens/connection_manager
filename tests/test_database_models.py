import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from database import utils


def test_pactical_test():
    print(utils.ServerTypeEnum.LINUX)
    assert 2 == 2
