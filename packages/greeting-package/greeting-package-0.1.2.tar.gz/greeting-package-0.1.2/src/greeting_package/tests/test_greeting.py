from greeting_package.greeting import say_hello


def test_say_hello():
    name = "John"
    expected_output = "Hello, John!"
    assert say_hello(name) == expected_output
