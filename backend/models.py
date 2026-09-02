from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class SuspectProfile(BaseModel):
    id: str = "person_arjun_sharma"
    name: str = "Arjun Sharma"
    alias: Optional[str] = "Cipher King"
    role: str = "Primary Subject"  # Primary Subject, Secondary Subject, Person of Interest, Associate
    relationship_to_primary: Optional[str] = "Self"
    age: Optional[int] = 34
    gender: Optional[str] = "Male"
    photo_url: Optional[str] = "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=300"
    phone: Optional[str] = "+91-98765-10001"
    email: Optional[str] = "arjun.sharma@protonmail.com"
    address: Optional[str] = "Flat 402, Shivajinagar"
    city: Optional[str] = "Pune"
    occupation: Optional[str] = "Software Consultant / Tech Lead"
    organization: Optional[str] = "Apex Global Solutions"
    vehicle: Optional[str] = "MH12-AB-1234"
    social_usernames: Dict[str, str] = {"telegram": "@cipher_king", "twitter": "@arjun_s89", "instagram": "@arjun_cyber"}
    wallet_address: Optional[str] = "0x82a9b4fe82c19a...9b4"
    notes: Optional[str] = "Primary subject under investigation for Operation Nexus."
    risk_score: int = 92
    evidence_count: int = 14

class Case(BaseModel):
    id: str = "TRX-2026-017"
    title: str = "Operation Nexus"
    primary_suspect: SuspectProfile
    secondary_suspects: List[SuspectProfile] = []
    subject_known_identifiers: Dict[str, List[str]] = {}
    description: str = "Cross-domain intelligence fusion investigating an illicit financial transfer syndicate coordinating extortion, money laundering through informal channels, and crypto off-ramping connected to cyber incident #1042."
    investigation_type: str = "Cyber-Financial Crime"
    priority: str = "High"
    status: str = "Active"
    date_opened: str = "2026-08-15"
    lead_investigator: str = "Ins. Vikramaditya Rao (#INV-7092)"
    location: str = "Pune, Maharashtra"
    agency: str = "Special Cyber Crime & Intelligence Cell (SCCIC)"
    tags: List[str] = ["EXTORTION", "HAWALA_INDICATORS", "CRYPTO_FLOW", "DVR_FORENSIC"]
    evidence_count: int = 82
    last_activity: str = "10 mins ago"

class Entity(BaseModel):
    id: str
    label: str
    type: str
    risk_score: int = Field(default=50, ge=0, le=100)
    confidence: float = Field(default=0.9, ge=0.0, le=1.0)
    details: Optional[str] = ""
    status: str = "Confirmed"
    source_evidence_ids: List[str] = []
    tree_level: int = 1
    avatar: Optional[str] = None
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
    call_count: Optional[int] = 0
    first_observed: Optional[str] = ""
    last_observed: Optional[str] = ""

class EvidenceItem(BaseModel):
    id: str
    case_id: str = "TRX-2026-017"
    person_id: Optional[str] = "person_arjun_sharma"
    title: str
    evidence_type: str
    source: str
    acquisition_timestamp: str
    file_hash: str
    file_size_bytes: int = 1024500
    integrity_status: str = "VERIFIED"
    processing_status: str = "PROCESSED"
    provenance: str
    analyst_notes: str = ""

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
