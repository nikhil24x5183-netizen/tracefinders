import random
from datetime import datetime, timedelta
from typing import Dict, List, Any

random.seed(2026189)

def generate_synthetic_dataset() -> Dict[str, Any]:
    case_primary = {
        "id": "TRACE-2026-017",
        "title": "Operation Cipher Net - Cyber-Financial Syndicate Investigation",
        "subject_name": "Rahul Sharma",
        "primary_suspect": {
            "name": "Rahul Sharma",
            "role": "Primary Suspect / Syndicate Lead",
            "avatar_url": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=300&auto=format&fit=crop&q=80",
            "phone": "+91-98765-10001",
            "email": "rahul.sharma89@protonmail.com",
            "social_profiles": {
                "telegram": "@cipher_king",
                "twitter": "@r_sharma89",
                "instagram": "@rahul_cyber_99",
                "darkweb": "shadow_broker99"
            },
            "known_vehicles": ["MH-12-RS-9988"],
            "crypto_wallets": ["0x71a9b4fe82c19a...9b4"]
        },
        "secondary_suspects": [
            {
                "name": "Vikram Singh",
                "role": "Secondary Suspect / Driver & Field Logistics",
                "avatar_url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=300&auto=format&fit=crop&q=80",
                "phone": "+91-98765-20002",
                "email": "vikram.logistics@gmail.com",
                "social_profiles": {
                    "telegram": "@vikram_runner",
                    "instagram": "@v_singh_wheels"
                },
                "known_vehicles": ["MH12-AB-1234"],
                "crypto_wallets": []
            },
            {
                "name": "Amit Patel",
                "role": "Secondary Suspect / Hawala & Shell Corp Director",
                "avatar_url": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=300&auto=format&fit=crop&q=80",
                "phone": "+91-98765-30003",
                "email": "patel.amit@apexglobal.in",
                "social_profiles": {
                    "linkedin": "in/amit-patel-apex",
                    "darkweb": "fiat_mixer_07"
                },
                "known_vehicles": ["MH-14-XY-1001"],
                "crypto_wallets": ["0x3910ab12f0090884210419280011a0029b920199"]
            }
        ],
        "subject_known_identifiers": {
            "phone": ["+91-98765-10001", "+91-98765-10099"],
            "email": ["rahul.sharma89@protonmail.com", "r_sharma_cyber@gmail.com"],
            "aliases": ["Rahul S.", "r_sharma_1989", "Cipher_King", "shadow_broker99"],
            "vehicle": ["MH-12-RS-9988", "MH12-AB-1234"],
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
            "primary_suspect": {
                "name": "Syndicate Alpha Lead",
                "role": "Primary Suspect",
                "avatar_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=300&auto=format&fit=crop&q=80",
                "phone": "+91-98111-00001",
                "email": "alpha.boss@securesim.org",
                "social_profiles": {"telegram": "@alpha_telecom"},
                "known_vehicles": [],
                "crypto_wallets": []
            },
            "secondary_suspects": [],
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
    # Primary & Secondary Suspect Nodes with Indian face avatars
    nodes.append({"id": "person_rahul_sharma", "label": "Rahul Sharma", "type": "PERSON", "risk_score": 92, "confidence": 1.0, "details": "Primary Suspect / Syndicate Lead. Associated with Telegram @cipher_king.", "status": "Confirmed", "source_evidence_ids": ["EVD-DOC-001", "EVD-CDR-101", "EVD-BNK-201"], "tree_level": 0, "avatar": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=150"})
    nodes.append({"id": "person_vikram_singh", "label": "Vikram Singh", "type": "PERSON", "risk_score": 88, "confidence": 0.95, "details": "Secondary Suspect / Driver & Field Logistics. Driver of SUV MH12-AB-1234.", "status": "Confirmed", "source_evidence_ids": ["EVD-CDR-101", "EVD-DVR-501", "EVD-BNK-201"], "tree_level": 1, "avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150"})
    nodes.append({"id": "person_amit_patel", "label": "Amit Patel", "type": "PERSON", "risk_score": 81, "confidence": 0.92, "details": "Secondary Suspect / Hawala & Shell Director of Apex Global Logistics.", "status": "Confirmed", "source_evidence_ids": ["EVD-BNK-201", "EVD-BLK-301"], "tree_level": 1, "avatar": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150"})
    nodes.append({"id": "person_priya_verma", "label": "Priya Verma", "type": "PERSON", "risk_score": 68, "confidence": 0.88, "details": "Accountant receiving off-market UPI cash transfers.", "status": "Confirmed", "source_evidence_ids": ["EVD-BNK-202"], "tree_level": 2, "avatar": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=150"})

    first_names = ["Aarav", "Rohan", "Suresh", "Karan", "Ananya", "Deepak", "Manish", "Kavita", "Sanjay", "Rajesh"]
    last_names = ["Kulkarni", "Deshmukh", "Joshi", "Mehta", "Shah", "Nair", "Iyer", "Yadav", "Chauhan", "Rao"]
    
    for i in range(1, 20):
        fn = first_names[i % len(first_names)]
        ln = last_names[(i * 3) % len(last_names)]
        nodes.append({"id": f"person_synth_{i:03d}", "label": f"{fn} {ln}", "type": "PERSON", "risk_score": random.randint(15, 65), "confidence": round(random.uniform(0.75, 0.98), 2), "details": f"Background entity #{i} in urban communication network.", "status": "Confirmed", "source_evidence_ids": [f"EVD-CDR-10{random.randint(1,4)}"], "tree_level": 3})

    nodes.append({"id": "phone_rahul_1", "label": "+91-98765-10001", "type": "PHONE", "risk_score": 90, "confidence": 1.0, "details": "Primary MSISDN assigned to Rahul Sharma", "status": "Confirmed", "source_evidence_ids": ["EVD-CDR-101"], "tree_level": 1})
    nodes.append({"id": "phone_vikram_1", "label": "+91-98765-20002", "type": "PHONE", "risk_score": 85, "confidence": 1.0, "details": "Primary MSISDN assigned to Vikram Singh", "status": "Confirmed", "source_evidence_ids": ["EVD-CDR-101"], "tree_level": 2})
    nodes.append({"id": "phone_amit_1", "label": "+91-98765-30003", "type": "PHONE", "risk_score": 75, "confidence": 0.95, "details": "Business phone for Apex Global Logistics", "status": "Confirmed", "source_evidence_ids": ["EVD-CDR-102"], "tree_level": 2})

    nodes.append({"id": "acc_apex_global", "label": "ACC-IND-994101", "type": "BANK_ACCOUNT", "risk_score": 86, "confidence": 1.0, "details": "Current Account used for multi-hop fund routing", "status": "Confirmed", "source_evidence_ids": ["EVD-BNK-201"], "tree_level": 2})
    nodes.append({"id": "wallet_shadow", "label": "0x71a9b4...9b4", "type": "CRYPTO_WALLET", "risk_score": 94, "confidence": 0.98, "details": "Cold wallet referenced in OSINT threat intel", "status": "Confirmed", "source_evidence_ids": ["EVD-BLK-301", "EVD-OSINT-401"], "tree_level": 3})
    nodes.append({"id": "vehicle_mh12", "label": "MH12-AB-1234", "type": "VEHICLE", "risk_score": 82, "confidence": 0.96, "details": "Black SUV registered under Vikram Singh", "status": "Confirmed", "source_evidence_ids": ["EVD-DVR-501"], "tree_level": 2})
    nodes.append({"id": "camera_c12", "label": "Cam C12 - MG Road", "type": "CAMERA", "risk_score": 40, "confidence": 1.0, "details": "CCTV ANPR Camera at MG Road Corridor", "status": "Confirmed", "source_evidence_ids": ["EVD-DVR-501"], "tree_level": 3})

    edges = []
    edges.append({"id": "rel_1", "source": "person_rahul_sharma", "target": "person_vikram_singh", "relation": "COMMANDS", "timestamp": "2026-08-01 10:00:00", "confidence": 0.98, "source_evidence_ids": ["EVD-CDR-101"], "details": "Rahul Sharma directs field logistics of Vikram Singh", "domain": "COMMUNICATION"})
    edges.append({"id": "rel_2", "source": "person_rahul_sharma", "target": "person_amit_patel", "relation": "FINANCIALLY_DIRECTS", "timestamp": "2026-08-01 10:00:00", "confidence": 0.95, "source_evidence_ids": ["EVD-BNK-201"], "details": "Rahul Sharma controls shell director Amit Patel", "domain": "FINANCIAL"})
    edges.append({"id": "rel_3", "source": "person_rahul_sharma", "target": "phone_rahul_1", "relation": "USES", "timestamp": "2026-08-01 10:00:00", "confidence": 0.99, "source_evidence_ids": ["EVD-CDR-101"], "details": "Subscriber registration & CDR verification", "domain": "COMMUNICATION"})
    edges.append({"id": "rel_4", "source": "person_vikram_singh", "target": "phone_vikram_1", "relation": "USES", "timestamp": "2026-08-01 10:00:00", "confidence": 0.99, "source_evidence_ids": ["EVD-CDR-101"], "details": "CDR subscriber record match", "domain": "COMMUNICATION"})
    edges.append({"id": "rel_5", "source": "phone_rahul_1", "target": "phone_vikram_1", "relation": "CALLED", "timestamp": "2026-08-28 19:25:00", "confidence": 0.98, "source_evidence_ids": ["EVD-CDR-101"], "details": "14 encrypted voice calls logged between 19:20 and 20:00 (Pre-Incident Burst)", "domain": "COMMUNICATION"})
    edges.append({"id": "rel_6", "source": "person_vikram_singh", "target": "vehicle_mh12", "relation": "OWNS", "timestamp": "2026-01-15 00:00:00", "confidence": 0.95, "source_evidence_ids": ["EVD-DVR-501"], "details": "RTO vehicle registration match", "domain": "PHYSICAL"})
    edges.append({"id": "rel_7", "source": "vehicle_mh12", "target": "camera_c12", "relation": "OBSERVED_AT", "timestamp": "2026-08-28 20:12:00", "confidence": 0.94, "source_evidence_ids": ["EVD-DVR-501"], "details": "ANPR Camera C12 capture of MH12-AB-1234 moving away from spot", "domain": "DVR"})
    edges.append({"id": "rel_9", "source": "person_vikram_singh", "target": "acc_apex_global", "relation": "TRANSFERRED", "timestamp": "2026-08-28 20:45:00", "confidence": 0.97, "source_evidence_ids": ["EVD-BNK-201"], "details": "IMPS Transfer of ₹25,00,000 flagged as Hawala Cash Movement", "domain": "FINANCIAL"})
    edges.append({"id": "rel_11", "source": "acc_apex_global", "target": "wallet_shadow", "relation": "TRANSFERRED", "timestamp": "2026-08-28 21:15:00", "confidence": 0.92, "source_evidence_ids": ["EVD-BLK-301"], "details": "8.5 ETH off-ramped to crypto wallet", "domain": "BLOCKCHAIN"})
    edges.append({"id": "rel_12", "source": "wallet_shadow", "target": "person_rahul_sharma", "relation": "ASSOCIATED_WITH", "timestamp": "2026-08-29 02:30:00", "confidence": 0.86, "source_evidence_ids": ["EVD-OSINT-401"], "details": "Darkweb paste linking wallet 0x71a...9b4 to Cipher_King (Rahul Sharma)", "domain": "OSINT"})

    for i in range(1, 15):
        src = f"person_synth_{i:03d}"
        tgt = f"person_synth_{(i+1)%18+1:03d}"
        edges.append({
            "id": "rel_synth_" + str(i),
            "source": src,
            "target": tgt,
            "relation": random.choice(["CALLED", "ASSOCIATED_WITH"]),
            "timestamp": (incident_dt - timedelta(days=random.randint(1, 5))).strftime("%Y-%m-%d %H:%M:%S"),
            "confidence": round(random.uniform(0.75, 0.90), 2),
            "source_evidence_ids": [f"EVD-CDR-10{random.randint(1,4)}"],
            "details": f"Routine communication traffic #{i}",
            "domain": "COMMUNICATION"
        })

    evidence_items = [
        {"id": "EVD-DOC-001", "case_id": "TRACE-2026-017", "person_id": "person_rahul_sharma", "title": "FIR #1042/2026 - Cyber Extortion Report", "evidence_type": "DOCUMENT", "source": "Shivajinagar Police Station", "acquisition_timestamp": "2026-08-28 21:00:00", "file_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "file_size_bytes": 452000, "integrity_status": "VERIFIED", "processing_status": "PROCESSED", "provenance": "Certified copy obtained via Sec 91 CrPC.", "analyst_notes": "Primary Incident report detailing extortion complaint against Rahul Sharma."},
        {"id": "EVD-CDR-101", "case_id": "TRACE-2026-017", "person_id": "person_rahul_sharma", "title": "CDR Log - Target MSISDN +91-98765-10001", "evidence_type": "CDR", "source": "Telecom Node 4", "acquisition_timestamp": "2026-08-29 01:15:00", "file_hash": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284ddd200126d9069e", "file_size_bytes": 1840000, "integrity_status": "VERIFIED", "processing_status": "PROCESSED", "provenance": "Cryptographically signed export under Sec 65B.", "analyst_notes": "14 encrypted pre-incident calls between Rahul Sharma & Vikram Singh."},
        {"id": "EVD-BNK-201", "case_id": "TRACE-2026-017", "person_id": "person_vikram_singh", "title": "Financial Transaction Log - HDFC Acc #ACC-IND-994101", "evidence_type": "BANK", "source": "FIU Gateway", "acquisition_timestamp": "2026-08-29 04:30:00", "file_hash": "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e", "file_size_bytes": 920000, "integrity_status": "VERIFIED", "processing_status": "PROCESSED", "provenance": "Authorized FIU Statement pull.", "analyst_notes": "₹25L IMPS cash transfer initiated by Vikram Singh to Amit Patel's account."},
        {"id": "EVD-BLK-301", "case_id": "TRACE-2026-017", "person_id": "person_amit_patel", "title": "On-Chain Blockchain Ledger - Wallet 0x71a...9b4", "evidence_type": "BLOCKCHAIN", "source": "Etherscan Node API", "acquisition_timestamp": "2026-08-29 06:00:00", "file_hash": "2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae", "file_size_bytes": 310000, "integrity_status": "VERIFIED", "processing_status": "PROCESSED", "provenance": "Public blockchain RPC pull.", "analyst_notes": "Traces 8.5 ETH off-ramped by Amit Patel to cold wallet."},
        {"id": "EVD-OSINT-401", "case_id": "TRACE-2026-017", "person_id": "person_rahul_sharma", "title": "Public Web Threat Intel - Darkweb Harvest", "evidence_type": "OSINT", "source": "OSINT Intelligence Crawler", "acquisition_timestamp": "2026-08-29 08:20:00", "file_hash": "fcde2b2edba56bf408601fb721fe9b5c338d10ee429ea04fae5511b68fbf8fb9", "file_size_bytes": 120000, "integrity_status": "VERIFIED", "processing_status": "PROCESSED", "provenance": "Archived snapshot with cryptographic timestamp.", "analyst_notes": "Links wallet 0x71a...9b4 to handle Cipher_King (Rahul Sharma)."},
        {"id": "EVD-DVR-501", "case_id": "TRACE-2026-017", "person_id": "person_vikram_singh", "title": "CCTV Surveillance Stream - Cam C12 (MG Road)", "evidence_type": "DVR_NVR", "source": "City Surveillance Command", "acquisition_timestamp": "2026-08-29 09:45:00", "file_hash": "d41d8cd98f00b204e9800998ecf8427e56b3e66487e44a49c6d3ff3cf81734f2", "file_size_bytes": 45000000, "integrity_status": "VERIFIED", "processing_status": "PROCESSED", "provenance": "Seized NVR hard drive #NVR-702 carving.", "analyst_notes": "ANPR match for Vikram Singh's vehicle MH12-AB-1234."}
    ]

    # 3 REALISTIC CCTV SURVEILLANCE VIDEOS WITH INDIAN LOCATIONS & SUSPECTS
    dvr_videos = [
        {
            "id": "DVR-VID-01",
            "camera_id": "Cam C12 - MG Road",
            "location": "MG Road Junction - Coffee Shop Exterior, Pune",
            "timestamp": "2026-08-28 20:01:15 IST",
            "event_title": "Pre-Incident Meeting (Rahul Sharma & Vikram Singh)",
            "suspects_identified": ["Rahul Sharma (Primary)", "Vikram Singh (Secondary)"],
            "anpr_license_plate": "MH12-RS-9988",
            "confidence_score": "96.4%",
            "video_thumbnail": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800&auto=format&fit=crop&q=80",
            "description": "High-Definition ANPR and facial recognition carving captured Primary Suspect Rahul Sharma meeting Secondary Suspect Vikram Singh outside Caffeine Coffee Shop 6 minutes before Incident #1042."
        },
        {
            "id": "DVR-VID-02",
            "camera_id": "Cam C14 - Commercial Parking",
            "location": "Commercial Complex Parking Bay 4, Pune",
            "timestamp": "2026-08-28 20:12:40 IST",
            "event_title": "Money Laundering & Cash Handover (Vikram Singh & Amit Patel)",
            "suspects_identified": ["Vikram Singh (Secondary)", "Amit Patel (Shell Director)"],
            "anpr_license_plate": "MH12-AB-1234",
            "confidence_score": "94.8%",
            "video_thumbnail": "https://images.unsplash.com/photo-1573164713988-8665fc963095?w=800&auto=format&fit=crop&q=80",
            "description": "CCTV NVR frame carving captured SUV MH12-AB-1234 stopping near Parking Bay 4. Secondary Suspect Vikram Singh handed over black duffel bag (₹25L cash equivalent) to Shell Director Amit Patel."
        },
        {
            "id": "DVR-VID-03",
            "camera_id": "Cam C18 - Expressway Toll",
            "location": "Pune-Mumbai Expressway Toll Plaza Gate 3",
            "timestamp": "2026-08-28 20:45:10 IST",
            "event_title": "Vehicle Getaway & ANPR Match (SUV MH12-AB-1234)",
            "suspects_identified": ["Vikram Singh (Driver)", "SUV MH12-AB-1234"],
            "anpr_license_plate": "MH12-AB-1234",
            "confidence_score": "98.2%",
            "video_thumbnail": "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&auto=format&fit=crop&q=80",
            "description": "Automated ANPR camera captured vehicle MH12-AB-1234 passing toll plaza gate 3 at high velocity 38 minutes post-incident."
        }
    ]

    anomalies = [
        {"id": "ANM-001", "category": "Communication Burst", "title": "Unusual Pre-Incident Communication Burst", "severity": "HIGH", "timestamp": "2026-08-28 19:45:00", "affected_entity_ids": ["person_rahul_sharma", "person_vikram_singh"], "explanation": "Call frequency between Rahul Sharma and Vikram Singh spiked 420% prior to Incident #1042.", "evidence_ids": ["EVD-CDR-101"], "confidence": 0.94, "analyst_status": "Requires Review"},
        {"id": "ANM-002", "category": "Financial Transfer", "title": "Rapid Cash Movement / Hawala Indicator", "severity": "HIGH", "timestamp": "2026-08-28 20:45:00", "affected_entity_ids": ["person_vikram_singh", "acc_apex_global", "person_amit_patel"], "explanation": "₹25,00,000 cash transfer split into 3 shell accounts in 18 minutes without commercial invoices.", "evidence_ids": ["EVD-BNK-201"], "confidence": 0.89, "analyst_status": "Requires Review"},
        {"id": "ANM-003", "category": "Temporal Sighting", "title": "CCTV ANPR Temporal Sighting near Incident Spot", "severity": "HIGH", "timestamp": "2026-08-28 20:12:00", "affected_entity_ids": ["vehicle_mh12", "camera_c12"], "explanation": "SUV MH12-AB-1234 passed CCTV Cam C12 5 minutes after Incident #1042 reported 150m away.", "evidence_ids": ["EVD-DVR-501"], "confidence": 0.92, "analyst_status": "Requires Review"}
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
