import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from typing import Dict, List, Any, Optional

from backend.mock_data_generator import generate_synthetic_dataset
from backend.report_generator import report_generator

app = FastAPI(
    title="TRACE FINDERS — AI-Powered Criminal Network Intelligence & Evidence Fusion Workstation",
    description="SIH 2026 Problem Statement SIH26189 - AI-Powered Criminal Network Analysis System",
    version="10.0.0"
)

DATASTORE = generate_synthetic_dataset()

# ----------------- DATA INTEGRITY VALIDATION CHECK (REQUIREMENT 19) -----------------
def validate_person_data():
    profiles = DATASTORE["profiles"]
    phone_set, email_set, vehicle_set, account_set, wallet_set = set(), set(), set(), set(), set()
    
    for pid, p in profiles.items():
        assert p["phone"] not in phone_set, f"Duplicate phone for {pid}"
        assert p["email"] not in email_set, f"Duplicate email for {pid}"
        assert p["vehicle"] not in vehicle_set, f"Duplicate vehicle for {pid}"
        assert p["account_number"] not in account_set, f"Duplicate account for {pid}"
        assert p["wallet_address"] not in wallet_set, f"Duplicate wallet for {pid}"
        
        phone_set.add(p["phone"])
        email_set.add(p["email"])
        vehicle_set.add(p["vehicle"])
        account_set.add(p["account_number"])
        wallet_set.add(p["wallet_address"])
    
    print("[OK] DATA INTEGRITY VALIDATION PASSED: All 6 profiles have 100% isolated identifiers.")

validate_person_data()

# ----------------- GRAPH GENERATOR FUNCTION -----------------
def generate_person_graph(pid: str) -> Dict[str, Any]:
    if pid not in DATASTORE["profiles"]:
        pid = "P-001"
    
    root = DATASTORE["profiles"][pid]
    nodes = []
    edges = []

    nodes.append({
        "id": pid,
        "label": root["name"],
        "type": "PERSON",
        "role": root["role"],
        "risk_score": root["risk_score"],
        "tree_level": 0,
        "avatar": root["photo_url"],
        "personId": pid
    })

    connected_person_ids = []
    if pid == "P-001":
        connected_person_ids = ["P-002", "P-003", "P-004", "P-005"]
    elif pid == "P-002":
        connected_person_ids = ["P-001", "P-003"]
    elif pid == "P-003":
        connected_person_ids = ["P-001", "P-002"]
    elif pid == "P-004":
        connected_person_ids = ["P-001"]
    elif pid == "P-005":
        connected_person_ids = ["P-001"]
    elif pid == "P-006":
        connected_person_ids = ["P-001"]

    for other_id in connected_person_ids:
        other = DATASTORE["profiles"][other_id]
        nodes.append({
            "id": other_id,
            "label": other["name"],
            "type": "PERSON",
            "role": other["role"],
            "risk_score": other["risk_score"],
            "tree_level": 1,
            "avatar": other["photo_url"],
            "personId": other_id
        })
        edges.append({
            "id": f"EDGE-{pid}-{other_id}",
            "source": pid,
            "target": other_id,
            "relation": other["role"].upper(),
            "confidence": "85%",
            "evidence_id": f"EV-REL-{pid}-{other_id}"
        })

    nodes.append({
        "id": f"PHONE-{pid}",
        "label": f"Phone ({root['phone']})",
        "type": "PHONE",
        "tree_level": 1,
        "personId": pid
    })
    edges.append({
        "id": f"EDGE-{pid}-PHONE",
        "source": pid,
        "target": f"PHONE-{pid}",
        "relation": "REGISTERED PHONE",
        "evidence_id": f"EV-COM-{pid}-001"
    })

    nodes.append({
        "id": f"VEHICLE-{pid}",
        "label": f"Vehicle ({root['vehicle']})",
        "type": "VEHICLE",
        "tree_level": 1,
        "personId": pid
    })
    edges.append({
        "id": f"EDGE-{pid}-VEHICLE",
        "source": pid,
        "target": f"VEHICLE-{pid}",
        "relation": "REGISTERED VEHICLE",
        "evidence_id": f"EV-LOC-{pid}-001"
    })

    nodes.append({
        "id": f"FIN-{pid}",
        "label": f"Bank Acc ({root['account_number']})",
        "type": "BANK_ACCOUNT",
        "tree_level": 1,
        "personId": pid
    })
    edges.append({
        "id": f"EDGE-{pid}-FIN",
        "source": pid,
        "target": f"FIN-{pid}",
        "relation": "BANK WIRE ACCOUNT",
        "evidence_id": f"EV-FIN-{pid}-001"
    })

    nodes.append({
        "id": f"WALLET-{pid}",
        "label": f"Crypto Wallet ({root['wallet_address'][:10]}...)",
        "type": "WALLET",
        "tree_level": 1,
        "personId": pid
    })
    edges.append({
        "id": f"EDGE-{pid}-WALLET",
        "source": pid,
        "target": f"WALLET-{pid}",
        "relation": "BLOCKCHAIN WALLET",
        "evidence_id": f"EV-BC-{pid}-001"
    })

    nodes.append({
        "id": f"ORG-{pid}",
        "label": f"Org ({root['organization']})",
        "type": "ORGANIZATION",
        "tree_level": 1,
        "personId": pid
    })
    edges.append({
        "id": f"EDGE-{pid}-ORG",
        "source": pid,
        "target": f"ORG-{pid}",
        "relation": "EMPLOYMENT / ENTITY",
        "evidence_id": f"EV-OSINT-{pid}-001"
    })

    cctv_list = DATASTORE["cctv"].get(pid, [])
    if cctv_list:
        cctv_ev = cctv_list[0]
        nodes.append({
            "id": f"EVIDENCE-{cctv_ev['id']}",
            "label": f"CCTV ({cctv_ev['event_title']})",
            "type": "EVIDENCE",
            "tree_level": 2,
            "personId": pid
        })
        edges.append({
            "id": f"EDGE-{pid}-CCTV",
            "source": pid,
            "target": f"EVIDENCE-{cctv_ev['id']}",
            "relation": "SURVEILLANCE SIGHTING",
            "evidence_id": cctv_ev["id"]
        })

    return {
        "header_stats": {
            "case_id": "TRX-2026-017",
            "subject_id": pid,
            "subject_name": root["name"],
            "entities_count": len(nodes),
            "relationships_count": len(edges),
            "evidence_links_count": root.get("evidence_count", 14)
        },
        "nodes": nodes,
        "edges": edges
    }

# ----------------- REST API ROUTES -----------------

@app.get("/api/overview")
def get_overview_statistics(case_id: Optional[str] = "TRX-2026-017", person_id: Optional[str] = "P-001"):
    pid = person_id if person_id in DATASTORE["profiles"] else "P-001"
    prof = DATASTORE["profiles"][pid]
    cctv_list = DATASTORE["cctv"].get(pid, [])

    return {
        "case_summary": {
            "case_id": case_id,
            "title": "OPERATION NEXUS",
            "primary_subject": prof["name"],
            "person_id": pid,
            "entities_count": 137,
            "evidence_count": prof.get("evidence_count", 24),
            "relationships_count": prof.get("relationship_count", 7),
            "communications_count": prof["counts"].get("calls", 187) + prof["counts"].get("messages", 234),
            "financial_count": prof["counts"].get("financial", 63),
            "osint_count": prof["counts"].get("osint", 42),
            "blockchain_count": prof["counts"].get("blockchain", 18),
            "cctv_count": len(cctv_list)
        },
        "investigation_activity": [
            {"time": "09:42", "event": f"Communication activity logged for {prof['name']} ({prof['phone']})", "domain": "CDR"},
            {"time": "10:18", "event": f"Financial transaction verified for account {prof['account_number']}", "domain": "FINANCIAL"},
            {"time": "11:03", "event": f"Public-Source record matched for {prof['social_usernames'].get('twitter', '@user')}", "domain": "OSINT"},
            {"time": "13:41", "event": f"CCTV sighting recorded for vehicle {prof['vehicle']}", "domain": "DVR"},
            {"time": "15:08", "event": f"Blockchain wallet activity verified ({prof['wallet_address']})", "domain": "BLOCKCHAIN"}
        ]
    }

@app.get("/api/cases")
def get_all_cases():
    return {"cases": list(DATASTORE["cases"].values())}

@app.get("/api/persons/{person_id}")
def get_person_profile(person_id: str):
    pid = person_id if person_id in DATASTORE["profiles"] else "P-001"
    prof = DATASTORE["profiles"][pid]
    cctv_recs = DATASTORE["cctv"].get(pid, [])

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
        "cctv": cctv_recs
    }

@app.get("/api/graph")
def get_graph(case_id: Optional[str] = "TRX-2026-017", person_id: Optional[str] = "P-001"):
    pid = person_id if person_id in DATASTORE["profiles"] else "P-001"
    return generate_person_graph(pid)

@app.get("/api/cameras")
def get_cameras_inventory(
    search: Optional[str] = None,
    status: Optional[str] = None,
    location: Optional[str] = None,
    camera_type: Optional[str] = None
):
    cameras = DATASTORE["camera_inventory"]

    if search:
        q = search.lower()
        cameras = [c for c in cameras if q in c["id"].lower() or q in c["name"].lower() or q in c["location"].lower()]
    if status and status != "ALL":
        cameras = [c for c in cameras if c["status"] == status]
    if location and location != "ALL":
        cameras = [c for c in cameras if location.lower() in c["location"].lower()]
    if camera_type and camera_type != "ALL":
        cameras = [c for c in cameras if camera_type.lower() in c["camera_type"].lower()]

    active_cnt = len([c for c in DATASTORE["camera_inventory"] if c["status"] == "Active Recording"])
    archived_cnt = len([c for c in DATASTORE["camera_inventory"] if c["status"] == "Archived"])
    total_events = sum([c["events_count"] for c in DATASTORE["camera_inventory"]])
    total_evidence = sum([c["evidence_links"] for c in DATASTORE["camera_inventory"]])

    return {
        "summary": {
            "total_cameras": len(DATASTORE["camera_inventory"]),
            "active_cameras": active_cnt,
            "archived_cameras": archived_cnt,
            "total_events": total_events,
            "evidence_links": total_evidence
        },
        "cameras": cameras
    }

@app.get("/api/dvr")
def get_dvr(
    person_id: Optional[str] = "P-001",
    camera_id: Optional[str] = None,
    search: Optional[str] = None,
    status: Optional[str] = None
):
    pid = person_id if person_id in DATASTORE["profiles"] else "P-001"
    prof = DATASTORE["profiles"][pid]

    person_cctv_events = DATASTORE["cctv"].get(pid, [])
    if camera_id and camera_id != "ALL":
        person_cctv_events = [v for v in person_cctv_events if v["camera_id"] == camera_id]

    cameras = DATASTORE["camera_inventory"]
    if search:
        q = search.lower()
        cameras = [c for c in cameras if q in c["id"].lower() or q in c["name"].lower() or q in c["location"].lower()]
    if status and status != "ALL":
        cameras = [c for c in cameras if c["status"] == status]

    all_events_table = [
        {"time": "20:01:14", "camera_id": "CAM-04", "event": "Person Meeting", "person": "Arjun Sharma", "location": "Shivajinagar", "evidence_id": "EV-CCTV-031", "status": "Verified"},
        {"time": "20:17:38", "camera_id": "CAM-04", "event": "Physical Exchange Event", "person": "Rohan Mehta", "location": "Shivajinagar", "evidence_id": "EV-CCTV-032", "status": "Under Review"},
        {"time": "20:26:11", "camera_id": "CAM-04", "event": "Vehicle Departure", "person": "Vikram Patil", "location": "Shivajinagar", "evidence_id": "EV-CCTV-033", "status": "Verified"},
        {"time": "20:42:51", "camera_id": "CAM-01", "event": "Office Entry", "person": "Neha Kulkarni", "location": "Viman Nagar", "evidence_id": "EV-CCTV-NEH-001", "status": "Verified"},
        {"time": "15:15:00", "camera_id": "CAM-02", "event": "Security Scan Log", "person": "Priya Joshi", "location": "Baner", "evidence_id": "EV-CCTV-PRI-001", "status": "Verified"},
        {"time": "18:10:00", "camera_id": "CAM-12", "event": "Toll ANPR Reader", "person": "Vikram Patil", "location": "Expressway", "evidence_id": "EV-CCTV-VIK-001", "status": "Verified"}
    ]

    return {
        "header_stats": {
            "case_id": "TRX-2026-017",
            "subject_id": pid,
            "subject_name": prof["name"],
            "total_cameras": 12,
            "active_cameras": 10,
            "archived_cameras": 2,
            "total_events": 87,
            "evidence_links": 54,
            "person_events_count": len(DATASTORE["cctv"].get(pid, []))
        },
        "camera_inventory": cameras,
        "dvr_videos": person_cctv_events,
        "all_camera_events": all_events_table
    }

@app.get("/api/communications")
def get_communications(person_id: Optional[str] = "P-001"):
    pid = person_id if person_id in DATASTORE["profiles"] else "P-001"
    prof = DATASTORE["profiles"][pid]
    return {
        "total_events": prof["counts"]["calls"] + prof["counts"]["messages"],
        "calls": prof["counts"]["calls"],
        "messages": prof["counts"]["messages"],
        "unique_contacts": prof["counts"]["contacts"],
        "active_period": "03 Aug – 18 Aug 2026",
        "contacts": [
            {"id": "P-002", "name": "Rohan Mehta", "role": "Business Contact", "calls": 27, "phone": "+91 97765 4826"},
            {"id": "P-003", "name": "Priya Joshi", "role": "Associate", "calls": 14, "phone": "+91 96765 7315"}
        ],
        "history": [
            {"date": "18 Aug 2026", "time": "20:02:14", "direction": "Outgoing", "duration": "04:21", "evidence_id": f"EV-COM-{pid}-001", "contact": "Rohan Mehta"}
        ]
    }

@app.get("/api/financial")
def get_financial(person_id: Optional[str] = "P-001"):
    pid = person_id if person_id in DATASTORE["profiles"] else "P-001"
    prof = DATASTORE["profiles"][pid]
    return {
        "account": prof["account_number"],
        "balance": "₹14,50,000",
        "transactions": [
            {"date": "18 Aug 2026", "time": "20:58", "amount": "₹48,500", "direction": "OUT", "account": prof["account_number"], "counterparty": "Rohan Mehta", "reference": "TXN-88421", "evidence_id": f"EV-FIN-{pid}-001"}
        ]
    }

@app.get("/api/blockchain")
def get_blockchain(person_id: Optional[str] = "P-001"):
    pid = person_id if person_id in DATASTORE["profiles"] else "P-001"
    prof = DATASTORE["profiles"][pid]
    return {
        "address": prof["wallet_address"],
        "balance": "8.42 ETH",
        "associated_evidence": f"EV-BC-{pid}-001",
        "incoming": 12, "outgoing": 10,
        "transactions": [
            {"hash": f"TX-{pid}-001", "from_addr": prof["wallet_address"], "to_addr": "0x3910...199", "value": "1.20 ETH", "time": "18 Aug 2026 21:17:04", "evidence_id": f"EV-BC-{pid}-001"}
        ]
    }

@app.get("/api/osint")
def get_osint(person_id: Optional[str] = "P-001"):
    pid = person_id if person_id in DATASTORE["profiles"] else "P-001"
    prof = DATASTORE["profiles"][pid]
    return {"records": [{"id": f"PSI-{pid}-01", "subject": prof["name"], "source": "Public Web", "last_observed": "18 Aug 2026", "entity": prof["organization"], "location": prof["city"], "evidence_id": f"EV-OSINT-{pid}-001", "confidence": "90%", "value": f"{prof['social_usernames'].get('twitter', '@user')} profile"}]}

@app.get("/api/timeline")
def get_timeline(person_id: Optional[str] = "P-001"):
    pid = person_id if person_id in DATASTORE["profiles"] else "P-001"
    prof = DATASTORE["profiles"][pid]
    return {
        "temporal_assessment": f"TEMPORAL RELATIONSHIP DETECTED for {prof['name']}: Short window events logged.",
        "events": [
            {"id": f"EV-TIM-{pid}-01", "timestamp": "18 Aug 2026 20:01:00", "title": f"CCTV SIGHTING ({prof['name']})", "domain": "DVR", "details": f"CAM-04 capture of {prof['name']}.", "evidence_id": f"EV-CCTV-031", "person": prof["name"], "location": prof["city"]}
        ]
    }

@app.get("/api/evidence/{evidence_id}")
def get_evidence_detail(evidence_id: str):
    return {
        "id": evidence_id,
        "case_id": "TRX-2026-017",
        "personId": "P-001",
        "title": f"Evidence Record {evidence_id}",
        "evidence_type": "DVR/NVR Forensics",
        "source": "Surveillance CAM-04",
        "acquisition_timestamp": "18 Aug 2026 20:01:00",
        "acquisition_date": "18 Aug 2026",
        "acquisition_time": "20:01:00",
        "file_hash": "d41d8cd98f00b204e9800998ecf8427e56b3e66487e44a49c6d3ff3cf81734f2",
        "integrity_status": "Verified",
        "provenance": "Seized NVR hard drive #NVR-702 frame carving.",
        "analyst_notes": f"Surveillance video capture associated with evidence ID {evidence_id}."
    }

# ----------------- PERSON-SCOPED REPORT REST API (REQUIREMENTS 1 - 21) -----------------
@app.post("/api/reports/generate")
@app.get("/api/reports/generate")
def generate_report(case_id: Optional[str] = "TRX-2026-017", person_id: Optional[str] = "P-001"):
    pid = person_id if person_id in DATASTORE["profiles"] else "P-001"
    person_data = DATASTORE["profiles"][pid]
    cctv_events = DATASTORE["cctv"].get(pid, [])
    case_data = DATASTORE["cases"].get("TRX-2026-017", {})
    fusion_data = {"explainable_ai": {"WHAT": "Multi-hop intelligence chain correlated across CDR, DVR, and Financial logs."}}
    
    res = report_generator.generate_report(case_data, person_data, cctv_events, fusion_data)
    return res

@app.get("/api/search")
def global_search(q: str = Query(...)):
    query = q.lower()
    matched_profiles = [p for p in DATASTORE["profiles"].values() if query in p["name"].lower()]
    return {"query": q, "matched_cases": [], "matched_nodes": matched_profiles, "matched_evidence": []}

# Serve Static Files
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static"))

@app.get("/", response_class=HTMLResponse)
def serve_index():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return HTMLResponse("<h1>TRACE FINDERS Workstation Loading...</h1>")

app.mount("/static", StaticFiles(directory=static_dir), name="static")
