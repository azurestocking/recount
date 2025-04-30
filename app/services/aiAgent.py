from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.database import Base, Conversation, Message, TimelineEvent, Evidence
from app.models.schemas import MessageRequest, ChatResponse
from datetime import datetime
from typing import List, Optional, Dict, Any
import logging

from app.config.config import OPENAI_API_KEY
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationSummaryBufferMemory
from app.services.agent.agent_loop import agent_reasoning_loop
from app.services.faiss_connector import save_evidence_and_refresh
from app.services.tools.tool_registry import TOOL_REGISTRY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIAgent:
    def __init__(self, db_url: str):
        engine = create_engine(db_url)
        SessionLocal = sessionmaker(bind=engine)
        self.db = SessionLocal()

        # Initialize memory
        self.memory = ConversationSummaryBufferMemory(
            llm=ChatOpenAI(
                temperature=0,
                model="gpt-3.5-turbo",
                openai_api_key=OPENAI_API_KEY
            ),
            max_token_limit=3000,
            memory_key="history",
            return_messages=True
        )

    async def process_message(self, user_id: str, message: str, role: str, conversation_id: Optional[str] = None) -> ChatResponse:
        """Main method to process incoming messages"""

        try:
            conversation = None
            logger.info(f"Processing message for user {user_id} with role {role} and conversation_id {conversation_id}")

            if role == "user":
                # 1. Create or get conversation
                if conversation_id:
                    conversation = self.db.query(Conversation).filter(Conversation.id == conversation_id).first()
                    if not conversation:
                        conversation = self._get_or_create_conversation(user_id)
                else:
                    conversation = self._get_or_create_conversation(user_id)

                # 2. Store user message
                logger.info(f"Storing user message: {message}")
                user_message = self._store_message(
                    conversation_id=conversation.id,
                    role=role,
                    content=message
                )

                # 3. Call agent reasoning loop
                logger.info(f"Calling agent reasoning loop for message")
                agent_output = await agent_reasoning_loop(
                    user_input=message,
                    db_session=self.db,
                    memory=self.memory,
                    conversation_id=conversation.id
                )

                if agent_output is None:
                    logger.error(f"agent_reasoning_loop returned None for user {user_id}")
                    return ChatResponse(
                        conversation_id=conversation.id if conversation else None,
                        message="Agent failed to generate a valid response.",
                        events=[],
                        evidence=[]
                    )

                # 4. Based on output, decide what to save
                final_response = agent_output.message
                events = agent_output.events
                evidences = agent_output.evidence

                # 5. Store AI response
                ai_message = self._store_message(
                    conversation_id=conversation.id,
                    role="assistant",
                    content=final_response
                )

                # 6. Commit
                self.db.commit()

            elif role == "guest":
                logger.info(f"[Guest] Processing guest message without DB storage")

                agent_output = await agent_reasoning_loop(
                    user_input=message,
                    db_session=self.db,
                    memory=self.memory,
                    conversation_id=None
                )

                if agent_output is None:
                    logger.error(f"agent_reasoning_loop returned None for guest {user_id}")
                    return ChatResponse(
                        conversation_id=None,
                        message="Agent failed to generate a valid response.",
                        events=[],
                        evidence=[]
                    )

                final_response = agent_output.message
                events = agent_output.events
                evidences = agent_output.evidence

                ai_message = self._store_message(
                    conversation_id=None,
                    role="assistant",
                    content=final_response
                )

                # 6. Commit
                self.db.commit()

            return ChatResponse(
                    conversation_id=None,
                    message=final_response,
                    events=events,
                    evidence=evidences
                )

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error processing message: {str(e)}")

            return ChatResponse(
                message="An error occurred while processing your message.",
                conversation_id=conversation_id,
                events=[],
                evidence=[]
            )

    def _get_or_create_conversation(self, user_id: str) -> Conversation:
        """Create new conversation or get existing active one"""
        try:
            conversation = (
                self.db.query(Conversation)
                .filter(Conversation.user_id == user_id, Conversation.status == 'active')
                .order_by(Conversation.created_at.desc())
                .first()
            )

            if conversation:
                return conversation

            conversation = Conversation(user_id=user_id)
            self.db.add(conversation)
            self.db.flush()  # Flush to get the id but don't commit yet
            return conversation

        except Exception as e:
            self.db.rollback()
            raise

    def _store_message(self, conversation_id: str, role: str, content: str, tokens_used: int = 0) -> Message:
        """Store a message in the database"""
        try:
            message = Message(
                conversation_id=conversation_id,
                role=role,
                content=content,
                tokens_used=tokens_used,
                message_metadata={
                    "timestamp": datetime.now().isoformat(),
                    "processed": False
                }
            )
            self.db.add(message)
            self.db.flush()  # Flush to get the id but don't commit yet
            return message

        except Exception as e:
            self.db.rollback()
            raise

    def _process_extracted_info(self, conversation: Conversation, ai_response: dict, source_message: Message):
        """Process and store extracted information"""
        try:
            # Store timeline events
            if "events" in ai_response:
                for event in ai_response["events"]:
                    timeline_event = TimelineEvent(
                        conversation_id=conversation.id,
                        source_message_id=source_message.id,
                        event_date=event["event_date"],
                        description=event["description"],
                        confidence_score=event["confidence"]
                    )
                    self.db.add(timeline_event)

            # Store evidence
            if "evidence" in ai_response:
                for evidence_item in ai_response["evidence"]:
                    evidence = Evidence(
                        conversation_id=conversation.id,
                        type=evidence_item["type"],
                        file_path=evidence_item["path"],
                        description=evidence_item["description"],
                        metadata=evidence_item.get("metadata", None)
                    )
                    self.db.add(evidence)
                    self.db.flush()  # 拿到 evidence.id

                    # ✅ 插入完 evidence，同时保存 embedding 并且刷新 cache
                    if evidence.description:
                        save_evidence_and_refresh(self.db, evidence.id, evidence.description)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error in _process_extracted_info: {e}")
            raise

    async def _generate_ai_response(self, message: str) -> dict:
        """Generate AI response and extract information"""
        # This is where you'd integrate with your AI model
        # Example structure:
        return {
            "response": "AI generated response",
            "tokens": 150,
            "events": [
                {
                    "description": "Extracted event",
                    "confidence": 0.95,
                    "event_date": datetime.now()
                }
            ],
            "evidence": [
                {
                    "type": "document",
                    "path": "/path/to/file.pdf",
                    "description": "Supporting document"
                }
            ]
        }

    def close(self):
        self.db.close()

    def get_conversation_history(self, conversation_id: str) -> List[dict]:
        """Get all messages for a specific conversation"""
        try:
            messages = (
                self.db.query(Message)
                .filter(Message.conversation_id == conversation_id)
                .order_by(Message.created_at.asc())
                .all()
            )
            
            return [
                {
                    "id": message.id,
                    "role": message.role,
                    "content": message.content,
                    "created_at": message.created_at.isoformat(),
                    "tokens_used": message.tokens_used
                }
                for message in messages
            ]
            
        except Exception as e:
            self.db.rollback()
            raise

    def get_user_conversations(self, user_id: str) -> List[dict]:
        """Get all conversations for a user"""
        try:
            conversations = (
                self.db.query(Conversation)
                .filter(Conversation.user_id == user_id)
                .order_by(Conversation.created_at.desc())
                .all()
            )
            
            return [
                {
                    "id": conv.id,
                    "status": conv.status,
                    "title": conv.title,
                    "created_at": conv.created_at.isoformat(),
                    "updated_at": conv.updated_at.isoformat()
                }
                for conv in conversations
            ]
            
        except Exception as e:
            self.db.rollback()
            raise

    def get_timeline_events(self, conversation_id: str) -> List[dict]:
        """Get timeline events for a conversation"""
        try:
            # Query timeline events for the conversation
            events = (
                self.db.query(TimelineEvent)
                .filter(TimelineEvent.conversation_id == conversation_id)
                .order_by(TimelineEvent.event_date.asc())
                .all()
            )
            
            # Format events for response
            return [
                {
                    "time": event.event_date.isoformat(),
                    "title": event.description,
                    "description": event.description,
                    "confidence": event.confidence_score
                }
                for event in events
            ]
            
        except Exception as e:
            self.db.rollback()
            print(f"Error getting timeline events: {str(e)}")
            raise

    # Extract Evidences automatically
    # async def extract_evidence(self, user_input: str) -> List[Dict[str, Any]]:
    #     """Extract evidence from user input"""
    #     try:
    #         client = openai.OpenAI(api_key=OPENAI_API_KEY)
    #         response = client.chat.completions.create(
    #             model="gpt-4",
    #             messages=[
    #                 {"role": "system", "content": "You are an evidence extraction assistant. From the user's statement, extract all information that can serve as evidence. Return a JSON list. Each item should include 'type' (e.g., document, photo, witness statement) and 'description'. If there is no evidence, return an empty list."},
    #                 {"role": "user", "content": user_input}
    #             ],
    #             temperature=0,
    #             max_tokens=300
    #         )
    #         extracted = response.choices[0].message.content.strip()
    #         return json.loads(extracted)
    #     except Exception as e:
    #         logging.error(f"Error extracting evidence: {e}")
    #         return []
    #
    # # Extract Evidents automatically
    # async def extract_events(self, user_input: str) -> List[Dict[str, Any]]:
    #     """Extract timeline events from user input"""
    #     try:
    #         client = openai.OpenAI(api_key=OPENAI_API_KEY)
    #         response = client.chat.completions.create(
    #             model="gpt-4",
    #             messages=[
    #                 {"role": "system", "content": "You are an event extraction assistant. From the user's statement, extract all timeline events. Return a JSON list. Each item should include 'description' and 'event_date' (if the date is unknown, use 'unknown'). If there are no events, return an empty list."},
    #                 {"role": "user", "content": user_input}
    #             ],
    #             temperature=0,
    #             max_tokens=300
    #         )
    #         extracted = response.choices[0].message.content.strip()
    #         return json.loads(extracted)
    #     except Exception as e:
    #         logging.error(f"Error extracting events: {e}")
    #         return []

    # # Deduplicate evidences with evidences in local database
    # async def deduplicate_evidences(self, new_evidences: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    #     """Deduplicate evidences by sending all at once to GPT for batch semantic comparison."""
    #     existing_evidences = self.db.query(Evidence).all()
    #     existing_descriptions = [evi.description for evi in existing_evidences if evi.description]
    #
    #     if not existing_descriptions or not new_evidences:
    #         return new_evidences  # Nothing to compare
    #
    #     client = openai.OpenAI(api_key=OPENAI_API_KEY)
    #
    #     try:
    #         existing_list_text = "\n".join([f"{idx + 1}. {desc}" for idx, desc in enumerate(existing_descriptions)])
    #         new_list_text = "\n".join([f"{idx + 1}. {evi['description']}" for idx, evi in enumerate(new_evidences)])
    #
    #         prompt = (
    #             f"You are a semantic duplication detector.\n\n"
    #             f"Here is a list of existing evidences:\n{existing_list_text}\n\n"
    #             f"Here is a list of new evidences:\n{new_list_text}\n\n"
    #             f"For each new evidence, determine if it duplicates any existing evidence semantically.\n"
    #             f"Return a JSON array where each item includes:\n"
    #             f"- new_evidence_index (integer, starting from 1)\n"
    #             f"- is_duplicate (true or false)\n\n"
    #             f"Example Output:\n"
    #             f"[{{\"new_evidence_index\": 1, \"is_duplicate\": false}}, {{\"new_evidence_index\": 2, \"is_duplicate\": true}}]"
    #         )
    #
    #         response = client.chat.completions.create(
    #             model="gpt-4",
    #             messages=[
    #                 {"role": "system", "content": "You are a semantic duplication detector."},
    #                 {"role": "user", "content": prompt}
    #             ],
    #             temperature=0,
    #             max_tokens=1000
    #         )
    #
    #         answer = response.choices[0].message.content.strip()
    #         duplication_results = json.loads(answer)
    #
    #         non_duplicate_evidences = []
    #         for item in duplication_results:
    #             idx = item['new_evidence_index'] - 1  # Convert back to 0-based index
    #             if not item['is_duplicate']:
    #                 non_duplicate_evidences.append(new_evidences[idx])
    #
    #         return non_duplicate_evidences
    #
    #     except Exception as e:
    #         logging.error(f"Error during batch evidence duplication check: {e}")
    #         return new_evidences  # Conservative fallback
    #
    # # Deduplicate events with events in local database
    # async def deduplicate_events(self, new_events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    #     """Deduplicate timeline events by sending all at once to GPT for batch semantic comparison."""
    #     existing_events = self.db.query(TimelineEvent).all()
    #     existing_descriptions = [event.description for event in existing_events if event.description]
    #
    #     if not existing_descriptions or not new_events:
    #         return new_events  # Nothing to compare
    #
    #     client = openai.OpenAI(api_key=OPENAI_API_KEY)
    #
    #     try:
    #         existing_list_text = "\n".join([f"{idx + 1}. {desc}" for idx, desc in enumerate(existing_descriptions)])
    #         new_list_text = "\n".join([f"{idx + 1}. {ev['description']}" for idx, ev in enumerate(new_events)])
    #
    #         prompt = (
    #             f"You are a semantic duplication detector.\n\n"
    #             f"Here is a list of existing timeline events:\n{existing_list_text}\n\n"
    #             f"Here is a list of new timeline events:\n{new_list_text}\n\n"
    #             f"For each new event, determine if it duplicates any existing event semantically.\n"
    #             f"Return a JSON array where each item includes:\n"
    #             f"- new_event_index (integer, starting from 1)\n"
    #             f"- is_duplicate (true or false)\n\n"
    #             f"Example Output:\n"
    #             f"[{{\"new_event_index\": 1, \"is_duplicate\": false}}, {{\"new_event_index\": 2, \"is_duplicate\": true}}]"
    #         )
    #
    #         response = client.chat.completions.create(
    #             model="gpt-4",
    #             messages=[
    #                 {"role": "system", "content": "You are a semantic duplication detector."},
    #                 {"role": "user", "content": prompt}
    #             ],
    #             temperature=0,
    #             max_tokens=1000
    #         )
    #
    #         answer = response.choices[0].message.content.strip()
    #         duplication_results = json.loads(answer)
    #
    #         non_duplicate_events = []
    #         for item in duplication_results:
    #             idx = item['new_event_index'] - 1  # Convert back to 0-based index
    #             if not item['is_duplicate']:
    #                 non_duplicate_events.append(new_events[idx])
    #
    #         return non_duplicate_events
    #
    #     except Exception as e:
    #         logging.error(f"Error during batch event duplication check: {e}")
    #         return new_events  # Conservative fallback
    #
    # # Detect if there is contradictions in the statement
    # async def detect_contradictions(self, user_input: str) -> List[str]:
    #     """Detect contradictions between the new input and conversation history, return clarification questions if needed."""
    #     try:
    #         # Get summarized memory
    #         memory_context = self.memory.load_memory_variables({}).get('history', '')
    #
    #         prompt = (
    #             f"You are a contradiction detection assistant.\n\n"
    #             f"Here is the conversation history:\n{memory_context}\n\n"
    #             f"Here is the new statement:\n{user_input}\n\n"
    #             f"Analyze whether there are any contradictions or inconsistencies between the conversation history and the new statement.\n"
    #             f"If contradictions are found, list clarification questions to resolve them.\n"
    #             f"If there are no contradictions, return an empty JSON array [].\n\n"
    #             f"Example Output:\n"
    #             f"[\"Clarification question 1\", \"Clarification question 2\"]"
    #         )
    #
    #         client = openai.OpenAI(api_key=OPENAI_API_KEY)
    #         response = client.chat.completions.create(
    #             model="gpt-4",
    #             messages=[
    #                 {"role": "system", "content": "You are a contradiction detection assistant."},
    #                 {"role": "user", "content": prompt}
    #             ],
    #             temperature=0,
    #             max_tokens=500
    #         )
    #
    #         clarifications = json.loads(response.choices[0].message.content.strip())
    #         return clarifications
    #
    #     except Exception as e:
    #         logging.error(f"Error in contradiction detection: {e}")
    #         return []
    #
    # # Detect if the evidence chain is broken or not
    # async def detect_broken_chains(self, events: List[Dict[str, Any]], evidences: List[Dict[str, Any]]) -> List[str]:
    #     """Check if the collected events and evidences form a complete logical chain, and generate follow-up questions if missing."""
    #     try:
    #         events_text = "\n".join([f"- {ev['description']}" for ev in events])
    #         evidences_text = "\n".join([f"- {evi['description']}" for evi in evidences])
    #
    #         prompt = (
    #             f"You are a chain completeness checker.\n\n"
    #             f"Here are the extracted timeline events:\n{events_text}\n\n"
    #             f"Here are the extracted evidences:\n{evidences_text}\n\n"
    #             f"Analyze whether these events and evidences together form a complete logical sequence.\n"
    #             f"If any links are missing, generate follow-up questions to fill the gaps.\n"
    #             f"If the chain is complete, return an empty JSON array [].\n\n"
    #             f"Example Output:\n"
    #             f"[\"Follow-up question 1\", \"Follow-up question 2\"]"
    #         )
    #
    #         client = openai.OpenAI(api_key=OPENAI_API_KEY)
    #         response = client.chat.completions.create(
    #             model="gpt-4",
    #             messages=[
    #                 {"role": "system", "content": "You are a chain completeness checker."},
    #                 {"role": "user", "content": prompt}
    #             ],
    #             temperature=0,
    #             max_tokens=500
    #         )
    #
    #         follow_up_questions = json.loads(response.choices[0].message.content.strip())
    #         return follow_up_questions
    #
    #     except Exception as e:
    #         logging.error(f"Error in chain completeness detection: {e}")
    #         return []
    #
    # # Detect if there is follow-up questions, if there is not, generate the victim testimony
    # async def finalize_victim_testimony(self, user_input: str, clarifications: List[str], follow_ups: List[str]) -> \
    # Dict[str, Any]:
    #     """Finalize the victim testimony if the story is complete, otherwise suggest follow-up questions."""
    #     try:
    #         client = openai.OpenAI(api_key=OPENAI_API_KEY)
    #
    #         if not clarifications and not follow_ups:
    #             # No contradictions, no missing chain parts -> Summarize into formal testimony
    #             memory_context = self.memory.load_memory_variables({}).get('history', '')
    #
    #             prompt = (
    #                 f"You are a legal assistant.\n\n"
    #                 f"Based on the following conversation history, generate a formal and concise victim testimony in English:\n\n"
    #                 f"{memory_context}\n\n"
    #                 f"The testimony should be logically coherent, chronological, and fact-based."
    #             )
    #
    #             response = client.chat.completions.create(
    #                 model="gpt-4",
    #                 messages=[
    #                     {"role": "system", "content": "You are a legal assistant."},
    #                     {"role": "user", "content": prompt}
    #                 ],
    #                 temperature=0,
    #                 max_tokens=800
    #             )
    #
    #             final_testimony = response.choices[0].message.content.strip()
    #
    #             return {
    #                 "final_testimony": final_testimony,
    #                 "next_questions": []
    #             }
    #
    #         else:
    #             # If there are clarification or follow-up questions, prioritize them
    #             questions = clarifications + follow_ups
    #             return {
    #                 "final_testimony": None,
    #                 "next_questions": questions
    #             }
    #
    #     except Exception as e:
    #         logging.error(f"Error during finalization: {e}")
    #         return {
    #             "final_testimony": None,
    #             "next_questions": []
    #         }


    # async def generate_answer_with_graph_rag(self, user_query: str) -> Dict[str, Any]:
    #     """
    #     First iteration: extract evidence, extract events, update memory, and generate a simple AI response.
    #     """
    #     try:
    #         # Step 0: Update memory with user query
    #         self.memory.save_context({"input": user_query}, {})
    #
    #         # Step 1: Extract evidences
    #         evidence_list = await self.extract_evidence(user_query)
    #
    #         # Step 2: Extract events
    #         event_list = await self.extract_events(user_query)
    #
    #         # Step 3: Generate simple AI answer
    #         client = openai.OpenAI(api_key=OPENAI_API_KEY)
    #         response = client.chat.completions.create(
    #             model="gpt-4",
    #             messages=[
    #                 {"role": "system", "content": "You are a professional legal assistant. Based on the user's query and your current knowledge, generate a concise, logical, and professional response."},
    #                 {"role": "user", "content": user_query}
    #             ],
    #             temperature=0,
    #             max_tokens=500
    #         )
    #
    #         answer = response.choices[0].message.content.strip()
    #
    #         # Step 4: Update memory with AI response
    #         self.memory.save_context({"input": user_query}, {"output": answer})
    #
    #         # Step 5: Return standard format
    #         return {
    #             "response": answer,
    #             "tokens": response.usage.total_tokens,
    #             "evidence": evidence_list,
    #             "events": event_list
    #         }
    #
    #     except Exception as e:
    #         logging.error(f"Error in generate_answer_with_graph_rag: {e}")
    #         return {
    #             "response": "Sorry, an error occurred.",
    #             "tokens": 0,
    #             "evidence": [],
    #             "events": []
    #         }