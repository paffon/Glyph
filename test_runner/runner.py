"""
Test runner orchestration.

This module contains the TestRunner class that orchestrates scenario execution.
"""

from test_runner.environment import TestEnvironment
from test_runner.scenarios import get_scenario, get_all_scenarios
from test_runner.utils import print_section_header


class TestRunner:
    """Orchestrates the execution of test scenarios."""
    
    def __init__(self):
        self.env = TestEnvironment()
    
    def display_menu(self):
        """Display the interactive menu."""
        print_section_header("GLYPH MCP SERVICE - INTERACTIVE TEST RUNNER")
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
        """
        Run the selected scenario.
        
        Args:
            choice: The user's menu choice.
            
        Returns:
            True to continue running, False to quit.
        """
        if choice.lower() == 'q':
            return False
        
        if choice.lower() == 'a':
            # Run all scenarios
            scenarios = get_all_scenarios(self.env)
            for scenario in scenarios:
                scenario.run()
                input("\nPress Enter to continue to next scenario...")
            return True
        
        # Run single scenario
        scenario = get_scenario(choice, self.env)
        if scenario:
            scenario.run()
            return True
        else:
            print(f"\nInvalid choice: {choice}")
            return True
    
    def run(self):
        """Main runner loop."""
        try:
            self.env.setup()
            
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
            self.env.teardown()
            print("\nGoodbye!")