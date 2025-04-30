from fastapi import APIRouter, Depends, HTTPException, Body, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.database import Incident, TimelineEvent, Evidence, Base
from app.models import schemas
from app.models.database import Base
from app.models.database import Conversation
from app.models.database import Message
from app.models.database import User
from app.models.database import Affidavit
from app.models.database import Evidence as EvidenceModel
from app.models.database import TimelineEvent as TimelineEventModel
from app.models.database import Incident as IncidentModel
from app.database.database import get_db
from datetime import datetime
import logging

# JWT config (should match auth.py)
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication")

router = APIRouter()
logger = logging.getLogger(__name__)

# Dependency to get DB session
from app.database.database import get_db

@router.get("/", response_model=List[schemas.IncidentResponse], summary="List all incidents for the user")
def list_incidents(db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    logger.info(f"Listing incidents for user: {user_id}")
    incidents = db.query(IncidentModel).filter(IncidentModel.user_id == user_id).all()
    logger.info(f"Found {len(incidents)} incidents")
    return incidents

@router.get("/{incident_id}", response_model=schemas.IncidentResponse, summary="Get details for a single incident")
def get_incident(incident_id: str, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    incident = db.query(IncidentModel).filter(IncidentModel.id == incident_id, IncidentModel.user_id == user_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident

@router.post("/", response_model=schemas.IncidentResponse, status_code=status.HTTP_201_CREATED, summary="Create a new incident")
def create_incident(incident: schemas.IncidentCreate, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    db_incident = IncidentModel(
        title=incident.title,
        description=incident.description,
        status=incident.status or 'in_progress',
        location=incident.location,
        user_id=user_id,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident

@router.put("/{incident_id}", response_model=schemas.IncidentResponse, summary="Update an incident (e.g., mark as resolved)")
def update_incident(incident_id: str, update: schemas.IncidentUpdate, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    incident = db.query(IncidentModel).filter(IncidentModel.id == incident_id, IncidentModel.user_id == user_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    for field, value in update.dict(exclude_unset=True).items():
        setattr(incident, field, value)
    incident.updated_at = datetime.now()
    db.commit()
    db.refresh(incident)
    return incident

@router.post("/{incident_id}/timeline", response_model=schemas.TimelineEventResponse, status_code=status.HTTP_201_CREATED, summary="Add a timeline event to an incident")
def add_timeline_event(incident_id: str, event: schemas.TimelineEventCreate, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    incident = db.query(IncidentModel).filter(IncidentModel.id == incident_id, IncidentModel.user_id == user_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    db_event = TimelineEventModel(
        incident_id=incident_id,
        event_date=event.event_date,
        description=event.description,
        confidence_score=event.confidence_score,
        created_at=datetime.now(),
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.get("/{incident_id}/timeline", response_model=List[schemas.TimelineEventResponse], summary="Get timeline events for an incident")
def get_timeline_events(incident_id: str, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    """
    Get timeline events for an incident, sorted by event date.
    Returns events with formatted time (HH:MM AM/PM) and description.
    """
    # Only allow if user owns the incident
    incident = db.query(IncidentModel).filter(IncidentModel.id == incident_id, IncidentModel.user_id == user_id).first()
    logger.info(f"Incident: {incident}")
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    try:
        events = (
            db.query(TimelineEventModel)
            .filter(TimelineEventModel.incident_id == incident_id)
            .order_by(TimelineEventModel.event_date.desc())  # Most recent first
            .all()
        )
        logger.info(f"Events: {events}")
        # Convert to response models with proper time formatting
        response_events = []
        for event in events:
            try:
                response_event = schemas.TimelineEventResponse.from_orm(event)
                response_events.append(response_event)
            except Exception as e:
                logger.error(f"Error converting event {event.id}: {str(e)}")
                continue
                
        return response_events

    except Exception as e:
        logger.error(f"Error fetching timeline events: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error fetching timeline events"
        )

@router.get("/{incident_id}/evidence", response_model=List[schemas.EvidenceResponse], summary="Get exhibits/evidence for an incident")
def get_evidence(incident_id: str, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    # Only allow if user owns the incident
    incident = db.query(IncidentModel).filter(IncidentModel.id == incident_id, IncidentModel.user_id == user_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    evidence = db.query(EvidenceModel).filter(EvidenceModel.incident_id == incident_id).all()
    return evidence

class ConversationStartRequest(schemas.BaseModel):
    title: str
    description: str = ""
    first_message: str = ""
    incident_id: Optional[str] = None

@router.post("/start_conversation", summary="Start a conversation, creating an incident if needed")
def start_conversation(
    req: ConversationStartRequest = Body(...),
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    # If no incident_id, create a new incident
    if not req.incident_id:
        incident = IncidentModel(
            title=req.title,
            description=req.description,
            status='in_progress',
            user_id=user_id,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        db.add(incident)
        db.commit()
        db.refresh(incident)
        incident_id = incident.id
    else:
        incident = db.query(IncidentModel).filter(IncidentModel.id == req.incident_id, IncidentModel.user_id == user_id).first()
        if not incident:
            raise HTTPException(status_code=404, detail="Incident not found")
        incident_id = incident.id
    # Create the conversation
    conversation = Conversation(
        user_id=user_id,
        incident_id=incident_id,
        title=req.title,
        status='active',
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    # Optionally, add the first message
    if req.first_message:
        message = Message(
            conversation_id=conversation.id,
            role='user',
            content=req.first_message,
            created_at=datetime.now(),
        )
        db.add(message)
        db.commit()
    return {
        "incident_id": incident_id,
        "conversation_id": conversation.id
    }

@router.delete("/{incident_id}", status_code=204, summary="Delete an incident")
def delete_incident(incident_id: str, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    incident = db.query(IncidentModel).filter(IncidentModel.id == incident_id, IncidentModel.user_id == user_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    db.delete(incident)
    db.commit()
    return 

@router.get("/{incident_id}/conversations", response_model=List[schemas.ConversationResponse], summary="Get conversations for an incident")
def get_incident_conversations(incident_id: str, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    """
    Get all conversations and their messages for an incident.
    """
    # Check if incident exists and belongs to user
    incident = db.query(IncidentModel).filter(
        IncidentModel.id == incident_id,
        IncidentModel.user_id == user_id
    ).first()
    logger.info(f"/conversation - Incident: {incident}")
    
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    try:
        # Get conversations with their messages
        conversations = (
            db.query(Conversation)
            .filter(Conversation.incident_id == incident_id)
            .order_by(Conversation.created_at.desc())
            .all()
        )
        logger.info(f"/conversation - Conversations: {conversations}")

        # Load messages for each conversation
        for conv in conversations:
            conv.messages = (
                db.query(Message)
                .filter(Message.conversation_id == conv.id)
                .order_by(Message.created_at.asc())
                .all()
            )

        return conversations

    except Exception as e:
        logger.error(f"Error fetching conversations: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error fetching conversations"
        ) 