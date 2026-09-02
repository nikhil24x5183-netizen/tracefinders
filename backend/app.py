import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from fastapi import FastAPI, HTTPException, Body, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import time

from backend.models import Case, Entity, Relationship, EvidenceItem, Anomaly, InvestigativeLead, AuditBlock, SuspectProfile
from backend.mock_data_generator import generate_synthetic_dataset
from backend.graph_engine import graph_engine
from backend.nlp_extractor import nlp_engine
from backend.anomaly_engine import anomaly_engine
from backend.fusion_engine import fusion_engine
from backend.blockchain_ledger import evidence_ledger
from backend.report_generator import report_generator

app = FastAPI(
    title="TRACE-X — AI-Powered Criminal Network Intelligence & Evidence Fusion Workstation",
    description="SIH 2026 Problem Statement SIH26189 - AI-Powered Criminal Network Analysis System",
    version="4.0.0"
)

DATASTORE = generate_synthetic_dataset()

# Seed ledger
for evd in DATASTORE["evidence_items"]:
    evidence_ledger.add_evidence_block(
        case_id=evd["case_id"],
        action_type="EVIDENCE_ACQUIRED",
        actor="INV-004",
        data_payload={
            "evidence_id": evd["id"],
            "title": evd["title"],
            "file_hash": evd["file_hash"],
            "provenance": evd["provenance"]
        }
    )

class CreateCaseWizardRequest(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    investigation_type: str = "Cyber-Financial Crime"
    priority: str = "HIGH"
    date_opened: str = "2026-09-02"
    lead_investigator: str = "Ins. Vikramaditya Rao (#INV-7092)"
    location: str = "Pune, Maharashtra"
    agency: str = "Special Cyber Crime & Intelligence Cell (SCCIC)"
    tags: List[str] = ["NEW_INVESTIGATION"]
    primary_suspect: SuspectProfile
    secondary_suspects: List[SuspectProfile] = []

class TamperRequest(BaseModel):
    block_index: int
    field_to_tamper: str = "title"
    tampered_value: str = "[EXPUNGED / ILLEGALLY MUTATED EVIDENCE]"

class EntityResolutionRequest(BaseModel):
    candidate_id: str
    action: str  # CONFIRM, REJECT, REVIEW
    notes: Optional[str] = ""

# ----------------- REST API ROUTES -----------------

@app.get("/api/overview")
def get_overview_statistics(case_id: Optional[str] = "TRX-2026-017", person_id: Optional[str] = "person_arjun_sharma"):
    case_obj = DATASTORE["cases"].get(case_id, DATASTORE["cases"]["TRX-2026-017"])
    
    return {
        "case_summary": {
            "case_id": case_obj["id"],
            "title": case_obj["title"],
            "primary_subject": case_obj["primary_suspect"]["name"],
            "secondary_subjects_count": len(case_obj["secondary_suspects"]),
            "entities_count": len(DATASTORE["nodes"]),
            "evidence_count": case_obj.get("evidence_count", 148),
            "relationships_count": case_obj.get("relationships_count", 37),
            "communications_count": case_obj.get("communications_count", 421),
            "financial_count": case_obj.get("financial_count", 63),
            "osint_count": case_obj.get("osint_count", 42),
            "blockchain_count": case_obj.get("blockchain_count", 18),
            "cctv_count": case_obj.get("cctv_count", 9)
        },
        "investigation_activity": [
            {"time": "09:42", "event": "New communication cluster detected (+91 98765 1201 ➔ Rohan Mehta)", "domain": "CDR"},
            {"time": "10:18", "event": "Financial transaction linked to Arjun Sharma (XXXX4821 ➔ ₹48,500)", "domain": "FINANCIAL"},
            {"time": "11:03", "event": "Public-Source mention discovered (@arjun_s_demo ➔ Nexus Logistics)", "domain": "OSINT"},
            {"time": "12:27", "event": "Potential relationship detected between Arjun Sharma and Rohan Mehta", "domain": "GRAPH"},
            {"time": "13:41", "event": "CCTV event linked to vehicle MH12 AB 4821 (CAM-04 ANPR match)", "domain": "DVR"},
            {"time": "15:08", "event": "Blockchain wallet activity correlated (0xDEMO...A721 ➔ 1.20 ETH)", "domain": "BLOCKCHAIN"},
            {"time": "16:22", "event": "Evidence integrity verification completed (Verified)", "domain": "AUDIT"}
        ],
        "ai_leads": DATASTORE["leads"]
    }

@app.get("/api/cases")
def get_all_cases():
    return {"cases": list(DATASTORE["cases"].values())}

@app.get("/api/cases/{case_id}")
def get_case_details(case_id: str):
    if case_id not in DATASTORE["cases"]:
        raise HTTPException(status_code=404, detail="Case not found")
    c = DATASTORE["cases"][case_id]
    evd_cards = [e for e in DATASTORE["evidence_items"] if e["case_id"] == case_id]
    return {
        "case": c,
        "evidence_cards": evd_cards
    }

@app.post("/api/cases")
def create_case_wizard(req: CreateCaseWizardRequest):
    case_id = req.id or f"TRX-2026-{len(DATASTORE['cases']) + 18:03d}"
    primary = req.primary_suspect.dict()
    secondaries = [s.dict() for s in req.secondary_suspects]
    
    new_case = {
        "id": case_id,
        "title": req.title.upper(),
        "primary_suspect": primary,
        "secondary_suspects": secondaries,
        "subject_known_identifiers": {
            "phone": [primary.get("phone", "")],
            "email": [primary.get("email", "")],
            "aliases": [primary.get("alias", primary.get("name"))],
            "vehicle": [primary.get("vehicle", "")],
            "wallet": [primary.get("wallet_address", "")]
        },
        "description": req.description,
        "investigation_type": req.investigation_type,
        "priority": req.priority,
        "status": "ACTIVE",
        "date_opened": req.date_opened,
        "lead_investigator": req.lead_investigator,
        "agency": req.agency,
        "location": req.location,
        "tags": req.tags,
        "evidence_count": 5,
        "relationships_count": 3,
        "communications_count": 12,
        "financial_count": 4,
        "osint_count": 3,
        "blockchain_count": 1,
        "cctv_count": 1,
        "last_activity": "18 Aug 2026 21:17"
    }
    
    DATASTORE["cases"][case_id] = new_case
    return {"success": True, "case": new_case}

@app.get("/api/persons/{person_id}")
def get_person_profile(person_id: str):
    node = next((n for n in DATASTORE["nodes"] if n["id"] == person_id), None)
    case_obj = DATASTORE["cases"]["TRX-2026-017"]
    
    person_data = None
    if case_obj["primary_suspect"]["id"] == person_id:
        person_data = case_obj["primary_suspect"]
    else:
        person_data = next((s for s in case_obj["secondary_suspects"] if s["id"] == person_id), None)
        
    if not person_data and person_id == DATASTORE["ambiguous_candidate"]["id"]:
        person_data = DATASTORE["ambiguous_candidate"]

    if not person_data:
        person_data = {
            "id": person_id,
            "name": node["label"] if node else person_id,
            "alias": node["label"] if node else person_id,
            "role": "Person of Interest",
            "relationship_to_primary": "Associate",
            "age": 32,
            "gender": "Male",
            "photo_url": node.get("avatar") if node else "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=300",
            "phone": "+91 98765 9999",
            "email": "contact.demo@example.test",
            "address": "Pune, Maharashtra",
            "city": "Pune, Maharashtra",
            "occupation": "Associate",
            "organization": "Nexus Logistics",
            "vehicle": "MH12 XY 9988",
            "social_usernames": {"telegram": "@associate_demo"},
            "wallet_address": "0x3910...199",
            "notes": "Person of Interest linked to primary subject.",
            "risk_score": 65,
            "evidence_count": 12,
            "relationship_count": 4,
            "status": "Person of Interest",
            "last_updated": "18 Aug 2026 21:17"
        }
        
    person_evidence = [e for e in DATASTORE["evidence_items"] if e.get("person_id") == person_id or person_id == "person_arjun_sharma"]
    person_relationships = [e for e in DATASTORE["edges"] if e["source"] == person_id or e["target"] == person_id]
    
    return {
        "person": person_data,
        "connected_counts": {
            "communications": 24,
            "financial": 8,
            "osint": 5,
            "blockchain": 3,
            "cctv": 4
        },
        "connected_people": [
            {"name": "Rohan Mehta", "role": "Business Contact"},
            {"name": "Priya Joshi", "role": "Associate"},
            {"name": "Vikram Patil", "role": "Person of Interest"},
            {"name": "Neha Kulkarni", "role": "Employee"}
        ],
        "evidence_items": person_evidence,
        "relationships": person_relationships
    }

@app.get("/api/evidence/{evidence_id}")
def get_evidence_detail(evidence_id: str):
    evd = next((e for e in DATASTORE["evidence_items"] if e["id"] == evidence_id), None)
    if not evd:
        evd = {
            "id": evidence_id,
            "case_id": "TRX-2026-017",
            "person_id": "person_arjun_sharma",
            "title": f"Evidence Record {evidence_id}",
            "evidence_type": "Communication Analysis",
            "source": "Communication Dataset",
            "acquisition_timestamp": "18 Aug 2026 20:02:14",
            "acquisition_date": "18 Aug 2026",
            "acquisition_time": "20:02:14",
            "file_hash": "8f31c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852c91a",
            "file_size_bytes": 1840000,
            "integrity_status": "Verified",
            "processing_status": "PROCESSED",
            "provenance": "Communication Dataset",
            "analyst_notes": "Log record associated with primary subject Arjun Sharma.",
            "confidence": 0.95,
            "extracted_entities": ["Arjun Sharma", "Rohan Mehta", "Pune"],
            "related_events": ["EV-CCTV-031", "EV-FIN-014", "EV-REL-074"],
            "duration": "04:21",
            "direction": "Outgoing"
        }
    return evd

@app.get("/api/relationships/{rel_id}/evidence")
def get_relationship_evidence(rel_id: str):
    rel = next((e for e in DATASTORE["edges"] if e["id"] == rel_id), None)
    if not rel:
        rel = DATASTORE["edges"][0]
        
    evd_items = [e for e in DATASTORE["evidence_items"] if e["id"] in rel.get("source_evidence_ids", [])]
    if not evd_items:
        evd_items = [DATASTORE["evidence_items"][0], DATASTORE["evidence_items"][1]]

    return {
        "relationship": rel,
        "supporting_evidence": evd_items
    }

@app.get("/api/evidence")
def get_evidence_list(case_id: Optional[str] = None, person_id: Optional[str] = None):
    items = DATASTORE["evidence_items"]
    if case_id:
        items = [e for e in items if e["case_id"] == case_id]
    return {"evidence_items": items}

@app.get("/api/graph")
def get_graph(case_id: Optional[str] = "TRX-2026-017", person_id: Optional[str] = "person_arjun_sharma"):
    analytics = graph_engine.analyze_graph(DATASTORE["nodes"], DATASTORE["edges"])
    return {
        "nodes": DATASTORE["nodes"],
        "edges": DATASTORE["edges"],
        "analytics": analytics
    }

@app.get("/api/timeline")
def get_timeline(case_id: Optional[str] = "TRX-2026-017", person_id: Optional[str] = None):
    timeline_events = [
        {"id": "EV-CCTV-031", "timestamp": "18 Aug 2026 20:01:14", "title": "PERSON MEETING", "domain": "DVR", "details": "CCTV CAM-04 capture of Arjun Sharma and Rohan Mehta.", "evidence_id": "EV-CCTV-031", "person": "Arjun Sharma", "location": "Pune"},
        {"id": "EV-COM-023", "timestamp": "18 Aug 2026 20:02:07", "title": "COMMUNICATION EVENT (Outgoing 04:21)", "domain": "CDR", "details": "Cell tower connection initiated to Rohan Mehta.", "evidence_id": "EV-COM-023", "person": "Arjun Sharma", "location": "Pune"},
        {"id": "EV-COM-024", "timestamp": "18 Aug 2026 20:11:23", "title": "COMMUNICATION EVENT (Incoming 02:44)", "domain": "CDR", "details": "Incoming call from Rohan Mehta.", "evidence_id": "EV-COM-023", "person": "Rohan Mehta", "location": "Pune"},
        {"id": "EV-CCTV-032", "timestamp": "18 Aug 2026 20:17:38", "title": "PHYSICAL EVENT (FINANCIAL EXCHANGE)", "domain": "DVR", "details": "Surveillance CAM-04 capture of envelope exchange.", "evidence_id": "EV-CCTV-032", "person": "Arjun Sharma", "location": "Pune"},
        {"id": "EV-COM-025", "timestamp": "18 Aug 2026 20:19:04", "title": "COMMUNICATION EVENT (Outgoing 06:12)", "domain": "CDR", "details": "Follow-up communication recorded.", "evidence_id": "EV-COM-023", "person": "Arjun Sharma", "location": "Pune"},
        {"id": "EV-CCTV-033", "timestamp": "18 Aug 2026 20:26:11", "title": "VEHICLE DEPARTURE (MH12 AB 4821)", "domain": "DVR", "details": "ANPR sighting of SUV driven by Vikram Patil.", "evidence_id": "EV-CCTV-033", "person": "Vikram Patil", "location": "Pune"},
        {"id": "EV-COM-026", "timestamp": "18 Aug 2026 20:42:51", "title": "PHONE EVENT (Burst)", "domain": "CDR", "details": "SIM-box tower handoff recorded.", "evidence_id": "EV-COM-001", "person": "Arjun Sharma", "location": "Pune"},
        {"id": "EV-FIN-014", "timestamp": "18 Aug 2026 21:03:18", "title": "FINANCIAL EVENT (₹48,500 Wire)", "domain": "FINANCIAL", "details": "Account XXXX4821 wire transfer to Rohan Mehta.", "evidence_id": "EV-FIN-014", "person": "Rohan Mehta", "location": "Pune"},
        {"id": "EV-BC-042", "timestamp": "18 Aug 2026 21:17:04", "title": "BLOCKCHAIN EVENT (1.20 ETH)", "domain": "BLOCKCHAIN", "details": "Wallet 0xDEMO...A721 transaction.", "evidence_id": "EV-BC-042", "person": "Arjun Sharma", "location": "Blockchain"}
    ]
    return {
        "temporal_assessment": "TEMPORAL RELATIONSHIP DETECTED: Multiple communication, physical, and financial events occur within a short temporal window and may warrant investigator review.",
        "events": timeline_events
    }

@app.get("/api/communications")
def get_communications(person_id: Optional[str] = "person_arjun_sharma"):
    rohan_call_timeline = [
        {"date": "18 Aug 2026", "time": "20:02:14", "direction": "Outgoing", "duration": "04:21", "evidence_id": "EV-COM-023"},
        {"date": "18 Aug 2026", "time": "20:11:23", "direction": "Incoming", "duration": "02:44", "evidence_id": "EV-COM-023"},
        {"date": "18 Aug 2026", "time": "20:19:04", "direction": "Outgoing", "duration": "06:12", "evidence_id": "EV-COM-023"},
        {"date": "18 Aug 2026", "time": "20:31:18", "direction": "Incoming", "duration": "01:18", "evidence_id": "EV-COM-023"},
        {"date": "17 Aug 2026", "time": "19:42:05", "direction": "Outgoing", "duration": "03:09", "evidence_id": "EV-COM-001"}
    ]
    
    return {
        "total_events": 421,
        "calls": 187,
        "messages": 234,
        "unique_contacts": 11,
        "active_period": "03 Aug – 18 Aug 2026",
        "contacts": [
            {"id": "person_rohan_mehta", "name": "Rohan Mehta", "role": "Business Contact", "calls": 27, "phone": "+91 98765 2002"},
            {"id": "person_priya_joshi", "name": "Priya Joshi", "role": "Associate", "calls": 14, "phone": "+91 98765 3003"},
            {"id": "person_vikram_patil", "name": "Vikram Patil", "role": "Person of Interest", "calls": 9, "phone": "+91 98765 4004"},
            {"id": "person_neha_kulkarni", "name": "Neha Kulkarni", "role": "Employee", "calls": 6, "phone": "+91 98765 5005"},
            {"id": "person_unknown", "name": "UNKNOWN CONTACT", "role": "Unknown", "calls": 4, "phone": "+91 98999 0000"}
        ],
        "rohan_call_timeline": rohan_call_timeline,
        "communication_edges": [e for e in DATASTORE["edges"] if e.get("domain") == "COMMUNICATION"]
    }

@app.get("/api/financial")
def get_financial(person_id: Optional[str] = "person_arjun_sharma"):
    accounts = [
        {"bank": "HDFC Account", "account_number": "XXXX4821", "type": "Current Account", "balance": "₹14,50,000"},
        {"bank": "Axis Account", "account_number": "XXXX7194", "type": "Corporate Account", "balance": "₹8,20,000"}
    ]
    
    transactions = [
        {"date": "18 Aug 2026", "time": "20:58", "amount": "₹48,500", "direction": "OUT", "account": "XXXX4821", "counterparty": "Rohan Mehta", "reference": "TXN-88421", "evidence_id": "EV-FIN-014", "dest_account": "XXXX7312", "correlation": "EV-COM-031", "location": "Pune", "confidence": "71%", "indicator": "Temporal proximity between communication and financial activity."},
        {"date": "18 Aug 2026", "time": "15:20", "amount": "₹72,000", "direction": "IN", "account": "XXXX7194", "counterparty": "Priya Joshi", "reference": "TXN-88422", "evidence_id": "EV-REL-074", "dest_account": "XXXX7194", "correlation": "EV-DOC-057", "location": "Pune", "confidence": "93%", "indicator": "Corporate wire deposit."},
        {"date": "17 Aug 2026", "time": "18:45", "amount": "₹19,800", "direction": "OUT", "account": "XXXX4821", "counterparty": "Vikram Patil", "reference": "TXN-88423", "evidence_id": "EV-FIN-014", "dest_account": "XXXX9901", "correlation": "EV-CCTV-033", "location": "Pune", "confidence": "90%", "indicator": "Logistics expense payment."},
        {"date": "16 Aug 2026", "time": "11:10", "amount": "₹1,25,000", "direction": "IN", "account": "XXXX7194", "counterparty": "Nexus Logistics", "reference": "TXN-88424", "evidence_id": "EV-REL-074", "dest_account": "XXXX7194", "correlation": "EV-DOC-057", "location": "Pune", "confidence": "94%", "indicator": "Retainer credit transfer."},
        {"date": "15 Aug 2026", "time": "14:30", "amount": "₹38,200", "direction": "OUT", "account": "XXXX4821", "counterparty": "Priya Joshi", "reference": "TXN-88425", "evidence_id": "EV-FIN-014", "dest_account": "XXXX5544", "correlation": "EV-FIN-014", "location": "Pune", "confidence": "91%", "indicator": "Consulting disbursement."}
    ]
    
    hawala_indicators = [
        {"name": "Repeated third-party transfers", "status": "OBSERVED", "details": "Transfers without commercial documentation observed across counterparty accounts."},
        {"name": "Rapid account movement", "status": "OBSERVED", "details": "Movement between multiple accounts within short interval."},
        {"name": "Multiple counterparties", "status": "OBSERVED", "details": "Multiple counterparty accounts linked within 48-hour window."},
        {"name": "Transaction timing correlated with communication", "status": "OBSERVED", "details": "Financial activity initiated within minutes of CDR call burst."},
        {"name": "Geographical separation", "status": "NOT OBSERVED", "details": "Counterparties located within Western Maharashtra corridor."},
        {"name": "Unusual settlement pattern", "status": "INCONCLUSIVE", "details": "Requires ongoing ledger observation."}
    ]
    
    return {
        "accounts": accounts,
        "transactions": transactions,
        "hawala_analysis": {
            "title": "INFORMAL VALUE TRANSFER INDICATORS",
            "assessment": "Potential informal value transfer pattern",
            "status": "Requires investigative verification",
            "indicators": hawala_indicators
        }
    }

@app.get("/api/blockchain")
def get_blockchain(person_id: Optional[str] = "person_arjun_sharma"):
    wallet_info = {
        "address": "0xDEMO...A721",
        "associated_evidence": "EV-BC-042",
        "balance": "8.42 ETH",
        "incoming": 23,
        "outgoing": 24,
        "total_observed": 47,
        "disclaimer": "Wallet association based on available evidence."
    }
    
    transactions = [
        {"id": "TX-DEMO-001", "hash": "TX-DEMO-001", "from_addr": "0x3910...199", "to_addr": "0xDEMO...A721", "value": "0.84 ETH", "time": "18 Aug 2026 21:17:04", "evidence_id": "EV-BC-042"},
        {"id": "TX-DEMO-002", "hash": "TX-DEMO-002", "from_addr": "0xDEMO...A721", "to_addr": "0xDEMO...F921", "value": "1.20 ETH", "time": "18 Aug 2026 21:40:12", "evidence_id": "EV-BC-042"},
        {"id": "TX-DEMO-003", "hash": "TX-DEMO-003", "from_addr": "0xDEMO...A721", "to_addr": "0x9910...E22", "value": "0.42 ETH", "time": "17 Aug 2026 14:10:00", "evidence_id": "EV-BC-042"},
        {"id": "TX-DEMO-004", "hash": "TX-DEMO-004", "from_addr": "0x44a1...B01", "to_addr": "0xDEMO...A721", "value": "2.10 ETH", "time": "16 Aug 2026 09:25:30", "evidence_id": "EV-BC-042"}
    ]
    
    return {
        "wallet": wallet_info,
        "transactions": transactions
    }

@app.get("/api/osint")
def get_osint(person_id: Optional[str] = "person_arjun_sharma"):
    records = [
        {
            "id": "PSI-023",
            "subject": "Arjun Sharma",
            "source": "Public Web",
            "last_observed": "18 Aug 2026",
            "entity": "Rohan Mehta",
            "location": "Pune",
            "evidence_id": "EV-OSINT-023",
            "confidence": "76%",
            "value": "@arjun_s_demo profile & forum post"
        },
        {
            "id": "PSI-024",
            "subject": "Arjun Sharma",
            "source": "Public Web Directory",
            "last_observed": "18 Aug 2026",
            "entity": "Nexus Logistics",
            "location": "Pune",
            "evidence_id": "EV-DOC-057",
            "confidence": "91%",
            "value": "Nexus Logistics MCA Registration reference"
        },
        {
            "id": "PSI-025",
            "subject": "Arjun Sharma",
            "source": "Public Mapping Directory",
            "last_observed": "18 Aug 2026",
            "entity": "Pune Junction Hub",
            "location": "Pune",
            "evidence_id": "EV-LOC-061",
            "confidence": "90%",
            "value": "Public Location Mention"
        },
        {
            "id": "PSI-026",
            "subject": "Arjun Sharma",
            "source": "Public Blockchain Explorer",
            "last_observed": "18 Aug 2026",
            "entity": "0xDEMO...A721",
            "location": "Blockchain",
            "evidence_id": "EV-BC-042",
            "confidence": "94%",
            "value": "Public Wallet Reference"
        }
    ]
    return {"records": records}

@app.get("/api/dvr")
def get_dvr(person_id: Optional[str] = "person_arjun_sharma"):
    return {
        "dvr_videos": DATASTORE["dvr_videos"]
    }

@app.get("/api/fusion")
def get_evidence_fusion(case_id: Optional[str] = "TRX-2026-017", person_id: Optional[str] = "person_arjun_sharma"):
    return fusion_engine.generate_fusion_analysis(case_id, DATASTORE["nodes"], DATASTORE["edges"], DATASTORE["evidence_items"])

@app.get("/api/analytics")
def get_analytics():
    return {
        "communication_analytics": {
            "peak_window": "18 Aug 2026 20:00–21:00",
            "total_calls": 187,
            "total_messages": 234
        },
        "financial_analytics": {
            "transactions": 63,
            "unusual_transactions": 8,
            "high_value_transactions": 5
        },
        "relationship_analytics": {
            "strong_relationships": 7,
            "potential_relationships": 12,
            "needs_review": 6
        },
        "influential_entities": graph_engine.analyze_graph(DATASTORE["nodes"], DATASTORE["edges"]).get("influential_entities", [])
    }

@app.get("/api/leads")
def get_investigative_leads():
    return {"leads": DATASTORE["leads"]}

@app.get("/api/audit")
def get_audit_trail():
    return {
        "audit_events": DATASTORE["audit_events"],
        "blockchain_audit": [b.to_dict() for b in evidence_ledger.chain]
    }

@app.post("/api/entity-resolution/action")
def handle_entity_resolution(req: EntityResolutionRequest):
    cand = DATASTORE["ambiguous_candidate"]
    cand["status"] = f"Actioned: {req.action}"
    return {"success": True, "candidate": cand, "message": f"Candidate match {req.candidate_id} actioned as {req.action}."}

@app.post("/api/audit/tamper")
def tamper_audit_ledger(req: TamperRequest):
    tamper_res = evidence_ledger.simulate_tamper(req.block_index, req.field_to_tamper, req.tampered_value)
    verification = evidence_ledger.verify_integrity()
    return {
        "tamper_action": tamper_res,
        "audit_verification": verification
    }

@app.post("/api/reports/generate")
def generate_report(case_id: Optional[str] = "TRX-2026-017", person_id: Optional[str] = "person_arjun_sharma"):
    case_data = DATASTORE["cases"].get(case_id, DATASTORE["cases"]["TRX-2026-017"])
    fusion_data = fusion_engine.generate_fusion_analysis(case_id, DATASTORE["nodes"], DATASTORE["edges"], DATASTORE["evidence_items"])
    res = report_generator.generate_report(case_data, DATASTORE["nodes"], DATASTORE["edges"], DATASTORE["evidence_items"], fusion_data)
    return res

@app.get("/api/search")
def global_search(q: str = Query(...)):
    query = q.lower()
    matched_nodes = [n for n in DATASTORE["nodes"] if query in n["label"].lower() or query in n.get("details", "").lower()]
    matched_evidence = [e for e in DATASTORE["evidence_items"] if query in e["title"].lower() or query in e.get("analyst_notes", "").lower() or query in e["id"].lower()]
    matched_edges = [e for e in DATASTORE["edges"] if query in e.get("details", "").lower() or query in e.get("relation", "").lower()]
    matched_cases = [c for c in DATASTORE["cases"].values() if query in c["title"].lower() or query in c["id"].lower()]
    
    return {
        "query": q,
        "matched_cases": matched_cases,
        "matched_nodes": matched_nodes,
        "matched_evidence": matched_evidence,
        "matched_relationships": matched_edges
    }

# Serve Static Files
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static"))

@app.get("/", response_class=HTMLResponse)
def serve_index():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return HTMLResponse("<h1>TRACE-X Workstation Loading...</h1>")

app.mount("/static", StaticFiles(directory=static_dir), name="static")
