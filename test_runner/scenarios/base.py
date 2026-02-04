"""
Base class for test scenarios.

This module provides the base scenario class with shared functionality.
"""

from test_runner.utils import print_scenario_header, print_result


class BaseScenario:
    """Base class for all test scenarios."""
    
    def __init__(self, env):
        """
        Initialize the scenario with the test environment.
        
        Args:
            env: TestEnvironment instance providing access to test directories.
        """
        self.env = env
    
    def print_header(self, number, title, description):
        """Print the scenario header."""
        print_scenario_header(number, title, description)
    
    def print_result(self, result_label, result_data):
        """Print formatted result."""
        print_result(result_label, result_data)
    
    def run(self):
        """
        Run the scenario.
        
        Subclasses must implement this method.
        """
        raise NotImplementedError("Subclasses must implement run()")