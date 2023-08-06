"""
Unit test file.
"""
import unittest

# flake8: noqa: F401
# pylint: disable=unused-import,missing-docstring,too-few-public-methods,import-outside-toplevel,useless-return


class MainTester(unittest.TestCase):
    """Main tester class."""

    def test_imports(self) -> None:
        """Test command line interface (CLI)."""
        # Just make sure the imports work
        from sudo_win32 import cli  # pylint: disable=unused-import

        return


if __name__ == "__main__":
    unittest.main()
