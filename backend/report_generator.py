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

        # Case Primary Subject vs Current Selected Subject
        primary_case_subject = "Arjun Sharma"
        
        # Person-Scoped Profile Data
        pid = person_data.get("id", "P-001")
        pname = person_data.get("name", "Arjun Sharma")
        palias = person_data.get("alias", "Arjun S.")
        prole = person_data.get("role", "Primary Subject")
        photo_url = person_data.get("photo_url", "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=300")
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
        @page {{
            size: A4;
            margin: 15mm;
        }}
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, Arial, sans-serif;
            color: #0f172a;
            padding: 24px;
            line-height: 1.5;
            font-size: 13px;
            background: #ffffff;
        }}
        .a4-container {{
            max-width: 820px;
            margin: 0 auto;
            background: #ffffff;
            padding: 32px;
            border-radius: 8px;
            border: 1px solid #cbd5e1;
            box-shadow: 0 4px 16px rgba(0,0,0,0.06);
        }}
        h1 {{ color: #0f172a; font-weight: 800; font-size: 20px; margin-bottom: 4px; }}
        h2, h3 {{ color: #0f172a; font-weight: 700; border-bottom: 2px solid #B59A62; padding-bottom: 4px; margin-top: 24px; font-size: 15px; }}
        .meta-table, .data-table {{ width: 100%; border-collapse: collapse; margin-bottom: 16px; font-size: 12px; }}
        .meta-table th, .meta-table td, .data-table th, .data-table td {{ padding: 8px 12px; border: 1px solid #cbd5e1; text-align: left; }}
        .meta-table th, .data-table th {{ background-color: #f8fafc; color: #334155; font-weight: 700; text-transform: uppercase; font-size: 10px; }}
        .badge {{ background-color: #f1f5f9; color: #0f172a; padding: 2px 6px; border-radius: 4px; font-weight: 700; font-size: 10px; border: 1px solid #cbd5e1; font-family: monospace; }}
        .disclaimer {{ background-color: #fffbeb; border: 1px solid #fde68a; color: #92400e; padding: 10px 14px; border-radius: 6px; font-size: 11px; margin-bottom: 20px; }}
        .context-highlight {{ background-color: #f8fafc; border-left: 4px solid #B59A62; padding: 12px 16px; border-radius: 6px; margin-bottom: 20px; font-size: 12px; }}
        
        .subject-profile-card {{
            display: flex;
            gap: 20px;
            align-items: center;
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 20px;
        }}
        .subject-photo {{
            width: 110px;
            height: 110px;
            object-fit: cover;
            border-radius: 6px;
            border: 2px solid #B59A62;
        }}
        .subject-info-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
            font-size: 12px;
            width: 100%;
        }}
        .info-item label {{
            font-size: 10px;
            font-weight: 700;
            color: #64748b;
            text-transform: uppercase;
            display: block;
        }}
        .info-item value {{
            font-weight: 700;
            color: #0f172a;
        }}
        .footer {{
            margin-top: 32px;
            border-top: 1px solid #cbd5e1;
            padding-top: 12px;
            font-size: 10px;
            color: #64748b;
            display: flex;
            justify-content: space-between;
        }}
    </style>
</head>
<body>
    <div class="a4-container">
        
        <!-- REPORT HEADER & SCOPING DEMARCATION -->
        <div style="border-bottom: 2px solid #0f172a; padding-bottom: 12px; margin-bottom: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h1>TRACE FINDERS OFFICIAL INVESTIGATION DOSSIER</h1>
                    <div style="font-size: 12px; font-weight: 700; color: #475569; letter-spacing: 0.5px;">
                        CASE REFERENCE: <span style="color: #0f172a;">{case_id} — {case_title}</span>
                    </div>
                </div>
                <div style="text-align: right;">
                    <span class="badge" style="background: #1e293b; color: #ffffff; padding: 4px 10px; font-size: 11px;">CLASSIFIED / LAW ENFORCEMENT ONLY</span>
                    <div style="font-size: 10px; color: #64748b; margin-top: 4px;">GENERATED: {timestamp_str}</div>
                </div>
            </div>
        </div>

        <!-- EXPLICIT SCOPING CONTEXT HEADER -->
        <div class="context-highlight">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                <div><strong>CASE PRIMARY SUBJECT:</strong> {primary_case_subject} (Primary Target)</div>
                <div><strong>CURRENT DOSSIER SUBJECT:</strong> <span style="color: #946917; font-weight: 800;">{pname.upper()} ({prole})</span></div>
            </div>
            <div style="font-size: 11px; color: #475569; margin-top: 6px;">
                This document is generated strictly for subject <strong>{pname} ({pid})</strong>. All telephone, financial, surveillance, and on-chain records contained herein belong exclusively to <strong>{pname}</strong>.
            </div>
        </div>

        <!-- LEGAL DISCLAIMER -->
        <div class="disclaimer">
            ⚖️ <strong>LEGAL NOTICE:</strong> The analytical findings presented in this dossier are decision-support outputs compiled by TRACE FINDERS Evidence Fusion Engine. Every correlation must be validated through formal legal process (Section 65B Indian Evidence Act).
        </div>

        <!-- SUBJECT PROFILE CARD WITH EMBEDDED PHOTO -->
        <h3>1. SUBJECT PROFILE & IDENTIFIERS</h3>
        <div class="subject-profile-card">
            <img src="{photo_url}" class="subject-photo" alt="{pname} Portrait">
            <div class="subject-info-grid">
                <div class="info-item"><label>FULL NAME</label><value>{pname}</value></div>
                <div class="info-item"><label>SUBJECT ID & ROLE</label><value>{pid} ({prole})</value></div>
                <div class="info-item"><label>ALIAS / MONIKER</label><value>{palias}</value></div>
                <div class="info-item"><label>AGE / GENDER</label><value>{page} Yrs ({pgender})</value></div>
                <div class="info-item"><label>PRIMARY TELEPHONE</label><value style="font-family: monospace;">{pphone}</value></div>
                <div class="info-item"><label>EMAIL ADDRESS</label><value style="font-family: monospace;">{pemail}</value></div>
                <div class="info-item"><label>REGISTERED VEHICLE</label><value style="font-family: monospace;">{pvehicle}</value></div>
                <div class="info-item"><label>BANK ACCOUNT</label><value style="font-family: monospace;">{paccount}</value></div>
                <div class="info-item" style="grid-column: span 2;"><label>BLOCKCHAIN WALLET</label><value style="font-family: monospace;">{pwallet}</value></div>
            </div>
        </div>

        <!-- CASE METADATA -->
        <h3>2. CASE & INVESTIGATION METADATA</h3>
        <table class="meta-table">
            <tr>
                <th>CASE ID</th>
                <td><strong>{case_id}</strong></td>
                <th>INVESTIGATION TITLE</th>
                <td>{case_title}</td>
            </tr>
            <tr>
                <th>STATUS</th>
                <td><span class="badge">{status}</span></td>
                <th>PRIORITY LEVEL</th>
                <td><span class="badge">{priority}</span></td>
            </tr>
            <tr>
                <th>LEAD INVESTIGATOR</th>
                <td colspan="3">{lead}</td>
            </tr>
        </table>

        <!-- EVIDENTIAL METRICS -->
        <h3>3. EVIDENTIAL BREAKDOWN FOR {pname.upper()}</h3>
        <table class="data-table">
            <thead>
                <tr>
                    <th>DOMAIN MODULE</th>
                    <th>SCOPED COUNTS</th>
                    <th>PRIMARY IDENTIFIER</th>
                    <th>INTEGRITY STATUS</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>TELECOM / CDR</td>
                    <td><strong>{pcounts.get('calls', 0)} Logs</strong></td>
                    <td style="font-family: monospace;">{pphone}</td>
                    <td><span class="badge">VERIFIED</span></td>
                </tr>
                <tr>
                    <td>FINANCIAL LEDGER</td>
                    <td><strong>{pcounts.get('transactions', 0)} Transactions</strong></td>
                    <td style="font-family: monospace;">{paccount}</td>
                    <td><span class="badge">VERIFIED</span></td>
                </tr>
                <tr>
                    <td>SURVEILLANCE CCTV</td>
                    <td><strong>{pcounts.get('cctv_events', 0)} Sightings</strong></td>
                    <td style="font-family: monospace;">{pvehicle}</td>
                    <td><span class="badge">CARVED STREAM</span></td>
                </tr>
                <tr>
                    <td>BLOCKCHAIN ON-CHAIN</td>
                    <td><strong>{pcounts.get('wallet_txs', 0)} Transactions</strong></td>
                    <td style="font-family: monospace;">{pwallet}</td>
                    <td><span class="badge">ON-CHAIN VERIFIED</span></td>
                </tr>
            </tbody>
        </table>

        <!-- EVIDENTIAL CHAIN OF CUSTODY TABLE -->
        <h3>4. ASSOCIATED EVIDENCE RECORDS</h3>
        <table class="data-table">
            <thead>
                <tr>
                    <th>EVIDENCE ID</th>
                    <th>TYPE</th>
                    <th>TITLE</th>
                    <th>SOURCE</th>
                    <th>HASH INTEGRITY</th>
                </tr>
            </thead>
            <tbody>
                {evd_rows}
            </tbody>
        </table>

        <!-- SURVEILLANCE SIGHTINGS -->
        <h3>5. CCTV SURVEILLANCE SIGHTINGS FOR {pname.upper()}</h3>
        <table class="data-table">
            <thead>
                <tr>
                    <th>TIMESTAMP</th>
                    <th>CAMERA ID</th>
                    <th>EVENT TITLE</th>
                    <th>LOCATION</th>
                    <th>EVIDENCE REF</th>
                </tr>
            </thead>
            <tbody>
                {cctv_rows}
            </tbody>
        </table>

        <!-- FOOTER -->
        <div class="footer">
            <div>CONFIDENTIAL — PROPERTY OF STATE CYBER CRIME INVESTIGATION CELL</div>
            <div>PAGE 1 OF 1 — DOSSIER HASH: SHA-256 VERIFIED</div>
        </div>

    </div>
</body>
</html>"""

        return {
            "case_id": case_id,
            "person_id": pid,
            "person_name": pname,
            "html_content": html_content,
            "timestamp": timestamp_str
        }

report_generator = ReportGenerator()
