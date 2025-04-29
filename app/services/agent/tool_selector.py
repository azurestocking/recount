from typing import Dict

def tool_selector(inputs: Dict[str, any]) -> str:
    """
    Select which tool to run based on the current inputs.
    :param inputs: Current conversation inputs
    :return: Tool name registered in TOOL_REGISTRY
    """

    # Step 1: If there's no retrieved_documents yet, run hybrid search first
    if not inputs.get("retrieved_documents"):
        return "hybrid_search"

    # Step 2: If retrieved_documents available but no reasoning_prompt, run graph reasoning
    if inputs.get("retrieved_documents") and not inputs.get("reasoning_prompt"):
        return "graph_reasoning"

    # Step 3: If no extracted evidence, extract evidence first
    if not inputs.get("extracted_evidence"):
        return "extract_evidence"

    # Step 4: If no extracted events, extract events
    if not inputs.get("extracted_events"):
        return "extract_event"

    # Step 5: If evidence exists but not deduplicated, deduplicate evidences
    if inputs.get("extracted_evidence") and not inputs.get("deduplicated_evidence"):
        return "deduplicate_evidence"

    # Step 6: If events exist but not deduplicated, deduplicate events
    if inputs.get("extracted_events") and not inputs.get("deduplicated_events"):
        return "deduplicate_event"

    # # Step 7: If no contradiction detection yet, detect contradictions
    # if not inputs.get("clarifications"):
    #     return "detect_contradictions"
    #
    # # Step 8: If no chain integrity check yet, check chain completeness
    # if not inputs.get("follow_ups"):
    #     return "check_chain_integrity"
    #
    # # Step 9: Finally, finalize the victim testimony
    # return "finalize_testimony"
    # Step 7
    if "clarifications" not in inputs:
        return "detect_contradictions"

    # Step 8
    if "follow_ups" not in inputs:
        return "check_chain_integrity"

    # Step 9
    return "finalize_testimony"
