import random
from datetime import datetime, timedelta
from typing import Dict, List, Any

random.seed(2026189)

def generate_synthetic_dataset() -> Dict[str, Any]:
    case_primary = {
        "id": "TRACE-2026-017",
        "title": "Operation Cipher Net - Cyber-Financial Syndicate Investigation",
        "subject_name": "Rahul Sharma",
        "subject_known_identifiers": {
            "phone": ["+91-98765-10001", "+91-98765-10099"],
            "email": ["rahul.sharma89@protonmail.com", "r_sharma_cyber@gmail.com"],
            "aliases": ["Rahul S.", "r_sharma_1989", "Cipher_King", "shadow_broker99"],
            "vehicle": ["MH-12-RS-9988", "MH-14-XY-1001"],
            "wallet": ["0x71a9b4fe82c19a004812f883b1029c71a9b4fe82", "0x3910ab12f0090884210419280011a0029b920199"],
            "account": ["ACC-IND-994101", "ACC-HDFC-882104"]
        },
        "description": "Cross-domain intelligence fusion investigating an illicit financial transfer syndicate coordinating extortion, money laundering through informal channels (hawala indicators), and crypto off-ramping connected to cyber extortion incident #1042.",
        "investigator": "Ins. Vikramaditya Rao (#INV-7092)",
        "agency": "Special Cyber Crime & Intelligence Cell (SCCIC)",
        "priority": "HIGH",
        "status": "ACTIVE",
        "start_date": "2026-08-15",
        "end_date": None,
        "tags": ["EXTORTION", "MONEY_LAUNDERING", "HAWALA_INDICATORS", "CRYPTO_FLOW", "DVR_FORENSIC"]
    }

    cases_db = {
        "TRACE-2026-017": case_primary,
        "TRACE-2026-004": {
            "id": "TRACE-2026-004",
            "title": "Investigation into Telecommunication Fraud Syndicate B",
            "subject_name": "Unknown Syndicate Alpha",
            "subject_known_identifiers": {"phone": ["+91-98111-00001"]},
            "description": "Parallel inquiry into SIM-box operation in Western Corridor.",
            "investigator": "Sub-Ins. Neha Gupta (#INV-4401)",
            "agency": "State Cyber Cell",
            "priority": "MEDIUM",
            "status": "ACTIVE",
            "start_date": "2026-07-01",
            "end_date": None,
            "tags": ["SIM_BOX", "TELECOM_FRAUD"]
        }
    }

    incident_dt = datetime(2026, 8, 28, 20, 7, 0)
    
    nodes = []
    nodes.append({"id": "person_rahul_sharma", "label": "Rahul Sharma", "type": "PERSON", "risk_score": 92, "confidence": 1.0, "details": "Primary Subject in Case TRACE-2026-017. Associated with multiple telecom and crypto identifiers.", "status": "Confirmed", "source_evidence_ids": ["EVD-DOC-001", "EVD-CDR-101", "EVD-BNK-201"]})
    nodes.append({"id": "person_vikram_singh", "label": "Vikram Singh", "type": "PERSON", "risk_score": 88, "confidence": 0.95, "details": "High network centrality hub. Key logistics and driver coordinator.", "status": "Confirmed", "source_evidence_ids": ["EVD-CDR-101", "EVD-DVR-501", "EVD-BNK-201"]})
    nodes.append({"id": "person_amit_patel", "label": "Amit Patel", "type": "PERSON", "risk_score": 81, "confidence": 0.92, "details": "Registered director of Apex Global Logistics. Facilitator of multi-hop transactions.", "status": "Confirmed", "source_evidence_ids": ["EVD-BNK-201", "EVD-BLK-301"]})
    nodes.append({"id": "person_priya_verma", "label": "Priya Verma", "type": "PERSON", "risk_score": 68, "confidence": 0.88, "details": "Accountant receiving repeated off-market UPI cash transfers.", "status": "Confirmed", "source_evidence_ids": ["EVD-BNK-202"]})
    nodes.append({"id": "person_r_sharma_ambiguous", "label": "R. Sharma (Unverified)", "type": "PERSON", "risk_score": 54, "confidence": 0.62, "details": "Identity Resolution Candidate: Name similarity with Rahul Sharma, shared cell tower location in Pune, but distinct phone operator.", "status": "Needs Review", "source_evidence_ids": ["EVD-DOC-004", "EVD-OSINT-402"]})

    first_names = ["Aarav", "Rohan", "Suresh", "Karan", "Ananya", "Deepak", "Manish", "Kavita", "Sanjay", "Rajesh", "Pooja", "Sunil", "Meera", "Alok", "Vivek", "Nitin", "Tarun", "Gaurav", "Preeti", "Ritu"]
    last_names = ["Kulkarni", "Deshmukh", "Joshi", "Mehta", "Shah", "Nair", "Iyer", "Yadav", "Chauhan", "Rao", "Gupta", "Agarwal", "Reddy", "Bhat", "Saxena"]
    
    for i in range(1, 46):
        fn = first_names[i % len(first_names)]
        ln = last_names[(i * 3) % len(last_names)]
        nodes.append({"id": f"person_synth_{i:03d}", "label": f"{fn} {ln}", "type": "PERSON", "risk_score": random.randint(15, 65), "confidence": round(random.uniform(0.75, 0.98), 2), "details": f"Synthetic background entity #{i} in urban communication directory.", "status": "Confirmed", "source_evidence_ids": [f"EVD-CDR-10{random.randint(1,4)}"]})

    nodes.append({"id": "phone_rahul_1", "label": "+91-98765-10001", "type": "PHONE", "risk_score": 90, "confidence": 1.0, "details": "Primary MSISDN assigned to Rahul Sharma", "status": "Confirmed", "source_evidence_ids": ["EVD-CDR-101"]})
    nodes.append({"id": "phone_vikram_1", "label": "+91-98765-20002", "type": "PHONE", "risk_score": 85, "confidence": 1.0, "details": "Primary MSISDN assigned to Vikram Singh", "status": "Confirmed", "source_evidence_ids": ["EVD-CDR-101"]})
    nodes.append({"id": "phone_amit_1", "label": "+91-98765-30003", "type": "PHONE", "risk_score": 75, "confidence": 0.95, "details": "Business phone for Apex Global Logistics", "status": "Confirmed", "source_evidence_ids": ["EVD-CDR-102"]})

    nodes.append({"id": "acc_apex_global", "label": "ACC-IND-994101 (Apex Global)", "type": "BANK_ACCOUNT", "risk_score": 86, "confidence": 1.0, "details": "HDFC Current Account used for rapid multi-hop fund routing", "status": "Confirmed", "source_evidence_ids": ["EVD-BNK-201"]})
    nodes.append({"id": "wallet_shadow", "label": "0x71a9b4fe82c19a...9b4", "type": "CRYPTO_WALLET", "risk_score": 94, "confidence": 0.98, "details": "Tether / Ethereum cold wallet referenced in OSINT threat intel", "status": "Confirmed", "source_evidence_ids": ["EVD-BLK-301", "EVD-OSINT-401"]})
    nodes.append({"id": "vehicle_mh12", "label": "MH12-AB-1234 (SUV)", "type": "VEHICLE", "risk_score": 82, "confidence": 0.96, "details": "Black Mahindra XUV700 registered under Vikram Singh", "status": "Confirmed", "source_evidence_ids": ["EVD-DVR-501"]})
    nodes.append({"id": "camera_c12", "label": "Cam C12 - MG Road Junction", "type": "CAMERA", "risk_score": 40, "confidence": 1.0, "details": "High-Definition ANPR & Face CCTV Camera at MG Road Corridor", "status": "Confirmed", "source_evidence_ids": ["EVD-DVR-501"]})
    nodes.append({"id": "incident_1042", "label": "Incident #1042 (Cyber Extortion Event)", "type": "INCIDENT", "risk_score": 100, "confidence": 1.0, "details": "Targeted Cyber Extortion & Ransom Drop Event on 2026-08-28 20:07 IST", "status": "Confirmed", "source_evidence_ids": ["EVD-DOC-001"]})
    nodes.append({"id": "org_apex", "label": "Apex Global Logistics Pvt Ltd", "type": "ORGANIZATION", "risk_score": 78, "confidence": 0.95, "details": "Logistics shell company used for layer 2 transaction masking", "status": "Confirmed", "source_evidence_ids": ["EVD-BNK-201"]})

    edges = []
    edges.append({"id": "rel_1", "source": "person_rahul_sharma", "target": "phone_rahul_1", "relation": "USES", "timestamp": "2026-08-01 10:00:00", "confidence": 0.99, "source_evidence_ids": ["EVD-CDR-101"], "details": "Subscriber registration & CDR verification", "domain": "COMMUNICATION"})
    edges.append({"id": "rel_2", "source": "person_vikram_singh", "target": "phone_vikram_1", "relation": "USES", "timestamp": "2026-08-01 10:00:00", "confidence": 0.99, "source_evidence_ids": ["EVD-CDR-101"], "details": "CDR subscriber record match", "domain": "COMMUNICATION"})
    edges.append({"id": "rel_3", "source": "phone_rahul_1", "target": "phone_vikram_1", "relation": "CALLED", "timestamp": "2026-08-28 19:25:00", "confidence": 0.98, "source_evidence_ids": ["EVD-CDR-101"], "details": "14 encrypted voice calls logged between 19:20 and 20:00 (Pre-Incident Burst)", "domain": "COMMUNICATION"})
    edges.append({"id": "rel_4", "source": "person_vikram_singh", "target": "vehicle_mh12", "relation": "OWNS", "timestamp": "2026-01-15 00:00:00", "confidence": 0.95, "source_evidence_ids": ["EVD-DVR-501"], "details": "RTO vehicle ownership database record", "domain": "PHYSICAL"})
    edges.append({"id": "rel_5", "source": "vehicle_mh12", "target": "camera_c12", "relation": "OBSERVED_AT", "timestamp": "2026-08-28 20:12:00", "confidence": 0.94, "source_evidence_ids": ["EVD-DVR-501"], "details": "ANPR Camera C12 capture of MH12-AB-1234 moving away from Incident site", "domain": "DVR"})
    edges.append({"id": "rel_6", "source": "incident_1042", "target": "camera_c12", "relation": "LOCATED_AT", "timestamp": "2026-08-28 20:07:00", "confidence": 1.0, "source_evidence_ids": ["EVD-DOC-001"], "details": "Incident spot location within 150m of Camera C12", "domain": "PHYSICAL"})
    edges.append({"id": "rel_7", "source": "person_vikram_singh", "target": "acc_apex_global", "relation": "TRANSFERRED", "timestamp": "2026-08-28 20:45:00", "confidence": 0.97, "source_evidence_ids": ["EVD-BNK-201"], "details": "IMPS Transfer of ₹25,00,000 flagged as Hawala/Rapid Cash Movement", "domain": "FINANCIAL"})
    edges.append({"id": "rel_8", "source": "person_amit_patel", "target": "org_apex", "relation": "WORKS_FOR", "timestamp": "2025-06-01 00:00:00", "confidence": 0.99, "source_evidence_ids": ["EVD-BNK-201"], "details": "Director status in MCA filing", "domain": "FINANCIAL"})
    edges.append({"id": "rel_9", "source": "acc_apex_global", "target": "wallet_shadow", "relation": "TRANSFERRED", "timestamp": "2026-08-28 21:15:00", "confidence": 0.92, "source_evidence_ids": ["EVD-BLK-301"], "details": "Layer 3 conversion into 8.5 ETH off-ramped to crypto wallet", "domain": "BLOCKCHAIN"})
    edges.append({"id": "rel_10", "source": "wallet_shadow", "target": "person_rahul_sharma", "relation": "ASSOCIATED_WITH", "timestamp": "2026-08-29 02:30:00", "confidence": 0.86, "source_evidence_ids": ["EVD-OSINT-401"], "details": "Darkweb paste bin post linking wallet 0x71a...9b4 to handle 'Cipher_King' (Rahul Sharma)", "domain": "OSINT"})

    for i in range(1, 40):
        src = f"person_synth_{i:03d}"
        tgt = f"person_synth_{(i+1)%45+1:03d}"
        edges.append({
            "id": "rel_synth_" + str(i),
            "source": src,
            "target": tgt,
            "relation": random.choice(["CALLED", "MESSAGED", "ASSOCIATED_WITH"]),
            "timestamp": (incident_dt - timedelta(days=random.randint(1, 10))).strftime("%Y-%m-%d %H:%M:%S"),
            "confidence": round(random.uniform(0.70, 0.90), 2),
            "source_evidence_ids": [f"EVD-CDR-10{random.randint(1,4)}"],
            "details": f"Routine telecom traffic record #{i}",
            "domain": "COMMUNICATION"
        })

    evidence_items = [
        {"id": "EVD-DOC-001", "case_id": "TRACE-2026-017", "title": "FIR #1042/2026 - Cyber Extortion & Ransom Call Report", "evidence_type": "DOCUMENT", "source": "Shivajinagar Police Station, Crime Branch", "acquisition_timestamp": "2026-08-28 21:00:00", "file_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "file_size_bytes": 452000, "integrity_status": "VERIFIED", "processing_status": "PROCESSED", "provenance": "Certified copy obtained via Lawful Interception Request #LIR-8821.", "analyst_notes": "Primary Incident filing detailing victim complaint and extortion demands."},
        {"id": "EVD-CDR-101", "case_id": "TRACE-2026-017", "title": "Call Detail Records (CDR) - Target MSISDN +91-98765-10001", "evidence_type": "CDR", "source": "Telecom Service Provider (TSP) Node 4", "acquisition_timestamp": "2026-08-29 01:15:00", "file_hash": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284ddd200126d9069e", "file_size_bytes": 1840000, "integrity_status": "VERIFIED", "processing_status": "PROCESSED", "provenance": "Cryptographically signed CSV export under Section 65B Indian Evidence Act.", "analyst_notes": "Reveals pre-incident call burst of 14 calls to +91-98765-20002."},
        {"id": "EVD-BNK-201", "case_id": "TRACE-2026-017", "title": "Financial Transaction Log - HDFC Current Acc #ACC-IND-994101", "evidence_type": "BANK", "source": "Financial Intelligence Unit (FIU) Gateway", "acquisition_timestamp": "2026-08-29 04:30:00", "file_hash": "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e", "file_size_bytes": 920000, "integrity_status": "VERIFIED", "processing_status": "PROCESSED", "provenance": "Authorized Section 91 CrPC Bank Statement Fetch.", "analyst_notes": "Shows ₹25L IMPS transfer followed by 3 rapid fan-out split transfers."},
        {"id": "EVD-BLK-301", "case_id": "TRACE-2026-017", "title": "On-Chain Ledger Capture - Wallet 0x71a9b4fe82c19a...9b4", "evidence_type": "BLOCKCHAIN", "source": "Etherscan Node Forensics API", "acquisition_timestamp": "2026-08-29 06:00:00", "file_hash": "2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae", "file_size_bytes": 310000, "integrity_status": "VERIFIED", "processing_status": "PROCESSED", "provenance": "Public blockchain node RPC pull with SHA-256 block proof.", "analyst_notes": "Traces 8.5 ETH receipt from DEX pool."},
        {"id": "EVD-OSINT-401", "case_id": "TRACE-2026-017", "title": "Public Web Threat Intelligence Harvest #OS-88", "evidence_type": "OSINT", "source": "Authorized Open Source Intelligence Crawler", "acquisition_timestamp": "2026-08-29 08:20:00", "file_hash": "fcde2b2edba56bf408601fb721fe9b5c338d10ee429ea04fae5511b68fbf8fb9", "file_size_bytes": 120000, "integrity_status": "VERIFIED", "processing_status": "PROCESSED", "provenance": "Archived snapshot with Wayback Machine cryptographic header.", "analyst_notes": "Links wallet 0x71a...9b4 to handle Cipher_King."},
        {"id": "EVD-DVR-501", "case_id": "TRACE-2026-017", "title": "NVR Forensic Video Frame Extraction - Cam C12 (MG Road)", "evidence_type": "DVR_NVR", "source": "City Surveillance Command & Control Center", "acquisition_timestamp": "2026-08-29 09:45:00", "file_hash": "d41d8cd98f00b204e9800998ecf8427e56b3e66487e44a49c6d3ff3cf81734f2", "file_size_bytes": 45000000, "integrity_status": "VERIFIED", "processing_status": "PROCESSED", "provenance": "Seized NVR hard drive #NVR-702 frame hash carving.", "analyst_notes": "ALPR match for vehicle MH12-AB-1234 at 20:12:00."}
    ]

    anomalies = [
        {"id": "ANM-001", "category": "Communication Burst", "title": "Unusual Pre-Incident Communication Burst Detected", "severity": "HIGH", "timestamp": "2026-08-28 19:45:00", "affected_entity_ids": ["person_rahul_sharma", "person_vikram_singh"], "explanation": "Communication frequency between +91-98765-10001 (Rahul Sharma) and +91-98765-20002 (Vikram Singh) increased by 420% during the 45 minutes preceding Incident #1042.", "evidence_ids": ["EVD-CDR-101", "EVD-DOC-001"], "confidence": 0.94, "analyst_status": "Requires Review"},
        {"id": "ANM-002", "category": "Financial / Informal Transfer", "title": "Rapid Multi-Hop Fund Transfer & Hawala Risk Indicator", "severity": "HIGH", "timestamp": "2026-08-28 20:45:00", "affected_entity_ids": ["person_vikram_singh", "acc_apex_global", "person_amit_patel"], "explanation": "Anomalous fund velocity: ₹25,00,000 deposited into HDFC Acc #ACC-IND-994101 was split into 3 accounts within 18 minutes without typical commercial invoice trail.", "evidence_ids": ["EVD-BNK-201"], "confidence": 0.89, "analyst_status": "Requires Review"},
        {"id": "ANM-003", "category": "Temporal Correlation", "title": "Cross-Domain Temporal Convergence around Incident #1042", "severity": "HIGH", "timestamp": "2026-08-28 20:12:00", "affected_entity_ids": ["vehicle_mh12", "camera_c12", "incident_1042"], "explanation": "Vehicle MH12-AB-1234 passed CCTV Cam C12 exactly 5 minutes after Incident #1042 was reported 150 meters away.", "evidence_ids": ["EVD-DVR-501", "EVD-DOC-001"], "confidence": 0.92, "analyst_status": "Requires Review"}
    ]

    leads = [
        {
            "id": "LEAD-2026-01",
            "title": "Multi-Domain Evidence Chain Linking Rahul Sharma to Incident #1042",
            "summary": "AI Evidence Fusion engine correlated CDR communication spikes, vehicle ANPR sightings, rapid bank transfers, and crypto off-ramping into a unified 6-hop evidence chain.",
            "confidence": 0.93,
            "evidence_chain": [
                {"step": 1, "domain": "CDR", "description": "Rahul Sharma (+91-98765-10001) calls Vikram Singh (+91-98765-20002) 14 times before Incident #1042.", "evidence_id": "EVD-CDR-101"},
                {"step": 2, "domain": "DVR", "description": "Vehicle MH12-AB-1234 (registered to Vikram Singh) detected at Cam C12 5 mins post-incident.", "evidence_id": "EVD-DVR-501"},
                {"step": 3, "domain": "FINANCIAL", "description": "Vikram Singh initiates ₹25L transfer to Apex Global Logistics (managed by Amit Patel).", "evidence_id": "EVD-BNK-201"},
                {"step": 4, "domain": "BLOCKCHAIN", "description": "Apex Global account converts ₹25L to 8.5 ETH sent to Crypto Wallet 0x71a...9b4.", "evidence_id": "EVD-BLK-301"},
                {"step": 5, "domain": "OSINT", "description": "Wallet 0x71a...9b4 linked to handle 'Cipher_King' / Rahul Sharma in OSINT threat paste.", "evidence_id": "EVD-OSINT-401"}
            ],
            "recommended_actions": [
                "Issue legal notice under Sec 91 CrPC for raw tower dump at MG Road Junction.",
                "Inspect original TSP signed CDR logs for IMEI device correlation.",
                "Verify beneficiary KYCs of Apex Global Logistics bank accounts.",
                "Perform manual forensic verification of Cam C12 raw video stream hash.",
                "Re-evaluate ambiguous entity candidate R. Sharma (+91-98765-99999) for alias confirmation."
            ],
            "human_review_required": True
        }
    ]

    return {
        "cases": cases_db,
        "nodes": nodes,
        "edges": edges,
        "evidence_items": evidence_items,
        "anomalies": anomalies,
        "leads": leads
    }
