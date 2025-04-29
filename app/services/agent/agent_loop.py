from app.services.agent.tool_selector import tool_selector
from app.services.tools.tool_registry import TOOL_REGISTRY
from app.services.agent.agent_saver import save_extracted_info
# from typing import Dict, Any
# import logging
#
# logger = logging.getLogger(__name__)
#
# async def agent_reasoning_loop(
#     user_input: str,
#     db_session,
#     memory,
#     conversation_id: str = None,
#     max_turns: int = 10
# ) -> Dict[str, Any]:
#     """
#     Main reasoning loop of the agent.
#     Dynamically selects tools, executes them, saves extracted evidence/events.
#     """
#
#     logger.info("Starting agent reasoning loop.")
#
#     # Initialize inputs
#     inputs = {
#         "user_input": user_input,
#         "db_session": db_session,
#         "memory_summary": memory.load_memory_variables({}).get("history", "")
#     }
#
#     for turn in range(max_turns):
#         logger.info(f"Agent turn {turn + 1}")
#
#         # Select the next tool
#         tool_name = tool_selector(inputs)
#         tool = TOOL_REGISTRY.get(tool_name)
#
#         if not tool:
#             logger.error(f"Tool '{tool_name}' not found in registry.")
#             raise ValueError(f"Tool '{tool_name}' not found.")
#
#         logger.info(f"Selected tool: {tool_name}")
#
#         # Execute the selected tool
#         outputs = await tool.run(inputs)
#         logger.info(f"Tool '{tool_name}' executed successfully.")
#
#         # Save extracted evidences/events immediately if available
#         if conversation_id:
#             save_extracted_info(db_session, conversation_id, outputs)
#
#         # Update memory
#         memory.save_context(inputs, outputs)
#
#         # Merge new outputs into inputs for next step
#         inputs.update(outputs)
#
#         # Check for finalization
#         if outputs.get("final_testimony"):
#             logger.info("Final testimony generated. Agent reasoning loop completed.")
#             return {
#                 "status": "completed",
#                 "final_testimony": outputs["final_testimony"]
#             }
#
#         if outputs.get("next_questions"):
#             logger.info("Follow-up questions generated. Awaiting further user input.")
#             return {
#                 "status": "need_followup",
#                 "next_questions": outputs["next_questions"]
#             }
#
#     logger.warning("Max turns exceeded without reaching a final answer.")
#     return {
#         "status": "max_turns_exceeded",
#         "message": "Agent exceeded maximum reasoning steps without completing."
#     }

from typing import Dict, Any
from app.models.schemas import ChatResponse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# async def agent_reasoning_loop(
#     user_input: str,
#     db_session,
#     memory,
#     conversation_id: str = None,
#     max_turns: int = 10
# ) -> ChatResponse:
#     """Main reasoning loop returning standardized ChatResponse"""
#
#     logger.info("Starting agent reasoning loop.")
#
#     inputs = {
#         "user_input": user_input,
#         "db_session": db_session,
#         "memory_summary": memory.load_memory_variables({}).get("history", "")
#     }
#
#     events = []
#     evidences = []
#     final_message = ""
#
#     for turn in range(max_turns):
#         logger.info(f"Agent turn {turn + 1}")
#
#         tool_name = tool_selector(inputs)
#         tool = TOOL_REGISTRY.get(tool_name)
#
#         if not tool:
#             logger.error(f"Tool '{tool_name}' not found in registry.")
#             raise ValueError(f"Tool '{tool_name}' not found.")
#
#         outputs = await tool.run(inputs)
#         logger.info(f"Executed tool: {tool_name}")
#
#         # Immediately save extracted info if needed
#         if conversation_id:
#             save_extracted_info(db_session, conversation_id, outputs)
#
#         memory.save_context(inputs, outputs)
#         inputs.update(outputs)
#
#         # Collect evidence/events
#         if outputs.get("extracted_events"):
#             events.extend(outputs.get("extracted_events", []))
#         if outputs.get("extracted_evidence"):
#             evidences.extend(outputs.get("extracted_evidence", []))
#
#         if outputs.get("deduplicated_events"):
#             events.extend(outputs.get("deduplicated_events", []))
#         if outputs.get("deduplicated_evidence"):
#             evidences.extend(outputs.get("deduplicated_evidence", []))
#
#         # Decide if finished
#         if outputs.get("final_testimony"):
#             final_message = outputs["final_testimony"]
#             break
#
#         if outputs.get("next_questions"):
#             final_message = "\n".join(outputs["next_questions"])
#             break
#
#     if not final_message:
#         final_message = "Agent reasoning completed but no conclusive output."
#
#     return ChatResponse(
#         conversation_id=conversation_id,
#         message=final_message,
#         events=events,
#         evidence=evidences
#     )

# async def agent_reasoning_loop(
#     user_input: str,
#     db_session,
#     memory,
#     conversation_id: str = None,
#     max_turns: int = 10
# ) -> ChatResponse:
#     """Main reasoning loop returning standardized ChatResponse"""
#     try:
#         logger.info("Starting agent reasoning loop.")
#
#         inputs = {
#             "user_input": user_input,
#             "db_session": db_session,
#             "memory_summary": memory.load_memory_variables({}).get("history", "")
#         }
#
#         events = []
#         evidences = []
#         final_message = ""
#
#         for turn in range(max_turns):
#             logger.info(f"Agent turn {turn + 1}")
#
#             tool_name = tool_selector(inputs)
#             tool = TOOL_REGISTRY.get(tool_name)
#
#             if not tool:
#                 logger.error(f"Tool '{tool_name}' not found in registry.")
#                 final_message = f"Error: Tool '{tool_name}' not found."
#                 break  # 不 raise了，继续走流程
#
#             outputs = await tool.run(inputs)
#             logger.info(f"Executed tool: {tool_name}")
#             print(f"[Turn {turn}] Tool outputs: {outputs}")
#
#             if conversation_id:
#                 save_extracted_info(db_session, conversation_id, outputs)
#
#             memory.save_context(inputs, outputs)
#             inputs.update(outputs)
#
#             if outputs.get("extracted_events"):
#                 events.extend(outputs.get("extracted_events", []))
#             if outputs.get("extracted_evidence"):
#                 evidences.extend(outputs.get("extracted_evidence", []))
#
#             if outputs.get("deduplicated_events"):
#                 events.extend(outputs.get("deduplicated_events", []))
#             if outputs.get("deduplicated_evidence"):
#                 evidences.extend(outputs.get("deduplicated_evidence", []))
#
#             if outputs.get("final_testimony"):
#                 final_message = outputs["final_testimony"]
#                 break
#
#             if outputs.get("next_questions"):
#                 final_message = "\n".join(outputs["next_questions"])
#                 break
#
#         if not final_message:
#             final_message = "Agent reasoning completed but no conclusive output."
#
#         return ChatResponse(
#             conversation_id=conversation_id,
#             message=final_message,
#             events=events,
#             evidence=evidences
#         )
#
#     except Exception as e:
#         print(f"Error during agent_reasoning_loop: {e}")
#         logger.error(f"Error during agent_reasoning_loop: {str(e)}")
#         return ChatResponse(
#             conversation_id=conversation_id,
#             message=f"Agent failed due to internal error: {str(e)}",
#             events=[],
#             evidence=[]
#         )

async def agent_reasoning_loop(
    user_input: str,
    db_session,
    memory,
    conversation_id: str = None,
    max_turns: int = 10
) -> ChatResponse:
    """Main reasoning loop returning standardized ChatResponse"""
    logger.info("Starting agent reasoning loop.")

    inputs = {
            "user_input": user_input,
            "db_session": db_session,
            "memory_summary": memory.load_memory_variables({}).get("history", "")
        }

    events = []
    evidences = []
    final_message = ""

    tool_attempt_counter = {}
    previous_tool_name = None
    forced_tool = None

    for turn in range(max_turns):
        logger.info(f"Agent turn {turn + 1}")

        if forced_tool:
            tool_name = forced_tool
            forced_tool = None
        else:
            tool_name = tool_selector(inputs)

        if previous_tool_name != tool_name:
            tool_attempt_counter = {}

        if should_force_switch_tool(tool_name, tool_attempt_counter, max_attempts=1):
            logger.warning(f"Tool '{tool_name}' exceeded max attempts, forcing switch.")
            forced_tool = force_switch_tool(tool_name)
            continue

        previous_tool_name = tool_name

        tool = TOOL_REGISTRY.get(tool_name)

        if not tool:
            logger.error(f"Tool '{tool_name}' not found in registry.")
            final_message = f"Error: Tool '{tool_name}' not found."
            break  # 不 raise了，继续走流程

        outputs = await tool.run(inputs)
        logger.info(f"Executed tool: {tool_name}")
        print(f"[Turn {turn}] Tool outputs: {outputs}")

        # if conversation_id:
        save_extracted_info(db_session, conversation_id, outputs)
        inputs.update(outputs)
        if "error" not in outputs:
            first_value = next(iter(outputs.values()), None)
            if isinstance(first_value, str):
                # 如果第一个value是字符串
                clean_inputs = {"input": inputs.get("user_input", "")}
                memory.save_context(clean_inputs, {"output": first_value})
            else:
                logger.warning(f"Skipping memory save: first output value is not a string: {outputs}")
        else:
            logger.warning(f"Skipping memory save due to error in outputs: {outputs}")

        if outputs.get("extracted_events"):
            events.extend(outputs.get("extracted_events", []))
        if outputs.get("extracted_evidence"):
            evidences.extend(outputs.get("extracted_evidence", []))

        if outputs.get("deduplicated_events"):
            events.extend(outputs.get("deduplicated_events", []))
        if outputs.get("deduplicated_evidence"):
            evidences.extend(outputs.get("deduplicated_evidence", []))

        if outputs.get("final_testimony"):
            final_message = outputs["final_testimony"]
            break

        if outputs.get("next_questions"):
            next_questions = outputs["next_questions"]
            if next_questions and isinstance(next_questions[0], dict):
                questions = [q["clarification_question"] for q in next_questions if "clarification_question" in q]
                final_message = "\n".join(questions)
            elif next_questions and isinstance(next_questions[0], str):
                final_message = "\n".join(next_questions)
            break

    if not final_message:
        final_message = "Agent reasoning completed but no conclusive output."

    events = sanitize_events(events)
    return ChatResponse(
            conversation_id=conversation_id,
            message=final_message,
            events=events,
            evidence=evidences
    )

def should_force_switch_tool(tool_name: str, tool_attempt_counter: dict, max_attempts: int = 2) -> bool:
    """
    Decide whether to force switch tool based on consecutive attempts.

    Args:
        tool_name (str): Current tool name.
        tool_attempt_counter (dict): A dict to track tool attempt counts.
        max_attempts (int): Maximum allowed consecutive attempts before forcing a switch.

    Returns:
        bool: Whether to force switch tool.
    """
    if tool_name not in tool_attempt_counter:
        tool_attempt_counter[tool_name] = 1
    else:
        tool_attempt_counter[tool_name] += 1

    if tool_attempt_counter[tool_name] > max_attempts:
        return True
    else:
        return False

def force_switch_tool(current_tool_name: str) -> str:
    """
    Force switch to the next logical tool based on the current tool.

    Args:
        current_tool_name (str): Current tool name.

    Returns:
        str: Next tool name.
    """

    NEXT_TOOL_MAP = {
        "extract_evidence": "extract_event",
        "extract_event": "detect_contradictions",
        "deduplicate_evidence": "detect_contradictions",
        "deduplicate_event": "detect_contradictions",
        "detect_contradictions": "check_chain_integrity",
        "check_chain_integrity": "finalize_testimony",
    }

    return NEXT_TOOL_MAP.get(current_tool_name, "finalize_testimony")  # 默认直接跳finalize

from datetime import datetime

def sanitize_events(events: list) -> list:
    sanitized = []
    for e in events:
        if not isinstance(e, dict):
            continue  # 跳过非字典
        event = e.copy()
        # 补confidence
        if "confidence" not in event:
            event["confidence"] = 1.0
        # 修event_date
        if "event_date" not in event or event["event_date"] in ("", None, "unknown"):
            event["event_date"] = datetime.utcnow()
        sanitized.append(event)
    return sanitized

