# 📡 REST API SPECIFICATION — TRACE FINDERS

**API Version:** `v1.0.0`  
**Base URL (Vercel Cloud):** `https://criminalnetworkanalysis.vercel.app/api`  
**Base URL (Local Node):** `http://localhost:8000/api`  
**Content-Type:** `application/json`  

---

## 📑 API Endpoints Summary

| Method | Path | Description | Query Parameters |
| :--- | :--- | :--- | :--- |
| `GET` | `/overview` | Case overview statistics & activity stream | `case_id`, `person_id` |
| `GET` | `/cases` | Registered case list & suspects | None |
| `GET` | `/persons/{person_id}` | Detailed single person profile | Path: `person_id` |
| `GET` | `/fusion` | Multi-hop evidence chain & XAI assessment | `person_id` |
| `GET` | `/graph` | Vis.js Knowledge Graph nodes & edges | `case_id`, `person_id` |
| `GET` | `/communications` | CDR telecom history & contact tree | `person_id` |
| `GET` | `/financial` | Financial ledger transactions & Hawala triggers | `person_id` |
| `GET` | `/blockchain` | EVM/UTXO wallet transactions | `person_id` |
| `GET` | `/osint` | Public-source crawled intelligence records | `person_id` |
| `GET` | `/dvr` | CCTV camera inventory & 24h event timeline | `person_id` |
| `GET` | `/timeline` | Person investigative chronology events | `person_id` |
| `GET` | `/evidence/{id}` | Single evidence record details & SHA-256 hash | Path: `id` |
| `GET` | `/reports/generate` | Render person-scoped HTML dossier | `case_id`, `person_id` |
| `GET` | `/search` | Global entity & evidence search query | `q` |

---

## 🔍 Endpoint Specifications

### 1. `GET /api/overview`
Retrieves operational summary metrics, recent investigation activity stream, and AI leads.

#### Query Parameters
- `case_id` (string, default: `"TRX-2026-017"`)
- `person_id` (string, default: `"P-001"`)

#### Response (`200 OK`)
```json
{
  "status": "success",
  "case_summary": {
    "case_id": "TRX-2026-017",
    "title": "OPERATION NEXUS",
    "primary_subject": "Arjun Sharma",
    "evidence_count": 24,
    "relationships_count": 7,
    "communications_count": 421,
    "financial_count": 63,
    "osint_count": 42,
    "blockchain_count": 18,
    "cctv_count": 3
  },
  "investigation_activity": [
    {
      "time": "09:42",
      "event": "Communication activity logged for Arjun Sharma (+91 98765 1201)",
      "domain": "CDR"
    }
  ]
}
```

---

### 2. `GET /api/fusion`
Returns the person-scoped 5-step cross-domain multi-hop evidence chain and XAI rationale.

#### Query Parameters
- `person_id` (string, required, e.g. `"P-001"`)

#### Response (`200 OK`)
```json
{
  "person_id": "P-001",
  "person_name": "Arjun Sharma",
  "role": "Primary Subject",
  "multi_hop_chain": [
    {
      "step": 1,
      "domain": "PROFILE",
      "label": "Arjun Sharma Profile Identified",
      "detail": "Phone: +91 98765 1201 | City: Pune",
      "badge": "EV-PROF-001"
    }
  ],
  "explainable_ai": {
    "title": "MULTI-HOP INTELLIGENCE CORRELATION FOR ARJUN SHARMA",
    "confidence_score": "88%",
    "action_status": "VERIFIED CORRELATION",
    "what": "High cross-domain evidence link score observed.",
    "why": "Matching timestamps between CDR tower log and ANPR camera.",
    "alternative_explanation": "Coincidental proximity during commercial hours.",
    "supporting_evidence": ["EV-COM-001", "EV-CCTV-031"]
  }
}
```

---

### 3. `GET /api/graph`
Returns nodes and edges formatted for interactive Vis.js graph rendering.

#### Query Parameters
- `case_id` (string)
- `person_id` (string)

#### Response (`200 OK`)
```json
{
  "header_stats": {
    "subject_name": "Arjun Sharma",
    "entities_count": 8,
    "relationships_count": 7,
    "evidence_links_count": 14
  },
  "nodes": [
    {
      "id": "P-001",
      "label": "Arjun Sharma",
      "type": "PERSON",
      "role": "Primary Subject",
      "tree_level": 1
    }
  ],
  "edges": [
    {
      "id": "EDGE-001",
      "source": "P-001",
      "target": "PHONE-P-001",
      "relation": "USES_PHONE",
      "evidence_id": "EV-COM-001"
    }
  ]
}
```

---

### 4. `GET /api/dvr`
Returns CCTV camera inventory (all 12 cameras) and 24-hour event markers.

#### Response (`200 OK`)
```json
{
  "camera_inventory": [
    {
      "id": "CAM-01",
      "name": "TechDesk Gate 1",
      "location": "Viman Nagar, Pune",
      "camera_type": "Fixed CCTV",
      "status": "Active Recording",
      "recording_window": "00:00 - 23:59",
      "events_count": 14,
      "evidence_links": 6
    }
  ]
}
```
