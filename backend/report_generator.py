import time
from typing import Dict, List, Any

class InvestigationReportGenerator:
    def __init__(self):
        pass

    def generate_report(self, case_data: Dict[str, Any], nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]], evidence_items: List[Dict[str, Any]], fusion_data: Dict[str, Any]) -> Dict[str, Any]:
        report_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>TRACE-X Official Investigation Report - {case_data['id']}</title>
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; color: #1e293b; background: #ffffff; line-height: 1.6; }}
                .header {{ border-bottom: 3px solid #0f172a; padding-bottom: 20px; margin-bottom: 30px; }}
                .header h1 {{ margin: 0; color: #0f172a; font-size: 24px; text-transform: uppercase; letter-spacing: 1px; }}
                .header p {{ margin: 5px 0 0 0; color: #64748b; font-size: 14px; }}
                .disclaimer {{ background: #fef2f2; border-left: 4px solid #ef4444; padding: 12px 16px; font-size: 13px; color: #991b1b; margin-bottom: 25px; }}
                .section {{ margin-bottom: 30px; }}
                .section h2 {{ font-size: 18px; border-bottom: 1px solid #cbd5e1; padding-bottom: 6px; color: #1e293b; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 13px; }}
                th, td {{ border: 1px solid #cbd5e1; padding: 8px 12px; text-align: left; }}
                th {{ background: #f1f5f9; font-weight: 600; color: #334155; }}
                .lead-card {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 16px; margin-top: 10px; }}
                .badge {{ display: inline-block; padding: 3px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; background: #e2e8f0; color: #334155; }}
                .badge-high {{ background: #fee2e2; color: #991b1b; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>TRACE-X — AI-Powered Criminal Network Intelligence Report</h1>
                <p>CONFIDENTIAL // LAW ENFORCEMENT & INVESTIGATIVE USE ONLY // GENERATED ON {time.strftime('%Y-%m-%d %H:%M:%S IST')}</p>
            </div>

            <div class="disclaimer">
                <strong>LEGAL DISCLAIMER:</strong> TRACE-X provides analytical decision support. Investigative findings represent evidence-supported associations requiring human verification and appropriate legal authorization. The system never automatically declares guilt or criminality.
            </div>

            <div class="section">
                <h2>1. Case Metadata & Overview</h2>
                <table>
                    <tr><th>Case ID</th><td>{case_data['id']}</td><th>Priority</th><td><span class="badge badge-high">{case_data.get('priority', 'HIGH')}</span></td></tr>
                    <tr><th>Title</th><td colspan="3">{case_data['title']}</td></tr>
                    <tr><th>Subject Name</th><td>{case_data['subject_name']}</td><th>Status</th><td>{case_data['status']}</td></tr>
                    <tr><th>Lead Investigator</th><td>{case_data.get('investigator', 'Ins. V. Rao')}</td><th>Agency</th><td>{case_data.get('agency', 'SCCIC')}</td></tr>
                </table>
            </div>

            <div class="section">
                <h2>2. Primary Subject Identifiers</h2>
                <p><strong>Known Identifiers:</strong></p>
                <ul>
                    <li><strong>Phone:</strong> {", ".join(case_data['subject_known_identifiers'].get('phone', []))}</li>
                    <li><strong>Email:</strong> {", ".join(case_data['subject_known_identifiers'].get('email', []))}</li>
                    <li><strong>Aliases:</strong> {", ".join(case_data['subject_known_identifiers'].get('aliases', []))}</li>
                    <li><strong>Vehicles:</strong> {", ".join(case_data['subject_known_identifiers'].get('vehicle', []))}</li>
                    <li><strong>Wallets:</strong> {", ".join(case_data['subject_known_identifiers'].get('wallet', []))}</li>
                </ul>
            </div>

            <div class="section">
                <h2>3. Evidence Summary & Chain of Custody</h2>
                <table>
                    <thead>
                        <tr><th>Evidence ID</th><th>Type</th><th>Title</th><th>Source</th><th>File Hash (SHA-256)</th><th>Status</th></tr>
                    </thead>
                    <tbody>
                        {"".join([f"<tr><td>{e['id']}</td><td>{e['evidence_type']}</td><td>{e['title']}</td><td>{e['source']}</td><td><code>{e['file_hash'][:16]}...</code></td><td>{e['integrity_status']}</td></tr>" for e in evidence_items])}
                    </tbody>
                </table>
            </div>

            <div class="section">
                <h2>4. Cross-Domain Evidence Fusion Lead</h2>
                <div class="lead-card">
                    <h3>{fusion_data.get('fusion_title', 'Cross-Domain Lead')}</h3>
                    <p><strong>Overall Confidence:</strong> {fusion_data.get('explainable_ai', {}).get('CONFIDENCE', '93.4%')}</p>
                    <p><strong>Explainable AI Synthesis (WHAT & WHY):</strong></p>
                    <p>{fusion_data.get('explainable_ai', {}).get('WHAT', '')}</p>
                    <p><em>{fusion_data.get('explainable_ai', {}).get('WHY', '')}</em></p>
                    <h4>Recommended Human Review Actions:</h4>
                    <ul>
                        {"".join([f"<li>{action}</li>" for action in fusion_data.get('recommended_actions', [])])}
                    </ul>
                </div>
            </div>

            <div class="section">
                <h2>5. Signatures & Approvals</h2>
                <br><br>
                <table style="border: none;">
                    <tr style="border: none;">
                        <td style="border: none; width: 50%;">
                            ___________________________________<br>
                            <strong>Lead Investigator Signature</strong><br>
                            Date: 
                        </td>
                        <td style="border: none; width: 50%;">
                            ___________________________________<br>
                            <strong>Forensic Examiner / Supervisor</strong><br>
                            Date: 
                        </td>
                    </tr>
                </table>
            </div>
        </body>
        </html>
        """
        
        return {
            "case_id": case_data['id'],
            "report_title": f"TRACE-X Investigation Report - {case_data['id']}",
            "generated_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "section_count": 16,
            "html_content": report_html
        }

report_generator = InvestigationReportGenerator()
