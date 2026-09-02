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
    description="Professional Investigation Workstation for SIH26189",
    version="3.0.0"
)

DATASTORE = generate_synthetic_dataset()

for evd in DATASTORE["evidence_items"]:
    evidence_ledger.add_evidence_block(
        case_id=evd["case_id"],
        action_type="EVIDENCE_ACQUIRED",
        actor="Ins. Vikramaditya Rao (#INV-7092)",
        data_payload={
            "evidence_id": evd["id"],
            "title": evd["title"],
            "file_hash": evd["file_hash"],
            "provenance": evd["provenance"]
        }
    )

class CreateCaseWizardRequest(BaseModel):
    # Step 1: Case Info
    id: Optional[str] = None
    title: str
    description: str
    investigation_type: str = "Cyber-Financial Crime"
    priority: str = "High"
    date_opened: str = "2026-09-02"
    lead_investigator: str = "Ins. Vikramaditya Rao (#INV-7092)"
    location: str = "Pune, Maharashtra"
    agency: str = "Special Cyber Crime & Intelligence Cell (SCCIC)"
    tags: List[str] = ["NEW_INVESTIGATION"]
    
    # Step 2: Primary Suspect Profile
    primary_suspect: SuspectProfile
    
    # Step 3: Secondary Suspect Profiles
    secondary_suspects: List[SuspectProfile] = []

class TamperRequest(BaseModel):
    block_index: int
    field_to_tamper: str = "title"
    tampered_value: str = "[EXPUNGED / ILLEGALLY MUTATED EVIDENCE]"

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
            "evidence_count": len(DATASTORE["evidence_items"]),
            "relationships_count": len(DATASTORE["edges"]),
            "temporal_events_count": 19,
            "investigative_leads_count": len(DATASTORE["leads"]),
            "pending_review_count": 3
        },
        "recent_activity": [
            {"time": "10 mins ago", "event": "New CDR dataset imported for TRX-2026-017", "domain": "CDR"},
            {"time": "25 mins ago", "event": "Financial hawala indicator flagged on HDFC Acc ACC-IND-994101", "domain": "FINANCIAL"},
            {"time": "45 mins ago", "event": "Blockchain wallet 0x82...9b4 linked via OSINT crawl", "domain": "BLOCKCHAIN"},
            {"time": "1 hour ago", "event": "CCTV Cam C12 ANPR frame hash verified on Blockchain Ledger", "domain": "DVR"}
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
    return DATASTORE["cases"][case_id]

@app.post("/api/cases")
def create_case_wizard(req: CreateCaseWizardRequest):
    case_id = req.id or f"TRX-2026-{len(DATASTORE['cases']) + 18:03d}"
    
    primary = req.primary_suspect.dict()
    secondaries = [s.dict() for s in req.secondary_suspects]
    
    new_case = {
        "id": case_id,
        "title": req.title,
        "primary_suspect": primary,
        "secondary_suspects": secondaries,
        "subject_known_identifiers": {
            "phone": [primary.get("phone", "")] if primary.get("phone") else [],
            "email": [primary.get("email", "")] if primary.get("email") else [],
            "aliases": [primary.get("alias", primary.get("name"))],
            "vehicle": [primary.get("vehicle", "")] if primary.get("vehicle") else [],
            "wallet": [primary.get("wallet_address", "")] if primary.get("wallet_address") else [],
            "account": []
        },
        "description": req.description,
        "investigation_type": req.investigation_type,
        "priority": req.priority,
        "status": "Active",
        "date_opened": req.date_opened,
        "lead_investigator": req.lead_investigator,
        "agency": req.agency,
        "location": req.location,
        "tags": req.tags,
        "evidence_count": 0,
        "last_activity": "Just created"
    }
    
    DATASTORE["cases"][case_id] = new_case
    
    # Ingest Primary Node
    p_id = primary["id"] or f"person_{primary['name'].lower().replace(' ', '_')}"
    if not any(n["id"] == p_id for n in DATASTORE["nodes"]):
        DATASTORE["nodes"].append({
            "id": p_id,
            "label": primary["name"],
            "type": "PERSON",
            "risk_score": primary.get("risk_score", 85),
            "confidence": 1.0,
            "details": f"Primary Subject in Case {case_id}. Occupation: {primary.get('occupation')}",
            "status": "Confirmed",
            "source_evidence_ids": ["EVD-DOC-001"],
            "tree_level": 0,
            "avatar": primary.get("photo_url")
        })

    # Ingest Secondary Nodes
    for sec in secondaries:
        s_id = sec["id"] or f"person_{sec['name'].lower().replace(' ', '_')}"
        if not any(n["id"] == s_id for n in DATASTORE["nodes"]):
            DATASTORE["nodes"].append({
                "id": s_id,
                "label": sec["name"],
                "type": "PERSON",
                "risk_score": sec.get("risk_score", 75),
                "confidence": 0.9,
                "details": f"Secondary Subject in Case {case_id}. Role: {sec['role']}",
                "status": "Confirmed",
                "source_evidence_ids": ["EVD-DOC-001"],
                "tree_level": 1,
                "avatar": sec.get("photo_url")
            })
            DATASTORE["edges"].append({
                "id": f"rel_sec_{hash(s_id)&0xfffffff}",
                "source": p_id,
                "target": s_id,
                "relation": "ASSOCIATED_WITH",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "confidence": 0.9,
                "source_evidence_ids": ["EVD-DOC-001"],
                "details": f"Association link: {sec['role']}",
                "domain": "COMMUNICATION",
                "call_count": 5
            })

    evidence_ledger.add_evidence_block(
        case_id=case_id,
        action_type="CASE_CREATED",
        actor=req.lead_investigator,
        data_payload={"title": req.title, "agency": req.agency, "primary_subject": primary["name"]}
    )
    
    return {"success": True, "case": new_case}

@app.get("/api/persons/{person_id}")
def get_person_profile(person_id: str):
    node = next((n for n in DATASTORE["nodes"] if n["id"] == person_id), None)
    if not node:
        raise HTTPException(status_code=404, detail="Person not found")
        
    case_obj = DATASTORE["cases"]["TRX-2026-017"]
    person_data = None
    if case_obj["primary_suspect"]["id"] == person_id:
        person_data = case_obj["primary_suspect"]
    else:
        person_data = next((s for s in case_obj["secondary_suspects"] if s["id"] == person_id), None)
        
    if not person_data:
        person_data = {
            "id": node["id"],
            "name": node["label"],
            "alias": node["label"],
            "role": "Person of Interest",
            "relationship_to_primary": "Associate",
            "age": 30,
            "gender": "Unknown",
            "photo_url": node.get("avatar") or "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=300",
            "phone": "+91-98765-99999",
            "email": f"{node['label'].lower().replace(' ', '.')}@domain.in",
            "address": "Pune, Maharashtra",
            "city": "Pune",
            "occupation": "Entity",
            "organization": "Unknown",
            "vehicle": "",
            "social_usernames": {"telegram": f"@{node['label'].lower().replace(' ', '_')}"},
            "wallet_address": "",
            "notes": node.get("details", ""),
            "risk_score": node.get("risk_score", 60),
            "evidence_count": 5
        }
        
    # Get person-specific evidence & relationships
    person_evidence = [e for e in DATASTORE["evidence_items"] if e.get("person_id") == person_id]
    person_relationships = [e for e in DATASTORE["edges"] if e["source"] == person_id or e["target"] == person_id]
    
    return {
        "person": person_data,
        "evidence_items": person_evidence,
        "relationships": person_relationships
    }

@app.get("/api/relationships/{rel_id}/evidence")
def get_relationship_evidence(rel_id: str):
    rel = next((e for e in DATASTORE["edges"] if e["id"] == rel_id), None)
    if not rel:
        raise HTTPException(status_code=404, detail="Relationship not found")
        
    evd_items = [e for e in DATASTORE["evidence_items"] if e["id"] in rel.get("source_evidence_ids", [])]
    return {
        "relationship": rel,
        "supporting_evidence": evd_items
    }

@app.get("/api/evidence")
def get_evidence_list(case_id: Optional[str] = None, person_id: Optional[str] = None):
    items = DATASTORE["evidence_items"]
    if case_id:
        items = [e for e in items if e["case_id"] == case_id]
    if person_id and person_id != "ALL":
        items = [e for e in items if e.get("person_id") == person_id]
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
    timeline_events = []
    for e in DATASTORE["edges"]:
        timeline_events.append({
            "id": e["id"],
            "timestamp": e.get("timestamp", "2026-08-28 20:00:00"),
            "domain": e.get("domain", "GENERAL"),
            "title": f"{e['relation']} link: {e['source']} → {e['target']}",
            "details": e.get("details", ""),
            "evidence_id": e.get("source_evidence_ids", ["EVD-DOC-001"])[0]
        })
    timeline_events.sort(key=lambda x: x["timestamp"])
    return {"events": timeline_events}

@app.get("/api/communications")
def get_communications(person_id: Optional[str] = "person_arjun_sharma"):
    comm_edges = [e for e in DATASTORE["edges"] if e.get("domain") == "COMMUNICATION"]
    if person_id and person_id != "ALL":
        comm_edges = [e for e in comm_edges if e["source"] == person_id or e["target"] == person_id]
    return {
        "total_calls": 42,
        "total_messages": 18,
        "unique_contacts": 9,
        "last_contact": "17 Aug 2026",
        "communication_edges": comm_edges
    }

@app.get("/api/financial")
def get_financial(person_id: Optional[str] = "person_arjun_sharma"):
    fin_edges = [e for e in DATASTORE["edges"] if e.get("domain") == "FINANCIAL"]
    return {
        "total_transactions": 54,
        "incoming": "₹45,00,000",
        "outgoing": "₹25,00,000",
        "related_accounts": ["HDFC Acc ****4721", "ICICI Acc ****9901"],
        "financial_edges": fin_edges
    }

@app.get("/api/blockchain")
def get_blockchain(person_id: Optional[str] = "person_arjun_sharma"):
    blk_edges = [e for e in DATASTORE["edges"] if e.get("domain") == "BLOCKCHAIN"]
    return {
        "monitored_wallets": ["0x82a9b4fe82c19a...9b4"],
        "total_volume": "18.5 ETH",
        "blockchain_edges": blk_edges
    }

@app.get("/api/osint")
def get_osint(person_id: Optional[str] = "person_arjun_sharma"):
    osint_edges = [e for e in DATASTORE["edges"] if e.get("domain") == "OSINT"]
    return {
        "crawled_sources": 52,
        "correlated_handles": ["@cipher_king", "@arjun_s89", "shadow_broker99"],
        "osint_edges": osint_edges
    }

@app.get("/api/dvr")
def get_dvr(person_id: Optional[str] = "person_arjun_sharma"):
    dvr_edges = [e for e in DATASTORE["edges"] if e.get("domain") == "DVR"]
    return {
        "dvr_edges": dvr_edges,
        "dvr_videos": DATASTORE.get("dvr_videos", [])
    }

@app.get("/api/fusion")
def get_evidence_fusion(case_id: Optional[str] = "TRX-2026-017", person_id: Optional[str] = "person_arjun_sharma"):
    return fusion_engine.generate_fusion_analysis(case_id, DATASTORE["nodes"], DATASTORE["edges"], DATASTORE["evidence_items"])

@app.get("/api/leads")
def get_investigative_leads():
    return {"leads": DATASTORE["leads"]}

@app.get("/api/audit")
def get_audit_trail():
    verification = evidence_ledger.verify_integrity()
    return {
        "blockchain_audit": [b.to_dict() for b in evidence_ledger.chain],
        "integrity_verification": verification
    }

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
    matched_evidence = [e for e in DATASTORE["evidence_items"] if query in e["title"].lower() or query in e.get("analyst_notes", "").lower()]
    matched_edges = [e for e in DATASTORE["edges"] if query in e.get("details", "").lower() or query in e.get("relation", "").lower()]
    return {
        "query": q,
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
    return HTMLResponse("<h1>TRACE-X Platform Loading...</h1>")

app.mount("/static", StaticFiles(directory=static_dir), name="static")
