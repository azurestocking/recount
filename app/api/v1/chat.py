from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import MessageRequest, ChatResponse
from app.services.aiAgent import AIAgent
from app.config.dependencies import get_ai_agent
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


# POST /chat
@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(
        request: MessageRequest,
        agent: AIAgent = Depends(get_ai_agent)
):
    """
    Handle incoming user message and generate AI response.
    """
    try:
        role = "user"
        if request.user_id.startswith("guest-"):
            role = "guest"

        logger.info(f"[Chat] Received message from {request.user_id} with role={role}")

        response = await agent.process_message(
            user_id=request.user_id,
            message=request.message,
            role=role,
            conversation_id=request.conversation_id
        )

        if response is None:
            logger.error(f"[Chat] agent.process_message returned None for {request.user_id}")
            return ChatResponse(
                message="Agent failed to generate a response.",
                conversation_id=None,
                events=[],
                evidence=[]
            )

        logger.info(f"[Chat] Successfully processed message for {request.user_id}")
        return response

    except Exception as e:
        import traceback
        logger.error(f"[Chat] Exception: {str(e)}")
        logger.error(traceback.format_exc())

        return ChatResponse(
            message=f"Server error: {str(e)}",
            conversation_id=None,
            events=[],
            evidence=[]
        )


# GET /conversations/{conversation_id}/history
@router.get("/conversations/{conversation_id}/history")
async def get_conversation_history(
        conversation_id: str,
        agent: AIAgent = Depends(get_ai_agent)
):
    """
    Retrieve conversation history by conversation ID.
    """
    try:
        logger.info(f"[History] Retrieving history for conversation {conversation_id}")
        history = agent.get_conversation_history(conversation_id)
        return {"history": history}
    except Exception as e:
        logger.error(f"[History] Error retrieving history: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


# GET /conversations/{conversation_id}/timeline
@router.get("/conversations/{conversation_id}/timeline")
async def get_conversation_timeline(
        conversation_id: str,
        agent: AIAgent = Depends(get_ai_agent)
):
    """
    Retrieve timeline events by conversation ID.
    """
    try:
        logger.info(f"[Timeline] Retrieving timeline for conversation {conversation_id}")
        timeline = agent.get_timeline_events(conversation_id)
        return {"timeline": timeline}
    except Exception as e:
        logger.error(f"[Timeline] Error retrieving timeline: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


# GET /users/{user_id}/conversations
@router.get("/users/{user_id}/conversations")
async def get_user_conversations(
        user_id: str,
        agent: AIAgent = Depends(get_ai_agent)
):
    """
    Retrieve all conversations for a specific user.
    """
    try:
        logger.info(f"[UserConversations] Retrieving conversations for user {user_id}")
        conversations = agent.get_user_conversations(user_id)
        return {"conversations": conversations}
    except Exception as e:
        logger.error(f"[UserConversations] Error retrieving conversations: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

