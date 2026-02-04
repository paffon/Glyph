#!/usr/bin/env python3
"""
Interactive Test Runner for Glyph MCP Service

This script allows developers to interactively trigger scenarios and observe
the actual behavior of various Glyph tools and functions. It uses a combination
of temporary test environments and actual function calls to demonstrate real behavior.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from read_an_asset import read_asset, read_asset_exact
from tools.init_assistant_dir import init_assistant_dir
from tools.add_design_log import add_design_log
from tools.add_operation import add_operation
from tools.persist_artifact import persist_artifacts
from tools.reference_graph import update_reference_graph, get_references_from, find_references_to
from tools.md_to_dict import md_to_dict
from response import GlyphMCPResponse


class TestRunner:
    def __init__(self):
        self.temp_dir = None
        self.test_assets_dir = None
        self.test_project_dir = None
        
    def setup_test_environment(self):
        """Create temporary test environment with various scenarios."""
        print("\n" + "="*80)
        print("SETTING UP TEST ENVIRONMENT")
        print("="*80)
        
        # Create main temp directory
        self.temp_dir = tempfile.mkdtemp(prefix="glyph_test_")
        print(f"Created temp directory: {self.temp_dir}")
        
        # Create test assets directory structure
        self.test_assets_dir = os.path.join(self.temp_dir, "test_assets")
        os.makedirs(self.test_assets_dir)
        
        # Create a unique file
        unique_dir = os.path.join(self.test_assets_dir, "unique")
        os.makedirs(unique_dir)
        with open(os.path.join(unique_dir, "unique_asset.md"), 'w') as f:
            f.write("# Unique Asset\n\nThis file exists only once.")
        
        # Create duplicate files in different locations
        dup_dir1 = os.path.join(self.test_assets_dir, "location1")
        dup_dir2 = os.path.join(self.test_assets_dir, "location2", "nested")
        os.makedirs(dup_dir1)
        os.makedirs(dup_dir2)
        
        with open(os.path.join(dup_dir1, "duplicate.md"), 'w') as f:
            f.write("# Duplicate in Location 1\n\nThis is the first copy.")
        
        with open(os.path.join(dup_dir2, "duplicate.md"), 'w') as f:
            f.write("# Duplicate in Location 2\n\nThis is the second copy in a nested folder.")
        
        # Create test project directory
        self.test_project_dir = os.path.join(self.temp_dir, "test_project")
        os.makedirs(self.test_project_dir)
        
        # Create ad_hoc directory with test files for persist_artifacts
        ad_hoc_dir = os.path.join(self.test_project_dir, ".assistant", "ad_hoc")
        os.makedirs(ad_hoc_dir)
        
        with open(os.path.join(ad_hoc_dir, "test_artifact1.txt"), 'w') as f:
            f.write("This is a test artifact file.")
        
        with open(os.path.join(ad_hoc_dir, "test_artifact2.py"), 'w') as f:
            f.write("# Python test artifact\nprint('Hello from artifact')")
        
        # Create a test markdown file for md_to_dict
        test_md_path = os.path.join(self.temp_dir, "test_doc.md")
        with open(test_md_path, 'w') as f:
            f.write("""# Main Title

Some content under main title.

## Section 1

Content for section 1.

### Subsection 1.1

Nested content.

## Section 2

Content for section 2.
""")
        
        print(f"Created test assets at: {self.test_assets_dir}")
        print(f"Created test project at: {self.test_project_dir}")
        print("Test environment ready!\n")
        
    def teardown_test_environment(self):
        """Clean up temporary test environment."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            print(f"\nCleaned up temp directory: {self.temp_dir}")
    
    def print_scenario_header(self, number, title, description):
        """Print a formatted scenario header."""
        print("\n" + "="*80)
        print(f"SCENARIO {number}: {title}")
        print("="*80)
        print(f"Description: {description}")
        print("-"*80)
    
    def print_result(self, result_label, result_data):
        """Print formatted result."""
        print(f"\n{result_label}:")
        print("-"*80)
        print(result_data)
        print("-"*80)
    
    # ========================================================================
    # SCENARIO IMPLEMENTATIONS
    # ========================================================================
    
    def scenario_1_read_unique_asset(self):
        """Read a unique asset file - success case."""
        self.print_scenario_header(
            1,
            "Read Unique Asset",
            "Attempting to read an asset file that exists only once in the assets directory."
        )
        
        with patch('read_an_asset._get_assets_dir', return_value=self.test_assets_dir):
            print("\nCalling: read_asset('unique_asset.md')")
            result = read_asset('unique_asset.md')
            self.print_result("Result", result)
    
    def scenario_2_read_nonexistent_asset(self):
        """Read a non-existent asset file."""
        self.print_scenario_header(
            2,
            "Read Non-existent Asset",
            "Attempting to read an asset file that doesn't exist."
        )
        
        with patch('read_an_asset._get_assets_dir', return_value=self.test_assets_dir):
            print("\nCalling: read_asset('does_not_exist.md')")
            result = read_asset('does_not_exist.md')
            self.print_result("Result", result)
    
    def scenario_3_read_duplicate_asset(self):
        """Read an asset with duplicate names - error with recommendations."""
        self.print_scenario_header(
            3,
            "Read Duplicate Asset Names",
            "Attempting to read an asset that exists in multiple locations. "
            "The system should detect this and provide helpful guidance."
        )
        
        with patch('read_an_asset._get_assets_dir', return_value=self.test_assets_dir):
            print("\nCalling: read_asset('duplicate.md')")
            result = read_asset('duplicate.md')
            self.print_result("Result", result)
            
            print("\n" + "!"*80)
            print("OBSERVATION: The system detected multiple files and provided:")
            print("  1. A clear error message")
            print("  2. Previews of each file to help identify the correct one")
            print("  3. A recommendation to use read_asset_exact() with the full path")
            print("!"*80)
    
    def scenario_4_read_asset_exact_success(self):
        """Use read_asset_exact to resolve duplicate names."""
        self.print_scenario_header(
            4,
            "Read Asset Exact - Success",
            "Following up from scenario 3, we now use read_asset_exact() with the specific path."
        )
        
        with patch('read_an_asset._get_assets_dir', return_value=self.test_assets_dir):
            target_path = "location2/nested/duplicate.md"
            print(f"\nCalling: read_asset_exact('{target_path}')")
            result = read_asset_exact(target_path)
            self.print_result("Result", result)
    
    def scenario_5_read_asset_exact_not_found(self):
        """Use read_asset_exact with invalid path."""
        self.print_scenario_header(
            5,
            "Read Asset Exact - Not Found",
            "Attempting to use read_asset_exact() with a path that doesn't exist."
        )
        
        with patch('read_an_asset._get_assets_dir', return_value=self.test_assets_dir):
            print("\nCalling: read_asset_exact('wrong/path/file.md')")
            result = read_asset_exact('wrong/path/file.md')
            self.print_result("Result", result)
    
    def scenario_6_init_assistant_dir_success(self):
        """Initialize assistant directory - success."""
        self.print_scenario_header(
            6,
            "Initialize Assistant Directory - Success",
            "Creating a new .assistant directory structure in an empty project."
        )
        
        new_project = os.path.join(self.temp_dir, "new_project")
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
    
    def scenario_7_init_assistant_dir_already_exists(self):
        """Initialize assistant directory that already exists - no overwrite."""
        self.print_scenario_header(
            7,
            "Initialize Assistant Directory - Already Exists",
            "Attempting to initialize when .assistant directory already exists (overwrite=False)."
        )
        
        existing_project = os.path.join(self.temp_dir, "existing_project")
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
        
        print("\n" + "!"*80)
        print("OBSERVATION: The system prevents accidental overwrites and suggests")
        print("to ask the user for explicit confirmation.")
        print("!"*80)
    
    def scenario_8_init_assistant_dir_with_overwrite(self):
        """Initialize assistant directory with overwrite."""
        self.print_scenario_header(
            8,
            "Initialize Assistant Directory - With Overwrite",
            "Overwriting an existing .assistant directory (creates backup)."
        )
        
        overwrite_project = os.path.join(self.temp_dir, "overwrite_project")
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
        
        print("\n" + "!"*80)
        print("OBSERVATION: Original .assistant directory was backed up with timestamp.")
        print("!"*80)
    
    def scenario_9_add_design_log_success(self):
        """Add a design log - success."""
        self.print_scenario_header(
            9,
            "Add Design Log - Success",
            "Creating a new design log in an initialized project."
        )
        
        # Initialize project first
        dl_project = os.path.join(self.temp_dir, "dl_project")
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
    
    def scenario_10_add_design_log_not_initialized(self):
        """Add a design log - directory not initialized."""
        self.print_scenario_header(
            10,
            "Add Design Log - Not Initialized",
            "Attempting to add a design log when .assistant directory doesn't exist."
        )
        
        uninit_project = os.path.join(self.temp_dir, "uninit_project")
        os.makedirs(uninit_project)
        
        print(f"\nProject directory: {uninit_project}")
        print("Calling: add_design_log(abs_path=project_path, title='Test', short_desc='Test')")
        
        response = add_design_log(uninit_project, "Test", "Test")
        
        self.print_result("Response Object", str(response.model_dump()))
    
    def scenario_11_add_operation_success(self):
        """Add an operation document - success."""
        self.print_scenario_header(
            11,
            "Add Operation Document - Success",
            "Creating a new operation document in an initialized project."
        )
        
        op_project = os.path.join(self.temp_dir, "op_project")
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
    
    def scenario_12_persist_artifacts_success(self):
        """Persist artifacts from ad_hoc to artifacts directory."""
        self.print_scenario_header(
            12,
            "Persist Artifacts - Success",
            "Moving files from ad_hoc directory to artifacts directory with serial numbering."
        )
        
        # Use the pre-created test_project with ad_hoc files
        print(f"\nProject directory: {self.test_project_dir}")
        
        # List ad_hoc files
        ad_hoc_dir = os.path.join(self.test_project_dir, ".assistant", "ad_hoc")
        print("\nFiles in ad_hoc directory:")
        for file in os.listdir(ad_hoc_dir):
            print(f"  - {file}")
        
        print("\nCalling: persist_artifacts(")
        print("    abs_path=project_path,")
        print("    files=['test_artifact1.txt', 'test_artifact2.py']")
        print(")")
        
        response = persist_artifacts(
            self.test_project_dir,
            ['test_artifact1.txt', 'test_artifact2.py']
        )
        
        self.print_result("Response Object", str(response.model_dump()))
        
        artifacts_dir = os.path.join(self.test_project_dir, ".assistant", "artifacts")
        if os.path.exists(artifacts_dir):
            print("\nFiles in artifacts directory:")
            for file in os.listdir(artifacts_dir):
                if not os.path.isdir(os.path.join(artifacts_dir, file)):
                    print(f"  - {file}")
    
    def scenario_13_persist_artifacts_file_not_found(self):
        """Persist artifacts - file not found."""
        self.print_scenario_header(
            13,
            "Persist Artifacts - File Not Found",
            "Attempting to persist a file that doesn't exist in ad_hoc directory."
        )
        
        print(f"\nProject directory: {self.test_project_dir}")
        print("Calling: persist_artifacts(abs_path=project_path, files=['nonexistent.txt'])")
        
        response = persist_artifacts(self.test_project_dir, ['nonexistent.txt'])
        
        self.print_result("Response Object", str(response.model_dump()))
    
    def scenario_14_md_to_dict_success(self):
        """Parse a markdown file into a hierarchical dictionary."""
        self.print_scenario_header(
            14,
            "Markdown to Dictionary - Success",
            "Parsing a markdown file into a hierarchical dictionary structure."
        )
        
        test_md_path = os.path.join(self.temp_dir, "test_doc.md")
        
        print(f"\nMarkdown file: {test_md_path}")
        print("Calling: md_to_dict(file_path)")
        
        response = md_to_dict(test_md_path)
        
        self.print_result("Response Object", str(response.model_dump()))
        
        if response.success and response.result:
            print("\nParsed structure (formatted):")
            import json
            print(json.dumps(response.result, indent=2))
    
    def scenario_15_md_to_dict_file_not_found(self):
        """Parse a non-existent markdown file."""
        self.print_scenario_header(
            15,
            "Markdown to Dictionary - File Not Found",
            "Attempting to parse a markdown file that doesn't exist."
        )
        
        fake_path = os.path.join(self.temp_dir, "nonexistent.md")
        
        print(f"\nMarkdown file: {fake_path}")
        print("Calling: md_to_dict(file_path)")
        
        response = md_to_dict(fake_path)
        
        self.print_result("Response Object", str(response.model_dump()))
    
    def scenario_16_update_reference_graph(self):
        """Update the reference graph by scanning files."""
        self.print_scenario_header(
            16,
            "Update Reference Graph",
            "Scanning design logs, operations, and artifacts to build a reference graph."
        )
        
        # Create a project with some cross-referencing files
        ref_project = os.path.join(self.temp_dir, "ref_project")
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
    
    def scenario_17_get_references_from(self):
        """Get all files referenced by a specific file."""
        self.print_scenario_header(
            17,
            "Get References From File",
            "Finding all files that are referenced by a specific file."
        )
        
        # Use the project from scenario 16
        ref_project = os.path.join(self.temp_dir, "ref_project2")
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
    
    def scenario_18_find_references_to(self):
        """Find all files that reference a specific file."""
        self.print_scenario_header(
            18,
            "Find References To File",
            "Finding all files that reference a specific file."
        )
        
        # Use the project from scenario 17
        ref_project = os.path.join(self.temp_dir, "ref_project3")
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
    
    def scenario_19_invalid_absolute_path(self):
        """Test with invalid (relative) path - validation check."""
        self.print_scenario_header(
            19,
            "Invalid Path Validation",
            "Attempting to use a tool with a relative path instead of absolute path."
        )
        
        print("\nCalling: init_assistant_dir(abs_path='./relative/path', overwrite=False)")
        
        response = init_assistant_dir("./relative/path", False)
        
        self.print_result("Response Object", str(response.model_dump()))
        
        print("\n" + "!"*80)
        print("OBSERVATION: The system validates paths and provides clear error messages")
        print("about the requirement for absolute paths.")
        print("!"*80)
    
    def scenario_20_multiple_design_logs_numbering(self):
        """Test sequential numbering of design logs."""
        self.print_scenario_header(
            20,
            "Multiple Design Logs - Sequential Numbering",
            "Creating multiple design logs to demonstrate automatic sequential numbering."
        )
        
        numbering_project = os.path.join(self.temp_dir, "numbering_project")
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
        
        print("\n" + "!"*80)
        print("OBSERVATION: Files are automatically numbered sequentially (dl_1, dl_2, dl_3)")
        print("!"*80)
    
    # ========================================================================
    # MENU AND MAIN RUNNER
    # ========================================================================
    
    def display_menu(self):
        """Display the interactive menu."""
        print("\n" + "="*80)
        print("GLYPH MCP SERVICE - INTERACTIVE TEST RUNNER")
        print("="*80)
        print("\nAvailable Scenarios:")
        print("\n--- Asset Reading ---")
        print("  1. Read unique asset (success)")
        print("  2. Read non-existent asset (error)")
        print("  3. Read duplicate asset names (helpful error)")
        print("  4. Read asset exact - success")
        print("  5. Read asset exact - not found")
        print("\n--- Assistant Directory Initialization ---")
        print("  6. Initialize assistant directory (success)")
        print("  7. Initialize when already exists (no overwrite)")
        print("  8. Initialize with overwrite (creates backup)")
        print("\n--- Design Logs ---")
        print("  9. Add design log (success)")
        print(" 10. Add design log - not initialized")
        print(" 20. Multiple design logs - sequential numbering")
        print("\n--- Operations ---")
        print(" 11. Add operation document (success)")
        print("\n--- Artifact Persistence ---")
        print(" 12. Persist artifacts (success)")
        print(" 13. Persist artifacts - file not found")
        print("\n--- Markdown Processing ---")
        print(" 14. Parse markdown to dictionary (success)")
        print(" 15. Parse markdown - file not found")
        print("\n--- Reference Graph ---")
        print(" 16. Update reference graph")
        print(" 17. Get references from a file")
        print(" 18. Find references to a file")
        print("\n--- Input Validation ---")
        print(" 19. Invalid path validation")
        print("\n--- Special Commands ---")
        print("  a. Run all scenarios")
        print("  q. Quit")
        print("\n" + "="*80)
    
    def run_scenario(self, choice):
        """Run the selected scenario."""
        scenarios = {
            '1': self.scenario_1_read_unique_asset,
            '2': self.scenario_2_read_nonexistent_asset,
            '3': self.scenario_3_read_duplicate_asset,
            '4': self.scenario_4_read_asset_exact_success,
            '5': self.scenario_5_read_asset_exact_not_found,
            '6': self.scenario_6_init_assistant_dir_success,
            '7': self.scenario_7_init_assistant_dir_already_exists,
            '8': self.scenario_8_init_assistant_dir_with_overwrite,
            '9': self.scenario_9_add_design_log_success,
            '10': self.scenario_10_add_design_log_not_initialized,
            '11': self.scenario_11_add_operation_success,
            '12': self.scenario_12_persist_artifacts_success,
            '13': self.scenario_13_persist_artifacts_file_not_found,
            '14': self.scenario_14_md_to_dict_success,
            '15': self.scenario_15_md_to_dict_file_not_found,
            '16': self.scenario_16_update_reference_graph,
            '17': self.scenario_17_get_references_from,
            '18': self.scenario_18_find_references_to,
            '19': self.scenario_19_invalid_absolute_path,
            '20': self.scenario_20_multiple_design_logs_numbering,
        }
        
        if choice in scenarios:
            scenarios[choice]()
            return True
        elif choice.lower() == 'a':
            for key in sorted(scenarios.keys(), key=lambda x: int(x)):
                scenarios[key]()
                input("\nPress Enter to continue to next scenario...")
            return True
        elif choice.lower() == 'q':
            return False
        else:
            print(f"\nInvalid choice: {choice}")
            return True
    
    def run(self):
        """Main runner loop."""
        try:
            self.setup_test_environment()
            
            while True:
                self.display_menu()
                choice = input("\nEnter scenario number (or 'a' for all, 'q' to quit): ").strip()
                
                if not self.run_scenario(choice):
                    break
                
                if choice.lower() != 'a':
                    input("\nPress Enter to return to menu...")
            
        except KeyboardInterrupt:
            print("\n\nInterrupted by user.")
        finally:
            self.teardown_test_environment()
            print("\nGoodbye!")


def main():
    """Entry point for the test runner."""
    runner = TestRunner()
    runner.run()


if __name__ == "__main__":
    main()
