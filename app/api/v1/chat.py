from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from app.models.schemas import MessageRequest, ChatResponse
from app.services.aiAgent import AIAgent
from app.config.dependencies import get_ai_agent
import logging
import speech_recognition as sr
import tempfile
import os
from pydub import AudioSegment
import io
import base64
import requests
import subprocess
import shutil

router = APIRouter()
logger = logging.getLogger(__name__)


# Path to ffmpeg executable
FFMPEG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                           "temp", "ffmpeg-2025-04-23-git-25b0a8e295-essentials_build", "bin", "ffmpeg.exe")


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
@router.post("/speech-to-text")
async def speech_to_text(audio_file: UploadFile = File(...)):
    """
    Convert speech from an audio file to text
    """
    input_temp_path = None
    output_temp_path = None
    
    try:
        logger.info("Processing speech-to-text conversion")
        
        # Read the uploaded file content
        content = await audio_file.read()
        
        # Create temporary files for input and output
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as input_temp_file:
            input_temp_file.write(content)
            input_temp_path = input_temp_file.name
            
        output_temp_path = input_temp_path.replace(".webm", ".wav")
        
        try:
            # Use ffmpeg to convert the audio to WAV format
            logger.info(f"Converting audio using ffmpeg from {input_temp_path} to {output_temp_path}")
            logger.info(f"FFMPEG_PATH: {FFMPEG_PATH}")
            
            # Check if ffmpeg exists
            if not os.path.exists(FFMPEG_PATH):
                logger.error(f"FFmpeg not found at {FFMPEG_PATH}")
                raise HTTPException(status_code=500, detail="FFmpeg not found")
            
            # Run ffmpeg command
            result = subprocess.run([
                FFMPEG_PATH,
                "-i", input_temp_path,
                "-acodec", "pcm_s16le",
                "-ar", "16000",
                "-ac", "1",
                output_temp_path
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"FFmpeg conversion failed: {result.stderr}")
                raise HTTPException(status_code=500, detail=f"Audio conversion failed: {result.stderr}")
            
            logger.info("Audio conversion successful")
            
            # Initialize recognizer
            recognizer = sr.Recognizer()
            text = None
            
            # Process the converted audio file
            with sr.AudioFile(output_temp_path) as source:
                # Adjust for ambient noise to improve recognition
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio_data = recognizer.record(source)
                
                # Use Google's speech recognition
                text = recognizer.recognize_google(audio_data)
                
                logger.info(f"Successfully converted speech to text: {text}")
            
            # Clean up temporary files after the audio file is closed
            if input_temp_path and os.path.exists(input_temp_path):
                os.unlink(input_temp_path)
            if output_temp_path and os.path.exists(output_temp_path):
                os.unlink(output_temp_path)
            
            return {"text": text}
                
        except sr.UnknownValueError:
            logger.error("Speech recognition could not understand audio")
            raise HTTPException(status_code=400, detail="Could not understand audio")
        except sr.RequestError as e:
            logger.error(f"Speech recognition service error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Speech recognition service error: {str(e)}")
        except Exception as e:
            logger.error(f"Error processing audio file: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing audio file: {str(e)}")
            
    except Exception as e:
        logger.error(f"Error in speech-to-text conversion: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in speech-to-text conversion: {str(e)}")
    finally:
        # Clean up temporary files in case of any errors
        try:
            if input_temp_path and os.path.exists(input_temp_path):
                os.unlink(input_temp_path)
            if output_temp_path and os.path.exists(output_temp_path):
                os.unlink(output_temp_path)
        except Exception as e:
            logger.error(f"Error cleaning up temporary files: {str(e)}")

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

