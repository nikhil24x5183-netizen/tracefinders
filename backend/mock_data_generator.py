import random
from datetime import datetime, timedelta
from typing import Dict, List, Any

random.seed(2026189)

def generate_synthetic_dataset() -> Dict[str, Any]:
    # PRIMARY SUBJECT: ARJUN SHARMA
    arjun_profile = {
        "id": "person_arjun_sharma",
        "name": "Arjun Sharma",
        "alias": "Arjun S.",
        "role": "Primary Subject",
        "relationship_to_primary": "Self",
        "age": 34,
        "gender": "Male",
        "photo_url": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=300&auto=format&fit=crop&q=80",
        "phone": "+91 98765 1201",
        "email": "arjun.sharma.demo@example.test",
        "address": "Flat 402, Shivajinagar",
        "city": "Pune, Maharashtra",
        "occupation": "Logistics Consultant",
        "organization": "Nexus Logistics",
        "vehicle": "MH12 AB 4821",
        "social_usernames": {
            "twitter": "@arjun_s_demo",
            "telegram": "@cipher_king",
            "instagram": "@arjun_cyber"
        },
        "wallet_address": "0xDEMO...A721",
        "notes": "Primary subject under investigation for Operation Nexus.",
        "risk_score": 92,
        "evidence_count": 24,
        "relationship_count": 7,
        "status": "Under Investigation",
        "last_updated": "18 Aug 2026 21:17"
    }

    secondary_suspects = [
        {
            "id": "person_rohan_mehta",
            "name": "Rohan Mehta",
            "alias": "Rohan M.",
            "role": "Business Contact",
            "relationship_to_primary": "Business Contact",
            "age": 31,
            "gender": "Male",
            "photo_url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=300&auto=format&fit=crop&q=80",
            "phone": "+91 98765 2002",
            "email": "rohan.m.demo@example.test",
            "address": "Kothrud, Pune",
            "city": "Pune, Maharashtra",
            "occupation": "Logistics Supervisor",
            "organization": "Nexus Express",
            "vehicle": "MH12 XY 9988",
            "social_usernames": {"telegram": "@rohan_runner"},
            "wallet_address": "0x3910ab...199",
            "notes": "27 communication events logged with Arjun Sharma.",
            "risk_score": 85,
            "evidence_count": 18,
            "relationship_count": 5,
            "status": "Under Investigation",
            "last_updated": "18 Aug 2026 20:58"
        },
        {
            "id": "person_priya_joshi",
            "name": "Priya Joshi",
            "alias": "Priya J.",
            "role": "Associate",
            "relationship_to_primary": "Associate",
            "age": 29,
            "gender": "Female",
            "photo_url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=300&auto=format&fit=crop&q=80",
            "phone": "+91 98765 3003",
            "email": "priya.j.demo@example.test",
            "address": "Baner Road, Pune",
            "city": "Pune, Maharashtra",
            "occupation": "Senior Accountant",
            "organization": "Nexus Logistics",
            "vehicle": "MH14 CD 5544",
            "social_usernames": {"linkedin": "in/priya-joshi-demo"},
            "wallet_address": "",
            "notes": "Managed corporate accounts for fund routing.",
            "risk_score": 78,
            "evidence_count": 14,
            "relationship_count": 4,
            "status": "Associate",
            "last_updated": "18 Aug 2026 15:20"
        },
        {
            "id": "person_vikram_patil",
            "name": "Vikram Patil",
            "alias": "Vicky",
            "role": "Person of Interest",
            "relationship_to_primary": "Person of Interest",
            "age": 36,
            "gender": "Male",
            "photo_url": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=300&auto=format&fit=crop&q=80",
            "phone": "+91 98765 4004",
            "email": "vikram.p.demo@example.test",
            "address": "Hadapsar, Pune",
            "city": "Pune, Maharashtra",
            "occupation": "Personal Driver",
            "organization": "Private Fleet",
            "vehicle": "MH12 AB 4821",
            "social_usernames": {"telegram": "@vicky_driver"},
            "wallet_address": "",
            "notes": "Observed driving vehicle MH12 AB 4821 near meeting location.",
            "risk_score": 72,
            "evidence_count": 11,
            "relationship_count": 3,
            "status": "Person of Interest",
            "last_updated": "18 Aug 2026 20:26"
        },
        {
            "id": "person_neha_kulkarni",
            "name": "Neha Kulkarni",
            "alias": "NK",
            "role": "Employee",
            "relationship_to_primary": "Employee",
            "age": 28,
            "gender": "Female",
            "photo_url": "https://images.unsplash.com/photo-1580489944761-15a19d654956?w=300&auto=format&fit=crop&q=80",
            "phone": "+91 98765 5005",
            "email": "neha.k.demo@example.test",
            "address": "Viman Nagar, Pune",
            "city": "Pune, Maharashtra",
            "occupation": "IT Analyst",
            "organization": "TechDesk Systems",
            "vehicle": "",
            "social_usernames": {"twitter": "@neha_k_demo"},
            "wallet_address": "",
            "notes": "Shared IP subnet access with primary subject's VPN server.",
            "risk_score": 58,
            "evidence_count": 8,
            "relationship_count": 2,
            "status": "Employee",
            "last_updated": "18 Aug 2026 11:00"
        }
    ]

    # ENTITY RESOLUTION CANDIDATE MATCH (REQUIREMENT 25)
    ambiguous_candidate = {
        "id": "person_arjun_s_candidate",
        "name": "Arjun S.",
        "alias": "Arjun S (Unresolved)",
        "role": "Candidate Match",
        "relationship_to_primary": "Candidate Match",
        "age": 35,
        "gender": "Male",
        "photo_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300",
        "phone": "+91 98765 9999",
        "email": "arjun.s.ambiguous@example.test",
        "address": "Camp Area, Pune",
        "city": "Pune, Maharashtra",
        "occupation": "Trader",
        "organization": "Unknown",
        "vehicle": "",
        "social_usernames": {"twitter": "@arjun_s_trader"},
        "wallet_address": "",
        "notes": "POTENTIAL MATCH (Confidence 43%). Signals: Name similarity, Location overlap, Organization overlap. Status: Unresolved.",
        "risk_score": 43,
        "evidence_count": 2,
        "relationship_count": 1,
        "status": "Unresolved Candidate"
    }

    # SEEDED DEMO CASES (REQUIREMENT 2 & 23)
    cases_db = {
        "TRX-2026-017": {
            "id": "TRX-2026-017",
            "title": "OPERATION NEXUS",
            "primary_suspect": arjun_profile,
            "secondary_suspects": secondary_suspects,
            "subject_known_identifiers": {
                "phone": ["+91 98765 1201"],
                "email": ["arjun.sharma.demo@example.test"],
                "aliases": ["Arjun S.", "Cipher King"],
                "vehicle": ["MH12 AB 4821"],
                "wallet": ["0xDEMO...A721"],
                "account": ["XXXX4821", "XXXX7194"]
            },
            "description": "Cross-domain intelligence fusion investigating an illicit financial transfer syndicate coordinating extortion, money laundering through informal channels, and crypto off-ramping connected to cyber incident #1042.",
            "investigation_type": "Cyber-Financial Crime",
            "priority": "HIGH",
            "status": "ACTIVE",
            "date_opened": "2026-08-15",
            "lead_investigator": "Ins. Vikramaditya Rao (#INV-7092)",
            "agency": "Special Cyber Crime & Intelligence Cell (SCCIC)",
            "location": "Pune, Maharashtra",
            "tags": ["EXTORTION", "HAWALA_INDICATORS", "CRYPTO_FLOW", "DVR_FORENSIC"],
            "evidence_count": 148,
            "relationships_count": 37,
            "communications_count": 421,
            "financial_count": 63,
            "osint_count": 42,
            "blockchain_count": 18,
            "cctv_count": 9,
            "last_activity": "18 Aug 2026 21:17"
        },
        "TRX-2026-014": {
            "id": "TRX-2026-014",
            "title": "OPERATION MERIDIAN",
            "primary_suspect": {
                "id": "person_vikram_patil_lead",
                "name": "Vikram Patil",
                "alias": "Patil Boss",
                "role": "Primary Subject",
                "photo_url": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=300",
                "phone": "+91 98111 0001",
                "email": "patil.v@meridian.org",
                "city": "Mumbai, Maharashtra",
                "occupation": "Transport Operator",
                "vehicle": "MH01 AB 9900",
                "wallet_address": "0xDEMO...B881"
            },
            "secondary_suspects": [secondary_suspects[0], secondary_suspects[1]],
            "description": "Inquiry into SIM-box telecom routing syndicate operating near Western Corridor.",
            "investigation_type": "Telecom Fraud",
            "priority": "MEDIUM",
            "status": "ACTIVE",
            "date_opened": "2026-07-01",
            "lead_investigator": "Sub-Ins. Neha Gupta (#INV-4401)",
            "agency": "State Cyber Cell",
            "location": "Mumbai, Maharashtra",
            "tags": ["SIM_BOX", "TELECOM_FRAUD"],
            "evidence_count": 41,
            "relationships_count": 18,
            "communications_count": 180,
            "financial_count": 22,
            "osint_count": 14,
            "blockchain_count": 5,
            "cctv_count": 4,
            "last_activity": "18 Aug 2026 19:40"
        },
        "TRX-2026-011": {
            "id": "TRX-2026-011",
            "title": "OPERATION VECTOR",
            "primary_suspect": {
                "id": "person_amit_deshmukh",
                "name": "Amit Deshmukh",
                "alias": "Vector Lead",
                "role": "Primary Subject",
                "photo_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300",
                "phone": "+91 98222 0002",
                "email": "amit.d@vector.org",
                "city": "Nashik, Maharashtra",
                "occupation": "Trader",
                "vehicle": "MH15 XY 1001",
                "wallet_address": ""
            },
            "secondary_suspects": [secondary_suspects[2]],
            "description": "Investigation into shell company invoice layering and tax evasion.",
            "investigation_type": "Financial Fraud",
            "priority": "HIGH",
            "status": "REVIEW",
            "date_opened": "2026-06-10",
            "lead_investigator": "Ins. S. Kulkarni (#INV-3301)",
            "agency": "Economic Offences Wing",
            "location": "Nashik, Maharashtra",
            "tags": ["INVOICE_FRAUD", "SHELL_CORP"],
            "evidence_count": 58,
            "relationships_count": 24,
            "communications_count": 210,
            "financial_count": 45,
            "osint_count": 18,
            "blockchain_count": 8,
            "cctv_count": 5,
            "last_activity": "18 Aug 2026 17:15"
        },
        "TRX-2026-009": {
            "id": "TRX-2026-009",
            "title": "OPERATION ATLAS",
            "primary_suspect": {
                "id": "person_karan_shah",
                "name": "Karan Shah",
                "alias": "Atlas Lead",
                "role": "Primary Subject",
                "photo_url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=300",
                "phone": "+91 98333 0003",
                "email": "karan.s@atlas.org",
                "city": "Pune, Maharashtra",
                "occupation": "Contractor",
                "vehicle": "MH12 PQ 4455",
                "wallet_address": ""
            },
            "secondary_suspects": [],
            "description": "Concluded inquiry into public procurement portal cyber breach.",
            "investigation_type": "Cyber Intrusion",
            "priority": "MEDIUM",
            "status": "CLOSED",
            "date_opened": "2026-05-01",
            "lead_investigator": "Sub-Ins. R. Deshmukh",
            "agency": "Special Cyber Cell",
            "location": "Pune, Maharashtra",
            "tags": ["PORTAL_BREACH", "CONCLUDED"],
            "evidence_count": 32,
            "relationships_count": 12,
            "communications_count": 95,
            "financial_count": 14,
            "osint_count": 10,
            "blockchain_count": 2,
            "cctv_count": 2,
            "last_activity": "16 Aug 2026 12:00"
        },
        "TRX-2026-006": {
            "id": "TRX-2026-006",
            "title": "OPERATION SIGNAL",
            "primary_suspect": {
                "id": "person_sanjay_more",
                "name": "Sanjay More",
                "alias": "Signal Lead",
                "role": "Primary Subject",
                "photo_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=300",
                "phone": "+91 98444 0004",
                "email": "sanjay.m@signal.org",
                "city": "Nagpur, Maharashtra",
                "occupation": "Dealer",
                "vehicle": "MH31 RS 8877",
                "wallet_address": ""
            },
            "secondary_suspects": [],
            "description": "Probe into unauthorized VoIP gateway routing.",
            "investigation_type": "Telecom Fraud",
            "priority": "LOW",
            "status": "ACTIVE",
            "date_opened": "2026-04-12",
            "lead_investigator": "Sub-Ins. A. Joshi",
            "agency": "Nagpur Cyber Crime Cell",
            "location": "Nagpur, Maharashtra",
            "tags": ["VOIP_GATEWAY"],
            "evidence_count": 24,
            "relationships_count": 9,
            "communications_count": 64,
            "financial_count": 8,
            "osint_count": 6,
            "blockchain_count": 0,
            "cctv_count": 1,
            "last_activity": "18 Aug 2026 14:10"
        },
        "TRX-2026-003": {
            "id": "TRX-2026-003",
            "title": "OPERATION HORIZON",
            "primary_suspect": {
                "id": "person_neha_kulkarni_lead",
                "name": "Neha Kulkarni",
                "alias": "Horizon Lead",
                "role": "Primary Subject",
                "photo_url": "https://images.unsplash.com/photo-1580489944761-15a19d654956?w=300",
                "phone": "+91 98555 0005",
                "email": "neha.k@horizon.org",
                "city": "Mumbai, Maharashtra",
                "occupation": "Analyst",
                "vehicle": "MH02 UV 3322",
                "wallet_address": ""
            },
            "secondary_suspects": [],
            "description": "Analysis of phishing infrastructure targeting regional cooperative banks.",
            "investigation_type": "Phishing & Banking Cybercrime",
            "priority": "MEDIUM",
            "status": "REVIEW",
            "date_opened": "2026-03-01",
            "lead_investigator": "Ins. V. Rao",
            "agency": "SCCIC",
            "location": "Mumbai, Maharashtra",
            "tags": ["PHISHING", "BANKING_CYBERCRIME"],
            "evidence_count": 45,
            "relationships_count": 16,
            "communications_count": 140,
            "financial_count": 28,
            "osint_count": 20,
            "blockchain_count": 6,
            "cctv_count": 3,
            "last_activity": "17 Aug 2026 18:30"
        }
    }

    # KNOWLEDGE GRAPH NODES (TREE VIEW DEFAULT & SHORT EDGE LABELS - REQUIREMENT 9 & 10)
    nodes = [
        {"id": "person_arjun_sharma", "label": "Arjun Sharma", "type": "PERSON", "risk_score": 92, "confidence": 1.0, "details": "Primary Subject / Logistics Consultant.", "status": "Under Investigation", "source_evidence_ids": ["EV-COM-001", "EV-FIN-014"], "tree_level": 0, "avatar": arjun_profile["photo_url"]},
        {"id": "person_rohan_mehta", "label": "Rohan Mehta", "type": "PERSON", "risk_score": 85, "confidence": 0.95, "details": "Business Contact. 27 communication events logged.", "status": "Business Contact", "source_evidence_ids": ["EV-COM-001", "EV-FIN-014"], "tree_level": 1, "avatar": secondary_suspects[0]["photo_url"]},
        {"id": "person_priya_joshi", "label": "Priya Joshi", "type": "PERSON", "risk_score": 78, "confidence": 0.92, "details": "Associate / Senior Accountant.", "status": "Associate", "source_evidence_ids": ["EV-FIN-014", "EV-REL-074"], "tree_level": 1, "avatar": secondary_suspects[1]["photo_url"]},
        {"id": "person_vikram_patil", "label": "Vikram Patil", "type": "PERSON", "risk_score": 72, "confidence": 0.90, "details": "Person of Interest / Personal Driver.", "status": "Person of Interest", "source_evidence_ids": ["EV-CCTV-031", "EV-CCTV-033"], "tree_level": 1, "avatar": secondary_suspects[2]["photo_url"]},
        {"id": "person_neha_kulkarni", "label": "Neha Kulkarni", "type": "PERSON", "risk_score": 58, "confidence": 0.85, "details": "Employee / IT Analyst.", "status": "Employee", "source_evidence_ids": ["EV-OSINT-023", "EV-DOC-057"], "tree_level": 2, "avatar": secondary_suspects[3]["photo_url"]},
        {"id": "person_arjun_s_candidate", "label": "Arjun S. (Candidate)", "type": "PERSON", "risk_score": 43, "confidence": 0.43, "details": "Unresolved Candidate Match (Confidence 43%). Name similarity + location overlap.", "status": "Unresolved Candidate", "source_evidence_ids": ["EV-OSINT-023"], "tree_level": 3, "avatar": ambiguous_candidate["photo_url"]},

        {"id": "phone_arjun_1", "label": "+91 98765 1201", "type": "PHONE", "risk_score": 90, "confidence": 1.0, "details": "Primary MSISDN assigned to Arjun Sharma", "status": "Confirmed", "source_evidence_ids": ["EV-COM-001"], "tree_level": 1},
        {"id": "acc_hdfc_demo", "label": "XXXX4821", "type": "BANK_ACCOUNT", "risk_score": 86, "confidence": 1.0, "details": "HDFC Account XXXX4821", "status": "Confirmed", "source_evidence_ids": ["EV-FIN-014"], "tree_level": 2},
        {"id": "acc_axis_demo", "label": "XXXX7194", "type": "BANK_ACCOUNT", "risk_score": 74, "confidence": 0.95, "details": "Axis Account XXXX7194", "status": "Confirmed", "source_evidence_ids": ["EV-REL-074"], "tree_level": 2},
        {"id": "wallet_shadow", "label": "0xDEMO...A721", "type": "CRYPTO_WALLET", "risk_score": 94, "confidence": 0.98, "details": "Cold wallet 0xDEMO...A721 (Balance: 8.42 ETH)", "status": "Confirmed", "source_evidence_ids": ["EV-BC-042"], "tree_level": 3},
        {"id": "vehicle_mh12", "label": "MH12 AB 4821", "type": "VEHICLE", "risk_score": 82, "confidence": 0.96, "details": "Black SUV MH12 AB 4821", "status": "Confirmed", "source_evidence_ids": ["EV-CCTV-031"], "tree_level": 2},
        {"id": "loc_pune", "label": "Pune, Maharashtra", "type": "LOCATION", "risk_score": 50, "confidence": 1.0, "details": "Primary operational location", "status": "Confirmed", "source_evidence_ids": ["EV-LOC-061"], "tree_level": 3},
        {"id": "incident_1042", "label": "Incident #1042", "type": "INCIDENT", "risk_score": 100, "confidence": 1.0, "details": "Cyber Extortion Incident #1042", "status": "Confirmed", "source_evidence_ids": ["EV-COM-001"], "tree_level": 0}
    ]

    # SHORT EDGE LABELS REQUIRED BY REQUIREMENT 10
    edges = [
        {"id": "REL-014", "source": "person_arjun_sharma", "target": "person_rohan_mehta", "relation": "CALL", "timestamp": "18 Aug 2026 20:02:14", "confidence": 0.82, "source_evidence_ids": ["EV-COM-001", "EV-COM-023"], "details": "27 Communication events logged between Arjun Sharma and Rohan Mehta", "domain": "COMMUNICATION", "call_count": 27, "first_observed": "03 Aug 2026", "last_observed": "18 Aug 2026", "supporting_evidence_count": 7, "shared_locations_count": 3, "shared_organizations_count": 1, "explanation": "Repeated communication and shared temporal activity observed across multiple evidence sources.", "alt_explanation": "Business coordination may account for some of the observed activity.", "temporal_correlation": "3 events within 42 minutes"},
        {"id": "REL-022", "source": "person_arjun_sharma", "target": "person_priya_joshi", "relation": "TRANSFER", "timestamp": "18 Aug 2026 21:03:18", "confidence": 0.92, "source_evidence_ids": ["EV-FIN-014", "EV-REL-074"], "details": "8 corporate transfers managed by Priya Joshi for Arjun Sharma", "domain": "FINANCIAL", "call_count": 8, "first_observed": "10 Aug 2026", "last_observed": "18 Aug 2026", "supporting_evidence_count": 5, "shared_locations_count": 2, "shared_organizations_count": 1, "explanation": "Observed transaction structure matches selected red-flag indicators.", "alt_explanation": "Routine corporate accounting transfers.", "temporal_correlation": "Correlated with evening wire window"},
        {"id": "REL-031", "source": "person_arjun_sharma", "target": "person_vikram_patil", "relation": "MEETING", "timestamp": "18 Aug 2026 20:26:11", "confidence": 0.90, "source_evidence_ids": ["EV-CCTV-031", "EV-CCTV-033"], "details": "Vikram Patil observed driving vehicle MH12 AB 4821 for Arjun Sharma", "domain": "DVR", "call_count": 6, "first_observed": "01 Aug 2026", "last_observed": "18 Aug 2026", "supporting_evidence_count": 4, "shared_locations_count": 2, "shared_organizations_count": 0, "explanation": "Vehicle observation at CCTV CAM-04.", "alt_explanation": "Chauffeur service for corporate meeting.", "temporal_correlation": "Observed departing 9 mins post-meeting"},
        {"id": "REL-045", "source": "person_arjun_sharma", "target": "person_neha_kulkarni", "relation": "BUSINESS", "timestamp": "18 Aug 2026 11:00:00", "confidence": 0.85, "source_evidence_ids": ["EV-OSINT-023", "EV-DOC-057"], "details": "Shared IP subnet access with primary subject's VPN server", "domain": "OSINT", "call_count": 2, "first_observed": "05 Aug 2026", "last_observed": "18 Aug 2026", "supporting_evidence_count": 3, "shared_locations_count": 1, "shared_organizations_count": 1, "explanation": "Public-source mention linking Neha Kulkarni to TechDesk Systems.", "alt_explanation": "Co-worker relationship.", "temporal_correlation": "Workplace hours correlation"},
        {"id": "REL-051", "source": "person_arjun_sharma", "target": "phone_arjun_1", "relation": "CALL", "timestamp": "01 Aug 2026 10:00:00", "confidence": 1.0, "source_evidence_ids": ["EV-COM-001"], "details": "Subscriber registration match for Arjun Sharma (+91 98765 1201)", "domain": "COMMUNICATION"},
        {"id": "REL-062", "source": "person_arjun_sharma", "target": "acc_hdfc_demo", "relation": "TRANSFER", "timestamp": "01 Aug 2026 10:00:00", "confidence": 1.0, "source_evidence_ids": ["EV-FIN-014"], "details": "Primary HDFC Account XXXX4821", "domain": "FINANCIAL"},
        {"id": "REL-073", "source": "person_arjun_sharma", "target": "wallet_shadow", "relation": "WALLET", "timestamp": "18 Aug 2026 21:17:04", "confidence": 0.94, "source_evidence_ids": ["EV-BC-042"], "details": "Cold wallet 0xDEMO...A721 (Balance: 8.42 ETH). Wallet association based on available evidence.", "domain": "BLOCKCHAIN"},
        {"id": "REL-084", "source": "person_arjun_sharma", "target": "vehicle_mh12", "relation": "VEHICLE", "timestamp": "01 Aug 2026 10:00:00", "confidence": 0.96, "source_evidence_ids": ["EV-CCTV-031"], "details": "RTO Registration for black SUV MH12 AB 4821", "domain": "PHYSICAL"},
        {"id": "REL-095", "source": "person_arjun_sharma", "target": "loc_pune", "relation": "SHARED LOCATION", "timestamp": "18 Aug 2026 20:01:14", "confidence": 1.0, "source_evidence_ids": ["EV-LOC-061"], "details": "Primary operational location in Pune", "domain": "PHYSICAL"},
        {"id": "REL-101", "source": "person_arjun_sharma", "target": "incident_1042", "relation": "DOCUMENT", "timestamp": "28 Aug 2026 20:07:00", "confidence": 1.0, "source_evidence_ids": ["EV-COM-001"], "details": "Primary subject of Cyber Extortion Incident #1042", "domain": "GENERAL"}
    ]

    # STANDARDIZED EVIDENCE IDENTIFIERS REQUIRED BY REQUIREMENT 7
    evidence_items = [
        {"id": "EV-COM-001", "case_id": "TRX-2026-017", "person_id": "person_arjun_sharma", "title": "Communication Record - MSISDN +91 98765 1201", "evidence_type": "Communication Analysis", "source": "Communication Dataset", "acquisition_timestamp": "18 Aug 2026 20:02:14", "acquisition_date": "18 Aug 2026", "acquisition_time": "20:02:14", "file_hash": "8f31c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852c91a", "file_size_bytes": 1840000, "integrity_status": "Verified", "processing_status": "PROCESSED", "provenance": "Communication Dataset export under Sec 65B.", "analyst_notes": "187 calls and 234 messages logged between Arjun Sharma (+91 98765 1201) and contacts.", "confidence": 0.98, "extracted_entities": ["Arjun Sharma", "Rohan Mehta", "+91 98765 1201"], "related_events": ["EV-CCTV-031", "EV-FIN-014", "EV-REL-074"], "duration": "04:21", "direction": "Outgoing"},
        {"id": "EV-COM-023", "case_id": "TRX-2026-017", "person_id": "person_rohan_mehta", "title": "Communication Record - Rohan Mehta", "evidence_type": "Communication Analysis", "source": "Communication Dataset", "acquisition_timestamp": "18 Aug 2026 20:02:14", "acquisition_date": "18 Aug 2026", "acquisition_time": "20:02:14", "file_hash": "8f31b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284ddd200126d9069e", "file_size_bytes": 920000, "integrity_status": "Verified", "processing_status": "PROCESSED", "provenance": "Communication Dataset", "analyst_notes": "Outgoing communication event to Rohan Mehta duration 04:21.", "confidence": 0.95, "extracted_entities": ["Arjun Sharma", "Rohan Mehta", "Pune"], "related_events": ["EV-CCTV-031", "EV-FIN-014", "EV-REL-074"], "duration": "04:21", "direction": "Outgoing"},
        {"id": "EV-FIN-014", "case_id": "TRX-2026-017", "person_id": "person_rohan_mehta", "title": "Bank Wire Ledger - XXXX4821", "evidence_type": "Financial Record", "source": "Financial Intelligence Ledger", "acquisition_timestamp": "18 Aug 2026 20:58:18", "acquisition_date": "18 Aug 2026", "acquisition_time": "20:58:18", "file_hash": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284ddd200126d9069e", "file_size_bytes": 920000, "integrity_status": "Verified", "processing_status": "PROCESSED", "provenance": "Financial Statement pull under Sec 91 CrPC.", "analyst_notes": "₹48,500 Outgoing transfer from XXXX4821 linked to Rohan Mehta.", "confidence": 0.95, "extracted_entities": ["Account XXXX4821", "Rohan Mehta", "₹48,500"], "related_events": ["EV-COM-023", "EV-REL-074"]},
        {"id": "EV-OSINT-023", "case_id": "TRX-2026-017", "person_id": "person_arjun_sharma", "title": "Public-Source Record PSI-023", "evidence_type": "Public-Source Intelligence", "source": "Public Web Crawler", "acquisition_timestamp": "18 Aug 2026 11:03:00", "acquisition_date": "18 Aug 2026", "acquisition_time": "11:03:00", "file_hash": "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e", "file_size_bytes": 120000, "integrity_status": "Verified", "processing_status": "PROCESSED", "provenance": "Public Web Directory Archive.", "analyst_notes": "Public mention linking @arjun_s_demo to Rohan Mehta and Nexus Logistics.", "confidence": 0.88, "extracted_entities": ["@arjun_s_demo", "Rohan Mehta"], "related_events": ["EV-DOC-057"]},
        {"id": "EV-CCTV-031", "case_id": "TRX-2026-017", "person_id": "person_arjun_sharma", "title": "CCTV Surveillance Event - PERSON MEETING", "evidence_type": "DVR/NVR Forensics", "source": "Surveillance CAM-04", "acquisition_timestamp": "18 Aug 2026 20:01:14", "acquisition_date": "18 Aug 2026", "acquisition_time": "20:01:14", "file_hash": "d41d8cd98f00b204e9800998ecf8427e56b3e66487e44a49c6d3ff3cf81734f2", "file_size_bytes": 62000000, "integrity_status": "Verified", "processing_status": "PROCESSED", "provenance": "Seized NVR hard drive #NVR-702 frame carving.", "analyst_notes": "Surveillance CAM-04 captured meeting between Arjun Sharma and Rohan Mehta.", "confidence": 0.96, "extracted_entities": ["Arjun Sharma", "Rohan Mehta", "CAM-04"], "related_events": ["EV-COM-023", "EV-CCTV-032"]},
        {"id": "EV-CCTV-032", "case_id": "TRX-2026-017", "person_id": "person_rohan_mehta", "title": "CCTV Surveillance Event - FINANCIAL EXCHANGE EVENT", "evidence_type": "DVR/NVR Forensics", "source": "Surveillance CAM-04", "acquisition_timestamp": "18 Aug 2026 20:17:38", "acquisition_date": "18 Aug 2026", "acquisition_time": "20:17:38", "file_hash": "7a91c8901b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e", "file_size_bytes": 58000000, "integrity_status": "Verified", "processing_status": "PROCESSED", "provenance": "Surveillance Stream CAM-04.", "analyst_notes": "Surveillance CAM-04 captured physical exchange event at 20:17:38 IST.", "confidence": 0.94, "extracted_entities": ["Arjun Sharma", "Rohan Mehta", "CAM-04"], "related_events": ["EV-FIN-014"]},
        {"id": "EV-CCTV-033", "case_id": "TRX-2026-017", "person_id": "person_vikram_patil", "title": "CCTV Surveillance Event - VEHICLE DEPARTURE", "evidence_type": "DVR/NVR Forensics", "source": "Surveillance CAM-04", "acquisition_timestamp": "18 Aug 2026 20:26:11", "acquisition_date": "18 Aug 2026", "acquisition_time": "20:26:11", "file_hash": "2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae", "file_size_bytes": 45000000, "integrity_status": "Verified", "processing_status": "PROCESSED", "provenance": "Surveillance CAM-04 ANPR frame carve.", "analyst_notes": "ANPR capture of black SUV MH12 AB 4821 departing meeting location.", "confidence": 0.96, "extracted_entities": ["MH12 AB 4821", "Vikram Patil", "CAM-04"], "related_events": ["EV-CCTV-031"]},
        {"id": "EV-BC-042", "case_id": "TRX-2026-017", "person_id": "person_arjun_sharma", "title": "Blockchain Transaction Ledger - 0xDEMO...A721", "evidence_type": "Blockchain Workspace", "source": "Blockchain Ledger API", "acquisition_timestamp": "18 Aug 2026 21:17:04", "acquisition_date": "18 Aug 2026", "acquisition_time": "21:17:04", "file_hash": "fcde2b2edba56bf408601fb721fe9b5c338d10ee429ea04fae5511b68fbf8fb9", "file_size_bytes": 310000, "integrity_status": "Verified", "processing_status": "PROCESSED", "provenance": "Public blockchain RPC pull.", "analyst_notes": "TX-DEMO-002 transaction of 1.20 ETH to recipient 0xDEMO...F921.", "confidence": 0.94, "extracted_entities": ["0xDEMO...A721", "1.20 ETH"], "related_events": ["EV-FIN-014"]},
        {"id": "EV-DOC-057", "case_id": "TRX-2026-017", "person_id": "person_priya_joshi", "title": "Corporate Registration Document", "evidence_type": "Document Intelligence", "source": "Ministry of Corporate Affairs Gateway", "acquisition_timestamp": "18 Aug 2026 15:08:00", "acquisition_date": "18 Aug 2026", "acquisition_time": "15:08:00", "file_hash": "9b74c2d2390a81498b0493019808381273891729837198273891723891723981", "file_size_bytes": 210000, "integrity_status": "Verified", "processing_status": "PROCESSED", "provenance": "Certified MCA filing pull.", "analyst_notes": "Business registration linking Nexus Logistics to Priya Joshi.", "confidence": 0.91, "extracted_entities": ["Nexus Logistics", "Priya Joshi"], "related_events": ["EV-OSINT-023"]},
        {"id": "EV-LOC-061", "case_id": "TRX-2026-017", "person_id": "person_arjun_sharma", "title": "Cell Tower Geolocation Record", "evidence_type": "Location Intelligence", "source": "Cellular Network Provider", "acquisition_timestamp": "18 Aug 2026 20:01:14", "acquisition_date": "18 Aug 2026", "acquisition_time": "20:01:14", "file_hash": "1829379182739812739182739812739182739182739182739182739182739182", "file_size_bytes": 540000, "integrity_status": "Verified", "processing_status": "PROCESSED", "provenance": "Tower dump extract.", "analyst_notes": "Cell tower location fix in Shivajinagar, Pune.", "confidence": 0.93, "extracted_entities": ["Pune", "Arjun Sharma"], "related_events": ["EV-COM-023"]},
        {"id": "EV-REL-074", "case_id": "TRX-2026-017", "person_id": "person_priya_joshi", "title": "Account Linkage Record - XXXX7194", "evidence_type": "Financial Record", "source": "Bank Gateway API", "acquisition_timestamp": "18 Aug 2026 21:03:18", "acquisition_date": "18 Aug 2026", "acquisition_time": "21:03:18", "file_hash": "7198273918273918273918273918273918273918273918273918273918273918", "file_size_bytes": 480000, "integrity_status": "Verified", "processing_status": "PROCESSED", "provenance": "Authorized Financial Pull.", "analyst_notes": "Incoming deposit of ₹72,000 to Axis Account XXXX7194.", "confidence": 0.93, "extracted_entities": ["Axis Acc XXXX7194", "Priya Joshi"], "related_events": ["EV-FIN-014"]}
    ]

    # CCTV SURVEILLANCE EVENTS CONNECTED TO THE CASE (REQUIREMENT 17 & 18)
    dvr_videos = [
        {
            "id": "EV-CCTV-031",
            "camera_id": "CAM-04",
            "location": "Synthetic Pune Location A",
            "timestamp": "18 Aug 2026 20:01:14",
            "event_title": "PERSON MEETING",
            "suspects_identified": ["Arjun Sharma", "Rohan Mehta"],
            "anpr_license_plate": "MH12 AB 4821",
            "evidence_id": "EV-CCTV-031",
            "video_thumbnail": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800&auto=format&fit=crop&q=80",
            "description": "Surveillance CAM-04 captured physical meeting between Arjun Sharma and Rohan Mehta.",
            "label": "VERIFIED FRAME"
        },
        {
            "id": "EV-CCTV-032",
            "camera_id": "CAM-04",
            "location": "Synthetic Pune Location B",
            "timestamp": "18 Aug 2026 20:17:38",
            "event_title": "FINANCIAL EXCHANGE EVENT",
            "suspects_identified": ["Arjun Sharma", "Rohan Mehta"],
            "anpr_license_plate": "MH12 XY 9988",
            "evidence_id": "EV-CCTV-032",
            "video_thumbnail": "https://images.unsplash.com/photo-1573164713988-8665fc963095?w=800&auto=format&fit=crop&q=80",
            "description": "Surveillance CAM-04 captured physical exchange event at 20:17:38 IST.",
            "label": "VERIFIED FRAME"
        },
        {
            "id": "EV-CCTV-033",
            "camera_id": "CAM-04",
            "location": "Synthetic Pune Location C",
            "timestamp": "18 Aug 2026 20:26:11",
            "event_title": "VEHICLE DEPARTURE",
            "suspects_identified": ["Vikram Patil (Driver)", "MH12 AB 4821"],
            "anpr_license_plate": "MH12 AB 4821",
            "evidence_id": "EV-CCTV-033",
            "video_thumbnail": "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&auto=format&fit=crop&q=80",
            "description": "Vehicle MH12 AB 4821 departs meeting location at 20:26:11 IST.",
            "label": "VERIFIED FRAME"
        }
    ]

    # EXPLAINABLE AI INVESTIGATIVE LEADS (REQUIREMENT 20)
    leads = [
        {
            "id": "LEAD-001",
            "title": "Repeated communication and financial activity correlation",
            "lead": "Repeated communication and financial activity correlation",
            "confidence": 0.82,
            "supporting_evidence": ["EV-COM-023", "EV-COM-031", "EV-FIN-014", "EV-CCTV-031"],
            "observed_pattern": "Multiple communication events occur within a short interval of physical and financial events.",
            "evidence_chain": [
                {"step": 1, "domain": "CDR", "description": "Arjun Sharma (+91 98765 1201) initiates call to Rohan Mehta at 20:02:14.", "evidence_id": "EV-COM-023"},
                {"step": 2, "domain": "DVR", "description": "CCTV CAM-04 captures meeting at 20:01:14.", "evidence_id": "EV-CCTV-031"},
                {"step": 3, "domain": "FINANCIAL", "description": "₹48,500 Outgoing transfer to Rohan Mehta logged at 20:58:18.", "evidence_id": "EV-FIN-014"}
            ],
            "recommended_actions": [
                "Review associated communications and transaction records.",
                "Issue Sec 91 CrPC notice for raw tower dump at Shivajinagar Junction.",
                "Verify beneficiary KYCs of HDFC Account XXXX4821."
            ],
            "alternative_explanation": "Business coordination may account for some of the observed activity.",
            "status": "Needs Review",
            "human_review_required": True
        },
        {
            "id": "LEAD-002",
            "title": "Potential transaction layering pattern",
            "lead": "Rapid account movement across multiple counterparties",
            "confidence": 0.74,
            "supporting_evidence": ["EV-FIN-014", "EV-REL-074", "EV-BC-042"],
            "observed_pattern": "₹1,25,000 credit split into 3 destination accounts within 18 minutes without invoice reference.",
            "evidence_chain": [
                {"step": 1, "domain": "FINANCIAL", "description": "Credit deposit to Axis Account XXXX7194.", "evidence_id": "EV-REL-074"},
                {"step": 2, "domain": "BLOCKCHAIN", "description": "1.20 ETH off-ramped to wallet 0xDEMO...A721.", "evidence_id": "EV-BC-042"}
            ],
            "recommended_actions": [
                "Pull Section 91 CrPC Bank Statement for Axis Acc XXXX7194.",
                "Verify corporate registrar filings of Nexus Logistics."
            ],
            "alternative_explanation": "Routine corporate payroll processing.",
            "status": "Needs Review",
            "human_review_required": True
        },
        {
            "id": "LEAD-003",
            "title": "Temporal correlation between communication and physical meeting",
            "lead": "Call event occurred 53 seconds post-surveillance capture",
            "confidence": 0.79,
            "supporting_evidence": ["EV-COM-001", "EV-CCTV-031"],
            "observed_pattern": "Cell tower connection initiated immediately after CAM-04 sighting.",
            "evidence_chain": [
                {"step": 1, "domain": "DVR", "description": "CCTV CAM-04 captured meeting at 20:01:14.", "evidence_id": "EV-CCTV-031"},
                {"step": 2, "domain": "CDR", "description": "Outgoing call from Arjun to Rohan at 20:02:14.", "evidence_id": "EV-COM-001"}
            ],
            "recommended_actions": [
                "Perform frame carving analysis on CAM-04 raw video stream."
            ],
            "alternative_explanation": "Coincidental timing during regular business hours.",
            "status": "Needs Review",
            "human_review_required": True
        },
        {
            "id": "LEAD-004",
            "title": "Potential shared organizational connection",
            "lead": "Public-source intelligence correlates multiple subjects to Nexus Logistics",
            "confidence": 0.68,
            "supporting_evidence": ["EV-OSINT-023", "EV-DOC-057"],
            "observed_pattern": "Shared MCA registration filings and corporate web references.",
            "evidence_chain": [
                {"step": 1, "domain": "OSINT", "description": "Public-source web snapshot linking subjects to corporate website.", "evidence_id": "EV-OSINT-023"}
            ],
            "recommended_actions": [
                "Cross-reference MCA filings for official director status."
            ],
            "alternative_explanation": "Legitimate employment at common workplace.",
            "status": "Needs Review",
            "human_review_required": True
        },
        {
            "id": "LEAD-005",
            "title": "Possible identity ambiguity (Entity Resolution)",
            "lead": "Candidate match 'Arjun S.' shares name similarity and location overlap",
            "confidence": 0.43,
            "supporting_evidence": ["EV-OSINT-023"],
            "observed_pattern": "Name similarity + location overlap in public directory harvest.",
            "evidence_chain": [
                {"step": 1, "domain": "OSINT", "description": "Public profile 'Arjun S.' flagged during broad name harvest.", "evidence_id": "EV-OSINT-023"}
            ],
            "recommended_actions": [
                "Mark candidate as Unresolved / False Positive after manual review."
            ],
            "alternative_explanation": "Unrelated individual with common name.",
            "status": "Unresolved Candidate",
            "human_review_required": True
        }
    ]

    # OPERATIONAL AUDIT TRAIL LOG HISTORY (REQUIREMENT 27)
    audit_events = [
        {"timestamp": "18 Aug 2026 09:43", "actor": "INV-004", "action_type": "Opened Case", "object": "TRX-2026-017", "result": "Success"},
        {"timestamp": "18 Aug 2026 09:51", "actor": "INV-004", "action_type": "Viewed Evidence", "object": "EV-COM-023", "result": "Success"},
        {"timestamp": "18 Aug 2026 10:19", "actor": "INV-004", "action_type": "Expanded Relationship", "object": "REL-014", "result": "Success"},
        {"timestamp": "18 Aug 2026 10:44", "actor": "INV-004", "action_type": "Flagged Evidence", "object": "EV-FIN-014", "result": "Review Required"},
        {"timestamp": "18 Aug 2026 11:12", "actor": "INV-004", "action_type": "Viewed Financial Ledger", "object": "XXXX4821", "result": "Success"},
        {"timestamp": "18 Aug 2026 11:37", "actor": "INV-004", "action_type": "Opened CCTV Forensics", "object": "EV-CCTV-031", "result": "Success"},
        {"timestamp": "18 Aug 2026 12:01", "actor": "INV-004", "action_type": "Generated Report", "object": "Dossier TRX-2026-017", "result": "Success"}
    ]

    anomalies = [
        {"id": "ANM-001", "category": "Communication Burst", "title": "Potential Communication Anomaly", "severity": "High", "timestamp": "18 Aug 2026 19:45:00", "affected_entity_ids": ["person_arjun_sharma", "person_rohan_mehta"], "explanation": "Communication frequency between Arjun Sharma and Rohan Mehta increased prior to Incident #1042.", "evidence_ids": ["EV-COM-001"], "confidence": 0.94, "analyst_status": "Requires Human Review"},
        {"id": "ANM-002", "category": "Financial Movement", "title": "Potential Informal Value Transfer Pattern", "severity": "High", "timestamp": "18 Aug 2026 20:45:00", "affected_entity_ids": ["person_rohan_mehta", "acc_hdfc_demo", "person_priya_joshi"], "explanation": "Observed transaction structure matches selected red-flag indicators (71% confidence).", "evidence_ids": ["EV-FIN-014", "EV-REL-074"], "confidence": 0.71, "analyst_status": "Requires Human Review"},
        {"id": "ANM-003", "category": "Temporal Sighting", "title": "Potential Temporal Correlation", "severity": "High", "timestamp": "18 Aug 2026 20:12:00", "affected_entity_ids": ["vehicle_mh12", "camera_c12"], "explanation": "Vehicle MH12 AB 4821 passed CCTV CAM-04 within short temporal window of meeting.", "evidence_ids": ["EV-CCTV-031", "EV-CCTV-033"], "confidence": 0.92, "analyst_status": "Requires Human Review"}
    ]

    return {
        "cases": cases_db,
        "nodes": nodes,
        "edges": edges,
        "evidence_items": evidence_items,
        "dvr_videos": dvr_videos,
        "anomalies": anomalies,
        "leads": leads,
        "audit_events": audit_events,
        "ambiguous_candidate": ambiguous_candidate
    }
