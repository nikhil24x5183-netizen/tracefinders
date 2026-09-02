import time
from typing import Dict, List, Any

class ReportGenerator:
    def __init__(self):
        pass

    def generate_report(
        self,
        case_data: Dict[str, Any],
        person_data: Dict[str, Any],
        cctv_events: List[Dict[str, Any]],
        fusion_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        
        timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S IST")
        
        case_id = case_data.get("id", "TRX-2026-017")
        case_title = case_data.get("title", "OPERATION NEXUS")
        status = case_data.get("status", "Active Investigation")
        priority = case_data.get("priority", "High")
        lead = case_data.get("lead_investigator", "Ins. Vikramaditya Rao (#INV-7092)")

        # Case Primary Subject vs Current Selected Subject (Requirements 2, 6, 20, 21)
        primary_case_subject = "Arjun Sharma"
        
        # Person-Scoped Profile Data
        pid = person_data.get("id", "P-001")
        pname = person_data.get("name", "Arjun Sharma")
        palias = person_data.get("alias", "Arjun S.")
        prole = person_data.get("role", "Primary Subject")
        page = person_data.get("age", 34)
        pgender = person_data.get("gender", "Male")
        pcity = person_data.get("city", "Pune")
        poccupation = person_data.get("occupation", "Logistics Consultant")
        porg = person_data.get("organization", "Nexus Logistics")
        pphone = person_data.get("phone", "+91 98765 1201")
        pemail = person_data.get("email", "arjun.sharma.demo@example.test")
        pvehicle = person_data.get("vehicle", "MH12 AB 4821")
        paccount = person_data.get("account_number", "XXXX4821")
        pwallet = person_data.get("wallet_address", "0xDEMO...A721")
        prisk = person_data.get("risk_score", 92)
        pcounts = person_data.get("counts", {})

        evd_rows = ""
        # Build person-scoped evidence table (Requirement 8)
        person_evidences = [
            {"id": f"EV-CCTV-{pid}-001", "type": "DVR/NVR Forensics", "title": f"CCTV Sighting ({pname})", "source": "CAM-04 / CAM-01", "hash": "8f31c44298fc1c149a..."},
            {"id": f"EV-COM-{pid}-001", "type": "CDR / Telecommunication", "title": f"Call Log ({pphone})", "source": "Telecom Node #7092", "hash": "d41d8cd98f00b204e9..."},
            {"id": f"EV-FIN-{pid}-001", "type": "Financial Wire Ledger", "title": f"Bank Transfer (Acc {paccount})", "source": "NPCI Wire Clearing", "hash": "2a0487b99c15e6118d..."},
            {"id": f"EV-BC-{pid}-001", "type": "Blockchain On-Chain", "title": f"Crypto Transfer ({pwallet})", "source": "Ethereum Mainnet", "hash": "7f8b91c420e61f99a3..."}
        ]

        for e in person_evidences:
            evd_rows += f"<tr><td><strong>{e['id']}</strong></td><td>{e['type']}</td><td>{e['title']}</td><td>{e['source']}</td><td><span class='badge'>{e['hash']}</span></td></tr>"

        cctv_rows = ""
        for c in (cctv_events or [])[:5]:
            cctv_rows += f"<tr><td><strong>{c.get('timestamp', '')}</strong></td><td><span class='badge'>{c.get('camera_id', '')}</span></td><td>{c.get('event_title', '')}</td><td>{c.get('location', '')}</td><td>Ref: {c.get('evidence_id', '')}</td></tr>"
        if not cctv_rows:
            cctv_rows = f"<tr><td colspan='5'>No direct surveillance sightings logged for {pname} on selected filters.</td></tr>"

        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>TRACE FINDERS Official Investigation Dossier - {case_id} ({pname})</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #0f172a; padding: 28px; line-height: 1.5; font-size: 13px; background: #ffffff; }}
        h1, h2, h3 {{ color: #1e3a8a; font-weight: 800; border-bottom: 2px solid #2563eb; padding-bottom: 4px; margin-top: 24px; }}
        .meta-table, .data-table {{ width: 100%; border-collapse: collapse; margin-bottom: 16px; }}
        .meta-table th, .meta-table td, .data-table th, .data-table td {{ padding: 8px 12px; border: 1px solid #cbd5e1; text-align: left; }}
        .meta-table th, .data-table th {{ background-color: #f1f5f9; color: #334155; font-weight: 800; text-transform: uppercase; font-size: 11px; }}
        .badge {{ background-color: #eff6ff; color: #2563eb; padding: 2px 6px; border-radius: 4px; font-weight: 700; font-size: 10px; border: 1px solid #bfdbfe; }}
        .disclaimer {{ background-color: #fffbeb; border: 1px solid #fde68a; color: #92400e; padding: 12px; border-radius: 6px; font-size: 11px; margin-bottom: 20px; }}
        .context-highlight {{ background-color: #eff6ff; border-left: 4px solid #2563eb; padding: 12px 16px; border-radius: 6px; margin-bottom: 20px; font-size: 13px; }}
    </style>
</head>
<body>

    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div style="display: flex; align-items: center; gap: 14px;">
            <img src="/static/logo.png" style="height: 48px; width: auto;" alt="TRACE FINDERS LOGO">
            <div>
                <h1 style="margin:0; font-size: 20px; border-bottom: none; padding: 0;">TRACE FINDERS OFFICIAL INVESTIGATION DOSSIER</h1>
                <div style="font-size: 11px; color: #64748b; font-weight: 700;">CONFIDENTIAL // SIH26189 AI-POWERED CRIMINAL NETWORK ANALYSIS SYSTEM</div>
            </div>
        </div>
        <div style="text-align: right; font-size: 11px; color: #64748b;">
            <div>Generated: <strong>{timestamp_str}</strong></div>
            <div>Dossier Ref: <strong>{case_id}-{pid}-DOSSIER</strong></div>
        </div>
    </div>

    <hr style="margin: 16px 0; border: none; border-top: 1px solid #cbd5e1;">

    <!-- DYNAMIC INVESTIGATION CONTEXT LINE (REQUIREMENTS 2, 6, 20, 21) -->
    <div class="context-highlight">
        <div>📁 <strong>CASE REFERENCE:</strong> {case_id} — {case_title}</div>
        <div>👤 <strong>CASE PRIMARY SUBJECT:</strong> {primary_case_subject}</div>
        <div>🎯 <strong>CURRENT INVESTIGATION SUBJECT:</strong> <span style="font-size: 15px; font-weight: 800; color: #2563eb;">{pname.upper()}</span> (Role: <strong>{prole}</strong> | ID: <strong>{pid}</strong>)</div>
    </div>

    <div class="disclaimer">
        ⚖️ <strong>LEGAL NOTICE & STATUTORY COMPLIANCE STATEMENT:</strong><br>
        This dossier is generated by the TRACE FINDERS AI Evidence Fusion Workstation under SIH26189. All investigative leads represent decision-support findings requiring manual verification under Sec 91 & Sec 65B of the Indian Evidence Act.
    </div>

    <h2>1. Executive Summary & Subject Identifiers</h2>
    <table class="meta-table">
        <tr><th>Case Reference</th><td>{case_id}</td><th>Case Title</th><td>{case_title}</td></tr>
        <tr><th>Case Primary Subject</th><td>{primary_case_subject}</td><th>Status</th><td><span class="badge">{status}</span></td></tr>
        <tr><th>Current Subject View</th><td><strong style="color: #2563eb; font-size: 14px;">{pname}</strong></td><th>Role / Status</th><td><strong>{prole}</strong></td></tr>
        <tr><th>Age & Gender</th><td>{page} ({pgender})</td><th>City / Jurisdiction</th><td>{pcity}, Maharashtra</td></tr>
        <tr><th>Occupation</th><td>{poccupation}</td><th>Organization</th><td>{porg}</td></tr>
        <tr><th>Registered Phone</th><td><strong>{pphone}</strong></td><th>Registered Email</th><td>{pemail}</td></tr>
        <tr><th>Registered Vehicle</th><td><strong>{pvehicle}</strong></td><th>Bank Account</th><td><strong>{paccount}</strong></td></tr>
        <tr><th>Crypto Wallet</th><td><code>{pwallet}</code></td><th>Risk Score</th><td><span class="badge" style="background:#fef2f2; color:#dc2626;">{prisk} / 100 Risk</span></td></tr>
    </table>

    <h2>2. Person-Scoped Key Evidence Records ({pname})</h2>
    <table class="data-table">
        <thead>
            <tr><th>Evidence ID</th><th>Type</th><th>Title</th><th>Source</th><th>Hash Verification</th></tr>
        </thead>
        <tbody>
            {evd_rows}
        </tbody>
    </table>

    <h2>3. Communication & Telecommunication Analysis</h2>
    <table class="meta-table">
        <tr><th>Tracked Subject</th><td><strong>{pname}</strong> ({pphone})</td><th>Total CDR Events</th><td><strong>{pcounts.get('calls', 0) + pcounts.get('messages', 0)}</strong></td></tr>
        <tr><th>Calls Logged</th><td>{pcounts.get('calls', 0)}</td><th>Messages Logged</th><td>{pcounts.get('messages', 0)}</td></tr>
        <tr><th>Unique Contacts</th><td>{pcounts.get('contacts', 0)}</td><th>Active Window</th><td>03 Aug – 18 Aug 2026</td></tr>
    </table>

    <h2>4. Financial & Asset Ledger ({paccount})</h2>
    <table class="meta-table">
        <tr><th>Tracked Account</th><td><strong>{paccount}</strong> ({pname})</td><th>Ledger Balance</th><td><strong>₹14,50,000</strong></td></tr>
        <tr><th>Total Transactions</th><td>{pcounts.get('financial', 0)}</td><th>Risk Rationale</th><td>Observed wire transfer activities.</td></tr>
    </table>

    <h2>5. Blockchain Wallet Intelligence ({pwallet})</h2>
    <table class="meta-table">
        <tr><th>Wallet Address</th><td><code>{pwallet}</code></td><th>Wallet Balance</th><td><strong>8.42 ETH</strong></td></tr>
        <tr><th>On-Chain Txs</th><td>{pcounts.get('blockchain', 0)} Transactions</td><th>Evidence Link</th><td>EV-BC-{pid}-001</td></tr>
    </table>

    <h2>6. CCTV / DVR Surveillance Forensics</h2>
    <table class="data-table">
        <thead>
            <tr><th>Timestamp</th><th>Camera ID</th><th>Surveillance Event</th><th>Location</th><th>Linked Evidence</th></tr>
        </thead>
        <tbody>
            {cctv_rows}
        </tbody>
    </table>

    <h2>7. Explainable AI Investigative Leads ({pname})</h2>
    <div style="padding: 14px; background: #eff6ff; border: 1px solid #bfdbfe; border-left: 4px solid #2563eb; border-radius: 8px;">
        <div style="font-weight: 800; color: #1e3a8a; margin-bottom: 4px;">🧠 PRIMARY LEAD FOR {pname.upper()}:</div>
        <div>Multi-hop intelligence correlation indicates temporal activity overlap for {pname} across CDR logs ({pphone}) and surveillance sightings.</div>
    </div>

    <h2>8. Investigator Sign-Off & Certification</h2>
    <div style="margin-top: 40px; display: flex; justify-content: space-between;">
        <div>
            <div>__________________________________</div>
            <div><strong>Ins. Vikramaditya Rao (#INV-7092)</strong></div>
            <div>Lead Investigator, SCCIC</div>
        </div>
        <div>
            <div>__________________________________</div>
            <div><strong>Superintendent of Police</strong></div>
            <div>Cyber Crime Division</div>
        </div>
    </div>

</body>
</html>"""

        return {
            "case_id": case_id,
            "person_id": pid,
            "subject_name": pname,
            "generated_at": timestamp_str,
            "html_content": html_content
        }

report_generator = ReportGenerator()
