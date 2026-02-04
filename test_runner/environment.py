"""
Test environment management for the test runner.

This module handles creation and cleanup of temporary test directories and files.
"""

import os
import tempfile
import shutil


class TestEnvironment:
    """Manages the test environment with temporary directories and test files."""
    
    def __init__(self):
        self.temp_dir = None
        self.test_assets_dir = None
        self.test_project_dir = None
    
    def setup(self):
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
    
    def teardown(self):
        """Clean up temporary test environment."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            print(f"\nCleaned up temp directory: {self.temp_dir}")