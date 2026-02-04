"""
Operation document test scenarios.

This module contains scenarios for testing operation document functionality.
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from tools.add_operation import add_operation
from tools.init_assistant_dir import init_assistant_dir
from test_runner.scenarios.base import BaseScenario


class AddOperationSuccessScenario(BaseScenario):
    """Scenario 11: Add an operation document - success."""
    
    def run(self):
        self.print_header(
            11,
            "Add Operation Document - Success",
            "Creating a new operation document in an initialized project."
        )
        
        op_project = os.path.join(self.env.temp_dir, "op_project")
        os.makedirs(op_project)
        init_assistant_dir(op_project, False)
        
        print(f"\nProject directory: {op_project}")
        print("Calling: add_operation(abs_path=project_path, title='Database Migration')")
        
        response = add_operation(op_project, "Database Migration")
        
        self.print_result("Response Object", str(response.model_dump()))
        
        print("\nCreated files:")
        op_dir = os.path.join(op_project, ".assistant", "operations")
        for file in os.listdir(op_dir):
            print(f"  - {file}")