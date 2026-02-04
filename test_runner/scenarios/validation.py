"""
Input validation test scenarios.

This module contains scenarios for testing input validation.
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from tools.init_assistant_dir import init_assistant_dir
from test_runner.scenarios.base import BaseScenario
from test_runner.utils import print_observation


class InvalidAbsolutePathScenario(BaseScenario):
    """Scenario 19: Test with invalid (relative) path - validation check."""
    
    def run(self):
        self.print_header(
            19,
            "Invalid Path Validation",
            "Attempting to use a tool with a relative path instead of absolute path."
        )
        
        print("\nCalling: init_assistant_dir(abs_path='./relative/path', overwrite=False)")
        
        response = init_assistant_dir("./relative/path", False)
        
        self.print_result("Response Object", str(response.model_dump()))
        
        print_observation(
            "The system validates paths and provides clear error messages\n"
            "about the requirement for absolute paths."
        )