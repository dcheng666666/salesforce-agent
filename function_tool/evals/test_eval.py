import os
import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator


@pytest.mark.asyncio
async def test_coordinator_agent_evaluation():
    """
    Runs the agent evaluation.
    """
    await AgentEvaluator.evaluate(
        agent_module="function_tool.agent",
        agent_name="root_agent",
        # eval_dataset_file_path_or_dir=os.path.join(os.path.dirname(__file__), "data"), // 
        eval_dataset_file_path_or_dir=os.path.join(os.path.dirname(__file__), "data", "eval_case.evalset.test.json"),
        num_runs=1,
    )
