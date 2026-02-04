#!/usr/bin/env python3
"""
Entry point for the interactive test runner.

This script allows developers to interactively trigger scenarios and observe
the actual behavior of various Glyph tools and functions.
"""

from test_runner.runner import TestRunner


def main():
    """Entry point for the test runner."""
    runner = TestRunner()
    runner.run()


if __name__ == "__main__":
    main()