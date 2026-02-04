"""
Reference graph test scenarios.

This module contains scenarios for testing reference graph functionality.
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from tools.reference_graph import update_reference_graph, get_references_from, find_references_to
from tools.add_design_log import add_design_log
from tools.add_operation import add_operation
from tools.init_assistant_dir import init_assistant_dir
from test_runner.scenarios.base import BaseScenario


class UpdateReferenceGraphScenario(BaseScenario):
    """Scenario 16: Update the reference graph by scanning files."""
    
    def run(self):
        self.print_header(
            16,
            "Update Reference Graph",
            "Scanning design logs, operations, and artifacts to build a reference graph."
        )
        
        # Create a project with some cross-referencing files
        ref_project = os.path.join(self.env.temp_dir, "ref_project")
        os.makedirs(ref_project)
        init_assistant_dir(ref_project, False)
        
        # Add some design logs with references
        add_design_log(ref_project, "Authentication", "Auth system design")
        add_design_log(ref_project, "Database Schema", "DB design")
        
        # Add content with references
        dl_dir = os.path.join(ref_project, ".assistant", "design_logs")
        dl1_path = os.path.join(dl_dir, "dl_1_Authentication.md")
        with open(dl1_path, 'a') as f:
            f.write("\n\nThis design references dl_2_Database_Schema.md for data storage details.")
        
        print(f"\nProject directory: {ref_project}")
        print("Created design logs with cross-references")
        print("Calling: update_reference_graph(abs_path=project_path)")
        
        response = update_reference_graph(ref_project)
        
        self.print_result("Response Object", str(response.model_dump()))
        
        # Show the reference graph file
        ref_graph_path = os.path.join(ref_project, ".assistant", "reference_graph.csv")
        if os.path.exists(ref_graph_path):
            print("\nreference_graph.csv content:")
            with open(ref_graph_path, 'r') as f:
                print(f.read())


class GetReferencesFromScenario(BaseScenario):
    """Scenario 17: Get all files referenced by a specific file."""
    
    def run(self):
        self.print_header(
            17,
            "Get References From File",
            "Finding all files that are referenced by a specific file."
        )
        
        # Use the project from scenario 16
        ref_project = os.path.join(self.env.temp_dir, "ref_project2")
        os.makedirs(ref_project)
        init_assistant_dir(ref_project, False)
        
        add_design_log(ref_project, "Main Design", "Main design doc")
        add_design_log(ref_project, "Sub Design", "Sub design doc")
        add_operation(ref_project, "Implementation Steps")
        
        # Add cross-references
        dl_dir = os.path.join(ref_project, ".assistant", "design_logs")
        dl1_path = os.path.join(dl_dir, "dl_1_Main_Design.md")
        with open(dl1_path, 'a') as f:
            f.write("\n\nSee dl_2_Sub_Design.md and op_1_Implementation_Steps.md for details.")
        
        print(f"\nProject directory: {ref_project}")
        print("Calling: get_references_from(abs_path=project_path, file_name='dl_1_Main_Design.md')")
        
        response = get_references_from(ref_project, "dl_1_Main_Design.md")
        
        self.print_result("Response Object", str(response.model_dump()))


class FindReferencesToScenario(BaseScenario):
    """Scenario 18: Find all files that reference a specific file."""
    
    def run(self):
        self.print_header(
            18,
            "Find References To File",
            "Finding all files that reference a specific file."
        )
        
        # Use the project from scenario 17
        ref_project = os.path.join(self.env.temp_dir, "ref_project3")
        os.makedirs(ref_project)
        init_assistant_dir(ref_project, False)
        
        add_design_log(ref_project, "Core Design", "Core design")
        add_design_log(ref_project, "Feature A", "Feature A design")
        add_design_log(ref_project, "Feature B", "Feature B design")
        
        # Multiple files reference the core design
        dl_dir = os.path.join(ref_project, ".assistant", "design_logs")
        
        dl2_path = os.path.join(dl_dir, "dl_2_Feature_A.md")
        with open(dl2_path, 'a') as f:
            f.write("\n\nThis feature depends on dl_1_Core_Design.md")
        
        dl3_path = os.path.join(dl_dir, "dl_3_Feature_B.md")
        with open(dl3_path, 'a') as f:
            f.write("\n\nBuilds upon dl_1_Core_Design.md")
        
        print(f"\nProject directory: {ref_project}")
        print("Calling: find_references_to(abs_path=project_path, file_name='dl_1_Core_Design.md')")
        
        response = find_references_to(ref_project, "dl_1_Core_Design.md")
        
        self.print_result("Response Object", str(response.model_dump()))