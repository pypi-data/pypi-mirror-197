import pytest

from poc_package.skeleton import fibby, main

__author__ = "timothestes"
__copyright__ = "timothestes"
__license__ = "MIT"


def test_fib():
    """API Tests"""
    assert fibby(1) == 1
    assert fibby(2) == 1
    assert fibby(7) == 13
    with pytest.raises(AssertionError):
        fibby(-10)


def test_main(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts against stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(["7"])
    captured = capsys.readouterr()
    assert "The 7-th Fibonacci number is 13" in captured.out
