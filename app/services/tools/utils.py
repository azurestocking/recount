import json
import logging
import openai
from app.config.config import OPENAI_API_KEY
from typing import List, Dict, Any

# Extract Evidences automatically
async def extract_evidence_from_text(user_input: str) -> list:
    """Extract eapp.services.idence from a given user input text."""
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an evidence extraction assistant. From the user's statement, extract all information that can serve as evidence. Return a JSON list. Each item should include 'type' (e.g., document, photo, witness statement) and 'description'. If there is no evidence, return an empty list."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.9,
            max_tokens=300
        )
        extracted = response.choices[0].message.content.strip()
        return json.loads(extracted)
    except Exception as e:
        logging.error(f"Error extracting evidence: {e}")
        return []

# Extract Evidents automatically
async def extract_events_from_text(user_input: str) -> list:
    """Extract timeline events from a given user input text."""
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an event extraction assistant. From the user's statement, extract all timeline events. Return a JSON list. Each item should include 'description' and 'event_date' (if the date is unknown, use 'unknown'). If there are no events, return an empty list."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.9,
            max_tokens=300
        )
        extracted = response.choices[0].message.content.strip()
        return json.loads(extracted)
    except Exception as e:
        logging.error(f"Error extracting events: {e}")
        return []

# Deduplicate evidences with evidences in local database
async def deduplicate_evidences_from_db(db_session, new_evidences: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Deduplicate evidences by batch semantic comparison."""
    from app.models.database import Evidence  # 避免循环引用

    existing_evidences = db_session.query(Evidence).all()
    existing_descriptions = [evi.description for evi in existing_evidences if evi.description]

    if not existing_descriptions or not new_evidences:
        return new_evidences

    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)

        existing_list_text = "\n".join([f"{idx + 1}. {desc}" for idx, desc in enumerate(existing_descriptions)])
        new_list_text = "\n".join([f"{idx + 1}. {evi['description']}" for idx, evi in enumerate(new_evidences)])

        prompt = (
            f"You are a semantic duplication detector.\n\n"
            f"Existing evidences:\n{existing_list_text}\n\n"
            f"New evidences:\n{new_list_text}\n\n"
            f"For each new evidence, determine if it duplicates any existing one.\n"
            f"Return a JSON array of {{'new_evidence_index', 'is_duplicate'}}."
        )

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=1000
        )

        duplication_results = json.loads(response.choices[0].message.content.strip())
        non_duplicate_evidences = [
            new_evidences[item['new_evidence_index'] - 1]
            for item in duplication_results if not item['is_duplicate']
        ]
        return non_duplicate_evidences

    except Exception as e:
        logging.error(f"Error during evidence deduplication: {e}")
        return new_evidences

# Deduplicate events with events in local database
async def deduplicate_events_from_db(db_session, new_events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Deduplicate events by batch semantic comparison."""
    from app.models.database import TimelineEvent

    existing_events = db_session.query(TimelineEvent).all()
    existing_descriptions = [event.description for event in existing_events if event.description]

    if not existing_descriptions or not new_events:
        return new_events

    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)

        existing_list_text = "\n".join([f"{idx + 1}. {desc}" for idx, desc in enumerate(existing_descriptions)])
        new_list_text = "\n".join([f"{idx + 1}. {ev['description']}" for idx, ev in enumerate(new_events)])

        prompt = (
            f"You are a semantic duplication detector.\n\n"
            f"Existing timeline events:\n{existing_list_text}\n\n"
            f"New timeline events:\n{new_list_text}\n\n"
            f"For each new event, determine if it duplicates any existing one.\n"
            f"Return a JSON array of {{'new_event_index', 'is_duplicate'}}."
        )

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=1000
        )

        duplication_results = json.loads(response.choices[0].message.content.strip())
        non_duplicate_events = [
            new_events[item['new_event_index'] - 1]
            for item in duplication_results if not item['is_duplicate']
        ]
        return non_duplicate_events

    except Exception as e:
        logging.error(f"Error during event deduplication: {e}")
        return new_events

# Detect if there is contradictions in the statement
async def detect_contradictions_from_memory(memory_summary: str, user_input: str) -> List[str]:
    """Detect contradictions between memory and new input."""
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)

        prompt = (
            f"You are a contradiction detection assistant.\n\n"
            f"Conversation history:\n{memory_summary}\n\n"
            f"New statement:\n{user_input}\n\n"
            f"Identify contradictions and return clarification questions in JSON array. Return empty array if none."
        )

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=500
        )

        clarifications = json.loads(response.choices[0].message.content.strip())
        return clarifications

    except Exception as e:
        logging.error(f"Error in contradiction detection: {e}")
        return []

# Detect if the evidence chain is broken or not
async def detect_broken_evidence_chain(events: List[Dict[str, Any]], evidences: List[Dict[str, Any]]) -> List[str]:
    """Check if events + evidences form a complete logical chain."""
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)

        events_text = "\n".join([f"- {ev['description']}" for ev in events])
        evidences_text = "\n".join([f"- {evi['description']}" for evi in evidences])

        prompt = (
            f"You are a chain completeness checker.\n\n"
            f"Timeline events:\n{events_text}\n\n"
            f"Evidences:\n{evidences_text}\n\n"
            f"Analyze chain completeness.\n"
            f"List follow-up questions if any link is missing. Return empty array if chain is complete."
        )

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=500
        )

        follow_ups = json.loads(response.choices[0].message.content.strip())
        return follow_ups

    except Exception as e:
        logging.error(f"Error in broken chain detection: {e}")
        return []


# Detect if there is follow-up questions, if there is not, generate the victim testimony
# async def finalize_victim_testimony(memory_summary: str, clarifications: List[str], follow_ups: List[str]) -> Dict[str, Any]:
#     """Finalize victim testimony if complete, or suggest questions."""
#     try:
#         client = openai.OpenAI(api_key=OPENAI_API_KEY)
#
#         if not clarifications and not follow_ups:
#             prompt = (
#                 f"You are a legal assistant.\n\n"
#                 f"Based on the conversation history below, generate a formal and concise victim testimony in English.\n\n"
#                 f"{memory_summary}\n\n"
#                 f"The testimony should be chronological and fact-based."
#             )
#
#             response = client.chat.completions.create(
#                 model="gpt-4",
#                 messages=[{"role": "user", "content": prompt}],
#                 temperature=0,
#                 max_tokens=800
#             )
#
#             testimony = response.choices[0].message.content.strip()
#
#             return {
#                 "final_testimony": testimony,
#                 "next_questions": []
#             }
#         else:
#             return {
#                 "final_testimony": None,
#                 "next_questions": clarifications + follow_ups
#             }
#
#     except Exception as e:
#         logging.error(f"Error in finalization: {e}")
#         return {
#             "final_testimony": None,
#             "next_questions": []
#         }

async def finalize_victim_testimony(memory_summary: str, clarifications: List[str], follow_ups: List[str]) -> Dict[str, Any]:
    """Finalize victim testimony if complete, or suggest questions."""
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)

        if not clarifications and not follow_ups:
            prompt = (
                f"You are an empathetic legal assistant specializing in drafting affidavits based on victims' conversations.\n\n"

                f"You are given the conversation history between you and the victim so far.\n\n"
                                f"{memory_summary}\n\n"
                
                f"First, carefully review all prior inputs from the victim.\n\n"
                
                f"Determine whether the cumulative information is sufficient to draft a full affidavit.\n\n"
                f"The affidavit must include:\n\n"
                
                f"the affiant’s identity information (such as name, approximate age, occupation, and/or relationship to the matter),\n\n"
                
                f"a clear factual description of the key events,\n\n"
                
                f"an approximate timeline (when the events happened),\n\n"
                
                f"locations (where events took place),\n\n"
                
                f"and other critical factual details that an affidavit typically requires.\n\n"
                
                f"If the conversation history provides all these key elements, respond:\n\n"
                
                f"I understand your experience. Based on the information you shared, I will now generate a complete affidavit for you:' Then immediately proceed to draft the affidavit in formal language.\n\n"
                
                f"If the information is incomplete, first reassure and comfort the victim with a gentle sentence (e.g., 'Thank you for sharing this. You are doing an amazing job telling your story, and it’s perfectly okay to take things step by step.'\n\n"
                f"Then, ask one or two soft, specific follow-up questions designed to gather the missing critical details (e.g., 'If you feel comfortable, could you share when this happened?" or "Could you tell me roughly where this took place?')."
                
                f"Maintain a warm, supportive, and non-judgmental tone at all times.\n\n"
                f"Prioritize making the victim feel safe and empowered to continue sharing at their own pace.")

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.9,
                max_tokens=800
            )

            testimony = response.choices[0].message.content.strip()

            return {
                "final_testimony": testimony,
                "next_questions": []
            }
        else:
            return {
                "final_testimony": None,
                "next_questions": clarifications + follow_ups
            }

    except Exception as e:
        logging.error(f"Error in finalization: {e}")
        return {
            "final_testimony": None,
            "next_questions": []
        }