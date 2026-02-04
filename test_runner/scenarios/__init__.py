"""
Scenario registry and exports.

This module provides a central registry mapping scenario numbers to scenario classes.
"""

from test_runner.scenarios.asset_reading import (
    ReadUniqueAssetScenario,
    ReadNonexistentAssetScenario,
    ReadDuplicateAssetScenario,
    ReadAssetExactSuccessScenario,
    ReadAssetExactNotFoundScenario,
)
from test_runner.scenarios.init_assistant import (
    InitAssistantDirSuccessScenario,
    InitAssistantDirAlreadyExistsScenario,
    InitAssistantDirWithOverwriteScenario,
)
from test_runner.scenarios.design_logs import (
    AddDesignLogSuccessScenario,
    AddDesignLogNotInitializedScenario,
    MultipleDesignLogsNumberingScenario,
)
from test_runner.scenarios.operations import AddOperationSuccessScenario
from test_runner.scenarios.artifacts import (
    PersistArtifactsSuccessScenario,
    PersistArtifactsFileNotFoundScenario,
)
from test_runner.scenarios.markdown import (
    MdToDictSuccessScenario,
    MdToDictFileNotFoundScenario,
)
from test_runner.scenarios.reference_graph import (
    UpdateReferenceGraphScenario,
    GetReferencesFromScenario,
    FindReferencesToScenario,
)
from test_runner.scenarios.validation import InvalidAbsolutePathScenario


# Scenario registry: maps scenario number to scenario class
SCENARIO_REGISTRY = {
    '1': ReadUniqueAssetScenario,
    '2': ReadNonexistentAssetScenario,
    '3': ReadDuplicateAssetScenario,
    '4': ReadAssetExactSuccessScenario,
    '5': ReadAssetExactNotFoundScenario,
    '6': InitAssistantDirSuccessScenario,
    '7': InitAssistantDirAlreadyExistsScenario,
    '8': InitAssistantDirWithOverwriteScenario,
    '9': AddDesignLogSuccessScenario,
    '10': AddDesignLogNotInitializedScenario,
    '11': AddOperationSuccessScenario,
    '12': PersistArtifactsSuccessScenario,
    '13': PersistArtifactsFileNotFoundScenario,
    '14': MdToDictSuccessScenario,
    '15': MdToDictFileNotFoundScenario,
    '16': UpdateReferenceGraphScenario,
    '17': GetReferencesFromScenario,
    '18': FindReferencesToScenario,
    '19': InvalidAbsolutePathScenario,
    '20': MultipleDesignLogsNumberingScenario,
}


def get_scenario(scenario_number, env):
    """
    Get a scenario instance by its number.
    
    Args:
        scenario_number: The scenario number as a string.
        env: TestEnvironment instance to pass to the scenario.
        
    Returns:
        An instance of the requested scenario, or None if not found.
    """
    scenario_class = SCENARIO_REGISTRY.get(scenario_number)
    if scenario_class:
        return scenario_class(env)
    return None


def get_all_scenarios(env):
    """
    Get all scenarios in order.
    
    Args:
        env: TestEnvironment instance to pass to scenarios.
        
    Returns:
        List of scenario instances in numeric order.
    """
    return [
        get_scenario(key, env) 
        for key in sorted(SCENARIO_REGISTRY.keys(), key=lambda x: int(x))
    ]