"""
Utility functions for the test runner.

This module provides shared formatting and printing utilities used across scenarios.
"""


def print_scenario_header(number, title, description):
    """Print a formatted scenario header."""
    print("\n" + "="*80)
    print(f"SCENARIO {number}: {title}")
    print("="*80)
    print(f"Description: {description}")
    print("-"*80)


def print_result(result_label, result_data):
    """Print formatted result."""
    print(f"\n{result_label}:")
    print("-"*80)
    print(result_data)
    print("-"*80)


def print_observation(message):
    """Print a formatted observation message."""
    print("\n" + "!"*80)
    print(f"OBSERVATION: {message}")
    print("!"*80)


def print_section_header(title):
    """Print a section header."""
    print("\n" + "="*80)
    print(title)
    print("="*80)