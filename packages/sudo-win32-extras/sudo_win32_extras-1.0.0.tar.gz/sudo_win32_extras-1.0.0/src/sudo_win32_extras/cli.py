"""
Main entry point.
"""

import subprocess
import sys


def main() -> int:
    """Main entry point for the template_python_cmd package."""
    return subprocess.call(["sudo_win32"] + sys.argv[1:])
