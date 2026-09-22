import pytest

from hello import greeting, main


def test_greeting_default():
    assert greeting() == "Hello, World!"


def test_main_without_name_prints_world(capsys):
    main(["hello.py"])
    assert capsys.readouterr().out == "Hello, World!\n"


def test_main_joins_multiple_arguments(capsys):
    main(["hello.py", "Lê", "Cường"])
    assert capsys.readouterr().out == "Hello, Lê Cường!\n"


def test_main_empty_argument_falls_back_to_world(capsys):
    main(["hello.py", ""])
    assert capsys.readouterr().out == "Hello, World!\n"


def test_main_whitespace_only_arguments_fall_back_to_world(capsys):
    main(["hello.py", "", ""])
    assert capsys.readouterr().out == "Hello, World!\n"


@pytest.mark.parametrize("name", ["Cuong", "Lê Cường"])
def test_main_with_name_prints_name(capsys, name):
    main(["hello.py", name])
    assert capsys.readouterr().out == f"Hello, {name}!\n"
