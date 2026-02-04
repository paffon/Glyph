# Test Runner - Refactored Structure

The test runner has been refactored into a modular structure following SOLID, DRY, and KISS principles.

## Structure

```
test_runner/
├── __init__.py              # Package exports
├── main.py                  # Entry point
├── runner.py                # TestRunner orchestration
├── environment.py           # Test environment management
├── utils.py                 # Shared utilities
├── test_runner_old.py       # Original monolithic file (backup)
└── scenarios/               # Test scenario modules
    ├── __init__.py          # Scenario registry
    ├── base.py              # Base scenario class
    ├── asset_reading.py     # Scenarios 1-5
    ├── init_assistant.py    # Scenarios 6-8
    ├── design_logs.py       # Scenarios 9, 10, 20
    ├── operations.py        # Scenario 11
    ├── artifacts.py         # Scenarios 12-13
    ├── markdown.py          # Scenarios 14-15
    ├── reference_graph.py   # Scenarios 16-18
    └── validation.py        # Scenario 19
```

## Usage

Run the test runner from the project root:

```bash
python -m test_runner.main
```

## Architecture

### Single Responsibility Principle (SRP)
- **`environment.py`**: Manages test environment setup/teardown
- **`utils.py`**: Provides formatting utilities
- **`runner.py`**: Orchestrates scenario execution and menu
- **`scenarios/`**: Each module handles one domain of scenarios
- **`scenarios/base.py`**: Provides shared scenario functionality

### DRY (Don't Repeat Yourself)
- Common print functions centralized in `utils.py`
- Base scenario class eliminates code duplication
- Scenario registry pattern eliminates conditional logic

### KISS (Keep It Simple, Stupid)
- Clear module boundaries
- Simple inheritance hierarchy
- Straightforward registry pattern
- No over-engineering

### Open/Closed Principle
- Easy to add new scenarios without modifying existing code
- Just create a new scenario class and add to registry

## Adding New Scenarios

1. Create a new scenario class in the appropriate module (or create a new module):
   ```python
   class MyNewScenario(BaseScenario):
       def run(self):
           self.print_header(21, "My New Scenario", "Description")
           # Implementation here
   ```

2. Add to the registry in `scenarios/__init__.py`:
   ```python
   from test_runner.scenarios.my_module import MyNewScenario
   
   SCENARIO_REGISTRY = {
       # ... existing scenarios
       '21': MyNewScenario,
   }
   ```

3. Update the menu in `runner.py`

## Benefits of Refactoring

- **Maintainability**: Changes are localized to specific modules
- **Testability**: Each component can be tested independently
- **Readability**: Clear separation of concerns
- **Extensibility**: Easy to add new scenarios or modify existing ones
- **Reusability**: Components can be reused in other contexts