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

from backend.models import Case, Entity, Relationship, EvidenceItem, InvestigativeLead, SuspectProfile
from backend.mock_data_generator import generate_synthetic_dataset
from backend.report_generator import report_generator

app = FastAPI(
    title="TRACE-X — AI-Powered Criminal Network Intelligence & Evidence Fusion Workstation",
    description="SIH 2026 Problem Statement SIH26189 - AI-Powered Criminal Network Analysis System",
    version="5.0.0"
)

DATASTORE = generate_synthetic_dataset()

# ----------------- REST API ROUTES -----------------

@app.get("/api/overview")
def get_overview_statistics(case_id: Optional[str] = "TRX-2026-017", person_id: Optional[str] = "P-001"):
    pid = person_id or "P-001"
    prof = DATASTORE["profiles"].get(pid, DATASTORE["profiles"]["P-001"])
    counts = prof.get("counts", {})
    leads = DATASTORE["leads"].get(pid, DATASTORE["leads"]["P-001"])

    return {
        "case_summary": {
            "case_id": case_id,
            "title": "OPERATION NEXUS",
            "primary_subject": prof["name"],
            "person_id": pid,
            "entities_count": 137,
            "evidence_count": prof.get("evidence_count", 24),
            "relationships_count": prof.get("relationship_count", 7),
            "communications_count": counts.get("calls", 187) + counts.get("messages", 234),
            "financial_count": counts.get("financial", 63),
            "osint_count": counts.get("osint", 42),
            "blockchain_count": counts.get("blockchain", 18),
            "cctv_count": counts.get("cctv", 9)
        },
        "investigation_activity": [
            {"time": "09:42", "event": f"Communication activity logged for {prof['name']} ({prof['phone']})", "domain": "CDR"},
            {"time": "10:18", "event": f"Financial transaction verified for account {prof['account_number']}", "domain": "FINANCIAL"},
            {"time": "11:03", "event": f"Public-Source record matched for {prof['social_usernames'].get('twitter', '@user')}", "domain": "OSINT"},
            {"time": "13:41", "event": f"CCTV sighting recorded for vehicle {prof['vehicle']}", "domain": "DVR"},
            {"time": "15:08", "event": f"Blockchain wallet activity verified ({prof['wallet_address']})", "domain": "BLOCKCHAIN"}
        ],
        "ai_leads": leads
    }

@app.get("/api/cases")
def get_all_cases():
    return {"cases": list(DATASTORE["cases"].values())}

@app.get("/api/persons/{person_id}")
def get_person_profile(person_id: str):
    pid = person_id if person_id in DATASTORE["profiles"] else "P-001"
    prof = DATASTORE["profiles"][pid]
    comm = DATASTORE["communications"][pid]
    fin = DATASTORE["financial"][pid]
    blk = DATASTORE["blockchain"][pid]
    osint_recs = DATASTORE["osint"][pid]
    cctv_recs = DATASTORE["cctv"][pid]
    leads_recs = DATASTORE["leads"][pid]

    # Generate person-scoped relationships (Requirement 16)
    relationships = []
    for other_id, other_prof in DATASTORE["profiles"].items():
        if other_id != pid and other_id != "P-006":
            relationships.append({
                "id": f"REL-{pid}-{other_id}",
                "sourcePersonId": pid,
                "targetPersonId": other_id,
                "relation": "BUSINESS" if other_id in ["P-002", "P-003"] else "MEETING",
                "target_name": other_prof["name"],
                "target_role": other_prof["role"],
                "confidence": 0.85,
                "domain": "COMMUNICATION",
                "explanation": f"Observed communication & organizational link between {prof['name']} and {other_prof['name']}."
            })

    return {
        "person": prof,
        "connected_counts": prof["counts"],
        "relationships": relationships,
        "communications": comm,
        "financial": fin,
        "blockchain": blk,
        "osint": osint_recs,
        "cctv": cctv_recs,
        "leads": leads_recs
    }

@app.get("/api/communications")
def get_communications(person_id: Optional[str] = "P-001"):
    pid = person_id if person_id in DATASTORE["communications"] else "P-001"
    return DATASTORE["communications"][pid]

@app.get("/api/financial")
def get_financial(person_id: Optional[str] = "P-001"):
    pid = person_id if person_id in DATASTORE["financial"] else "P-001"
    fin_data = DATASTORE["financial"][pid]
    
    return {
        "account": fin_data["account"],
        "balance": fin_data["balance"],
        "transactions": fin_data["transactions"],
        "hawala_analysis": {
            "title": "INFORMAL VALUE TRANSFER INDICATORS",
            "assessment": f"Informal value transfer analysis for {DATASTORE['profiles'][pid]['name']}",
            "status": "Requires investigative verification",
            "indicators": [
                {"name": "Repeated third-party transfers", "status": "OBSERVED", "details": "Transfers logged across counterparty accounts."},
                {"name": "Rapid account movement", "status": "OBSERVED" if pid in ["P-001", "P-002"] else "NOT OBSERVED", "details": "Account activity within short window."},
                {"name": "Transaction timing correlated with communication", "status": "OBSERVED" if pid in ["P-001", "P-004"] else "NOT OBSERVED", "details": "Financial activity correlated with CDR bursts."}
            ]
        }
    }

@app.get("/api/blockchain")
def get_blockchain(person_id: Optional[str] = "P-001"):
    pid = person_id if person_id in DATASTORE["blockchain"] else "P-001"
    return DATASTORE["blockchain"][pid]

@app.get("/api/osint")
def get_osint(person_id: Optional[str] = "P-001"):
    pid = person_id if person_id in DATASTORE["osint"] else "P-001"
    return {"records": DATASTORE["osint"][pid]}

@app.get("/api/dvr")
def get_dvr(person_id: Optional[str] = "P-001"):
    pid = person_id if person_id in DATASTORE["cctv"] else "P-001"
    return {"dvr_videos": DATASTORE["cctv"][pid]}

@app.get("/api/timeline")
def get_timeline(person_id: Optional[str] = "P-001"):
    pid = person_id if person_id in DATASTORE["profiles"] else "P-001"
    prof = DATASTORE["profiles"][pid]

    events = [
        {"id": f"EV-TIM-{pid}-01", "timestamp": "18 Aug 2026 20:01:14", "title": f"CCTV SIGHTING ({prof['name']})", "domain": "DVR", "details": f"CAM-04 sighting of {prof['name']} with vehicle {prof['vehicle']}.", "evidence_id": f"EV-CCTV-{pid}-001", "person": prof["name"], "location": prof["city"]},
        {"id": f"EV-TIM-{pid}-02", "timestamp": "18 Aug 2026 20:02:07", "title": f"COMMUNICATION EVENT ({prof['phone']})", "domain": "CDR", "details": f"CDR call event logged for {prof['name']}.", "evidence_id": f"EV-COM-{pid}-001", "person": prof["name"], "location": prof["city"]},
        {"id": f"EV-TIM-{pid}-03", "timestamp": "18 Aug 2026 20:58:18", "title": f"FINANCIAL WIRE ({prof['account_number']})", "domain": "FINANCIAL", "details": f"Transaction recorded for account {prof['account_number']}.", "evidence_id": f"EV-FIN-{pid}-001", "person": prof["name"], "location": prof["city"]},
        {"id": f"EV-TIM-{pid}-04", "timestamp": "18 Aug 2026 21:17:04", "title": f"BLOCKCHAIN TRANSACTION ({prof['wallet_address']})", "domain": "BLOCKCHAIN", "details": f"On-chain transfer from wallet {prof['wallet_address']}.", "evidence_id": f"EV-BC-{pid}-001", "person": prof["name"], "location": "Blockchain"}
    ]

    return {
        "temporal_assessment": f"TEMPORAL RELATIONSHIP DETECTED for {prof['name']}: Multiple events occur within a short temporal window.",
        "events": events
    }

@app.get("/api/leads")
def get_investigative_leads(person_id: Optional[str] = "P-001"):
    pid = person_id if person_id in DATASTORE["leads"] else "P-001"
    return {"leads": DATASTORE["leads"][pid]}

@app.get("/api/graph")
def get_graph(case_id: Optional[str] = "TRX-2026-017", person_id: Optional[str] = "P-001"):
    pid = person_id if person_id in DATASTORE["profiles"] else "P-001"
    root = DATASTORE["profiles"][pid]

    nodes = [
        {"id": pid, "label": root["name"], "type": "PERSON", "risk_score": root["risk_score"], "tree_level": 0, "avatar": root["photo_url"]},
        {"id": f"{pid}_phone", "label": root["phone"], "type": "PHONE", "risk_score": 85, "tree_level": 1},
        {"id": f"{pid}_acc", "label": root["account_number"], "type": "BANK_ACCOUNT", "risk_score": 80, "tree_level": 1},
        {"id": f"{pid}_wallet", "label": root["wallet_address"], "type": "CRYPTO_WALLET", "risk_score": 88, "tree_level": 1},
        {"id": f"{pid}_vehicle", "label": root["vehicle"], "type": "VEHICLE", "risk_score": 75, "tree_level": 1}
    ]

    edges = [
        {"id": f"REL-{pid}-1", "source": pid, "target": f"{pid}_phone", "relation": "CALL", "domain": "COMMUNICATION"},
        {"id": f"REL-{pid}-2", "source": pid, "target": f"{pid}_acc", "relation": "TRANSFER", "domain": "FINANCIAL"},
        {"id": f"REL-{pid}-3", "source": pid, "target": f"{pid}_wallet", "relation": "WALLET", "domain": "BLOCKCHAIN"},
        {"id": f"REL-{pid}-4", "source": pid, "target": f"{pid}_vehicle", "relation": "VEHICLE", "domain": "PHYSICAL"}
    ]

    # Connect other people to root node
    for other_id, other_prof in DATASTORE["profiles"].items():
        if other_id != pid and other_id != "P-006":
            nodes.append({
                "id": other_id,
                "label": other_prof["name"],
                "type": "PERSON",
                "risk_score": other_prof["risk_score"],
                "tree_level": 1,
                "avatar": other_prof["photo_url"]
            })
            edges.append({
                "id": f"REL-{pid}-{other_id}",
                "source": pid,
                "target": other_id,
                "relation": "BUSINESS" if other_id in ["P-002", "P-003"] else "MEETING",
                "domain": "COMMUNICATION"
            })

    return {"nodes": nodes, "edges": edges}

@app.get("/api/evidence/{evidence_id}")
def get_evidence_detail(evidence_id: str):
    return {
        "id": evidence_id,
        "case_id": "TRX-2026-017",
        "personId": "P-001",
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
        "analyst_notes": "Standardized analytical evidence record.",
        "confidence": 0.95,
        "extracted_entities": ["Arjun Sharma", "Rohan Mehta", "Pune"],
        "related_events": ["EV-CCTV-031", "EV-FIN-014"]
    }

@app.get("/api/relationships/{rel_id}/evidence")
def get_relationship_evidence(rel_id: str):
    return {
        "relationship": {"id": rel_id, "first_observed": "03 Aug 2026", "last_observed": "18 Aug 2026", "explanation": "Observed communication & organizational correlation.", "alt_explanation": "Legitimate business coordination."},
        "supporting_evidence": [
            {"id": "EV-SUP-001", "title": "Supporting CDR Call Log"},
            {"id": "EV-SUP-002", "title": "Supporting Bank Transfer Receipt"}
        ]
    }

@app.get("/api/search")
def global_search(q: str = Query(...)):
    query = q.lower()
    matched_profiles = [p for p in DATASTORE["profiles"].values() if query in p["name"].lower() or query in p["phone"].lower() or query in p["email"].lower()]
    return {
        "query": q,
        "matched_cases": [DATASTORE["cases"]["TRX-2026-017"]],
        "matched_nodes": matched_profiles,
        "matched_evidence": [{"id": "EV-COM-ARJ-001", "title": f"Evidence Record matching '{q}'"}],
        "matched_relationships": []
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
