"""
Assistant directory initialization test scenarios.

This module contains scenarios for testing assistant directory initialization.
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from tools.init_assistant_dir import init_assistant_dir
from test_runner.scenarios.base import BaseScenario
from test_runner.utils import print_observation


class InitAssistantDirSuccessScenario(BaseScenario):
    """Scenario 6: Initialize assistant directory - success."""
    
    def run(self):
        self.print_header(
            6,
            "Initialize Assistant Directory - Success",
            "Creating a new .assistant directory structure in an empty project."
        )
        
        new_project = os.path.join(self.env.temp_dir, "new_project")
        os.makedirs(new_project)
        
        print(f"\nProject directory: {new_project}")
        print("Calling: init_assistant_dir(abs_path=project_path, overwrite=False)")
        
        response = init_assistant_dir(new_project, False)
        
        self.print_result("Response Object", str(response.model_dump()))
        
        print("\nDirectory structure created:")
        for root, dirs, files in os.walk(os.path.join(new_project, ".assistant")):
            level = root.replace(os.path.join(new_project, ".assistant"), '').count(os.sep)
            indent = ' ' * 2 * level
            print(f'{indent}{os.path.basename(root)}/')
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                print(f'{subindent}{file}')


class InitAssistantDirAlreadyExistsScenario(BaseScenario):
    """Scenario 7: Initialize assistant directory that already exists - no overwrite."""
    
    def run(self):
        self.print_header(
            7,
            "Initialize Assistant Directory - Already Exists",
            "Attempting to initialize when .assistant directory already exists (overwrite=False)."
        )
        
        existing_project = os.path.join(self.env.temp_dir, "existing_project")
        os.makedirs(existing_project)
        
        # First init
        print(f"\nProject directory: {existing_project}")
        print("First call: init_assistant_dir(abs_path=project_path, overwrite=False)")
        response1 = init_assistant_dir(existing_project, False)
        print(f"First init success: {response1.success}")
        
        # Try to init again
        print("\nSecond call: init_assistant_dir(abs_path=project_path, overwrite=False)")
        response2 = init_assistant_dir(existing_project, False)
        
        self.print_result("Response Object", str(response2.model_dump()))
        
        print_observation(
            "The system prevents accidental overwrites and suggests\n"
            "to ask the user for explicit confirmation."
        )


class InitAssistantDirWithOverwriteScenario(BaseScenario):
    """Scenario 8: Initialize assistant directory with overwrite."""
    
    def run(self):
        self.print_header(
            8,
            "Initialize Assistant Directory - With Overwrite",
            "Overwriting an existing .assistant directory (creates backup)."
        )
        
        overwrite_project = os.path.join(self.env.temp_dir, "overwrite_project")
        os.makedirs(overwrite_project)
        
        # First init
        print(f"\nProject directory: {overwrite_project}")
        response1 = init_assistant_dir(overwrite_project, False)
        print(f"First init success: {response1.success}")
        
        # Add a marker file
        marker_path = os.path.join(overwrite_project, ".assistant", "marker.txt")
        with open(marker_path, 'w') as f:
            f.write("This file will be backed up")
        print("Created marker file in .assistant directory")
        
        # Overwrite
        print("\nCalling: init_assistant_dir(abs_path=project_path, overwrite=True)")
        response2 = init_assistant_dir(overwrite_project, True)
        
        self.print_result("Response Object", str(response2.model_dump()))
        
        print("\nDirectory contents after overwrite:")
        for item in os.listdir(overwrite_project):
            print(f"  - {item}")
        
        print_observation("Original .assistant directory was backed up with timestamp.")