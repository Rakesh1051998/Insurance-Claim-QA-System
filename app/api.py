"""
FastAPI Application for Insurance Claim Question-Answering System
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import uuid
from datetime import datetime
import json
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from app.retriever import QuestionRetriever
from app.state_fusion import extract_and_merge
from app.termination import should_terminate

# ============================================================================
# Pydantic Models
# ============================================================================

class SessionCreate(BaseModel):
    """Request to create a new session"""
    initial_message: Optional[str] = Field(
        None, 
        description="Optional initial description of the incident"
    )

class SessionResponse(BaseModel):
    """Response after creating a session"""
    session_id: str
    question: Optional[Dict[str, Any]] = None
    message: str

class AnswerRequest(BaseModel):
    """Request to submit an answer"""
    answer: str = Field(..., description="User's answer to the current question")

class AnswerResponse(BaseModel):
    """Response after submitting an answer"""
    session_id: str
    extracted_fields: List[str]
    next_question: Optional[Dict[str, Any]] = None
    is_complete: bool
    completion_percentage: float
    message: str

class ClaimState(BaseModel):
    """Current state of the claim"""
    session_id: str
    category: Optional[str] = None
    answered_questions: int
    extracted_fields: Dict[str, Any]
    completion_percentage: float
    mandatory_fields_status: Dict[str, bool]
    is_complete: bool

class ClaimSummary(BaseModel):
    """Complete claim summary"""
    session_id: str
    total_questions_asked: int
    total_turns: int
    claim_data: Dict[str, Any]
    completion_status: Dict[str, Any]
    conversation_history: List[Dict[str, Any]]

# ============================================================================
# In-Memory Session Storage
# ============================================================================

class SessionManager:
    """Manage claim sessions in memory"""
    
    def __init__(self, question_bank_path: str):
        self.retriever = QuestionRetriever(question_bank_path)
        self.sessions: Dict[str, Dict[str, Any]] = {}
    
    def create_session(self, initial_message: Optional[str] = None) -> tuple[str, Optional[Dict], str]:
        """Create a new claim session"""
        session_id = str(uuid.uuid4())
        
        claim_state = {
            "category": None,
            "answered_question_ids": [],
            "already_extracted_categories": []
        }
        
        conversation_history = []
        message = "Session created. Please describe the incident."
        question = None
        
        # If initial message provided, process it
        if initial_message:
            # Extract information from initial message
            extracted_categories = extract_and_merge(initial_message, claim_state)
            
            conversation_history.append({
                "turn": 0,
                "timestamp": datetime.now().isoformat(),
                "user_input": initial_message,
                "extracted_categories": extracted_categories,
                "question": None
            })
            
            # Get first question
            question = self.retriever.get_next_question(claim_state)
            
            if question:
                claim_state["answered_question_ids"].append(question["id"])
                message = "Information extracted. Here's your first question."
            else:
                message = "Thank you! We have all the information we need."
        else:
            # Get first question without processing
            question = self.retriever.get_next_question(claim_state)
            if question:
                claim_state["answered_question_ids"].append(question["id"])
        
        # Store session
        self.sessions[session_id] = {
            "session_id": session_id,
            "claim_state": claim_state,
            "conversation_history": conversation_history,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        return session_id, question, message
    
    def submit_answer(self, session_id: str, answer: str) -> tuple[List[str], Optional[Dict], bool, float, str]:
        """Submit an answer and get next question"""
        if session_id not in self.sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session = self.sessions[session_id]
        claim_state = session["claim_state"]
        
        # Extract information from answer
        extracted_categories = extract_and_merge(answer, claim_state)
        
        # Get current question (the one being answered)
        current_question = None
        if session["conversation_history"]:
            last_turn = session["conversation_history"][-1]
            current_question = last_turn.get("question")
        
        # Add to conversation history
        turn_number = len(session["conversation_history"])
        session["conversation_history"].append({
            "turn": turn_number,
            "timestamp": datetime.now().isoformat(),
            "user_input": answer,
            "extracted_categories": extracted_categories,
            "question": current_question
        })
        
        # Check if we should terminate
        should_stop, reason, status_info = should_terminate(claim_state, self.retriever.questions)
        
        completion_percentage = status_info.get("completion_percentage", 0)
        message = reason
        next_question = None
        
        if not should_stop:
            # Get next question
            next_question = self.retriever.get_next_question(claim_state)
            
            if next_question:
                claim_state["answered_question_ids"].append(next_question["id"])
                message = "Answer recorded. Here's the next question."
            else:
                should_stop = True
                message = "Thank you! We have all the information we need."
        
        session["updated_at"] = datetime.now().isoformat()
        
        return extracted_categories, next_question, should_stop, completion_percentage, message
    
    def get_session(self, session_id: str) -> Dict[str, Any]:
        """Get session state"""
        if session_id not in self.sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session = self.sessions[session_id]
        claim_state = session["claim_state"]
        
        # Calculate completion
        mandatory_fields = {
            "category": claim_state.get("category") is not None,
            "loss_datetime": claim_state.get("loss_datetime") is not None,
            "loss_location": claim_state.get("loss_location") is not None
        }
        
        completed = sum(1 for v in mandatory_fields.values() if v)
        completion_percentage = (completed / len(mandatory_fields)) * 100
        
        is_complete, _, _ = should_terminate(claim_state, self.retriever.questions)
        
        # Extract only the extracted fields (not metadata)
        extracted_fields = {
            k: v for k, v in claim_state.items() 
            if k not in ["answered_question_ids", "already_extracted_categories"]
        }
        
        return {
            "session_id": session_id,
            "category": claim_state.get("category"),
            "answered_questions": len(claim_state["answered_question_ids"]),
            "extracted_fields": extracted_fields,
            "completion_percentage": completion_percentage,
            "mandatory_fields_status": mandatory_fields,
            "is_complete": is_complete
        }
    
    def get_summary(self, session_id: str) -> Dict[str, Any]:
        """Get complete claim summary"""
        if session_id not in self.sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session = self.sessions[session_id]
        claim_state = session["claim_state"]
        
        # Calculate completion status
        mandatory_fields = {
            "category": claim_state.get("category") is not None,
            "loss_datetime": claim_state.get("loss_datetime") is not None,
            "loss_location": claim_state.get("loss_location") is not None
        }
        
        completed = sum(1 for v in mandatory_fields.values() if v)
        completion_percentage = (completed / len(mandatory_fields)) * 100
        
        return {
            "session_id": session_id,
            "total_questions_asked": len(claim_state["answered_question_ids"]),
            "total_turns": len(session["conversation_history"]),
            "claim_data": claim_state,
            "completion_status": {
                "completion_percentage": completion_percentage,
                "mandatory_fields": mandatory_fields
            },
            "conversation_history": session["conversation_history"]
        }
    
    def delete_session(self, session_id: str):
        """Delete a session"""
        if session_id not in self.sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        del self.sessions[session_id]
    
    def list_sessions(self) -> List[Dict[str, Any]]:
        """List all active sessions"""
        return [
            {
                "session_id": sid,
                "created_at": session["created_at"],
                "updated_at": session["updated_at"],
                "total_turns": len(session["conversation_history"])
            }
            for sid, session in self.sessions.items()
        ]


# ============================================================================
# FastAPI Application
# ============================================================================

app = FastAPI(
    title="Insurance Claim Question-Answering API",
    description="REST API for vehicle insurance claim intake with intelligent questioning",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize session manager
session_manager = None

@app.on_event("startup")
async def startup_event():
    """Initialize the session manager on startup"""
    global session_manager
    question_bank_path = "data/question_bank_validated.jsonl"
    session_manager = SessionManager(question_bank_path)
    print(f"✓ Loaded question bank from {question_bank_path}")
    print(f"✓ API server ready with {len(session_manager.retriever.questions)} questions")


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Insurance Claim Question-Answering API",
        "version": "1.0.0",
        "total_questions": len(session_manager.retriever.questions) if session_manager else 0,
        "active_sessions": len(session_manager.sessions) if session_manager else 0
    }


@app.post("/session", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(request: SessionCreate):
    """
    Create a new claim session
    
    Optionally provide an initial description of the incident.
    Returns a session ID and the first question.
    """
    session_id, question, message = session_manager.create_session(request.initial_message)
    
    return SessionResponse(
        session_id=session_id,
        question=question,
        message=message
    )


@app.post("/session/{session_id}/answer", response_model=AnswerResponse)
async def submit_answer(session_id: str, request: AnswerRequest):
    """
    Submit an answer and get the next question
    
    The system will extract relevant information from your natural language answer
    and return the next question if more information is needed.
    """
    extracted, next_question, is_complete, completion, message = session_manager.submit_answer(
        session_id, 
        request.answer
    )
    
    return AnswerResponse(
        session_id=session_id,
        extracted_fields=extracted,
        next_question=next_question,
        is_complete=is_complete,
        completion_percentage=completion,
        message=message
    )


@app.get("/session/{session_id}", response_model=ClaimState)
async def get_session(session_id: str):
    """
    Get the current state of a claim session
    
    Returns extracted information and completion status.
    """
    return session_manager.get_session(session_id)


@app.get("/session/{session_id}/summary", response_model=ClaimSummary)
async def get_summary(session_id: str):
    """
    Get complete summary of a claim session
    
    Returns all extracted data, conversation history, and completion status.
    """
    return session_manager.get_summary(session_id)


@app.delete("/session/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(session_id: str):
    """
    Delete a claim session
    
    Use this to clean up when the session is no longer needed.
    """
    session_manager.delete_session(session_id)
    return None


@app.get("/sessions")
async def list_sessions():
    """
    List all active sessions
    
    Returns a summary of all currently active claim sessions.
    """
    return {
        "total_sessions": len(session_manager.sessions),
        "sessions": session_manager.list_sessions()
    }


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
