"""
Artifact persistence test scenarios.

This module contains scenarios for testing artifact persistence functionality.
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from tools.persist_artifact import persist_artifacts
from test_runner.scenarios.base import BaseScenario


class PersistArtifactsSuccessScenario(BaseScenario):
    """Scenario 12: Persist artifacts from ad_hoc to artifacts directory."""
    
    def run(self):
        self.print_header(
            12,
            "Persist Artifacts - Success",
            "Moving files from ad_hoc directory to artifacts directory with serial numbering."
        )
        
        # Use the pre-created test_project with ad_hoc files
        print(f"\nProject directory: {self.env.test_project_dir}")
        
        # List ad_hoc files
        ad_hoc_dir = os.path.join(self.env.test_project_dir, ".assistant", "ad_hoc")
        print("\nFiles in ad_hoc directory:")
        for file in os.listdir(ad_hoc_dir):
            print(f"  - {file}")
        
        print("\nCalling: persist_artifacts(")
        print("    abs_path=project_path,")
        print("    files=['test_artifact1.txt', 'test_artifact2.py']")
        print(")")
        
        response = persist_artifacts(
            self.env.test_project_dir,
            ['test_artifact1.txt', 'test_artifact2.py']
        )
        
        self.print_result("Response Object", str(response.model_dump()))
        
        artifacts_dir = os.path.join(self.env.test_project_dir, ".assistant", "artifacts")
        if os.path.exists(artifacts_dir):
            print("\nFiles in artifacts directory:")
            for file in os.listdir(artifacts_dir):
                if not os.path.isdir(os.path.join(artifacts_dir, file)):
                    print(f"  - {file}")


class PersistArtifactsFileNotFoundScenario(BaseScenario):
    """Scenario 13: Persist artifacts - file not found."""
    
    def run(self):
        self.print_header(
            13,
            "Persist Artifacts - File Not Found",
            "Attempting to persist a file that doesn't exist in ad_hoc directory."
        )
        
        print(f"\nProject directory: {self.env.test_project_dir}")
        print("Calling: persist_artifacts(abs_path=project_path, files=['nonexistent.txt'])")
        
        response = persist_artifacts(self.env.test_project_dir, ['nonexistent.txt'])
        
        self.print_result("Response Object", str(response.model_dump()))