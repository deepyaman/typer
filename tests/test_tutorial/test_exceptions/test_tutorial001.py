import os
import subprocess
from pathlib import Path

from typer.testing import CliRunner

from docs_src.exceptions import tutorial001 as mod

runner = CliRunner()


def test_traceback_rich():
    file_path = Path(mod.__file__)
    result = subprocess.run(
        ["coverage", "run", str(file_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={**os.environ, "_TYPER_STANDARD_TRACEBACK": ""},
    )
    assert "return get_command(self)(*args, **kwargs)" not in result.stderr

    assert "typer.run(main)" not in result.stderr
    assert "print(name + 3)" in result.stderr

    # TODO: when deprecating Python 3.6, remove second option
    assert (
        'TypeError: can only concatenate str (not "int") to str' in result.stderr
        or "TypeError: must be str, not int" in result.stderr
    )
    assert "name = 'morty'" in result.stderr


def test_standard_traceback_env_var():
    file_path = Path(mod.__file__)
    result = subprocess.run(
        ["coverage", "run", str(file_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={**os.environ, "_TYPER_STANDARD_TRACEBACK": "1"},
    )
    assert "return get_command(self)(*args, **kwargs)" in result.stderr

    assert "typer.run(main)" in result.stderr
    assert "print(name + 3)" in result.stderr

    # TODO: when deprecating Python 3.6, remove second option
    assert (
        'TypeError: can only concatenate str (not "int") to str' in result.stderr
        or "TypeError: must be str, not int" in result.stderr
    )
    assert "name = 'morty'" not in result.stderr


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
