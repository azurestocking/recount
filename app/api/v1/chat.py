from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import MessageRequest, ChatResponse
from app.services.aiAgent import AIAgent
from app.config.dependencies import get_ai_agent
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: MessageRequest,
    agent: AIAgent = Depends(get_ai_agent)
):
    """
    Process a chat message with the AI agent
    """
    try:
        role = "user"
        if request.user_id.startswith('guest-'):
            role = "guest"

        logger.info(f"Processing chat message for user {request.user_id}")
        response = await agent.process_message(
            user_id=request.user_id,
            message=request.message,
            role=role,
            conversation_id=request.conversation_id
        )
        
        logger.info(f"Successfully processed message for user {request.user_id}")
        return response
    except Exception as e:
        logger.error(f"Error processing message for user {request.user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversations/{conversation_id}/history")
async def get_conversation_history(
    conversation_id: str,
    agent: AIAgent = Depends(get_ai_agent)
):
    """
    Get the history of a conversation
    """
    try:
        logger.info(f"Getting conversation history for {conversation_id}")
        history = agent.get_conversation_history(conversation_id)
        logger.info(f"Successfully retrieved history for conversation {conversation_id}")
        return {"history": history}
    except Exception as e:
        logger.error(f"Error getting conversation history for {conversation_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversations/{conversation_id}/timeline")
async def get_timeline(
    conversation_id: str,
    agent: AIAgent = Depends(get_ai_agent)
):
    """
    Get timeline events for a conversation
    """
    try:
        logger.info(f"Getting timeline for conversation {conversation_id}")
        timeline = agent.get_timeline_events(conversation_id)
        logger.info(f"Successfully retrieved timeline for conversation {conversation_id}")
        return {"timeline": timeline}
    except Exception as e:
        logger.error(f"Error getting timeline for conversation {conversation_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users/{user_id}/conversations")
async def get_user_conversations(
    user_id: str,
    agent: AIAgent = Depends(get_ai_agent)
):
    """
    Get all conversations for a user
    """
    try:
        logger.info(f"Getting conversations for user {user_id}")
        conversations = agent.get_user_conversations(user_id)
        logger.info(f"Successfully retrieved conversations for user {user_id}")
        return {"conversations": conversations}
    except Exception as e:
        logger.error(f"Error getting conversations for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
