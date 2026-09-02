from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class SuspectProfile(BaseModel):
    id: str = "person_arjun_sharma"
    name: str = "Arjun Sharma"
    alias: Optional[str] = "Arjun S."
    role: str = "Primary Subject"  # Primary Subject, Associate, Business Contact, Employee, Person of Interest, Unknown
    relationship_to_primary: Optional[str] = "Self"
    age: Optional[int] = 34
    gender: Optional[str] = "Male"
    photo_url: Optional[str] = "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=300"
    phone: Optional[str] = "+91 98765 1201"
    email: Optional[str] = "arjun.sharma.demo@example.test"
    address: Optional[str] = "Flat 402, Shivajinagar"
    city: Optional[str] = "Pune, Maharashtra"
    occupation: Optional[str] = "Logistics Consultant"
    organization: Optional[str] = "Nexus Logistics"
    vehicle: Optional[str] = "MH12 AB 4821"
    social_usernames: Dict[str, str] = {"twitter": "@arjun_s_demo", "telegram": "@cipher_king", "instagram": "@arjun_cyber"}
    wallet_address: Optional[str] = "0xDEMO...A721"
    notes: Optional[str] = "Primary subject under investigation for Operation Nexus."
    risk_score: int = 92
    evidence_count: int = 24
    relationship_count: int = 7
    status: str = "Under Investigation"
    last_updated: str = "18 Aug 2026 21:17"

class Case(BaseModel):
    id: str = "TRX-2026-017"
    title: str = "OPERATION NEXUS"
    primary_suspect: SuspectProfile
    secondary_suspects: List[SuspectProfile] = []
    subject_known_identifiers: Dict[str, List[str]] = {}
    description: str = "Cross-domain intelligence fusion investigating an illicit financial transfer syndicate coordinating extortion, money laundering through informal channels, and crypto off-ramping connected to cyber incident #1042."
    investigation_type: str = "Cyber-Financial Crime"
    priority: str = "HIGH"
    status: str = "ACTIVE"
    date_opened: str = "2026-08-15"
    lead_investigator: str = "Ins. Vikramaditya Rao (#INV-7092)"
    location: str = "Pune, Maharashtra"
    agency: str = "Special Cyber Crime & Intelligence Cell (SCCIC)"
    tags: List[str] = ["EXTORTION", "HAWALA_INDICATORS", "CRYPTO_FLOW", "DVR_FORENSIC"]
    evidence_count: int = 148
    relationships_count: int = 37
    communications_count: int = 421
    financial_count: int = 63
    osint_count: int = 42
    blockchain_count: int = 18
    cctv_count: int = 9
    last_activity: str = "18 Aug 2026 21:17"

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
    first_observed: Optional[str] = "03 Aug 2026"
    last_observed: Optional[str] = "18 Aug 2026"
    supporting_evidence_count: int = 7
    shared_locations_count: int = 3
    shared_organizations_count: int = 1
    explanation: Optional[str] = ""
    alt_explanation: Optional[str] = ""
    temporal_correlation: Optional[str] = ""

class EvidenceItem(BaseModel):
    id: str  # e.g., EV-COM-001, EV-FIN-014, EV-OSINT-023, EV-CCTV-031, EV-BC-042
    case_id: str = "TRX-2026-017"
    person_id: Optional[str] = "person_arjun_sharma"
    title: str
    evidence_type: str
    source: str
    acquisition_timestamp: str
    acquisition_date: str = "18 Aug 2026"
    acquisition_time: str = "20:02:14"
    file_hash: str
    file_size_bytes: int = 1024500
    integrity_status: str = "Verified"
    processing_status: str = "PROCESSED"
    provenance: str = "Communication Dataset"
    analyst_notes: str = ""
    confidence: float = 0.95
    extracted_entities: List[str] = []
    related_events: List[str] = []
    duration: Optional[str] = None
    direction: Optional[str] = None

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
    analyst_status: str = "Requires Human Review"

class InvestigativeLead(BaseModel):
    id: str
    title: str
    lead: str
    confidence: float
    evidence_chain: List[Dict[str, Any]]
    recommended_actions: List[str]
    supporting_evidence: List[str] = []
    observed_pattern: str = ""
    alternative_explanation: Optional[str] = ""
    status: str = "Needs Review"
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
