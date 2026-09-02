import random
from datetime import datetime, timedelta
from typing import Dict, List, Any

random.seed(2026189)

def generate_synthetic_dataset() -> Dict[str, Any]:
    # DEMO CASE TRX-2026-017 (Operation Nexus)
    arjun_profile = {
        "id": "person_arjun_sharma",
        "name": "Arjun Sharma",
        "alias": "Cipher King",
        "role": "Primary Subject",
        "relationship_to_primary": "Self",
        "age": 34,
        "gender": "Male",
        "photo_url": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=300&auto=format&fit=crop&q=80",
        "phone": "+91-98765-10001",
        "email": "arjun.sharma@protonmail.com",
        "address": "Flat 402, Shivajinagar",
        "city": "Pune, Maharashtra",
        "occupation": "Software Consultant",
        "organization": "Apex Global Solutions",
        "vehicle": "MH12-AB-1234 (SUV)",
        "social_usernames": {
            "telegram": "@cipher_king",
            "twitter": "@arjun_s89",
            "instagram": "@arjun_cyber",
            "darkweb": "shadow_broker99"
        },
        "wallet_address": "0x82a9b4fe82c19a...9b4",
        "notes": "Primary subject under investigation for Operation Nexus.",
        "risk_score": 92,
        "evidence_count": 82
    }

    secondary_suspects = [
        {
            "id": "person_rohan_mehta",
            "name": "Rohan Mehta",
            "alias": "Runner R",
            "role": "Secondary Subject",
            "relationship_to_primary": "Associate / Field Contact",
            "age": 31,
            "gender": "Male",
            "photo_url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=300&auto=format&fit=crop&q=80",
            "phone": "+91-98765-20002",
            "email": "rohan.mehta@gmail.com",
            "address": "Kothrud, Pune",
            "city": "Pune",
            "occupation": "Logistics Supervisor",
            "organization": "Nexus Express",
            "vehicle": "MH12-XY-9988",
            "social_usernames": {"telegram": "@rohan_runner", "instagram": "@rohan_m_vlogs"},
            "wallet_address": "0x3910ab12f0090...199",
            "notes": "14 direct calls logged with Arjun Sharma prior to Incident #1042.",
            "risk_score": 85,
            "evidence_count": 24
        },
        {
            "id": "person_priya_joshi",
            "name": "Priya Joshi",
            "alias": "Priya J",
            "role": "Secondary Subject",
            "relationship_to_primary": "Business Contact / Accountant",
            "age": 29,
            "gender": "Female",
            "photo_url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=300&auto=format&fit=crop&q=80",
            "phone": "+91-98765-30003",
            "email": "priya.joshi@apexglobal.in",
            "address": "Baner Road, Pune",
            "city": "Pune",
            "occupation": "Senior Accountant",
            "organization": "Apex Global Solutions",
            "vehicle": "MH14-CD-5544",
            "social_usernames": {"linkedin": "in/priya-joshi-finance"},
            "wallet_address": "",
            "notes": "Managed bank accounts used for multi-hop cash deposits.",
            "risk_score": 78,
            "evidence_count": 18
        },
        {
            "id": "person_vikram_patil",
            "name": "Vikram Patil",
            "alias": "Vicky",
            "role": "Secondary Subject",
            "relationship_to_primary": "Employee / Driver",
            "age": 36,
            "gender": "Male",
            "photo_url": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=300&auto=format&fit=crop&q=80",
            "phone": "+91-98765-40004",
            "email": "vikram.patil@driver.in",
            "address": "Hadapsar, Pune",
            "city": "Pune",
            "occupation": "Personal Driver",
            "organization": "Private Fleet",
            "vehicle": "MH12-AB-1234",
            "social_usernames": {"telegram": "@vicky_driver"},
            "wallet_address": "",
            "notes": "Observed driving vehicle MH12-AB-1234 near meeting spot.",
            "risk_score": 72,
            "evidence_count": 15
        },
        {
            "id": "person_neha_kulkarni",
            "name": "Neha Kulkarni",
            "alias": "NK",
            "role": "Person of Interest",
            "relationship_to_primary": "Person of Interest",
            "age": 28,
            "gender": "Female",
            "photo_url": "https://images.unsplash.com/photo-1580489944761-15a19d654956?w=300&auto=format&fit=crop&q=80",
            "phone": "+91-98765-50005",
            "email": "neha.k@techdesk.io",
            "address": "Viman Nagar, Pune",
            "city": "Pune",
            "occupation": "IT Analyst",
            "organization": "TechDesk Systems",
            "vehicle": "",
            "social_usernames": {"twitter": "@neha_k_cyber"},
            "wallet_address": "",
            "notes": "Shared IP subnet access with primary subject's VPN server.",
            "risk_score": 58,
            "evidence_count": 9
        }
    ]

    case_primary = {
        "id": "TRX-2026-017",
        "title": "Operation Nexus",
        "primary_suspect": arjun_profile,
        "secondary_suspects": secondary_suspects,
        "subject_known_identifiers": {
            "phone": ["+91-98765-10001", "+91-98765-10099"],
            "email": ["arjun.sharma@protonmail.com"],
            "aliases": ["Arjun S.", "Cipher King", "shadow_broker99"],
            "vehicle": ["MH12-AB-1234"],
            "wallet": ["0x82a9b4fe82c19a...9b4"],
            "account": ["ACC-IND-994101", "ACC-HDFC-882104"]
        },
        "description": "Cross-domain intelligence fusion investigating an illicit financial transfer syndicate coordinating extortion, money laundering through informal channels, and crypto off-ramping connected to cyber extortion incident #1042.",
        "investigation_type": "Cyber-Financial Crime",
        "priority": "High",
        "status": "Active",
        "date_opened": "2026-08-15",
        "lead_investigator": "Ins. Vikramaditya Rao (#INV-7092)",
        "agency": "Special Cyber Crime & Intelligence Cell (SCCIC)",
        "location": "Pune, Maharashtra",
        "tags": ["EXTORTION", "HAWALA_INDICATORS", "CRYPTO_FLOW", "DVR_FORENSIC"],
        "evidence_count": 82,
        "last_activity": "10 mins ago"
    }

    case_secondary = {
        "id": "TRX-2026-014",
        "title": "Operation Metro",
        "primary_suspect": {
            "id": "person_vikram_patil_sub",
            "name": "Vikram Patil",
            "alias": "Patil Boss",
            "role": "Primary Subject",
            "relationship_to_primary": "Self",
            "age": 41,
            "gender": "Male",
            "photo_url": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=300",
            "phone": "+91-98111-00001",
            "email": "patil.v@metronet.org",
            "address": "Camp Area, Pune",
            "city": "Pune",
            "occupation": "Transport Operator",
            "organization": "Metro Logistics",
            "vehicle": "MH12-CD-9900",
            "social_usernames": {"telegram": "@patil_metro"},
            "wallet_address": "",
            "notes": "Parallel inquiry into SIM-box operation in Western Corridor.",
            "risk_score": 88,
            "evidence_count": 41
        },
        "secondary_suspects": [],
        "subject_known_identifiers": {"phone": ["+91-98111-00001"]},
        "description": "Parallel inquiry into SIM-box operation in Western Corridor.",
        "investigation_type": "Telecom Fraud",
        "priority": "Medium",
        "status": "Active",
        "date_opened": "2026-07-01",
        "lead_investigator": "Sub-Ins. Neha Gupta (#INV-4401)",
        "agency": "State Cyber Cell",
        "location": "Pune, Maharashtra",
        "tags": ["SIM_BOX", "TELECOM_FRAUD"],
        "evidence_count": 41,
        "last_activity": "1 hour ago"
    }

    cases_db = {
        "TRX-2026-017": case_primary,
        "TRX-2026-014": case_secondary
    }

    # KNOWLEDGE GRAPH NODES (TREE VIEW SUPPORTED)
    nodes = []
    # Primary & Secondary Person Nodes
    nodes.append({"id": "person_arjun_sharma", "label": "Arjun Sharma", "type": "PERSON", "risk_score": 92, "confidence": 1.0, "details": "Primary Subject / Syndicate Lead. Associated with Telegram @cipher_king.", "status": "Confirmed", "source_evidence_ids": ["EVD-DOC-001", "EVD-CDR-101"], "tree_level": 0, "avatar": arjun_profile["photo_url"]})
    nodes.append({"id": "person_rohan_mehta", "label": "Rohan Mehta", "type": "PERSON", "risk_score": 85, "confidence": 0.95, "details": "Secondary Subject / Associate. 14 calls logged with Arjun Sharma.", "status": "Confirmed", "source_evidence_ids": ["EVD-CDR-101", "EVD-DVR-501"], "tree_level": 1, "avatar": secondary_suspects[0]["photo_url"]})
    nodes.append({"id": "person_priya_joshi", "label": "Priya Joshi", "type": "PERSON", "risk_score": 78, "confidence": 0.92, "details": "Secondary Subject / Business Contact & Senior Accountant.", "status": "Confirmed", "source_evidence_ids": ["EVD-BNK-201"], "tree_level": 1, "avatar": secondary_suspects[1]["photo_url"]})
    nodes.append({"id": "person_vikram_patil", "label": "Vikram Patil", "type": "PERSON", "risk_score": 72, "confidence": 0.90, "details": "Secondary Subject / Driver of SUV MH12-AB-1234.", "status": "Confirmed", "source_evidence_ids": ["EVD-DVR-501"], "tree_level": 1, "avatar": secondary_suspects[2]["photo_url"]})
    nodes.append({"id": "person_neha_kulkarni", "label": "Neha Kulkarni", "type": "PERSON", "risk_score": 58, "confidence": 0.85, "details": "Person of Interest / Shared IP subnet access.", "status": "Confirmed", "source_evidence_ids": ["EVD-OSINT-401"], "tree_level": 2, "avatar": secondary_suspects[3]["photo_url"]})

    # Connected Entities
    nodes.append({"id": "phone_arjun_1", "label": "+91-98765-10001", "type": "PHONE", "risk_score": 90, "confidence": 1.0, "details": "Primary MSISDN assigned to Arjun Sharma", "status": "Confirmed", "source_evidence_ids": ["EVD-CDR-101"], "tree_level": 1})
    nodes.append({"id": "phone_rohan_1", "label": "+91-98765-20002", "type": "PHONE", "risk_score": 85, "confidence": 1.0, "details": "MSISDN assigned to Rohan Mehta", "status": "Confirmed", "source_evidence_ids": ["EVD-CDR-101"], "tree_level": 2})
    nodes.append({"id": "acc_apex_global", "label": "ACC-IND-994101", "type": "BANK_ACCOUNT", "risk_score": 86, "confidence": 1.0, "details": "HDFC Current Account used for rapid multi-hop fund routing", "status": "Confirmed", "source_evidence_ids": ["EVD-BNK-201"], "tree_level": 2})
    nodes.append({"id": "wallet_shadow", "label": "0x82a9b4...9b4", "type": "CRYPTO_WALLET", "risk_score": 94, "confidence": 0.98, "details": "Cold wallet referenced in OSINT threat intel", "status": "Confirmed", "source_evidence_ids": ["EVD-BLK-301"], "tree_level": 3})
    nodes.append({"id": "vehicle_mh12", "label": "MH12-AB-1234", "type": "VEHICLE", "risk_score": 82, "confidence": 0.96, "details": "Black SUV registered under Vikram Patil / Arjun Sharma", "status": "Confirmed", "source_evidence_ids": ["EVD-DVR-501"], "tree_level": 2})
    nodes.append({"id": "camera_c12", "label": "Cam C12 - MG Road", "type": "CAMERA", "risk_score": 40, "confidence": 1.0, "details": "CCTV ANPR Camera at MG Road Corridor", "status": "Confirmed", "source_evidence_ids": ["EVD-DVR-501"], "tree_level": 3})
    nodes.append({"id": "incident_1042", "label": "Incident #1042", "type": "INCIDENT", "risk_score": 100, "confidence": 1.0, "details": "Cyber Extortion Incident on 2026-08-28 20:07 IST", "status": "Confirmed", "source_evidence_ids": ["EVD-DOC-001"], "tree_level": 0})

    edges = []
    edges.append({"id": "rel_1", "source": "person_arjun_sharma", "target": "person_rohan_mehta", "relation": "COMMUNICATION", "timestamp": "2026-08-28 19:25:00", "confidence": 0.98, "source_evidence_ids": ["EVD-CDR-101"], "details": "14 Encrypted voice calls logged between Arjun Sharma & Rohan Mehta", "domain": "COMMUNICATION", "call_count": 14, "first_observed": "04 Aug 2026", "last_observed": "17 Aug 2026"})
    edges.append({"id": "rel_2", "source": "person_arjun_sharma", "target": "person_priya_joshi", "relation": "BUSINESS_CONTACT", "timestamp": "2026-08-10 10:00:00", "confidence": 0.95, "source_evidence_ids": ["EVD-BNK-201"], "details": "8 corporate transfers managed by Priya Joshi for Arjun Sharma", "domain": "FINANCIAL", "call_count": 8, "first_observed": "10 Aug 2026", "last_observed": "28 Aug 2026"})
    edges.append({"id": "rel_3", "source": "person_arjun_sharma", "target": "person_vikram_patil", "relation": "EMPLOYEE", "timestamp": "2026-08-01 10:00:00", "confidence": 0.92, "source_evidence_ids": ["EVD-DVR-501"], "details": "Vikram Patil observed driving vehicle MH12-AB-1234 for Arjun Sharma", "domain": "PHYSICAL", "call_count": 6, "first_observed": "01 Aug 2026", "last_observed": "28 Aug 2026"})
    edges.append({"id": "rel_4", "source": "person_arjun_sharma", "target": "phone_arjun_1", "relation": "USES", "timestamp": "2026-08-01 10:00:00", "confidence": 0.99, "source_evidence_ids": ["EVD-CDR-101"], "details": "Subscriber registration match for Arjun Sharma", "domain": "COMMUNICATION"})
    edges.append({"id": "rel_5", "source": "person_rohan_mehta", "target": "phone_rohan_1", "relation": "USES", "timestamp": "2026-08-01 10:00:00", "confidence": 0.99, "source_evidence_ids": ["EVD-CDR-101"], "details": "Subscriber registration match for Rohan Mehta", "domain": "COMMUNICATION"})
    edges.append({"id": "rel_6", "source": "phone_arjun_1", "target": "phone_rohan_1", "relation": "CALLED", "timestamp": "2026-08-28 19:25:00", "confidence": 0.98, "source_evidence_ids": ["EVD-CDR-101"], "details": "Pre-incident call burst of 14 calls", "domain": "COMMUNICATION"})
    edges.append({"id": "rel_7", "source": "person_rohan_mehta", "target": "acc_apex_global", "relation": "TRANSFERRED", "timestamp": "2026-08-28 20:45:00", "confidence": 0.97, "source_evidence_ids": ["EVD-BNK-201"], "details": "IMPS transfer of ₹25,00,000 to Apex Global Account", "domain": "FINANCIAL"})
    edges.append({"id": "rel_8", "source": "acc_apex_global", "target": "wallet_shadow", "relation": "TRANSFERRED", "timestamp": "2026-08-28 21:15:00", "confidence": 0.92, "source_evidence_ids": ["EVD-BLK-301"], "details": "8.5 ETH off-ramped to crypto wallet 0x82...9b4", "domain": "BLOCKCHAIN"})
    edges.append({"id": "rel_9", "source": "person_vikram_patil", "target": "vehicle_mh12", "relation": "DRIVES", "timestamp": "2026-08-28 20:26:00", "confidence": 0.94, "source_evidence_ids": ["EVD-DVR-501"], "details": "ANPR sighting of SUV MH12-AB-1234 driven by Vikram Patil", "domain": "DVR"})
    edges.append({"id": "rel_10", "source": "vehicle_mh12", "target": "camera_c12", "relation": "OBSERVED_AT", "timestamp": "2026-08-28 20:12:00", "confidence": 0.94, "source_evidence_ids": ["EVD-DVR-501"], "details": "CCTV Cam C12 capture at MG Road Corridor", "domain": "DVR"})

    evidence_items = [
        {"id": "EVD-DOC-001", "case_id": "TRX-2026-017", "person_id": "person_arjun_sharma", "title": "FIR #1042/2026 - Cyber Extortion Incident Report", "evidence_type": "DOCUMENT", "source": "Shivajinagar Police Station", "acquisition_timestamp": "2026-08-28 21:00:00", "file_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "file_size_bytes": 452000, "integrity_status": "VERIFIED", "processing_status": "PROCESSED", "provenance": "Certified copy obtained via Sec 91 CrPC.", "analyst_notes": "Primary Incident report detailing extortion complaint against Arjun Sharma."},
        {"id": "EVD-CDR-101", "case_id": "TRX-2026-017", "person_id": "person_arjun_sharma", "title": "Call Detail Records (CDR) - Target +91-98765-10001", "evidence_type": "CDR", "source": "Telecom Service Provider Node 4", "acquisition_timestamp": "2026-08-29 01:15:00", "file_hash": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284ddd200126d9069e", "file_size_bytes": 1840000, "integrity_status": "VERIFIED", "processing_status": "PROCESSED", "provenance": "Cryptographically signed export under Sec 65B.", "analyst_notes": "14 encrypted pre-incident calls between Arjun Sharma and Rohan Mehta."},
        {"id": "EVD-BNK-201", "case_id": "TRX-2026-017", "person_id": "person_rohan_mehta", "title": "Bank Transaction Log - HDFC Acc #ACC-IND-994101", "evidence_type": "BANK", "source": "FIU Gateway", "acquisition_timestamp": "2026-08-29 04:30:00", "file_hash": "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e", "file_size_bytes": 920000, "integrity_status": "VERIFIED", "processing_status": "PROCESSED", "provenance": "Authorized FIU Statement pull.", "analyst_notes": "₹25L IMPS cash transfer initiated by Rohan Mehta to Priya Joshi's company account."},
        {"id": "EVD-BLK-301", "case_id": "TRX-2026-017", "person_id": "person_priya_joshi", "title": "On-Chain Ledger Capture - Wallet 0x82a9b4...9b4", "evidence_type": "BLOCKCHAIN", "source": "Etherscan Node API", "acquisition_timestamp": "2026-08-29 06:00:00", "file_hash": "2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae", "file_size_bytes": 310000, "integrity_status": "VERIFIED", "processing_status": "PROCESSED", "provenance": "Public blockchain RPC pull.", "analyst_notes": "Traces 8.5 ETH off-ramped to cold wallet 0x82...9b4."},
        {"id": "EVD-OSINT-401", "case_id": "TRX-2026-017", "person_id": "person_arjun_sharma", "title": "Public Web Threat Intel - Darkweb Harvest", "evidence_type": "OSINT", "source": "OSINT Intelligence Crawler", "acquisition_timestamp": "2026-08-29 08:20:00", "file_hash": "fcde2b2edba56bf408601fb721fe9b5c338d10ee429ea04fae5511b68fbf8fb9", "file_size_bytes": 120000, "integrity_status": "VERIFIED", "processing_status": "PROCESSED", "provenance": "Archived snapshot with cryptographic timestamp.", "analyst_notes": "Links wallet 0x82...9b4 to handle Cipher_King (Arjun Sharma)."},
        {"id": "EVD-DVR-501", "case_id": "TRX-2026-017", "person_id": "person_vikram_patil", "title": "CCTV Surveillance Stream - Cam C12 (MG Road)", "evidence_type": "DVR_NVR", "source": "City Surveillance Command", "acquisition_timestamp": "2026-08-29 09:45:00", "file_hash": "d41d8cd98f00b204e9800998ecf8427e56b3e66487e44a49c6d3ff3cf81734f2", "file_size_bytes": 45000000, "integrity_status": "VERIFIED", "processing_status": "PROCESSED", "provenance": "Seized NVR hard drive #NVR-702 frame carving.", "analyst_notes": "ANPR match for Vikram Patil's vehicle MH12-AB-1234."}
    ]

    # 3 SYNTHETIC DEMO CCTV SURVEILLANCE VIDEOS (MASTER PROMPT REQUIREMENT 19)
    dvr_videos = [
        {
            "id": "DVR-VID-01",
            "camera_id": "Cam C12 - MG Road",
            "location": "Synthetic Location A (MG Road Junction Exterior)",
            "timestamp": "2026-08-28 20:01:00 IST",
            "event_title": "Person Meeting",
            "suspects_identified": ["Arjun Sharma (Primary)", "Rohan Mehta (Secondary)"],
            "anpr_license_plate": "MH12-AB-1234",
            "confidence_score": "96.4%",
            "video_thumbnail": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800&auto=format&fit=crop&q=80",
            "description": "SIMULATED INVESTIGATIVE SCENARIO: Two fictional individuals meet near a parked vehicle 6 minutes before Incident #1042 report.",
            "label": "SIMULATED INVESTIGATIVE SCENARIO"
        },
        {
            "id": "DVR-VID-02",
            "camera_id": "Cam C14 - Parking Lot B",
            "location": "Synthetic Location B (Commercial Complex Parking)",
            "timestamp": "2026-08-28 20:17:00 IST",
            "event_title": "Financial Exchange — Investigative Simulation",
            "suspects_identified": ["Rohan Mehta (Secondary)", "Priya Joshi (Secondary)"],
            "anpr_license_plate": "MH12-XY-9988",
            "confidence_score": "94.8%",
            "video_thumbnail": "https://images.unsplash.com/photo-1573164713988-8665fc963095?w=800&auto=format&fit=crop&q=80",
            "description": "SIMULATED INVESTIGATIVE SCENARIO: Two fictional individuals exchange an envelope/bag near Parking Bay 4. Note: Does not represent proof of money laundering.",
            "label": "SIMULATED INVESTIGATIVE SCENARIO"
        },
        {
            "id": "DVR-VID-03",
            "camera_id": "Cam C18 - Expressway Toll",
            "location": "Synthetic Location C (Expressway Toll Plaza Gate 3)",
            "timestamp": "2026-08-28 20:26:00 IST",
            "event_title": "Vehicle Departure",
            "suspects_identified": ["Vikram Patil (Driver)", "SUV MH12-AB-1234"],
            "anpr_license_plate": "MH12-AB-1234",
            "confidence_score": "98.2%",
            "video_thumbnail": "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&auto=format&fit=crop&q=80",
            "description": "SIMULATED INVESTIGATIVE SCENARIO: Vehicle leaves the meeting location at high velocity 19 minutes post-incident.",
            "label": "SIMULATED INVESTIGATIVE SCENARIO"
        }
    ]

    anomalies = [
        {"id": "ANM-001", "category": "Communication Burst", "title": "Potential Communication Anomaly Detected", "severity": "High", "timestamp": "2026-08-28 19:45:00", "affected_entity_ids": ["person_arjun_sharma", "person_rohan_mehta"], "explanation": "Communication frequency between Arjun Sharma and Rohan Mehta increased by 420% during the 45 minutes preceding Incident #1042.", "evidence_ids": ["EVD-CDR-101"], "confidence": 0.94, "analyst_status": "Requires Human Verification"},
        {"id": "ANM-002", "category": "Financial Movement", "title": "Potential Financial Pattern / Rapid Transfer", "severity": "High", "timestamp": "2026-08-28 20:45:00", "affected_entity_ids": ["person_rohan_mehta", "acc_apex_global", "person_priya_joshi"], "explanation": "₹25,00,000 deposit into HDFC Acc ACC-IND-994101 split into 3 accounts in 18 minutes.", "evidence_ids": ["EVD-BNK-201"], "confidence": 0.89, "analyst_status": "Requires Human Verification"},
        {"id": "ANM-003", "category": "Temporal Sighting", "title": "Potential Temporal Correlation around Incident #1042", "severity": "High", "timestamp": "2026-08-28 20:12:00", "affected_entity_ids": ["vehicle_mh12", "camera_c12"], "explanation": "Vehicle MH12-AB-1234 passed CCTV Cam C12 5 minutes after Incident #1042 reported 150m away.", "evidence_ids": ["EVD-DVR-501"], "confidence": 0.92, "analyst_status": "Requires Human Verification"}
    ]

    leads = [
        {
            "id": "LEAD-2026-01",
            "title": "Investigative Lead: Multi-Domain Evidence Chain Linking Arjun Sharma to Incident #1042",
            "summary": "AI Evidence Fusion engine correlated CDR communication spikes, vehicle ANPR sightings, rapid bank transfers, and crypto off-ramping into a unified 6-hop evidence chain.",
            "confidence": 0.93,
            "evidence_chain": [
                {"step": 1, "domain": "CDR", "description": "Arjun Sharma (+91-98765-10001) calls Rohan Mehta (+91-98765-20002) 14 times before Incident #1042.", "evidence_id": "EVD-CDR-101"},
                {"step": 2, "domain": "DVR", "description": "Vehicle MH12-AB-1234 (driven by Vikram Patil) detected at Cam C12 5 mins post-incident.", "evidence_id": "EVD-DVR-501"},
                {"step": 3, "domain": "FINANCIAL", "description": "Rohan Mehta initiates ₹25L transfer to Apex Global Account (managed by Priya Joshi).", "evidence_id": "EVD-BNK-201"},
                {"step": 4, "domain": "BLOCKCHAIN", "description": "Apex Global account converts ₹25L to 8.5 ETH sent to Crypto Wallet 0x82...9b4.", "evidence_id": "EVD-BLK-301"},
                {"step": 5, "domain": "OSINT", "description": "Wallet 0x82...9b4 linked to handle 'Cipher_King' / Arjun Sharma in OSINT threat paste.", "evidence_id": "EVD-OSINT-401"}
            ],
            "recommended_actions": [
                "Issue legal notice under Sec 91 CrPC for raw tower dump at MG Road Junction.",
                "Inspect original TSP signed CDR logs for IMEI device correlation.",
                "Verify beneficiary KYCs of Apex Global bank accounts.",
                "Perform forensic verification of Cam C12 raw video stream hash."
            ],
            "human_review_required": True
        }
    ]

    return {
        "cases": cases_db,
        "nodes": nodes,
        "edges": edges,
        "evidence_items": evidence_items,
        "dvr_videos": dvr_videos,
        "anomalies": anomalies,
        "leads": leads
    }
