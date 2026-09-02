import random
from datetime import datetime, timedelta
from typing import Dict, List, Any

random.seed(2026189)

def generate_synthetic_dataset() -> Dict[str, Any]:
    # PRIMARY SUBJECT: ARJUN SHARMA
    arjun_profile = {
        "id": "person_arjun_sharma",
        "name": "Arjun Sharma",
        "alias": "Cipher King",
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
        "organization": "Nexus Logistics Demo",
        "vehicle": "MH12 AB 4821",
        "social_usernames": {
            "telegram": "@cipher_king",
            "twitter": "@arjun_s_demo",
            "instagram": "@arjun_cyber",
            "darkweb": "shadow_broker99"
        },
        "wallet_address": "0xDEMO...A721",
        "notes": "Primary subject under investigation for Operation Nexus.",
        "risk_score": 92,
        "evidence_count": 24,
        "relationship_count": 7,
        "status": "Under Investigation"
    }

    secondary_suspects = [
        {
            "id": "person_rohan_mehta",
            "name": "Rohan Mehta",
            "alias": "Runner R",
            "role": "Business Contact",
            "relationship_to_primary": "Business Contact",
            "age": 31,
            "gender": "Male",
            "photo_url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=300&auto=format&fit=crop&q=80",
            "phone": "+91 98765 2002",
            "email": "rohan.m.demo@example.test",
            "address": "Kothrud, Pune",
            "city": "Pune",
            "occupation": "Logistics Supervisor",
            "organization": "Nexus Express Demo",
            "vehicle": "MH12 XY 9988",
            "social_usernames": {"telegram": "@rohan_runner", "instagram": "@rohan_m_vlogs"},
            "wallet_address": "0x3910ab...199",
            "notes": "27 direct calls logged with Arjun Sharma prior to Incident #1042.",
            "risk_score": 85,
            "evidence_count": 18,
            "relationship_count": 5,
            "status": "Person of Interest"
        },
        {
            "id": "person_priya_joshi",
            "name": "Priya Joshi",
            "alias": "Priya J",
            "role": "Associate",
            "relationship_to_primary": "Associate",
            "age": 29,
            "gender": "Female",
            "photo_url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=300&auto=format&fit=crop&q=80",
            "phone": "+91 98765 3003",
            "email": "priya.j.demo@example.test",
            "address": "Baner Road, Pune",
            "city": "Pune",
            "occupation": "Senior Accountant",
            "organization": "Nexus Logistics Demo",
            "vehicle": "MH14 CD 5544",
            "social_usernames": {"linkedin": "in/priya-joshi-demo"},
            "wallet_address": "",
            "notes": "Managed bank accounts used for multi-hop cash deposits.",
            "risk_score": 78,
            "evidence_count": 14,
            "relationship_count": 4,
            "status": "Associate"
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
            "city": "Pune",
            "occupation": "Personal Driver",
            "organization": "Private Fleet",
            "vehicle": "MH12 AB 4821",
            "social_usernames": {"telegram": "@vicky_driver"},
            "wallet_address": "",
            "notes": "Observed driving vehicle MH12 AB 4821 near meeting spot.",
            "risk_score": 72,
            "evidence_count": 11,
            "relationship_count": 3,
            "status": "Person of Interest"
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
            "city": "Pune",
            "occupation": "IT Analyst",
            "organization": "TechDesk Systems",
            "vehicle": "",
            "social_usernames": {"twitter": "@neha_k_demo"},
            "wallet_address": "",
            "notes": "Shared IP subnet access with primary subject's VPN server.",
            "risk_score": 58,
            "evidence_count": 8,
            "relationship_count": 2,
            "status": "Employee"
        }
    ]

    # AMBIGUOUS CANDIDATE (DELIBERATE FALSE-POSITIVE DEMO - POINT 31)
    ambiguous_candidate = {
        "id": "person_arjun_s_candidate",
        "name": "Arjun S.",
        "alias": "Arjun S (Unverified)",
        "role": "Person of Interest",
        "relationship_to_primary": "Candidate Match",
        "age": 35,
        "gender": "Male",
        "photo_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300",
        "phone": "+91 98765 9999",
        "email": "arjun.s.ambiguous@example.test",
        "address": "Camp Area, Pune",
        "city": "Pune",
        "occupation": "Trader",
        "organization": "Unknown",
        "vehicle": "",
        "social_usernames": {"twitter": "@arjun_s_trader"},
        "wallet_address": "",
        "notes": "POTENTIAL MATCH (Confidence 43%). Reason: Name similarity + location overlap. Insufficient evidence to establish identity.",
        "risk_score": 43,
        "evidence_count": 2,
        "relationship_count": 1,
        "status": "False Positive / Needs Review"
    }

    # 6 SEEDED DEMO CASES (MASTER PROMPT REQUIREMENT 5)
    cases_db = {
        "TRX-2026-017": {
            "id": "TRX-2026-017",
            "title": "Operation Nexus",
            "primary_suspect": arjun_profile,
            "secondary_suspects": secondary_suspects,
            "subject_known_identifiers": {
                "phone": ["+91 98765 1201"],
                "email": ["arjun.sharma.demo@example.test"],
                "aliases": ["Arjun S.", "Cipher King", "shadow_broker99"],
                "vehicle": ["MH12 AB 4821"],
                "wallet": ["0xDEMO...A721"],
                "account": ["XXXX 4821", "XXXX 7194"]
            },
            "description": "Cross-domain intelligence fusion investigating an illicit financial transfer syndicate coordinating extortion, money laundering through informal channels, and crypto off-ramping connected to cyber incident #1042.",
            "investigation_type": "Cyber-Financial Crime",
            "priority": "High",
            "status": "Active Investigation",
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
            "last_activity": "10 mins ago"
        },
        "TRX-2026-014": {
            "id": "TRX-2026-014",
            "title": "Operation Meridian",
            "primary_suspect": {
                "id": "person_vikram_patil_lead",
                "name": "Vikram Patil",
                "alias": "Patil Boss",
                "role": "Primary Subject",
                "photo_url": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=300",
                "phone": "+91 98111 0001",
                "email": "patil.v@meridian.org",
                "city": "Mumbai",
                "occupation": "Transport Operator",
                "vehicle": "MH01 AB 9900",
                "wallet_address": "0xDEMO...B881"
            },
            "secondary_suspects": [secondary_suspects[0], secondary_suspects[1]],
            "description": "Inquiry into SIM-box telecom routing syndicate operating near Western Corridor.",
            "investigation_type": "Telecom Fraud",
            "priority": "Medium",
            "status": "Active",
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
            "last_activity": "1 hour ago"
        },
        "TRX-2026-011": {
            "id": "TRX-2026-011",
            "title": "Operation Vector",
            "primary_suspect": {
                "id": "person_amit_deshmukh",
                "name": "Amit Deshmukh",
                "alias": "Vector Lead",
                "role": "Primary Subject",
                "photo_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300",
                "phone": "+91 98222 0002",
                "email": "amit.d@vector.org",
                "city": "Nashik",
                "occupation": "Trader",
                "vehicle": "MH15 XY 1001",
                "wallet_address": ""
            },
            "secondary_suspects": [secondary_suspects[2]],
            "description": "Investigation into shell company invoice layering and tax evasion.",
            "investigation_type": "Financial Fraud",
            "priority": "High",
            "status": "Review",
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
            "last_activity": "3 hours ago"
        },
        "TRX-2026-009": {
            "id": "TRX-2026-009",
            "title": "Operation Atlas",
            "primary_suspect": {
                "id": "person_karan_shah",
                "name": "Karan Shah",
                "alias": "Atlas Lead",
                "role": "Primary Subject",
                "photo_url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=300",
                "phone": "+91 98333 0003",
                "email": "karan.s@atlas.org",
                "city": "Pune",
                "occupation": "Contractor",
                "vehicle": "MH12 PQ 4455",
                "wallet_address": ""
            },
            "secondary_suspects": [],
            "description": "Concluded inquiry into public procurement portal cyber breach.",
            "investigation_type": "Cyber Intrusion",
            "priority": "Medium",
            "status": "Closed",
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
            "last_activity": "2 days ago"
        },
        "TRX-2026-006": {
            "id": "TRX-2026-006",
            "title": "Operation Signal",
            "primary_suspect": {
                "id": "person_sanjay_more",
                "name": "Sanjay More",
                "alias": "Signal Lead",
                "role": "Primary Subject",
                "photo_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=300",
                "phone": "+91 98444 0004",
                "email": "sanjay.m@signal.org",
                "city": "Nagpur",
                "occupation": "Dealer",
                "vehicle": "MH31 RS 8877",
                "wallet_address": ""
            },
            "secondary_suspects": [],
            "description": "Probe into unauthorized VoIP gateway routing.",
            "investigation_type": "Telecom Fraud",
            "priority": "Low",
            "status": "Active",
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
            "last_activity": "5 hours ago"
        },
        "TRX-2026-003": {
            "id": "TRX-2026-003",
            "title": "Operation Horizon",
            "primary_suspect": {
                "id": "person_neha_kulkarni_lead",
                "name": "Neha Kulkarni",
                "alias": "Horizon Lead",
                "role": "Primary Subject",
                "photo_url": "https://images.unsplash.com/photo-1580489944761-15a19d654956?w=300",
                "phone": "+91 98555 0005",
                "email": "neha.k@horizon.org",
                "city": "Mumbai",
                "occupation": "Analyst",
                "vehicle": "MH02 UV 3322",
                "wallet_address": ""
            },
            "secondary_suspects": [],
            "description": "Analysis of phishing infrastructure targeting regional cooperative banks.",
            "investigation_type": "Phishing & Banking Cybercrime",
            "priority": "Medium",
            "status": "Review",
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
            "last_activity": "1 day ago"
        }
    }

    # KNOWLEDGE GRAPH NODES (TREE DEFAULT)
    nodes = [
        {"id": "person_arjun_sharma", "label": "Arjun Sharma", "type": "PERSON", "risk_score": 92, "confidence": 1.0, "details": "Primary Subject / Logistics Consultant. Associated with Telegram @cipher_king.", "status": "Under Investigation", "source_evidence_ids": ["EV-001", "EV-014"], "tree_level": 0, "avatar": arjun_profile["photo_url"]},
        {"id": "person_rohan_mehta", "label": "Rohan Mehta", "type": "PERSON", "risk_score": 85, "confidence": 0.95, "details": "Business Contact. 27 direct calls logged with Arjun Sharma.", "status": "Business Contact", "source_evidence_ids": ["EV-001", "EV-014"], "tree_level": 1, "avatar": secondary_suspects[0]["photo_url"]},
        {"id": "person_priya_joshi", "label": "Priya Joshi", "type": "PERSON", "risk_score": 78, "confidence": 0.92, "details": "Associate / Senior Accountant at Nexus Logistics Demo.", "status": "Associate", "source_evidence_ids": ["EV-014", "EV-074"], "tree_level": 1, "avatar": secondary_suspects[1]["photo_url"]},
        {"id": "person_vikram_patil", "label": "Vikram Patil", "type": "PERSON", "risk_score": 72, "confidence": 0.90, "details": "Person of Interest / Personal Driver of MH12 AB 4821.", "status": "Person of Interest", "source_evidence_ids": ["EV-031", "EV-057"], "tree_level": 1, "avatar": secondary_suspects[2]["photo_url"]},
        {"id": "person_neha_kulkarni", "label": "Neha Kulkarni", "type": "PERSON", "risk_score": 58, "confidence": 0.85, "details": "Employee / Shared IP subnet access.", "status": "Employee", "source_evidence_ids": ["EV-023", "EV-061"], "tree_level": 2, "avatar": secondary_suspects[3]["photo_url"]},
        {"id": "person_arjun_s_candidate", "label": "Arjun S. (Candidate)", "type": "PERSON", "risk_score": 43, "confidence": 0.43, "details": "POTENTIAL MATCH (Confidence 43%). Name similarity + location overlap. Insufficient evidence to establish identity.", "status": "False Positive / Needs Review", "source_evidence_ids": ["EV-061"], "tree_level": 3, "avatar": ambiguous_candidate["photo_url"]},

        {"id": "phone_arjun_1", "label": "+91 98765 1201", "type": "PHONE", "risk_score": 90, "confidence": 1.0, "details": "Primary MSISDN assigned to Arjun Sharma", "status": "Confirmed", "source_evidence_ids": ["EV-001"], "tree_level": 1},
        {"id": "acc_hdfc_demo", "label": "HDFC Acc XXXX 4821", "type": "BANK_ACCOUNT", "risk_score": 86, "confidence": 1.0, "details": "HDFC Demo Account used for primary transactions", "status": "Confirmed", "source_evidence_ids": ["EV-014"], "tree_level": 2},
        {"id": "acc_axis_demo", "label": "Axis Acc XXXX 7194", "type": "BANK_ACCOUNT", "risk_score": 74, "confidence": 0.95, "details": "Axis Demo Account used for secondary routing", "status": "Confirmed", "source_evidence_ids": ["EV-074"], "tree_level": 2},
        {"id": "wallet_shadow", "label": "0xDEMO...A721", "type": "CRYPTO_WALLET", "risk_score": 94, "confidence": 0.98, "details": "Cold wallet referenced in OSINT threat intel (Balance: 8.42 ETH)", "status": "Confirmed", "source_evidence_ids": ["EV-042"], "tree_level": 3},
        {"id": "vehicle_mh12", "label": "MH12 AB 4821", "type": "VEHICLE", "risk_score": 82, "confidence": 0.96, "details": "Black SUV registered under Arjun Sharma / driven by Vikram Patil", "status": "Confirmed", "source_evidence_ids": ["EV-031"], "tree_level": 2},
        {"id": "loc_pune", "label": "Pune, Maharashtra", "type": "LOCATION", "risk_score": 50, "confidence": 1.0, "details": "Primary operational jurisdiction", "status": "Confirmed", "source_evidence_ids": ["EV-057"], "tree_level": 3},
        {"id": "incident_1042", "label": "Incident #1042", "type": "INCIDENT", "risk_score": 100, "confidence": 1.0, "details": "Cyber Extortion Incident on 2026-08-28 20:07 IST", "status": "Confirmed", "source_evidence_ids": ["EV-001"], "tree_level": 0}
    ]

    edges = [
        {"id": "rel_1", "source": "person_arjun_sharma", "target": "person_rohan_mehta", "relation": "COMMUNICATION", "timestamp": "2026-08-18 20:02:00", "confidence": 0.98, "source_evidence_ids": ["EV-001", "EV-023"], "details": "27 Encrypted calls logged between Arjun Sharma & Rohan Mehta", "domain": "COMMUNICATION", "call_count": 27, "first_observed": "04 Aug 2026", "last_observed": "18 Aug 2026", "explanation": "Repeated communication and shared temporal activity observed across multiple evidence sources.", "alt_explanation": "Business coordination may explain some of the communication.", "temporal_correlation": "3 events within 42 minutes"},
        {"id": "rel_2", "source": "person_arjun_sharma", "target": "person_priya_joshi", "relation": "ASSOCIATE", "timestamp": "2026-08-18 21:03:00", "confidence": 0.92, "source_evidence_ids": ["EV-014", "EV-074"], "details": "8 corporate transfers managed by Priya Joshi for Arjun Sharma", "domain": "FINANCIAL", "call_count": 8, "first_observed": "10 Aug 2026", "last_observed": "18 Aug 2026", "explanation": "Observed transaction structure matches selected red-flag indicators.", "alt_explanation": "Routine corporate accounting transfers.", "temporal_correlation": "Correlated with evening wire window"},
        {"id": "rel_3", "source": "person_arjun_sharma", "target": "person_vikram_patil", "relation": "PERSON_OF_INTEREST", "timestamp": "2026-08-18 20:26:00", "confidence": 0.90, "source_evidence_ids": ["EV-031", "EV-057"], "details": "Vikram Patil observed driving vehicle MH12 AB 4821 for Arjun Sharma", "domain": "DVR", "call_count": 6, "first_observed": "01 Aug 2026", "last_observed": "18 Aug 2026", "explanation": "Vehicle observation at CCTV Cam-04.", "alt_explanation": "Chauffeur service for corporate meeting.", "temporal_correlation": "Observed departing 9 mins post-meeting"},
        {"id": "rel_4", "source": "person_arjun_sharma", "target": "person_neha_kulkarni", "relation": "EMPLOYEE", "timestamp": "2026-08-18 11:00:00", "confidence": 0.85, "source_evidence_ids": ["EV-023", "EV-061"], "details": "Shared IP subnet access with primary subject's VPN server", "domain": "OSINT", "call_count": 2, "first_observed": "05 Aug 2026", "last_observed": "18 Aug 2026", "explanation": "Public web mention linking Neha Kulkarni to TechDesk Systems.", "alt_explanation": "Co-worker relationship.", "temporal_correlation": "Workplace hours correlation"},
        {"id": "rel_5", "source": "person_arjun_sharma", "target": "phone_arjun_1", "relation": "USES", "timestamp": "2026-08-01 10:00:00", "confidence": 1.0, "source_evidence_ids": ["EV-001"], "details": "Subscriber registration match for Arjun Sharma (+91 98765 1201)", "domain": "COMMUNICATION"},
        {"id": "rel_6", "source": "person_arjun_sharma", "target": "acc_hdfc_demo", "relation": "HOLDS_ACCOUNT", "timestamp": "2026-08-01 10:00:00", "confidence": 1.0, "source_evidence_ids": ["EV-014"], "details": "Primary HDFC Demo Account XXXX 4821", "domain": "FINANCIAL"},
        {"id": "rel_7", "source": "person_arjun_sharma", "target": "wallet_shadow", "relation": "ASSOCIATED_WALLET", "timestamp": "2026-08-18 21:17:00", "confidence": 0.94, "source_evidence_ids": ["EV-042"], "details": "Cold wallet 0xDEMO...A721 (Balance: 8.42 ETH). Wallet association based on available evidence.", "domain": "BLOCKCHAIN"},
        {"id": "rel_8", "source": "person_arjun_sharma", "target": "vehicle_mh12", "relation": "OWNS_VEHICLE", "timestamp": "2026-08-01 10:00:00", "confidence": 0.96, "source_evidence_ids": ["EV-031"], "details": "RTO Registration for black SUV MH12 AB 4821", "domain": "PHYSICAL"},
        {"id": "rel_9", "source": "person_arjun_sharma", "target": "loc_pune", "relation": "LOCATED_IN", "timestamp": "2026-08-18 20:01:00", "confidence": 1.0, "source_evidence_ids": ["EV-057"], "details": "Primary operational location in Pune", "domain": "PHYSICAL"},
        {"id": "rel_10", "source": "person_arjun_sharma", "target": "incident_1042", "relation": "SUBJECT_OF", "timestamp": "2026-08-28 20:07:00", "confidence": 1.0, "source_evidence_ids": ["EV-001"], "details": "Primary subject of Cyber Extortion Incident #1042", "domain": "GENERAL"}
    ]

    # SEEDED EVIDENCE CARDS (MASTER PROMPT REQUIREMENT 6)
    evidence_items = [
        {"id": "EV-001", "case_id": "TRX-2026-017", "person_id": "person_arjun_sharma", "title": "CDR Communication Record", "evidence_type": "CDR", "source": "Telecom Node 4", "acquisition_timestamp": "2026-08-18 20:02:00", "file_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "file_size_bytes": 1840000, "integrity_status": "VERIFIED", "processing_status": "PROCESSED", "provenance": "Cryptographically signed export under Sec 65B Indian Evidence Act.", "analyst_notes": "187 calls and 234 msgs logged between Arjun Sharma (+91 98765 1201) and contacts.", "confidence": 0.98, "extracted_entities": ["Arjun Sharma", "Rohan Mehta", "+91 98765 1201"]},
        {"id": "EV-014", "case_id": "TRX-2026-017", "person_id": "person_rohan_mehta", "title": "Bank Transaction - HDFC XXXX 4821", "evidence_type": "BANK", "source": "FIU Gateway", "acquisition_timestamp": "2026-08-18 21:03:00", "file_hash": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284ddd200126d9069e", "file_size_bytes": 920000, "integrity_status": "VERIFIED", "processing_status": "PROCESSED", "provenance": "Authorized FIU Statement pull.", "analyst_notes": "₹48,500 Outgoing transfer from HDFC XXXX 4821 linked to Rohan Mehta.", "confidence": 0.95, "extracted_entities": ["HDFC Acc XXXX 4821", "Rohan Mehta", "₹48,500"]},
        {"id": "EV-023", "case_id": "TRX-2026-017", "person_id": "person_arjun_sharma", "title": "Public Social Media Mention", "evidence_type": "OSINT", "source": "Public Web Crawler", "acquisition_timestamp": "2026-08-18 11:03:00", "file_hash": "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e", "file_size_bytes": 120000, "integrity_status": "VERIFIED", "processing_status": "PROCESSED", "provenance": "Archived snapshot with cryptographic timestamp.", "analyst_notes": "Public mention on tech forum linking @arjun_s_demo to Rohan Mehta.", "confidence": 0.88, "extracted_entities": ["@arjun_s_demo", "Rohan Mehta"]},
        {"id": "EV-031", "case_id": "TRX-2026-017", "person_id": "person_vikram_patil", "title": "Vehicle Observation - MH12 AB 4821", "evidence_type": "DVR_NVR", "source": "City Surveillance Command", "acquisition_timestamp": "2026-08-18 20:26:00", "file_hash": "2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae", "file_size_bytes": 45000000, "integrity_status": "VERIFIED", "processing_status": "PROCESSED", "provenance": "Seized NVR hard drive #NVR-702 frame hash carving.", "analyst_notes": "ANPR capture of black SUV MH12 AB 4821 departing meeting location.", "confidence": 0.96, "extracted_entities": ["MH12 AB 4821", "Vikram Patil", "CAM-04"]},
        {"id": "EV-042", "case_id": "TRX-2026-017", "person_id": "person_arjun_sharma", "title": "Blockchain Transaction - 0xDEMO...A721", "evidence_type": "BLOCKCHAIN", "source": "Etherscan Node API", "acquisition_timestamp": "2026-08-18 21:17:00", "file_hash": "fcde2b2edba56bf408601fb721fe9b5c338d10ee429ea04fae5511b68fbf8fb9", "file_size_bytes": 310000, "integrity_status": "VERIFIED", "processing_status": "PROCESSED", "provenance": "Public blockchain RPC pull.", "analyst_notes": "TX-DEMO-001 receipt of 0.84 ETH to wallet 0xDEMO...A721.", "confidence": 0.94, "extracted_entities": ["0xDEMO...A721", "0.84 ETH"]},
        {"id": "EV-057", "case_id": "TRX-2026-017", "person_id": "person_arjun_sharma", "title": "CCTV Meeting - CAM-04", "evidence_type": "DVR_NVR", "source": "Surveillance Camera CAM-04", "acquisition_timestamp": "2026-08-18 20:01:00", "file_hash": "d41d8cd98f00b204e9800998ecf8427e56b3e66487e44a49c6d3ff3cf81734f2", "file_size_bytes": 62000000, "integrity_status": "VERIFIED", "processing_status": "PROCESSED", "provenance": "CCTV NVR export with SHA-256 block proof.", "analyst_notes": "SIMULATED INVESTIGATIVE SCENARIO: Fictional people meeting at Pune Location A.", "confidence": 0.96, "extracted_entities": ["Arjun Sharma", "Rohan Mehta", "CAM-04"]},
        {"id": "EV-061", "case_id": "TRX-2026-017", "person_id": "person_priya_joshi", "title": "OSINT Website Reference - Nexus Logistics", "evidence_type": "OSINT", "source": "Corporate Registrar Crawler", "acquisition_timestamp": "2026-08-18 15:08:00", "file_hash": "9b74c2d2390a81498b0493019808381273891729837198273891723891723981", "file_size_bytes": 210000, "integrity_status": "VERIFIED", "processing_status": "PROCESSED", "provenance": "Public domain WHOIS and MCA filings snapshot.", "analyst_notes": "Business registration linking Nexus Logistics Demo to Priya Joshi.", "confidence": 0.91, "extracted_entities": ["Nexus Logistics Demo", "Priya Joshi"]},
        {"id": "EV-074", "case_id": "TRX-2026-017", "person_id": "person_priya_joshi", "title": "Financial Account Link - Axis XXXX 7194", "evidence_type": "BANK", "source": "Axis Bank Gateway", "acquisition_timestamp": "2026-08-18 21:03:00", "file_hash": "1829379182739812739182739812739182739182739182739182739182739182", "file_size_bytes": 540000, "integrity_status": "VERIFIED", "processing_status": "PROCESSED", "provenance": "Section 91 CrPC Bank Statement Fetch.", "analyst_notes": "Incoming ₹72,000 corporate deposit credited to Axis Demo Account XXXX 7194.", "confidence": 0.93, "extracted_entities": ["Axis Acc XXXX 7194", "Priya Joshi", "₹72,000"]}
    ]

    # 3 SYNTHETIC DEMO CCTV SURVEILLANCE VIDEOS (MASTER PROMPT REQUIREMENT 17 & 18)
    dvr_videos = [
        {
            "id": "DVR-VID-01",
            "camera_id": "CAM-04",
            "location": "Synthetic Pune Location A",
            "timestamp": "2026-08-18 20:01:00 IST",
            "event_title": "Person Meeting",
            "suspects_identified": ["Arjun Sharma", "Rohan Mehta"],
            "anpr_license_plate": "MH12 AB 4821",
            "evidence_id": "EV-001",
            "video_thumbnail": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800&auto=format&fit=crop&q=80",
            "description": "Two fictional people meet near a parked vehicle at Synthetic Pune Location A.",
            "label": "SYNTHETIC DEMO DATA"
        },
        {
            "id": "DVR-VID-02",
            "camera_id": "CAM-04",
            "location": "Synthetic Pune Location B",
            "timestamp": "2026-08-18 20:17:00 IST",
            "event_title": "Financial Exchange — Investigative Simulation",
            "suspects_identified": ["Arjun Sharma", "Rohan Mehta"],
            "anpr_license_plate": "MH12 XY 9988",
            "evidence_id": "EV-057",
            "video_thumbnail": "https://images.unsplash.com/photo-1573164713988-8665fc963095?w=800&auto=format&fit=crop&q=80",
            "description": "Two fictional individuals exchange an envelope/bag. Note: Does not represent proof of money laundering.",
            "label": "SIMULATED INVESTIGATIVE SCENARIO"
        },
        {
            "id": "DVR-VID-03",
            "camera_id": "CAM-04",
            "location": "Synthetic Pune Location C",
            "timestamp": "2026-08-18 20:26:00 IST",
            "event_title": "Vehicle Departure",
            "suspects_identified": ["Vikram Patil (Driver)", "MH12 AB 4821"],
            "anpr_license_plate": "MH12 AB 4821",
            "evidence_id": "EV-003",
            "video_thumbnail": "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&auto=format&fit=crop&q=80",
            "description": "Vehicle MH12 AB 4821 leaves the meeting location at 20:26 IST.",
            "label": "SYNTHETIC DEMO DATA"
        }
    ]

    # 5 SEEDED AI INVESTIGATIVE LEADS (MASTER PROMPT REQUIREMENT 21)
    leads = [
        {
            "id": "LEAD-01",
            "title": "Repeated communication + financial activity",
            "summary": "AI Evidence Fusion engine detected 27 calls and 3 cash transfers between Arjun Sharma and Rohan Mehta within a 45-minute window.",
            "confidence": 0.82,
            "supporting_evidence": ["EV-023", "EV-041", "EV-052"],
            "evidence_chain": [
                {"step": 1, "domain": "CDR", "description": "Arjun Sharma (+91 98765 1201) calls Rohan Mehta 14 times before Incident #1042.", "evidence_id": "EV-001"},
                {"step": 2, "domain": "DVR", "description": "Vehicle MH12 AB 4821 detected at CAM-04 at 20:26 IST.", "evidence_id": "EV-031"},
                {"step": 3, "domain": "FINANCIAL", "description": "₹48,500 Outgoing transfer to Rohan Mehta logged.", "evidence_id": "EV-014"}
            ],
            "recommended_actions": [
                "Issue legal notice under Sec 91 CrPC for raw tower dump.",
                "Inspect original TSP signed CDR logs for IMEI correlation.",
                "Verify beneficiary KYCs of HDFC Demo Account XXXX 4821."
            ],
            "alternative_explanation": "Business coordination between trade counterparties.",
            "status": "Needs Review",
            "human_review_required": True
        },
        {
            "id": "LEAD-02",
            "title": "Potential transaction layering pattern",
            "summary": "Anomalous fund velocity: ₹1,25,000 deposited into Axis Acc XXXX 7194 was split into 3 accounts in 18 minutes without commercial invoices.",
            "confidence": 0.74,
            "supporting_evidence": ["EV-061", "EV-074"],
            "evidence_chain": [
                {"step": 1, "domain": "FINANCIAL", "description": "Incoming ₹1,25,000 deposit credited to Axis Demo Account.", "evidence_id": "EV-074"},
                {"step": 2, "domain": "BLOCKCHAIN", "description": "0.84 ETH off-ramped to wallet 0xDEMO...A721.", "evidence_id": "EV-042"}
            ],
            "recommended_actions": [
                "Pull Section 91 CrPC Bank Statement for Axis Acc XXXX 7194.",
                "Verify corporate registrar filings of Nexus Logistics Demo."
            ],
            "alternative_explanation": "Routine corporate payroll processing.",
            "status": "Needs Review",
            "human_review_required": True
        },
        {
            "id": "LEAD-03",
            "title": "Temporal correlation between communication and physical meeting",
            "summary": "Phone call at 20:02 IST occurred 60 seconds after CCTV Cam-04 captured physical meeting at Synthetic Pune Location A.",
            "confidence": 0.79,
            "supporting_evidence": ["EV-001", "EV-057"],
            "evidence_chain": [
                {"step": 1, "domain": "DVR", "description": "CCTV Cam-04 captured meeting at 20:01 IST.", "evidence_id": "EV-057"},
                {"step": 2, "domain": "CDR", "description": "Outgoing call from Arjun to Rohan at 20:02 IST.", "evidence_id": "EV-001"}
            ],
            "recommended_actions": [
                "Perform frame carving analysis on Cam-04 raw video stream."
            ],
            "alternative_explanation": "Coincidental timing during regular business hours.",
            "status": "Needs Review",
            "human_review_required": True
        },
        {
            "id": "LEAD-04",
            "title": "Potential shared organizational connection",
            "summary": "Public web mention correlates Arjun Sharma, Priya Joshi, and Neha Kulkarni to Nexus Logistics Demo.",
            "confidence": 0.68,
            "supporting_evidence": ["EV-023", "EV-061"],
            "evidence_chain": [
                {"step": 1, "domain": "OSINT", "description": "Public domain snapshot linking subjects to corporate website.", "evidence_id": "EV-061"}
            ],
            "recommended_actions": [
                "Cross-reference MCA filings for official director status."
            ],
            "alternative_explanation": "Legitimate employment at common workplace.",
            "status": "Needs Review",
            "human_review_required": True
        },
        {
            "id": "LEAD-05",
            "title": "Possible identity ambiguity (False Positive)",
            "summary": "POTENTIAL MATCH (Confidence 43%). Public profile 'Arjun S.' shares name similarity and Pune location overlap, but evidence is insufficient.",
            "confidence": 0.43,
            "supporting_evidence": ["EV-061"],
            "evidence_chain": [
                {"step": 1, "domain": "OSINT", "description": "Public profile 'Arjun S.' flagged during broad name harvest.", "evidence_id": "EV-061"}
            ],
            "recommended_actions": [
                "Mark candidate as False Positive after manual verification."
            ],
            "alternative_explanation": "Unrelated individual with common name.",
            "status": "False Positive / Needs Review",
            "human_review_required": True
        }
    ]

    # AUDIT TRAIL LOG HISTORY (MASTER PROMPT REQUIREMENT 27)
    audit_events = [
        {"timestamp": "09:41", "actor": "Ins. Vikramaditya Rao", "action_type": "USER_LOGIN", "object": "System Authentication", "result": "Success"},
        {"timestamp": "09:43", "actor": "Ins. Vikramaditya Rao", "action_type": "CASE_OPENED", "object": "Case TRX-2026-017 (Operation Nexus)", "result": "Opened"},
        {"timestamp": "09:51", "actor": "Ins. Vikramaditya Rao", "action_type": "EVIDENCE_VIEWED", "object": "Evidence EV-023 (Social Media Mention)", "result": "Verified"},
        {"timestamp": "10:02", "actor": "Ins. Vikramaditya Rao", "action_type": "PERSON_PROFILE_OPENED", "object": "Subject Arjun Sharma", "result": "Loaded"},
        {"timestamp": "10:19", "actor": "Ins. Vikramaditya Rao", "action_type": "GRAPH_EXPANDED", "object": "Network Tree Level 2", "result": "Expanded"},
        {"timestamp": "10:44", "actor": "Ins. Vikramaditya Rao", "action_type": "EVIDENCE_REVIEWED", "object": "Evidence EV-042 (Blockchain Tx)", "result": "Marked Needs Review"},
        {"timestamp": "11:12", "actor": "Ins. Vikramaditya Rao", "action_type": "FINANCIAL_VIEWED", "object": "HDFC Acc XXXX 4821 Statements", "result": "Loaded"},
        {"timestamp": "11:37", "actor": "Ins. Vikramaditya Rao", "action_type": "CCTV_EVIDENCE_OPENED", "object": "Cam-04 Video EV-057", "result": "Played"},
        {"timestamp": "12:01", "actor": "Ins. Vikramaditya Rao", "action_type": "REPORT_GENERATED", "object": "Investigation Report TRX-2026-017", "result": "Generated"}
    ]

    anomalies = [
        {"id": "ANM-001", "category": "Communication Burst", "title": "Potential Communication Anomaly", "severity": "High", "timestamp": "2026-08-18 19:45:00", "affected_entity_ids": ["person_arjun_sharma", "person_rohan_mehta"], "explanation": "Communication frequency between Arjun Sharma and Rohan Mehta increased by 420% prior to Incident #1042.", "evidence_ids": ["EV-001"], "confidence": 0.94, "analyst_status": "Requires Human Review"},
        {"id": "ANM-002", "category": "Financial Movement", "title": "Potential Informal Value Transfer Pattern", "severity": "High", "timestamp": "2026-08-18 20:45:00", "affected_entity_ids": ["person_rohan_mehta", "acc_hdfc_demo", "person_priya_joshi"], "explanation": "Observed transaction structure matches selected red-flag indicators (71% confidence).", "evidence_ids": ["EV-014", "EV-074"], "confidence": 0.71, "analyst_status": "Requires Human Review"},
        {"id": "ANM-003", "category": "Temporal Sighting", "title": "Potential Temporal Correlation", "severity": "High", "timestamp": "2026-08-18 20:12:00", "affected_entity_ids": ["vehicle_mh12", "camera_c12"], "explanation": "Vehicle MH12 AB 4821 passed CCTV Cam-04 within short temporal window of meeting.", "evidence_ids": ["EV-031", "EV-057"], "confidence": 0.92, "analyst_status": "Requires Human Review"}
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
