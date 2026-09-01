// TRACE-X Intelligence Platform Frontend Application Controller
document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initGlobalSearch();
    loadOverviewData();
});

// Navigation Tab Switcher
function initNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            navItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');

            const targetTab = item.getAttribute('data-tab');
            switchTab(targetTab);
        });
    });
}

function switchTab(tabId) {
    const views = document.querySelectorAll('.tab-view');
    views.forEach(v => v.classList.remove('active'));

    const activeView = document.getElementById(`view-${tabId}`);
    if (activeView) {
        activeView.classList.add('active');
        
        if (tabId === 'overview') loadOverviewData();
        if (tabId === 'investigations') loadInvestigationsData();
        if (tabId === 'graph') loadGraphData();
        if (tabId === 'timeline') loadTimelineData();
        if (tabId === 'evidence') loadEvidenceData();
        if (tabId === 'communications') loadCommunicationsData();
        if (tabId === 'financial') loadFinancialData();
        if (tabId === 'blockchain') loadBlockchainData();
        if (tabId === 'osint') loadOSINTData();
        if (tabId === 'dvr') loadDVRData();
        if (tabId === 'analytics') loadAnalyticsData();
        if (tabId === 'fusion') loadFusionData();
        if (tabId === 'audit') loadAuditData();
        if (tabId === 'reports') loadReportData();
    }
}

// 1. Overview Loader
async function loadOverviewData() {
    try {
        const res = await fetch('/api/overview');
        const data = await res.json();

        const stats = data.investigation_statistics;
        document.getElementById('stat-active-cases').innerText = stats.active_investigations;
        document.getElementById('stat-evidence').innerText = stats.evidence_items;
        document.getElementById('stat-entities').innerText = stats.entities;
        document.getElementById('stat-relationships').innerText = stats.relationships;
        document.getElementById('stat-anomalies').innerText = stats.suspicious_patterns;
        document.getElementById('stat-leads').innerText = stats.high_priority_leads;

        const actList = document.getElementById('activity-feed');
        if (actList) {
            actList.innerHTML = data.recent_activity.map(act => `
                <div style="padding: 10px 0; border-bottom: 1px solid #e2e8f0; display: flex; justify-content: space-between; font-size: 12px;">
                    <span>⚡ <strong style="color: #0f172a;">${act.event}</strong></span>
                    <span style="color: #64748b; font-weight: 600;">${act.time}</span>
                </div>
            `).join('');
        }

        const alertList = document.getElementById('alert-panel');
        if (alertList) {
            alertList.innerHTML = data.alert_panel.map(al => `
                <div style="padding: 12px; background: #fef2f2; border-left: 4px solid #dc2626; border-radius: 8px; margin-bottom: 8px; font-size: 12px;">
                    <strong style="color: #991b1b;">🚨 [${al.severity}]</strong> ${al.alert}
                </div>
            `).join('');
        }
    } catch (err) {
        console.error('Failed to load overview data:', err);
    }
}

// 2. Investigations Workspace Loader & Modal Handlers
async function loadInvestigationsData() {
    try {
        const res = await fetch('/api/cases');
        const data = await res.json();
        const container = document.getElementById('investigations-list');
        if (!container) return;

        container.innerHTML = data.cases.map(c => `
            <div class="card" style="margin-bottom: 16px; border-left: 4px solid ${c.priority === 'HIGH' ? '#dc2626' : '#2563eb'};">
                <div class="card-title">
                    <span>${c.id}: ${c.title}</span>
                    <span class="badge ${c.priority === 'HIGH' ? 'badge-high' : 'badge-verified'}">${c.priority} PRIORITY</span>
                </div>
                <div style="font-size: 13px; margin-bottom: 8px;">
                    <strong>Primary Subject / Suspect:</strong> <span style="color: #2563eb; font-weight: 700;">${c.subject_name}</span>
                </div>
                <p style="font-size: 12px; color: #475569; margin-bottom: 12px;">${c.description}</p>
                <div style="font-size: 11px; color: #64748b; margin-bottom: 14px; display: flex; gap: 20px;">
                    <div>Investigator: <strong style="color: #0f172a;">${c.investigator}</strong></div>
                    <div>Agency: <strong style="color: #0f172a;">${c.agency}</strong></div>
                    <div>Start Date: <strong style="color: #0f172a;">${c.start_date}</strong></div>
                    <div>Status: <strong style="color: #16a34a;">${c.status}</strong></div>
                </div>
                <div style="display: flex; gap: 10px;">
                    <button class="btn" onclick="selectActiveCase('${c.id}')">🕸️ Analyze Network Graph</button>
                    <button class="btn btn-secondary" onclick="switchTab('fusion')">🔗 Open Evidence Fusion</button>
                </div>
            </div>
        `).join('');
    } catch (err) {
        console.error(err);
    }
}

function selectActiveCase(caseId) {
    document.getElementById('header-active-case').innerText = `ACTIVE CASE: ${caseId}`;
    switchTab('graph');
}

function openCreateCaseModal() {
    const modal = document.getElementById('create-case-modal');
    if (modal) modal.style.display = 'flex';
}

function closeCreateCaseModal() {
    const modal = document.getElementById('create-case-modal');
    if (modal) modal.style.display = 'none';
}

async function submitNewCase(e) {
    e.preventDefault();
    const title = document.getElementById('case-input-title').value.trim();
    const subject_name = document.getElementById('case-input-subject').value.trim();
    const investigator = document.getElementById('case-input-investigator').value.trim();
    const agency = document.getElementById('case-input-agency').value.trim();
    const priority = document.getElementById('case-input-priority').value;
    const description = document.getElementById('case-input-desc').value.trim();

    try {
        const res = await fetch('/api/cases', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, subject_name, investigator, agency, priority, description })
        });
        const data = await res.json();
        if (data.success) {
            alert(`✅ Case Registered Successfully!\n\nCase ID: ${data.case.id}\nStatus: Active Investigation logged on Blockchain Ledger.`);
            closeCreateCaseModal();
            loadInvestigationsData();
            loadOverviewData();
        }
    } catch (err) {
        console.error(err);
        alert('Failed to register case.');
    }
}

// 3. Interactive Network Graph Loader (Vis.js Canvas)
let visNetworkInstance = null;

async function loadGraphData() {
    try {
        const res = await fetch('/api/graph');
        const data = await res.json();

        const container = document.getElementById('graph-canvas');
        if (!container) return;

        const visNodes = data.nodes.map(n => ({
            id: n.id,
            label: `${n.label}\n(${n.type})`,
            shape: getNodeShape(n.type),
            color: getNodeColor(n.type),
            font: { color: '#0f172a', size: 12, strokeWidth: 2, strokeColor: '#ffffff' }
        }));

        const visEdges = data.edges.map(e => ({
            from: e.source,
            to: e.target,
            label: e.relation,
            arrows: 'to',
            color: { color: getDomainColor(e.domain) },
            font: { color: '#475569', size: 9, strokeWidth: 2, strokeColor: '#ffffff' }
        }));

        const visData = { nodes: new vis.DataSet(visNodes), edges: new vis.DataSet(visEdges) };
        const options = {
            nodes: { borderWidth: 2 },
            physics: { barnesHut: { gravitationalConstant: -3000, springLength: 95 } },
            interaction: { hover: true, tooltipDelay: 200 }
        };

        if (visNetworkInstance) visNetworkInstance.destroy();
        visNetworkInstance = new vis.Network(container, visData, options);

        visNetworkInstance.on('selectNode', function(params) {
            const nodeId = params.nodes[0];
            const entity = data.nodes.find(n => n.id === nodeId);
            if (entity) showEntityDrawer(entity);
        });

    } catch (err) {
        console.error('Failed to render graph:', err);
    }
}

function getNodeShape(type) {
    if (type === 'PERSON') return 'dot';
    if (type === 'PHONE' || type === 'DEVICE') return 'diamond';
    if (type === 'BANK_ACCOUNT' || type === 'CRYPTO_WALLET') return 'square';
    if (type === 'VEHICLE') return 'triangle';
    if (type === 'CAMERA' || type === 'LOCATION') return 'star';
    return 'ellipse';
}

function getNodeColor(type) {
    if (type === 'PERSON') return { background: '#ef4444', border: '#b91c1c' };
    if (type === 'PHONE') return { background: '#0284c7', border: '#0369a1' };
    if (type === 'BANK_ACCOUNT') return { background: '#16a34a', border: '#15803d' };
    if (type === 'CRYPTO_WALLET') return { background: '#d97706', border: '#b45309' };
    if (type === 'VEHICLE') return { background: '#7c3aed', border: '#6d28d9' };
    if (type === 'CAMERA') return { background: '#db2777', border: '#be185d' };
    return { background: '#2563eb', border: '#1d4ed8' };
}

function getDomainColor(domain) {
    if (domain === 'COMMUNICATION') return '#0284c7';
    if (domain === 'FINANCIAL') return '#16a34a';
    if (domain === 'BLOCKCHAIN') return '#d97706';
    if (domain === 'DVR') return '#db2777';
    if (domain === 'OSINT') return '#7c3aed';
    return '#64748b';
}

function showEntityDrawer(entity) {
    const drawer = document.getElementById('entity-drawer');
    if (!drawer) return;
    drawer.style.display = 'block';
    document.getElementById('drawer-entity-name').innerText = entity.label;
    document.getElementById('drawer-entity-type').innerText = entity.type;
    document.getElementById('drawer-entity-risk').innerText = `${entity.risk_score}/100`;
    document.getElementById('drawer-entity-status').innerText = entity.status;
    document.getElementById('drawer-entity-details').innerText = entity.details;
}

// 4. Multi-Domain Timeline Loader
async function loadTimelineData() {
    try {
        const res = await fetch('/api/timeline');
        const data = await res.json();
        const container = document.getElementById('timeline-container');
        if (!container) return;

        container.innerHTML = data.events.map(ev => `
            <div class="timeline-item">
                <div style="font-size: 11px; color: #2563eb; font-weight: 700;">[${ev.domain}] ${ev.timestamp}</div>
                <div style="font-size: 13px; font-weight: 700; color: #0f172a; margin: 2px 0;">${ev.title}</div>
                <div style="font-size: 12px; color: #475569;">${ev.details}</div>
                <span class="badge badge-verified" style="margin-top: 4px;">Source Ref: ${ev.evidence_id}</span>
            </div>
        `).join('');
    } catch (err) {
        console.error('Failed to load timeline:', err);
    }
}

// 5. Evidence Center Loader
async function loadEvidenceData() {
    try {
        const res = await fetch('/api/evidence');
        const data = await res.json();
        const tbody = document.getElementById('evidence-tbody');
        if (!tbody) return;

        tbody.innerHTML = data.evidence_items.map(e => `
            <tr>
                <td><strong>${e.id}</strong></td>
                <td><span class="badge badge-verified">${e.evidence_type}</span></td>
                <td>${e.title}</td>
                <td>${e.source}</td>
                <td><code style="font-size: 11px; color: #2563eb; font-weight: 600;">${e.file_hash.substring(0, 16)}...</code></td>
                <td><span class="badge ${e.integrity_status === 'VERIFIED' ? 'badge-verified' : 'badge-high'}">${e.integrity_status}</span></td>
                <td>${e.provenance}</td>
            </tr>
        `).join('');
    } catch (err) {
        console.error('Failed to load evidence:', err);
    }
}

// 6. Communications Loader
async function loadCommunicationsData() {
    try {
        const res = await fetch('/api/communications');
        const data = await res.json();
        const container = document.getElementById('comm-flagged-list');
        if (container) {
            container.innerHTML = data.communication_edges.map(c => `
                <div style="padding: 12px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; margin-bottom: 8px; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">
                    <div style="font-weight: 700; color: #0284c7; font-size: 13px;">📞 ${c.source} ➔ ${c.target}</div>
                    <div style="font-size: 12px; color: #475569; margin-top: 4px;">${c.details}</div>
                    <div style="font-size: 11px; color: #d97706; font-weight: 700; margin-top: 4px;">FLAGGED PATTERN: Pre-Incident Burst (14 Calls)</div>
                </div>
            `).join('');
        }
    } catch (err) {
        console.error(err);
    }
}

// 7. Financial Intelligence Loader
async function loadFinancialData() {
    try {
        const res = await fetch('/api/financial');
        const data = await res.json();
        const container = document.getElementById('fin-list');
        if (container) {
            container.innerHTML = data.financial_edges.map(f => `
                <div style="padding: 12px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; margin-bottom: 8px; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">
                    <div style="font-weight: 700; color: #16a34a; font-size: 13px;">💳 ${f.source} ➔ ${f.target}</div>
                    <div style="font-size: 12px; color: #475569; margin-top: 4px;">${f.details}</div>
                    <span class="badge badge-high" style="margin-top: 4px;">HAWALA INDICATOR: Rapid Off-Market Layering</span>
                </div>
            `).join('');
        }
    } catch (err) {
        console.error(err);
    }
}

// 8. Blockchain Loader
async function loadBlockchainData() {
    try {
        const res = await fetch('/api/blockchain');
        const data = await res.json();
        const container = document.getElementById('blk-list');
        if (container) {
            container.innerHTML = data.blockchain_edges.map(b => `
                <div style="padding: 12px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; margin-bottom: 8px; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">
                    <div style="font-weight: 700; color: #d97706; font-size: 13px;">⛓️ ${b.source} ➔ ${b.target}</div>
                    <div style="font-size: 12px; color: #475569; margin-top: 4px;">${b.details}</div>
                </div>
            `).join('');
        }
    } catch (err) {
        console.error(err);
    }
}

// 9. OSINT Loader
async function loadOSINTData() {
    try {
        const res = await fetch('/api/osint');
        const data = await res.json();
        const container = document.getElementById('osint-list');
        if (container) {
            container.innerHTML = data.osint_edges.map(o => `
                <div style="padding: 12px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; margin-bottom: 8px; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">
                    <div style="font-weight: 700; color: #7c3aed; font-size: 13px;">🌐 Public Correlation: ${o.source} ➔ ${o.target}</div>
                    <div style="font-size: 12px; color: #475569; margin-top: 4px;">${o.details}</div>
                </div>
            `).join('');
        }
    } catch (err) {
        console.error(err);
    }
}

// 10. DVR Loader
async function loadDVRData() {
    try {
        const res = await fetch('/api/dvr');
        const data = await res.json();
        const container = document.getElementById('dvr-list');
        if (container) {
            container.innerHTML = data.dvr_edges.map(d => `
                <div style="padding: 12px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; margin-bottom: 8px; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">
                    <div style="font-weight: 700; color: #db2777; font-size: 13px;">📹 Cam C12 Detection: ${d.source} ➔ ${d.target}</div>
                    <div style="font-size: 12px; color: #475569; margin-top: 4px;">${d.details}</div>
                </div>
            `).join('');
        }
    } catch (err) {
        console.error(err);
    }
}

// 11. Analytics & XAI Loader
async function loadAnalyticsData() {
    try {
        const res = await fetch('/api/graph');
        const data = await res.json();
        const tbody = document.getElementById('analytics-tbody');
        if (tbody && data.analytics && data.analytics.influential_entities) {
            tbody.innerHTML = data.analytics.influential_entities.map(e => `
                <tr>
                    <td><strong>${e.label}</strong></td>
                    <td>${e.type}</td>
                    <td>${e.degree_centrality}</td>
                    <td>${e.betweenness_centrality}</td>
                    <td>${e.pagerank}</td>
                    <td><span class="badge ${e.influence_score > 0.08 ? 'badge-high' : 'badge-verified'}">${e.assessment}</span></td>
                </tr>
            `).join('');
        }
    } catch (err) {
        console.error(err);
    }
}

// 12. Evidence Fusion & Lead Generator Loader
async function loadFusionData() {
    try {
        const res = await fetch('/api/fusion');
        const data = await res.json();
        const container = document.getElementById('fusion-chain-container');
        if (!container) return;

        container.innerHTML = `
            <div class="xai-box">
                <div class="xai-title">🧠 EXPLAINABLE AI SYNTHESIS (XAI)</div>
                <div style="font-size: 13px; font-weight: 700; margin-bottom: 6px; color: #0f172a;">WHAT WAS FOUND:</div>
                <p style="font-size: 12px; color: #334155; margin-bottom: 10px;">${data.explainable_ai.WHAT}</p>

                <div style="font-size: 13px; font-weight: 700; margin-bottom: 6px; color: #0f172a;">WHY IT WAS FLAGGED:</div>
                <p style="font-size: 12px; color: #475569; margin-bottom: 10px;">${data.explainable_ai.WHY}</p>

                <div class="xai-grid">
                    <div><strong>WHEN:</strong> ${data.explainable_ai.WHEN}</div>
                    <div><strong>WHERE:</strong> ${data.explainable_ai.WHERE}</div>
                    <div><strong>CONFIDENCE SCORE:</strong> <span style="color: #16a34a; font-weight: bold;">${data.explainable_ai.CONFIDENCE}</span></div>
                    <div><strong>LIMITATION:</strong> ${data.explainable_ai.LIMITATION}</div>
                </div>
            </div>

            <h4 style="margin: 20px 0 10px 0; font-size: 14px; color: #0284c7;">🔗 6-Hop Cross-Domain Evidence Chain:</h4>
            ${data.evidence_chain.map(c => `
                <div style="padding: 12px; background: #ffffff; border: 1px solid #e2e8f0; border-left: 4px solid #0284c7; border-radius: 8px; margin-bottom: 8px; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">
                    <div style="font-size: 12px; font-weight: 700; color: #0284c7;">Step ${c.step_index}: [${c.domain}] ${c.title}</div>
                    <div style="font-size: 13px; margin: 4px 0; color: #0f172a;"><strong>${c.from_entity}</strong> ➔ <strong>${c.to_entity}</strong></div>
                    <div style="font-size: 12px; color: #475569;">${c.details}</div>
                    <span class="badge badge-verified" style="margin-top: 4px;">Ref: ${c.evidence_ref}</span>
                </div>
            `).join('')}
        `;
    } catch (err) {
        console.error(err);
    }
}

// 13. Blockchain Audit Ledger Loader & Tamper Simulation
async function loadAuditData() {
    try {
        const res = await fetch('/api/audit');
        const data = await res.json();

        const statusEl = document.getElementById('blockchain-status');
        if (statusEl) {
            if (data.integrity_verification.is_valid) {
                statusEl.className = 'badge badge-verified';
                statusEl.innerText = '✅ ALL AUDIT BLOCKS VERIFIED IMMUTABLE & SECURE';
            } else {
                statusEl.className = 'badge badge-high';
                statusEl.innerText = `🚨 TAMPER ALERT: ${data.integrity_verification.reason}`;
            }
        }

        const tbody = document.getElementById('audit-tbody');
        if (tbody) {
            tbody.innerHTML = data.blockchain_audit.map(b => `
                <tr>
                    <td>#${b.index}</td>
                    <td>${b.timestamp}</td>
                    <td><strong>${b.action_type}</strong></td>
                    <td>${b.actor}</td>
                    <td><code style="font-size: 11px; color: #2563eb; font-weight: 600;">${b.block_hash.substring(0, 16)}...</code></td>
                    <td><button class="btn btn-secondary" style="padding: 4px 8px; font-size: 11px;" onclick="simulateBlockTamper(${b.index})">Corrupt Payload</button></td>
                </tr>
            `).join('');
        }
    } catch (err) {
        console.error(err);
    }
}

async function simulateBlockTamper(blockIndex) {
    try {
        const res = await fetch('/api/audit/tamper', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ block_index: blockIndex, field_to_tamper: 'title', tampered_value: '[TAMPERED / ALTERED RECORD]' })
        });
        const data = await res.json();
        alert(`🚨 TAMPER SIMULATION EXECUTED ON BLOCK #${blockIndex}!\n\nAudit Status: ${data.audit_verification.is_valid ? 'VALID' : 'FAILED - TAMPER DETECTED'}\nReason: ${data.audit_verification.reason || 'None'}`);
        loadAuditData();
    } catch (err) {
        console.error(err);
    }
}

// 14. Reports Loader
async function loadReportData() {
    try {
        const res = await fetch('/api/reports/generate', { method: 'POST' });
        const data = await res.json();
        const previewer = document.getElementById('report-preview-frame');
        if (previewer) {
            previewer.srcdoc = data.html_content;
        }
    } catch (err) {
        console.error(err);
    }
}

// Global Search
function initGlobalSearch() {
    const input = document.getElementById('global-search-input');
    if (!input) return;

    input.addEventListener('keypress', async (e) => {
        if (e.key === 'Enter') {
            const query = input.value.trim();
            if (!query) return;
            const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
            const data = await res.json();
            alert(`🔍 Search Results for "${query}":\nEntities Found: ${data.matched_nodes.length}\nEvidence Items: ${data.matched_evidence.length}\nRelationships: ${data.matched_relationships.length}`);
        }
    });
}
