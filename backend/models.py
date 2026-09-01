from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class Entity(BaseModel):
    id: str
    label: str
    type: str
    risk_score: int = Field(default=50, ge=0, le=100)
    confidence: float = Field(default=0.9, ge=0.0, le=1.0)
    details: Optional[str] = ""
    status: str = "Confirmed"
    source_evidence_ids: List[str] = []
    metadata: Dict[str, Any] = {}

class Relationship(BaseModel):
    id: str
    source: str
    target: str
    relation: str
    timestamp: str = ""
    confidence: float = Field(default=0.85, ge=0.0, le=1.0)
    source_evidence_ids: List[str] = []
    details: Optional[str] = ""
    domain: str = "GENERAL"

class EvidenceItem(BaseModel):
    id: str
    case_id: str
    title: str
    evidence_type: str
    source: str
    acquisition_timestamp: str
    file_hash: str
    file_size_bytes: int = 1024
    integrity_status: str = "VERIFIED"
    processing_status: str = "PROCESSED"
    provenance: str
    analyst_notes: str = ""

class Case(BaseModel):
    id: str
    title: str
    subject_name: str
    subject_known_identifiers: Dict[str, List[str]]
    description: str
    investigator: str
    agency: str
    priority: str = "HIGH"
    status: str = "ACTIVE"
    start_date: str
    end_date: Optional[str] = None
    tags: List[str] = []

class Anomaly(BaseModel):
    id: str
    category: str
    title: str
    severity: str
    timestamp: str
    affected_entity_ids: List[str]
    explanation: str
    evidence_ids: List[str]
    confidence: float
    analyst_status: str = "Requires Review"

class InvestigativeLead(BaseModel):
    id: str
    title: str
    summary: str
    confidence: float
    evidence_chain: List[Dict[str, Any]]
    recommended_actions: List[str]
    human_review_required: bool = True

class AuditBlock(BaseModel):
    index: int
    case_id: str
    timestamp: str
    action_type: str
    actor: str
    previous_hash: str
    block_hash: str
    data_payload: Dict[str, Any]
