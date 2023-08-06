"""Tests for the Python formatters."""

from textwrap import dedent

from markdown import Markdown


def test_output_markdown(md: Markdown) -> None:
    """Assert Markdown is converted to HTML.

    Parameters:
        md: A Markdown instance (fixture).
    """
    html = md.convert(
        dedent(
            """
            ```python exec="yes"
            print("**Bold!**")
            ```
            """
        )
    )
    assert html == "<p><strong>Bold!</strong></p>"


def test_output_html(md: Markdown) -> None:
    """Assert HTML is injected as is.

    Parameters:
        md: A Markdown instance (fixture).
    """
    html = md.convert(
        dedent(
            """
            ```python exec="yes" html="yes"
            print("**Bold!**")
            ```
            """
        )
    )
    assert html == "<p>**Bold!**\n</p>"


def test_error_raised(md: Markdown, caplog) -> None:
    """Assert errors properly log a warning and return a formatted traceback.

    Parameters:
        md: A Markdown instance (fixture).
        caplog: Pytest fixture to capture logs.
    """
    html = md.convert(
        dedent(
            """
            ```python exec="yes"
            raise ValueError("oh no!")
            ```
            """
        )
    )
    assert "Traceback" in html
    assert "ValueError" in html
    assert "oh no!" in html
    assert "Execution of python code block exited with errors" in caplog.text


def test_can_print_non_string_objects(md: Markdown) -> None:
    """Assert we can print non-string objects.

    Parameters:
        md: A Markdown instance (fixture).
    """
    html = md.convert(
        dedent(
            """
            ```python exec="yes"
            class NonString:
                def __str__(self):
                    return "string"

            nonstring = NonString()
            print(nonstring, nonstring)
            ```
            """
        )
    )
    assert "Traceback" not in html


def test_sessions(md: Markdown) -> None:
    """Assert sessions can be reused.

    Parameters:
        md: A Markdown instance (fixture).
    """
    html = md.convert(
        dedent(
            """
            ```python exec="1" session="a"
            a = 1
            ```

            ```pycon exec="1" session="b"
            >>> b = 2
            ```

            ```pycon exec="1" session="a"
            >>> print(f"a = {a}")
            >>> try:
            ...     print(b)
            ... except NameError:
            ...     print("ok")
            ... else:
            ...     print("ko")
            ```

            ```python exec="1" session="b"
            print(f"b = {b}")
            try:
                print(a)
            except NameError:
                print("ok")
            else:
                print("ko")
            ```
            """
        )
    )
    assert "a = 1" in html
    assert "b = 2" in html
    assert "ok" in html
    assert "ko" not in html
