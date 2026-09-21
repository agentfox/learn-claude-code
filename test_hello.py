import pytest

from hello import greeting, main


def test_greeting_default():
    assert greeting() == "Hello, World!"


def test_main_without_name_prints_world(capsys):
    main(["hello.py"])
    assert capsys.readouterr().out == "Hello, World!\n"


@pytest.mark.parametrize("name", ["Cuong", "Lê Cường"])
def test_main_with_name_prints_name(capsys, name):
    main(["hello.py", name])
    assert capsys.readouterr().out == f"Hello, {name}!\n"
