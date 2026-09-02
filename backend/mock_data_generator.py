import random
from typing import Dict, List, Any

random.seed(2026189)

def generate_synthetic_dataset() -> Dict[str, Any]:
    # 1. FIVE DISTINCT PRIMARY PERSON PROFILES + 1 AMBIGUOUS CANDIDATE (REQUIREMENT 1 & 3)
    profiles = {
        "P-001": {
            "id": "P-001",
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
            "city": "Pune",
            "occupation": "Logistics Consultant",
            "organization": "Nexus Logistics",
            "vehicle": "MH12 AB 4821",
            "social_usernames": {"twitter": "@arjun_s_demo", "telegram": "@cipher_king"},
            "wallet_address": "0xDEMO...A721",
            "account_number": "XXXX4821",
            "notes": "Primary subject under investigation for Operation Nexus.",
            "risk_score": 92,
            "evidence_count": 24,
            "relationship_count": 7,
            "status": "Under Investigation",
            "last_updated": "18 Aug 2026 21:17",
            "counts": {"total_events": 421, "calls": 187, "messages": 234, "contacts": 11, "financial": 63, "osint": 42, "blockchain": 18, "cctv": 9}
        },
        "P-002": {
            "id": "P-002",
            "name": "Rohan Mehta",
            "alias": "Rohan M.",
            "role": "Business Contact",
            "relationship_to_primary": "Business Contact",
            "age": 38,
            "gender": "Male",
            "photo_url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=300&auto=format&fit=crop&q=80",
            "phone": "+91 97765 4826",
            "email": "rohan.mehta.demo@example.test",
            "address": "Andheri West, Mumbai",
            "city": "Mumbai",
            "occupation": "Import & Distribution Consultant",
            "organization": "Mehta Global Imports",
            "vehicle": "MH01 CR 7814",
            "social_usernames": {"twitter": "@rohan_m_demo", "telegram": "@rohan_import"},
            "wallet_address": "0xDEMO...B492",
            "account_number": "XXXX7312",
            "notes": "Key commercial importer linked to cross-city invoice settlements.",
            "risk_score": 85,
            "evidence_count": 18,
            "relationship_count": 5,
            "status": "Under Investigation",
            "last_updated": "18 Aug 2026 20:58",
            "counts": {"total_events": 167, "calls": 96, "messages": 71, "contacts": 8, "financial": 31, "osint": 17, "blockchain": 11, "cctv": 4}
        },
        "P-003": {
            "id": "P-003",
            "name": "Priya Joshi",
            "alias": "Priya J.",
            "role": "Associate",
            "relationship_to_primary": "Associate",
            "age": 31,
            "gender": "Female",
            "photo_url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=300&auto=format&fit=crop&q=80",
            "phone": "+91 96765 7315",
            "email": "priya.joshi.demo@example.test",
            "address": "Baner Road, Pune",
            "city": "Pune",
            "occupation": "Accounts Executive",
            "organization": "Nexus Financial Advisory",
            "vehicle": "MH12 DK 2093",
            "social_usernames": {"linkedin": "in/priya-j-demo", "twitter": "@priya_j_demo"},
            "wallet_address": "0xDEMO...C381",
            "account_number": "XXXX6154",
            "notes": "Managed corporate accounts and audit statement reconciliation.",
            "risk_score": 78,
            "evidence_count": 14,
            "relationship_count": 4,
            "status": "Associate",
            "last_updated": "18 Aug 2026 15:20",
            "counts": {"total_events": 193, "calls": 74, "messages": 119, "contacts": 9, "financial": 18, "osint": 23, "blockchain": 4, "cctv": 3}
        },
        "P-004": {
            "id": "P-004",
            "name": "Vikram Patil",
            "alias": "Vicky",
            "role": "Person of Interest",
            "relationship_to_primary": "Person of Interest",
            "age": 41,
            "gender": "Male",
            "photo_url": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=300&auto=format&fit=crop&q=80",
            "phone": "+91 95765 6148",
            "email": "vikram.patil.demo@example.test",
            "address": "Gangapur Road, Nashik",
            "city": "Nashik",
            "occupation": "Transport Contractor",
            "organization": "Patil Heavy Freight",
            "vehicle": "MH15 TG 4428",
            "social_usernames": {"telegram": "@vikram_p_demo"},
            "wallet_address": "0xDEMO...D527",
            "account_number": "XXXX9087",
            "notes": "Monitored for vehicle fleet movements along the Western Corridor.",
            "risk_score": 72,
            "evidence_count": 11,
            "relationship_count": 3,
            "status": "Person of Interest",
            "last_updated": "18 Aug 2026 20:26",
            "counts": {"total_events": 101, "calls": 58, "messages": 43, "contacts": 6, "financial": 27, "osint": 12, "blockchain": 8, "cctv": 5}
        },
        "P-005": {
            "id": "P-005",
            "name": "Neha Kulkarni",
            "alias": "NK",
            "role": "Employee",
            "relationship_to_primary": "Employee",
            "age": 29,
            "gender": "Female",
            "photo_url": "https://images.unsplash.com/photo-1580489944761-15a19d654956?w=300&auto=format&fit=crop&q=80",
            "phone": "+91 94765 3852",
            "email": "neha.kulkarni.demo@example.test",
            "address": "Viman Nagar, Pune",
            "city": "Pune",
            "occupation": "Operations Coordinator",
            "organization": "TechDesk Systems",
            "vehicle": "MH12 EQ 9136",
            "social_usernames": {"twitter": "@neha_k_demo"},
            "wallet_address": "0xDEMO...E614",
            "account_number": "XXXX3246",
            "notes": "Coordinated office dispatch and VPN network gateway routing.",
            "risk_score": 58,
            "evidence_count": 8,
            "relationship_count": 2,
            "status": "Employee",
            "last_updated": "18 Aug 2026 11:00",
            "counts": {"total_events": 130, "calls": 42, "messages": 88, "contacts": 7, "financial": 11, "osint": 19, "blockchain": 2, "cctv": 2}
        },
        "P-006": {
            "id": "P-006",
            "name": "Arjun S.",
            "alias": "Arjun S (Unresolved)",
            "role": "Ambiguous Match Candidate",
            "relationship_to_primary": "Candidate Match",
            "age": 35,
            "gender": "Male",
            "photo_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&auto=format&fit=crop&q=80",
            "phone": "+91 98765 9999",
            "email": "arjun.s.ambiguous@example.test",
            "address": "Camp Area, Pune",
            "city": "Pune",
            "occupation": "Commodity Trader",
            "organization": "Unregistered Trading Firm",
            "vehicle": "MH12 AB 9999",
            "social_usernames": {"twitter": "@arjun_s_trader"},
            "wallet_address": "0xDEMO...F000",
            "account_number": "XXXX9999",
            "notes": "POTENTIAL MATCH (Confidence 43%). Signals: Name similarity, Location overlap. Status: Unresolved Candidate.",
            "risk_score": 43,
            "evidence_count": 2,
            "relationship_count": 1,
            "status": "Unresolved Candidate",
            "last_updated": "18 Aug 2026 09:00",
            "counts": {"total_events": 12, "calls": 5, "messages": 7, "contacts": 2, "financial": 3, "osint": 4, "blockchain": 1, "cctv": 0}
        }
    }

    # 2. PERSON-SCOPED COMMUNICATIONS (REQUIREMENT 6 & 7)
    communications = {
        "P-001": {
            "total_events": 421, "calls": 187, "messages": 234, "unique_contacts": 11, "active_period": "03 Aug – 18 Aug 2026",
            "contacts": [
                {"id": "P-002", "name": "Rohan Mehta", "role": "Business Contact", "calls": 27, "phone": "+91 97765 4826"},
                {"id": "P-003", "name": "Priya Joshi", "role": "Associate", "calls": 14, "phone": "+91 96765 7315"},
                {"id": "P-004", "name": "Vikram Patil", "role": "Person of Interest", "calls": 9, "phone": "+91 95765 6148"},
                {"id": "P-005", "name": "Neha Kulkarni", "role": "Employee", "calls": 6, "phone": "+91 94765 3852"},
                {"id": "EXT-01", "name": "UNKNOWN CONTACT", "role": "External", "calls": 4, "phone": "+91 98999 0000"}
            ],
            "history": [
                {"date": "18 Aug 2026", "time": "20:02:14", "direction": "Outgoing", "duration": "04:21", "evidence_id": "EV-COM-ARJ-001", "contact": "Rohan Mehta"},
                {"date": "18 Aug 2026", "time": "20:11:23", "direction": "Incoming", "duration": "02:44", "evidence_id": "EV-COM-ARJ-001", "contact": "Rohan Mehta"},
                {"date": "18 Aug 2026", "time": "20:19:04", "direction": "Outgoing", "duration": "06:12", "evidence_id": "EV-COM-ARJ-001", "contact": "Rohan Mehta"},
                {"date": "17 Aug 2026", "time": "15:10:00", "direction": "Outgoing", "duration": "03:15", "evidence_id": "EV-COM-ARJ-002", "contact": "Priya Joshi"}
            ]
        },
        "P-002": {
            "total_events": 167, "calls": 96, "messages": 71, "unique_contacts": 8, "active_period": "01 Aug – 18 Aug 2026",
            "contacts": [
                {"id": "P-001", "name": "Arjun Sharma", "role": "Primary Subject", "calls": 27, "phone": "+91 98765 1201"},
                {"id": "P-003", "name": "Priya Joshi", "role": "Associate", "calls": 11, "phone": "+91 96765 7315"},
                {"id": "EXT-02", "name": "Mumbai Port Forwarder", "role": "Commercial Contact", "calls": 18, "phone": "+91 97111 2233"}
            ],
            "history": [
                {"date": "18 Aug 2026", "time": "20:02:14", "direction": "Incoming", "duration": "04:21", "evidence_id": "EV-COM-ROH-001", "contact": "Arjun Sharma"},
                {"date": "18 Aug 2026", "time": "20:11:23", "direction": "Outgoing", "duration": "02:44", "evidence_id": "EV-COM-ROH-001", "contact": "Arjun Sharma"},
                {"date": "18 Aug 2026", "time": "17:40:10", "direction": "Outgoing", "duration": "05:08", "evidence_id": "EV-COM-ROH-002", "contact": "Mumbai Port Forwarder"}
            ]
        },
        "P-003": {
            "total_events": 193, "calls": 74, "messages": 119, "unique_contacts": 9, "active_period": "05 Aug – 18 Aug 2026",
            "contacts": [
                {"id": "P-001", "name": "Arjun Sharma", "role": "Primary Subject", "calls": 14, "phone": "+91 98765 1201"},
                {"id": "P-002", "name": "Rohan Mehta", "role": "Business Contact", "calls": 11, "phone": "+91 97765 4826"},
                {"id": "EXT-03", "name": "Audit Firm Desk", "role": "Office Contact", "calls": 15, "phone": "+91 96222 3344"}
            ],
            "history": [
                {"date": "18 Aug 2026", "time": "15:20:00", "direction": "Outgoing", "duration": "02:50", "evidence_id": "EV-COM-PRI-001", "contact": "Audit Firm Desk"},
                {"date": "17 Aug 2026", "time": "15:10:00", "direction": "Incoming", "duration": "03:15", "evidence_id": "EV-COM-PRI-002", "contact": "Arjun Sharma"}
            ]
        },
        "P-004": {
            "total_events": 101, "calls": 58, "messages": 43, "unique_contacts": 6, "active_period": "02 Aug – 18 Aug 2026",
            "contacts": [
                {"id": "P-001", "name": "Arjun Sharma", "role": "Primary Subject", "calls": 9, "phone": "+91 98765 1201"},
                {"id": "EXT-04", "name": "Nashik Freight Yard", "role": "Transport Contact", "calls": 22, "phone": "+91 95333 4455"}
            ],
            "history": [
                {"date": "18 Aug 2026", "time": "20:26:11", "direction": "Outgoing", "duration": "01:45", "evidence_id": "EV-COM-VIK-001", "contact": "Arjun Sharma"},
                {"date": "18 Aug 2026", "time": "18:12:00", "direction": "Incoming", "duration": "04:30", "evidence_id": "EV-COM-VIK-002", "contact": "Nashik Freight Yard"}
            ]
        },
        "P-005": {
            "total_events": 130, "calls": 42, "messages": 88, "unique_contacts": 7, "active_period": "04 Aug – 18 Aug 2026",
            "contacts": [
                {"id": "P-001", "name": "Arjun Sharma", "role": "Primary Subject", "calls": 6, "phone": "+91 98765 1201"},
                {"id": "EXT-05", "name": "TechDesk IT Help", "role": "Supplier Contact", "calls": 12, "phone": "+91 94444 5566"}
            ],
            "history": [
                {"date": "18 Aug 2026", "time": "11:00:00", "direction": "Outgoing", "duration": "03:22", "evidence_id": "EV-COM-NEH-001", "contact": "TechDesk IT Help"}
            ]
        },
        "P-006": {
            "total_events": 12, "calls": 5, "messages": 7, "unique_contacts": 2, "active_period": "10 Aug – 18 Aug 2026",
            "contacts": [
                {"id": "EXT-06", "name": "Commodity Exchange Desk", "role": "Market Contact", "calls": 5, "phone": "+91 98999 1111"}
            ],
            "history": [
                {"date": "18 Aug 2026", "time": "09:15:00", "direction": "Outgoing", "duration": "01:10", "evidence_id": "EV-COM-AMB-001", "contact": "Commodity Exchange Desk"}
            ]
        }
    }

    # 3. PERSON-SCOPED FINANCIAL LEDGER (REQUIREMENT 8)
    financial = {
        "P-001": {
            "account": "HDFC Acc XXXX4821",
            "balance": "₹14,50,000",
            "transactions": [
                {"date": "18 Aug 2026", "time": "20:58", "amount": "₹48,500", "direction": "OUT", "account": "XXXX4821", "counterparty": "Rohan Mehta", "reference": "TXN-88421", "evidence_id": "EV-FIN-ARJ-001", "confidence": "71%", "indicator": "Temporal proximity between communication and financial activity."},
                {"date": "17 Aug 2026", "time": "18:45", "amount": "₹19,800", "direction": "OUT", "account": "XXXX4821", "counterparty": "Vikram Patil", "reference": "TXN-88423", "evidence_id": "EV-FIN-ARJ-002", "confidence": "90%", "indicator": "Logistics expense payment."}
            ]
        },
        "P-002": {
            "account": "Axis Acc XXXX7312",
            "balance": "₹22,80,000",
            "transactions": [
                {"date": "18 Aug 2026", "time": "20:58", "amount": "₹48,500", "direction": "IN", "account": "XXXX7312", "counterparty": "Arjun Sharma", "reference": "TXN-88421", "evidence_id": "EV-FIN-ROH-001", "confidence": "85%", "indicator": "Incoming commercial transfer credit."},
                {"date": "16 Aug 2026", "time": "14:15", "amount": "₹1,85,000", "direction": "OUT", "account": "XXXX7312", "counterparty": "Mehta Global Imports", "reference": "TXN-99102", "evidence_id": "EV-FIN-ROH-002", "confidence": "92%", "indicator": "Corporate import settlement."}
            ]
        },
        "P-003": {
            "account": "ICICI Acc XXXX6154",
            "balance": "₹8,40,000",
            "transactions": [
                {"date": "18 Aug 2026", "time": "15:20", "amount": "₹72,000", "direction": "IN", "account": "XXXX6154", "counterparty": "Nexus Financial", "reference": "TXN-77301", "evidence_id": "EV-FIN-PRI-001", "confidence": "93%", "indicator": "Corporate advisory fee payout."}
            ]
        },
        "P-004": {
            "account": "Bank of Maharashtra Acc XXXX9087",
            "balance": "₹5,60,000",
            "transactions": [
                {"date": "17 Aug 2026", "time": "18:45", "amount": "₹19,800", "direction": "IN", "account": "XXXX9087", "counterparty": "Arjun Sharma", "reference": "TXN-88423", "evidence_id": "EV-FIN-VIK-001", "confidence": "90%", "indicator": "Freight service credit."}
            ]
        },
        "P-005": {
            "account": "Union Bank Acc XXXX3246",
            "balance": "₹3,90,000",
            "transactions": [
                {"date": "15 Aug 2026", "time": "11:30", "amount": "₹45,000", "direction": "IN", "account": "XXXX3246", "counterparty": "TechDesk Systems", "reference": "TXN-55104", "evidence_id": "EV-FIN-NEH-001", "confidence": "95%", "indicator": "Monthly payroll disbursement."}
            ]
        },
        "P-006": {
            "account": "State Bank Acc XXXX9999",
            "balance": "₹1,20,000",
            "transactions": [
                {"date": "18 Aug 2026", "time": "09:30", "amount": "₹12,500", "direction": "OUT", "account": "XXXX9999", "counterparty": "Local Mandi Desk", "reference": "TXN-11001", "evidence_id": "EV-FIN-AMB-001", "confidence": "43%", "indicator": "Unresolved cash transaction."}
            ]
        }
    }

    # 4. PERSON-SCOPED BLOCKCHAIN WALLETS (REQUIREMENT 9)
    blockchain = {
        "P-001": {
            "address": "0xDEMO...A721", "balance": "8.42 ETH", "associated_evidence": "EV-BC-ARJ-001", "incoming": 23, "outgoing": 24,
            "transactions": [
                {"hash": "TX-ARJ-001", "from_addr": "0xDEMO...A721", "to_addr": "0x3910...199", "value": "1.20 ETH", "time": "18 Aug 2026 21:17:04", "evidence_id": "EV-BC-ARJ-001"}
            ]
        },
        "P-002": {
            "address": "0xDEMO...B492", "balance": "14.15 ETH", "associated_evidence": "EV-BC-ROH-001", "incoming": 18, "outgoing": 13,
            "transactions": [
                {"hash": "TX-ROH-001", "from_addr": "0xDEMO...B492", "to_addr": "0x7720...A11", "value": "2.50 ETH", "time": "18 Aug 2026 19:40:00", "evidence_id": "EV-BC-ROH-001"}
            ]
        },
        "P-003": {
            "address": "0xDEMO...C381", "balance": "2.10 ETH", "associated_evidence": "EV-BC-PRI-001", "incoming": 4, "outgoing": 2,
            "transactions": [
                {"hash": "TX-PRI-001", "from_addr": "0xDEMO...C381", "to_addr": "0x9910...D44", "value": "0.50 ETH", "time": "17 Aug 2026 11:20:00", "evidence_id": "EV-BC-PRI-001"}
            ]
        },
        "P-004": {
            "address": "0xDEMO...D527", "balance": "5.80 ETH", "associated_evidence": "EV-BC-VIK-001", "incoming": 8, "outgoing": 6,
            "transactions": [
                {"hash": "TX-VIK-001", "from_addr": "0xDEMO...D527", "to_addr": "0x4430...E88", "value": "1.10 ETH", "time": "16 Aug 2026 16:05:00", "evidence_id": "EV-BC-VIK-001"}
            ]
        },
        "P-005": {
            "address": "0xDEMO...E614", "balance": "0.45 ETH", "associated_evidence": "EV-BC-NEH-001", "incoming": 2, "outgoing": 1,
            "transactions": [
                {"hash": "TX-NEH-001", "from_addr": "0xDEMO...E614", "to_addr": "0x1120...F99", "value": "0.15 ETH", "time": "15 Aug 2026 10:00:00", "evidence_id": "EV-BC-NEH-001"}
            ]
        },
        "P-006": {
            "address": "0xDEMO...F000", "balance": "0.10 ETH", "associated_evidence": "EV-BC-AMB-001", "incoming": 1, "outgoing": 0,
            "transactions": [
                {"hash": "TX-AMB-001", "from_addr": "0xDEMO...F000", "to_addr": "0x0000...000", "value": "0.10 ETH", "time": "18 Aug 2026 08:30:00", "evidence_id": "EV-BC-AMB-001"}
            ]
        }
    }

    # 5. PERSON-SCOPED OSINT RECORDS (REQUIREMENT 10)
    osint = {
        "P-001": [
            {"id": "PSI-ARJ-01", "subject": "Arjun Sharma", "source": "Public Web", "last_observed": "18 Aug 2026", "entity": "Rohan Mehta", "location": "Pune", "evidence_id": "EV-OSINT-ARJ-001", "confidence": "76%", "value": "@arjun_s_demo profile & forum post"}
        ],
        "P-002": [
            {"id": "PSI-ROH-01", "subject": "Rohan Mehta", "source": "Import Directory", "last_observed": "18 Aug 2026", "entity": "Mehta Global", "location": "Mumbai", "evidence_id": "EV-OSINT-ROH-001", "confidence": "88%", "value": "Mumbai Customs Import Filing #MC-881"}
        ],
        "P-003": [
            {"id": "PSI-PRI-01", "subject": "Priya Joshi", "source": "Corporate Registrar", "last_observed": "18 Aug 2026", "entity": "Nexus Advisory", "location": "Pune", "evidence_id": "EV-OSINT-PRI-001", "confidence": "94%", "value": "MCA Director Listing for Nexus Financial"}
        ],
        "P-004": [
            {"id": "PSI-VIK-01", "subject": "Vikram Patil", "source": "RTO Database", "last_observed": "18 Aug 2026", "entity": "MH15 TG 4428", "location": "Nashik", "evidence_id": "EV-OSINT-VIK-001", "confidence": "91%", "value": "Commercial Goods Permit Registration"}
        ],
        "P-005": [
            {"id": "PSI-NEH-01", "subject": "Neha Kulkarni", "source": "Tech Network Index", "last_observed": "18 Aug 2026", "entity": "TechDesk Systems", "location": "Pune", "evidence_id": "EV-OSINT-NEH-001", "confidence": "85%", "value": "Subnet Operator Contact Profile"}
        ],
        "P-006": [
            {"id": "PSI-AMB-01", "subject": "Arjun S.", "source": "Public Directory", "last_observed": "18 Aug 2026", "entity": "Commodity Desk", "location": "Pune", "evidence_id": "EV-OSINT-AMB-001", "confidence": "43%", "value": "Ambiguous Business Directory Entry"}
        ]
    }

    # 6. PERSON-SCOPED CCTV SURVEILLANCE VIDEOS (REQUIREMENT 11)
    cctv = {
        "P-001": [
            {"id": "EV-CCTV-ARJ-001", "camera_id": "CAM-04", "location": "Pune Location A", "timestamp": "18 Aug 2026 20:01:14", "event_title": "PERSON MEETING", "suspects_identified": ["Arjun Sharma", "Rohan Mehta"], "anpr_license_plate": "MH12 AB 4821", "evidence_id": "EV-CCTV-ARJ-001", "video_thumbnail": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800&auto=format&fit=crop&q=80", "description": "CAM-04 captured meeting between Arjun Sharma and Rohan Mehta.", "label": "VERIFIED STREAM"}
        ],
        "P-002": [
            {"id": "EV-CCTV-ROH-001", "camera_id": "CAM-08", "location": "Mumbai Port Dock B", "timestamp": "18 Aug 2026 17:40:00", "event_title": "CARGO INSPECTION SIGHTING", "suspects_identified": ["Rohan Mehta"], "anpr_license_plate": "MH01 CR 7814", "evidence_id": "EV-CCTV-ROH-001", "video_thumbnail": "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=800&auto=format&fit=crop&q=80", "description": "CAM-08 captured Rohan Mehta at freight dispatch dock.", "label": "VERIFIED STREAM"}
        ],
        "P-003": [
            {"id": "EV-CCTV-PRI-001", "camera_id": "CAM-02", "location": "Baner Financial Hub", "timestamp": "18 Aug 2026 15:15:00", "event_title": "OFFICE ENTRY", "suspects_identified": ["Priya Joshi"], "anpr_license_plate": "MH12 DK 2093", "evidence_id": "EV-CCTV-PRI-001", "video_thumbnail": "https://images.unsplash.com/photo-1497366216548-37526070297c?w=800&auto=format&fit=crop&q=80", "description": "CAM-02 entry log for Priya Joshi.", "label": "VERIFIED STREAM"}
        ],
        "P-004": [
            {"id": "EV-CCTV-VIK-001", "camera_id": "CAM-12", "location": "Highway Toll Plaza, Nashik", "timestamp": "18 Aug 2026 18:10:00", "event_title": "VEHICLE TOLL ANPR CAPTURE", "suspects_identified": ["Vikram Patil"], "anpr_license_plate": "MH15 TG 4428", "evidence_id": "EV-CCTV-VIK-001", "video_thumbnail": "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&auto=format&fit=crop&q=80", "description": "ANPR sighting of truck driven by Vikram Patil.", "label": "VERIFIED STREAM"}
        ],
        "P-005": [
            {"id": "EV-CCTV-NEH-001", "camera_id": "CAM-01", "location": "TechDesk Gate 1", "timestamp": "18 Aug 2026 10:55:00", "event_title": "FACILITY ACCESS LOG", "suspects_identified": ["Neha Kulkarni"], "anpr_license_plate": "MH12 EQ 9136", "evidence_id": "EV-CCTV-NEH-001", "video_thumbnail": "https://images.unsplash.com/photo-1573164713988-8665fc963095?w=800&auto=format&fit=crop&q=80", "description": "Badge access sighting for Neha Kulkarni.", "label": "VERIFIED STREAM"}
        ],
        "P-006": []
    }

    # 7. PERSON-SCOPED INVESTIGATIVE LEADS (REQUIREMENT 15)
    leads = {
        "P-001": [
            {"id": "LEAD-ARJ-001", "personId": "P-001", "title": "Communication and financial activity temporal correlation", "lead": "Multiple call bursts preceding wire transfer", "confidence": 0.82, "supporting_evidence": ["EV-COM-ARJ-001", "EV-FIN-ARJ-001"], "observed_pattern": "Call burst 53s prior to CAM-04 sighting.", "alternative_explanation": "Business coordination.", "status": "Needs Review"}
        ],
        "P-002": [
            {"id": "LEAD-ROH-001", "personId": "P-002", "title": "Repeated commercial import settlements across multiple counterparties", "lead": "Import invoice layering pattern", "confidence": 0.79, "supporting_evidence": ["EV-FIN-ROH-001", "EV-BC-ROH-001"], "observed_pattern": "Rapid customs settlement followed by crypto off-ramp.", "alternative_explanation": "Legitimate import supplier payments.", "status": "Needs Review"}
        ],
        "P-003": [
            {"id": "LEAD-PRI-001", "personId": "P-003", "title": "Organizational financial advisory reconciliation pattern", "lead": "Audit statement timing correlation", "confidence": 0.74, "supporting_evidence": ["EV-FIN-PRI-001", "EV-OSINT-PRI-001"], "observed_pattern": "Advisory fee deposit coinciding with MCA filing date.", "alternative_explanation": "Standard retainer accounting.", "status": "Needs Review"}
        ],
        "P-004": [
            {"id": "LEAD-VIK-001", "personId": "P-004", "title": "Vehicle freight movement correlation along Western Corridor", "lead": "Highway toll passage preceding meeting", "confidence": 0.81, "supporting_evidence": ["EV-CCTV-VIK-001", "EV-FIN-VIK-001"], "observed_pattern": "Truck passage logged 16 mins prior to Pune location arrival.", "alternative_explanation": "Scheduled freight route.", "status": "Needs Review"}
        ],
        "P-005": [
            {"id": "LEAD-NEH-001", "personId": "P-005", "title": "Workplace network subnet routing cluster", "lead": "Shared VPN gateway access during business hours", "confidence": 0.68, "supporting_evidence": ["EV-OSINT-NEH-001", "EV-CCTV-NEH-001"], "observed_pattern": "IP subnet activity matching server log timestamp.", "alternative_explanation": "Co-worker shared IT infrastructure.", "status": "Needs Review"}
        ],
        "P-006": [
            {"id": "LEAD-AMB-001", "personId": "P-006", "title": "Candidate identity match ambiguity (False Positive Demo)", "lead": "Name similarity + location overlap (Confidence 43%)", "confidence": 0.43, "supporting_evidence": ["EV-OSINT-AMB-001"], "observed_pattern": "Directory harvest returned similarity score of 43%.", "alternative_explanation": "Unrelated individual with common name.", "status": "Unresolved Candidate"}
        ]
    }

    # 8. CASES DATABASE
    cases_db = {
        "TRX-2026-017": {
            "id": "TRX-2026-017",
            "title": "OPERATION NEXUS",
            "primary_suspect": profiles["P-001"],
            "secondary_suspects": [profiles["P-002"], profiles["P-003"], profiles["P-004"], profiles["P-005"]],
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
        }
    }

    return {
        "profiles": profiles,
        "communications": communications,
        "financial": financial,
        "blockchain": blockchain,
        "osint": osint,
        "cctv": cctv,
        "leads": leads,
        "cases": cases_db
    }
