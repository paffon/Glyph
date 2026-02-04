"""
Design log test scenarios.

This module contains scenarios for testing design log functionality.
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from tools.add_design_log import add_design_log
from tools.init_assistant_dir import init_assistant_dir
from test_runner.scenarios.base import BaseScenario
from test_runner.utils import print_observation


class AddDesignLogSuccessScenario(BaseScenario):
    """Scenario 9: Add a design log - success."""
    
    def run(self):
        self.print_header(
            9,
            "Add Design Log - Success",
            "Creating a new design log in an initialized project."
        )
        
        # Initialize project first
        dl_project = os.path.join(self.env.temp_dir, "dl_project")
        os.makedirs(dl_project)
        init_assistant_dir(dl_project, False)
        
        print(f"\nProject directory: {dl_project}")
        print("Calling: add_design_log(")
        print("    abs_path=project_path,")
        print("    title='User Authentication System',")
        print("    short_desc='Design for implementing OAuth 2.0 authentication'")
        print(")")
        
        response = add_design_log(
            dl_project,
            "User Authentication System",
            "Design for implementing OAuth 2.0 authentication"
        )
        
        self.print_result("Response Object", str(response.model_dump()))
        
        print("\nCreated files:")
        dl_dir = os.path.join(dl_project, ".assistant", "design_logs")
        for file in os.listdir(dl_dir):
            print(f"  - {file}")
        
        # Show summary file content
        summary_path = os.path.join(dl_dir, "_summary.md")
        if os.path.exists(summary_path):
            print("\n_summary.md content:")
            with open(summary_path, 'r') as f:
                print(f.read())


class AddDesignLogNotInitializedScenario(BaseScenario):
    """Scenario 10: Add a design log - directory not initialized."""
    
    def run(self):
        self.print_header(
            10,
            "Add Design Log - Not Initialized",
            "Attempting to add a design log when .assistant directory doesn't exist."
        )
        
        uninit_project = os.path.join(self.env.temp_dir, "uninit_project")
        os.makedirs(uninit_project)
        
        print(f"\nProject directory: {uninit_project}")
        print("Calling: add_design_log(abs_path=project_path, title='Test', short_desc='Test')")
        
        response = add_design_log(uninit_project, "Test", "Test")
        
        self.print_result("Response Object", str(response.model_dump()))


class MultipleDesignLogsNumberingScenario(BaseScenario):
    """Scenario 20: Test sequential numbering of design logs."""
    
    def run(self):
        self.print_header(
            20,
            "Multiple Design Logs - Sequential Numbering",
            "Creating multiple design logs to demonstrate automatic sequential numbering."
        )
        
        numbering_project = os.path.join(self.env.temp_dir, "numbering_project")
        os.makedirs(numbering_project)
        init_assistant_dir(numbering_project, False)
        
        print(f"\nProject directory: {numbering_project}")
        
        # Add multiple design logs
        titles = [
            ("Initial Architecture", "System architecture overview"),
            ("API Design", "RESTful API specification"),
            ("Security Model", "Authentication and authorization")
        ]
        
        for i, (title, desc) in enumerate(titles, 1):
            print(f"\n{i}. Adding: {title}")
            response = add_design_log(numbering_project, title, desc)
            print(f"   Success: {response.success}")
        
        # List all created files
        dl_dir = os.path.join(numbering_project, ".assistant", "design_logs")
        print("\nAll design log files:")
        for file in sorted(os.listdir(dl_dir)):
            if file.endswith('.md') and not file.startswith('_'):
                print(f"  - {file}")
        
        print_observation("Files are automatically numbered sequentially (dl_1, dl_2, dl_3)")
