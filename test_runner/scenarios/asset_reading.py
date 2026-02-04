"""
Asset reading test scenarios.

This module contains scenarios for testing asset reading functionality.
"""

import os
import sys
from unittest.mock import patch

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from read_an_asset import read_asset, read_asset_exact
from test_runner.scenarios.base import BaseScenario
from test_runner.utils import print_observation


class ReadUniqueAssetScenario(BaseScenario):
    """Scenario 1: Read a unique asset file - success case."""
    
    def run(self):
        self.print_header(
            1,
            "Read Unique Asset",
            "Attempting to read an asset file that exists only once in the assets directory."
        )
        
        with patch('read_an_asset._get_assets_dir', return_value=self.env.test_assets_dir):
            print("\nCalling: read_asset('unique_asset.md')")
            result = read_asset('unique_asset.md')
            self.print_result("Result", result)


class ReadNonexistentAssetScenario(BaseScenario):
    """Scenario 2: Read a non-existent asset file."""
    
    def run(self):
        self.print_header(
            2,
            "Read Non-existent Asset",
            "Attempting to read an asset file that doesn't exist."
        )
        
        with patch('read_an_asset._get_assets_dir', return_value=self.env.test_assets_dir):
            print("\nCalling: read_asset('does_not_exist.md')")
            result = read_asset('does_not_exist.md')
            self.print_result("Result", result)


class ReadDuplicateAssetScenario(BaseScenario):
    """Scenario 3: Read an asset with duplicate names - error with recommendations."""
    
    def run(self):
        self.print_header(
            3,
            "Read Duplicate Asset Names",
            "Attempting to read an asset that exists in multiple locations. "
            "The system should detect this and provide helpful guidance."
        )
        
        with patch('read_an_asset._get_assets_dir', return_value=self.env.test_assets_dir):
            print("\nCalling: read_asset('duplicate.md')")
            result = read_asset('duplicate.md')
            self.print_result("Result", result)
            
            print_observation(
                "The system detected multiple files and provided:\n"
                "  1. A clear error message\n"
                "  2. Previews of each file to help identify the correct one\n"
                "  3. A recommendation to use read_asset_exact() with the full path"
            )


class ReadAssetExactSuccessScenario(BaseScenario):
    """Scenario 4: Use read_asset_exact to resolve duplicate names."""
    
    def run(self):
        self.print_header(
            4,
            "Read Asset Exact - Success",
            "Following up from scenario 3, we now use read_asset_exact() with the specific path."
        )
        
        with patch('read_an_asset._get_assets_dir', return_value=self.env.test_assets_dir):
            target_path = "location2/nested/duplicate.md"
            print(f"\nCalling: read_asset_exact('{target_path}')")
            result = read_asset_exact(target_path)
            self.print_result("Result", result)


class ReadAssetExactNotFoundScenario(BaseScenario):
    """Scenario 5: Use read_asset_exact with invalid path."""
    
    def run(self):
        self.print_header(
            5,
            "Read Asset Exact - Not Found",
            "Attempting to use read_asset_exact() with a path that doesn't exist."
        )
        
        with patch('read_an_asset._get_assets_dir', return_value=self.env.test_assets_dir):
            print("\nCalling: read_asset_exact('wrong/path/file.md')")
            result = read_asset_exact('wrong/path/file.md')
            self.print_result("Result", result)