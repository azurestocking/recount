from typing import Dict, Any
from app.services.tools import (
    extract_evidence_from_text,
    extract_events_from_text,
    deduplicate_evidences_from_db,
    deduplicate_events_from_db,
    detect_contradictions_from_memory,
    detect_broken_evidence_chain,
    finalize_victim_testimony,
    perform_graph_reasoning,
    perform_hybrid_search
)

class Tool:
    """Base class for all tools."""

    async def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

class ExtractEvidenceTool(Tool):
    async def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        try:
            user_input = inputs.get("user_input", "")
            evidence_list = await extract_evidence_from_text(user_input)
            return {"extracted_evidence": evidence_list}
        except Exception as e:
            return {"extracted_evidence": [], "error": str(e)}

class ExtractEventTool(Tool):
    async def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        try:
            user_input = inputs.get("user_input", "")
            event_list = await extract_events_from_text(user_input)
            return {"extracted_events": event_list}
        except Exception as e:
            return {"extracted_events": [], "error": str(e)}

class DeduplicateEvidenceTool(Tool):
    async def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        try:
            evidence_list = inputs.get("extracted_evidence", [])
            db_session = inputs.get("db_session")
            deduped_evidence = await deduplicate_evidences_from_db(db_session, evidence_list)
            return {"deduplicated_evidence": deduped_evidence}
        except Exception as e:
            return {"deduplicated_evidence": [], "error": str(e)}

class DeduplicateEventTool(Tool):
    async def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        try:
            event_list = inputs.get("extracted_events", [])
            db_session = inputs.get("db_session")
            deduped_events = await deduplicate_events_from_db(db_session, event_list)
            return {"deduplicated_events": deduped_events}
        except Exception as e:
            return {"deduplicated_events": [], "error": str(e)}

class ContradictionDetectorTool(Tool):
    async def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        try:
            user_input = inputs.get("user_input", "")
            memory_summary = inputs.get("memory_summary", "")
            clarifications = await detect_contradictions_from_memory(memory_summary, user_input)
            return {"clarifications": clarifications}
        except Exception as e:
            return {"clarifications": [], "error": str(e)}

class ChainIntegrityCheckerTool(Tool):
    async def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        try:
            events = inputs.get("deduplicated_events", [])
            evidences = inputs.get("deduplicated_evidence", [])
            follow_ups = await detect_broken_evidence_chain(events, evidences)
            return {"follow_ups": follow_ups}
        except Exception as e:
            return {"follow_ups": [], "error": str(e)}

class FinalizeTestimonyTool(Tool):
    async def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        try:
            memory_summary = inputs.get("memory_summary", "")
            clarifications = inputs.get("clarifications", [])
            follow_ups = inputs.get("follow_ups", [])
            result = await finalize_victim_testimony(memory_summary, clarifications, follow_ups)
            return result
        except Exception as e:
            return {"final_testimony": None, "next_questions": [], "error": str(e)}

class HybridSearchTool(Tool):
    async def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        try:
            user_input = inputs.get("user_input", "")
            db_session = inputs.get("db_session")
            print(user_input)
            retrieved_docs = await perform_hybrid_search(user_input, db_session)
            return {"retrieved_documents": retrieved_docs}
        except Exception as e:
            return {"retrieved_documents": [], "error": str(e)}

class GraphReasoningTool(Tool):
    async def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        try:
            retrieved_docs = inputs.get("retrieved_documents", [])
            user_input = inputs.get("user_input", "")
            db_session = inputs.get("db_session")

            if not retrieved_docs:
                return {"reasoning_prompt": None}

            reasoning_prompt = await perform_graph_reasoning(retrieved_docs, db_session, user_input)
            return {"reasoning_prompt": reasoning_prompt}
        except Exception as e:
            return {"reasoning_prompt": None, "error": str(e)}
