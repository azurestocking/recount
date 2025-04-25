from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.database import Base, Conversation, Message, TimelineEvent, Evidence
from app.models.schemas import MessageRequest, ChatResponse
from datetime import datetime
import json
from typing import List, Optional

class AIAgent:
    def __init__(self, db_url: str):
        engine = create_engine(db_url)
        SessionLocal = sessionmaker(bind=engine)
        self.db = SessionLocal()

    async def process_message(self, user_id: str, message: str, conversation_id: Optional[str] = None) -> ChatResponse:
        """Main method to process incoming messages"""
        try:
            # 1. Create or get existing conversation
            if conversation_id:
                # Try to get the specified conversation
                conversation = self.db.query(Conversation).filter(Conversation.id == conversation_id).first()
                if not conversation:
                    # If conversation doesn't exist, create a new one
                    conversation = self._get_or_create_conversation(user_id)
            else:
                # No conversation_id provided, create or get existing one
                conversation = self._get_or_create_conversation(user_id)

            # 2. Store user message
            user_message = self._store_message(
                conversation_id=conversation.id,
                role="user",
                content=message
            )

            # 3. Process with AI
            ai_response = await self._generate_ai_response(message)

            # 4. Store AI response
            ai_message = self._store_message(
                conversation_id=conversation.id,
                role="assistant",
                content=ai_response["response"],
                tokens_used=ai_response["tokens"]
            )

            # 5. Process and store any extracted information
            self._process_extracted_info(
                conversation=conversation,
                ai_response=ai_response,
                source_message=ai_message
            )

            self.db.commit()

            return ChatResponse(
                conversation_id=conversation.id,
                message=ai_response["response"],
                events=ai_response.get("events", []),
                evidence=ai_response.get("evidence", [])
            )

        except Exception as e:
            self.db.rollback()
            print(f"Error processing message: {str(e)}")
            raise

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
                        description=evidence_item["description"]
                    )
                    self.db.add(evidence)

        except Exception as e:
            self.db.rollback()
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