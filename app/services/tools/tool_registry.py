from app.services.tools.tool_definitions import (
    ExtractEvidenceTool,
    ExtractEventTool,
    DeduplicateEvidenceTool,
    DeduplicateEventTool,
    ContradictionDetectorTool,
    ChainIntegrityCheckerTool,
    FinalizeTestimonyTool,
    HybridSearchTool,
    GraphReasoningTool
)

TOOL_REGISTRY = {
    "extract_evidence": ExtractEvidenceTool(),
    "extract_event": ExtractEventTool(),
    "deduplicate_evidence": DeduplicateEvidenceTool(),
    "deduplicate_event": DeduplicateEventTool(),
    "detect_contradictions": ContradictionDetectorTool(),
    "check_chain_integrity": ChainIntegrityCheckerTool(),
    "finalize_testimony": FinalizeTestimonyTool(),
    "hybrid_search": HybridSearchTool(),
    "graph_reasoning": GraphReasoningTool(),
}

