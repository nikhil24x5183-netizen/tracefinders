import sys
import os

# Add parent directory to sys.path so 'backend' package imports work cleanly
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from fastapi import FastAPI, HTTPException, Body, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import time

from backend.models import Case, Entity, Relationship, EvidenceItem, Anomaly, InvestigativeLead, AuditBlock
from backend.mock_data_generator import generate_synthetic_dataset
from backend.graph_engine import graph_engine
from backend.nlp_extractor import nlp_engine
from backend.anomaly_engine import anomaly_engine
from backend.fusion_engine import fusion_engine
from backend.blockchain_ledger import evidence_ledger
from backend.report_generator import report_generator

app = FastAPI(
    title="TRACE-X — AI-Powered Criminal Network Intelligence & Evidence Fusion System",
    description="SIH 2026 Problem Statement SIH26189 - Blockchain & Cybersecurity",
    version="2.0.0"
)

# Seed synthetic dataset in memory
DATASTORE = generate_synthetic_dataset()

# Seed initial blockchain audit log blocks for all evidence items
for evd in DATASTORE["evidence_items"]:
    evidence_ledger.add_evidence_block(
        case_id=evd["case_id"],
        action_type="EVIDENCE_ACQUIRED",
        actor="Investigator Deshmukh (#IND-8842)",
        data_payload={
            "evidence_id": evd["id"],
            "title": evd["title"],
            "file_hash": evd["file_hash"],
            "provenance": evd["provenance"]
        }
    )

# Pydantic Requests
class NLPExtractRequest(BaseModel):
    text: str
    investigator_name: Optional[str] = "Investigator Deshmukh (#IND-8842)"
    auto_add_to_graph: Optional[bool] = True

class ResolveRequest(BaseModel):
    primary_entity_id: str
    candidate_entity_id: str

class TamperRequest(BaseModel):
    block_index: int
    field_to_tamper: str = "title"
    tampered_value: str = "[EXPUNGED / ILLEGALLY MUTATED EVIDENCE]"

class CreateCaseRequest(BaseModel):
    title: str
    subject_name: str
    description: str
    investigator: str
    agency: str
    priority: Optional[str] = "HIGH"

# ----------------- REST API ROUTES -----------------

@app.get("/api/overview")
def get_overview_statistics():
    return {
        "investigation_statistics": {
            "active_investigations": len(DATASTORE["cases"]),
            "evidence_items": len(DATASTORE["evidence_items"]),
            "entities": len(DATASTORE["nodes"]),
            "relationships": len(DATASTORE["edges"]),
            "suspicious_patterns": len(DATASTORE["anomalies"]),
            "high_priority_leads": len(DATASTORE["leads"])
        },
        "investigation_health": {
            "evidence_coverage": "94.2%",
            "unresolved_entities": 1,
            "high_risk_relationships": 8,
            "recent_evidence_count": 6,
            "pending_analyst_review": 3
        },
        "recent_activity": [
            {"time": "10 mins ago", "event": "New CDR dataset imported for Case TRACE-2026-017", "domain": "CDR"},
            {"time": "25 mins ago", "event": "Financial hawala indicator flagged on HDFC Acc ACC-IND-994101", "domain": "FINANCIAL"},
            {"time": "45 mins ago", "event": "Blockchain wallet 0x71a...9b4 linked via OSINT crawl", "domain": "BLOCKCHAIN"},
            {"time": "1 hour ago", "event": "Entity resolution candidate 'R. Sharma' flagged for review", "domain": "RESOLUTION"},
            {"time": "2 hours ago", "event": "CCTV Cam C12 ANPR frame hash verified on Blockchain Ledger", "domain": "DVR"}
        ],
        "alert_panel": [
            {"severity": "HIGH", "alert": "Unusual communication burst detected (420% spike pre-incident)"},
            {"severity": "HIGH", "alert": "Rapid multi-hop fund movement detected (₹25L transferred in 18 min)"},
            {"severity": "MEDIUM", "alert": "Temporal correlation detected around Incident #1042"}
        ]
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
def create_case(req: CreateCaseRequest):
    case_id = f"TRACE-2026-{len(DATASTORE['cases']) + 18:03d}"
    new_case = {
        "id": case_id,
        "title": req.title,
        "subject_name": req.subject_name,
        "subject_known_identifiers": {"phone": [], "email": [], "aliases": [], "vehicle": [], "wallet": [], "account": []},
        "description": req.description,
        "investigator": req.investigator,
        "agency": req.agency,
        "priority": req.priority,
        "status": "ACTIVE",
        "start_date": time.strftime("%Y-%m-%d"),
        "tags": ["NEW_INVESTIGATION"]
    }
    DATASTORE["cases"][case_id] = new_case
    evidence_ledger.add_evidence_block(
        case_id=case_id,
        action_type="CASE_INITIALIZED",
        actor=req.investigator,
        data_payload={"title": req.title, "agency": req.agency}
    )
    return {"success": True, "case": new_case}

@app.get("/api/evidence")
def get_evidence_list(case_id: Optional[str] = None):
    items = DATASTORE["evidence_items"]
    if case_id:
        items = [e for e in items if e["case_id"] == case_id]
    return {"evidence_items": items}

@app.get("/api/evidence/{evidence_id}")
def get_evidence_item(evidence_id: str):
    item = next((e for e in DATASTORE["evidence_items"] if e["id"] == evidence_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Evidence item not found")
    return item

@app.post("/api/evidence")
def upload_evidence_item(
    case_id: str = Query(...),
    title: str = Query(...),
    evidence_type: str = Query(...),
    source: str = Query(...),
    analyst_notes: Optional[str] = Query("")
):
    evd_id = f"EVD-{evidence_type[:3].upper()}-{len(DATASTORE['evidence_items']) + 601}"
    file_hash = f"sha256:{hash(title + str(time.time()))&0xffffffffffffffff:x}"
    
    new_evd = {
        "id": evd_id,
        "case_id": case_id,
        "title": title,
        "evidence_type": evidence_type,
        "source": source,
        "acquisition_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "file_hash": file_hash,
        "file_size_bytes": 1024500,
        "integrity_status": "VERIFIED",
        "processing_status": "PROCESSED",
        "provenance": f"Investigator Upload via Evidence Center on {time.strftime('%Y-%m-%d')}",
        "analyst_notes": analyst_notes
    }
    
    DATASTORE["evidence_items"].append(new_evd)
    
    evidence_ledger.add_evidence_block(
        case_id=case_id,
        action_type="EVIDENCE_MANUALLY_INGESTED",
        actor="Investigator",
        data_payload={"evidence_id": evd_id, "title": title, "file_hash": file_hash}
    )
    
    return {"success": True, "evidence": new_evd}

@app.post("/api/entities/extract")
def extract_entities(req: NLPExtractRequest):
    res = nlp_engine.extract_from_text(req.text)
    if req.auto_add_to_graph:
        for ent in res["entities"]:
            if not any(n["id"] == ent["id"] for n in DATASTORE["nodes"]):
                DATASTORE["nodes"].append(ent)
    return {"success": True, "extracted": res}

@app.post("/api/entities/resolve")
def resolve_entities(req: ResolveRequest):
    res = nlp_engine.resolve_entities(req.primary_entity_id, req.candidate_entity_id, DATASTORE["nodes"])
    return res

@app.get("/api/graph")
def get_graph():
    analytics = graph_engine.analyze_graph(DATASTORE["nodes"], DATASTORE["edges"])
    return {
        "nodes": DATASTORE["nodes"],
        "edges": DATASTORE["edges"],
        "analytics": analytics
    }

@app.get("/api/graph/path")
def get_shortest_path(source_id: str = Query(...), target_id: str = Query(...)):
    return graph_engine.find_shortest_path(DATASTORE["nodes"], DATASTORE["edges"], source_id, target_id)

@app.get("/api/timeline")
def get_timeline(period: Optional[str] = "24h"):
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
    return {"period": period, "events": timeline_events}

@app.get("/api/communications")
def get_communications():
    comm_edges = [e for e in DATASTORE["edges"] if e.get("domain") == "COMMUNICATION"]
    return {
        "total_calls": 1042,
        "unique_contacts": 84,
        "incoming_outgoing_ratio": "1.42",
        "flagged_bursts": 2,
        "communication_edges": comm_edges
    }

@app.get("/api/financial")
def get_financial():
    fin_edges = [e for e in DATASTORE["edges"] if e.get("domain") == "FINANCIAL"]
    return {
        "total_transactions": 540,
        "hawala_risk_indicators": 1,
        "circular_movement_chains": 1,
        "financial_edges": fin_edges
    }

@app.get("/api/blockchain")
def get_blockchain():
    blk_edges = [e for e in DATASTORE["edges"] if e.get("domain") == "BLOCKCHAIN"]
    return {
        "monitored_wallets": 8,
        "flagged_offramps": 1,
        "blockchain_edges": blk_edges
    }

@app.get("/api/osint")
def get_osint():
    osint_edges = [e for e in DATASTORE["edges"] if e.get("domain") == "OSINT"]
    return {
        "crawled_sources": 52,
        "correlated_handles": 3,
        "osint_edges": osint_edges
    }

@app.get("/api/dvr")
def get_dvr():
    dvr_edges = [e for e in DATASTORE["edges"] if e.get("domain") == "DVR"]
    return {
        "monitored_cameras": 20,
        "anpr_detections": 100,
        "dvr_edges": dvr_edges
    }

@app.get("/api/anomalies")
def get_anomalies():
    detected = anomaly_engine.detect_anomalies(DATASTORE["nodes"], DATASTORE["edges"], DATASTORE["evidence_items"])
    return {"anomalies": detected}

@app.get("/api/fusion")
def get_evidence_fusion(case_id: Optional[str] = "TRACE-2026-017"):
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
def generate_report(case_id: Optional[str] = "TRACE-2026-017"):
    case_data = DATASTORE["cases"].get(case_id, DATASTORE["cases"]["TRACE-2026-017"])
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
