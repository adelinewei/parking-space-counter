from src.hello_world import say_hello_world


def test_say_hello_world() -> None:
    assert say_hello_world() == "Hello world!"
