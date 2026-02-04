"""
Markdown processing test scenarios.

This module contains scenarios for testing markdown parsing functionality.
"""

import os
import sys
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from tools.md_to_dict import md_to_dict
from test_runner.scenarios.base import BaseScenario


class MdToDictSuccessScenario(BaseScenario):
    """Scenario 14: Parse a markdown file into a hierarchical dictionary."""
    
    def run(self):
        self.print_header(
            14,
            "Markdown to Dictionary - Success",
            "Parsing a markdown file into a hierarchical dictionary structure."
        )
        
        test_md_path = os.path.join(self.env.temp_dir, "test_doc.md")
        
        print(f"\nMarkdown file: {test_md_path}")
        print("Calling: md_to_dict(file_path)")
        
        response = md_to_dict(test_md_path)
        
        self.print_result("Response Object", str(response.model_dump()))
        
        if response.success and response.result:
            print("\nParsed structure (formatted):")
            print(json.dumps(response.result, indent=2))


class MdToDictFileNotFoundScenario(BaseScenario):
    """Scenario 15: Parse a non-existent markdown file."""
    
    def run(self):
        self.print_header(
            15,
            "Markdown to Dictionary - File Not Found",
            "Attempting to parse a markdown file that doesn't exist."
        )
        
        fake_path = os.path.join(self.env.temp_dir, "nonexistent.md")
        
        print(f"\nMarkdown file: {fake_path}")
        print("Calling: md_to_dict(file_path)")
        
        response = md_to_dict(fake_path)
        
        self.print_result("Response Object", str(response.model_dump()))