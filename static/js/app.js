// TRACE-X Intelligence Workstation Application Controller
let currentCaseId = 'TRX-2026-017';
let currentPersonId = 'person_arjun_sharma';
let currentGraphLayout = 'tree-ud';
let currentPersonDrawerId = null;
let currentDrawerTab = 'overview';
let visNetworkInstance = null;
let currentGraphData = null;

document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initGlobalSearch();
    loadOverviewData();
});

function toggleSidebar() {
    const sidebar = document.getElementById('app-sidebar');
    if (sidebar) sidebar.classList.toggle('collapsed');
}

function changeActiveCase(caseId) {
    currentCaseId = caseId;
    updateBreadcrumb();
    refreshActiveView();
}

function changeActivePerson(personId) {
    currentPersonId = personId;
    
    const personNames = {
        'person_arjun_sharma': 'Arjun Sharma',
        'person_rohan_mehta': 'Rohan Mehta',
        'person_priya_joshi': 'Priya Joshi',
        'person_vikram_patil': 'Vikram Patil',
        'person_neha_kulkarni': 'Neha Kulkarni',
        'person_arjun_s_candidate': 'Arjun S. (Ambiguous Match)'
    };
    const pName = personNames[personId] || personId;
    updateBreadcrumb();
    refreshActiveView();
}

function updateBreadcrumb() {
    const activeNav = document.querySelector('.nav-item.active');
    const moduleName = activeNav ? activeNav.innerText.trim().toUpperCase() : 'OVERVIEW';
    const selectP = document.getElementById('select-change-person');
    const pName = selectP ? selectP.options[selectP.selectedIndex].text.split('(')[0].trim().toUpperCase() : 'ARJUN SHARMA';
    
    document.getElementById('breadcrumb-text').innerText = `CASE > ${currentCaseId} > ${pName} > ${moduleName}`;
}

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
        updateBreadcrumb();
        
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

function refreshActiveView() {
    const activeNav = document.querySelector('.nav-item.active');
    if (activeNav) {
        switchTab(activeNav.getAttribute('data-tab'));
    }
}

// 1. DASHBOARD / OVERVIEW
async function loadOverviewData() {
    try {
        const res = await fetch(`/api/overview?case_id=${currentCaseId}&person_id=${currentPersonId}`);
        const data = await res.json();

        const actList = document.getElementById('activity-feed');
        if (actList && data.investigation_activity) {
            actList.innerHTML = data.investigation_activity.map(act => `
                <div style="padding: 10px 0; border-bottom: 1px solid #e2e8f0; display: flex; justify-content: space-between; font-size: 11px;">
                    <span>⚡ <strong style="color: #0f172a;">[${act.time}]</strong> ${act.event}</span>
                    <span class="badge badge-verified">${act.domain}</span>
                </div>
            `).join('');
        }

        const leadsPanel = document.getElementById('ai-leads-panel');
        if (leadsPanel && data.ai_leads) {
            leadsPanel.innerHTML = data.ai_leads.map(lead => `
                <div style="padding: 12px; background: #f0f9ff; border-left: 3px solid #0284c7; border-radius: 8px; margin-bottom: 8px;">
                    <div style="font-size: 12px; font-weight: 800; color: #0369a1;">${lead.title}</div>
                    <p style="font-size: 11px; color: #475569; margin: 4px 0;">${lead.summary}</p>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 4px;">
                        <span class="badge ${lead.confidence < 0.5 ? 'badge-high' : 'badge-verified'}">CONFIDENCE: ${Math.round(lead.confidence * 100)}%</span>
                        <span style="font-size: 10px; color: #64748b; font-weight: 700;">Status: ${lead.status}</span>
                    </div>
                </div>
            `).join('');
        }
    } catch (err) {
        console.error(err);
    }
}

// 2. INVESTIGATIONS SECTION (6 SEEDED CASES)
async function loadInvestigationsData() {
    try {
        const res = await fetch('/api/cases');
        const data = await res.json();
        const container = document.getElementById('cases-list-container');
        if (!container) return;

        container.innerHTML = data.cases.map(c => {
            const primary = c.primary_suspect || {};
            const secondaries = c.secondary_suspects || [];

            return `
                <div class="card" style="border-left: 4px solid ${c.priority === 'High' ? '#dc2626' : '#2563eb'};">
                    <div class="card-title">
                        <span>${c.id}: ${c.title} (${c.location})</span>
                        <span class="badge ${c.priority === 'High' ? 'badge-high' : 'badge-verified'}">${c.status}</span>
                    </div>

                    <!-- PRIMARY SUBJECT IDENTITY CARD -->
                    <div class="suspect-card" onclick="openPersonDrawer('${primary.id}')" style="cursor: pointer;">
                        <img src="${primary.photo_url || 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=300'}" class="suspect-avatar">
                        <div>
                            <div style="font-size: 14px; font-weight: 800; color: #0f172a;">${primary.name} <span class="badge badge-high" style="font-size: 9px;">Primary Subject</span></div>
                            <div style="font-size: 11px; color: #475569; margin: 2px 0;">Age: <strong>${primary.age || 34}</strong> | City: <strong>${primary.city || 'Pune'}</strong> | Occupation: <strong>${primary.occupation || 'Consultant'}</strong></div>
                            <div style="font-size: 11px; color: #2563eb;">📞 ${primary.phone} | ✉️ ${primary.email}</div>
                        </div>
                    </div>

                    <!-- SECONDARY SUBJECTS -->
                    ${secondaries.length > 0 ? `
                        <div style="font-size: 10px; font-weight: 800; color: #0284c7; text-transform: uppercase; margin: 10px 0 6px 0;">👥 Persons of Interest & Associates (${secondaries.length}):</div>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 8px; margin-bottom: 10px;">
                            ${secondaries.map(sec => `
                                <div style="padding: 8px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; display: flex; gap: 8px; align-items: center; cursor: pointer;" onclick="openPersonDrawer('${sec.id}')">
                                    <img src="${sec.photo_url || 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=300'}" style="width: 36px; height: 36px; border-radius: 50%; object-fit: cover;">
                                    <div>
                                        <div style="font-size: 12px; font-weight: 700; color: #0f172a;">${sec.name}</div>
                                        <div style="font-size: 10px; color: #0284c7;">${sec.role}</div>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    ` : ''}

                    <div style="display: grid; grid-template-columns: repeat(6, 1fr); gap: 8px; font-size: 11px; color: #475569; margin: 8px 0;">
                        <div>Evidence: <strong>${c.evidence_count || 148}</strong></div>
                        <div>Relationships: <strong>${c.relationships_count || 37}</strong></div>
                        <div>Calls: <strong>${c.communications_count || 421}</strong></div>
                        <div>Financial: <strong>${c.financial_count || 63}</strong></div>
                        <div>OSINT: <strong>${c.osint_count || 42}</strong></div>
                        <div>CCTV: <strong>${c.cctv_count || 9}</strong></div>
                    </div>

                    <p style="font-size: 11px; color: #475569; margin-bottom: 10px;">${c.description}</p>
                    <div style="display: flex; gap: 8px;">
                        <button class="btn" onclick="selectCaseAndPerson('${c.id}', '${primary.id}')">OPEN CASE WORKSPACE</button>
                    </div>
                </div>
            `;
        }).join('');
    } catch (err) {
        console.error(err);
    }
}

function selectCaseAndPerson(caseId, personId) {
    currentCaseId = caseId;
    currentPersonId = personId;
    document.getElementById('select-change-case').value = caseId;
    changeActivePerson(personId);
    switchTab('fusion');
}

// 3. EVIDENCE CENTER
async function loadEvidenceData() {
    try {
        const res = await fetch(`/api/evidence?case_id=${currentCaseId}`);
        const data = await res.json();
        const tbody = document.getElementById('evidence-tbody');
        if (!tbody) return;

        tbody.innerHTML = data.evidence_items.map(e => `
            <tr style="cursor: pointer;" onclick="openEvidenceDetailModal('${e.id}')">
                <td><strong style="color: #2563eb;">${e.id}</strong></td>
                <td><span class="badge badge-verified">${e.evidence_type}</span></td>
                <td><strong>${e.title}</strong></td>
                <td>${e.source}</td>
                <td><code style="font-size: 10px; color: #2563eb;">${e.file_hash.substring(0, 14)}...</code></td>
                <td><span class="badge badge-verified">${e.integrity_status}</span></td>
                <td><button class="btn btn-secondary" style="padding: 2px 8px; font-size: 10px;" onclick="event.stopPropagation(); openEvidenceDetailModal('${e.id}')">View Drawer</button></td>
            </tr>
        `).join('');
    } catch (err) {
        console.error(err);
    }
}

// STANDARDIZED EVIDENCE DETAIL DRAWER MODAL (MASTER PROMPT REQUIREMENT 22)
async function openEvidenceDetailModal(evidenceId) {
    const modal = document.getElementById('evidence-detail-modal');
    if (!modal) return;
    modal.style.display = 'flex';

    try {
        const res = await fetch(`/api/evidence/${evidenceId}`);
        const e = await res.json();

        document.getElementById('evidence-modal-body').innerHTML = `
            <div style="padding: 14px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; margin-bottom: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span style="font-size: 14px; font-weight: 800; color: #2563eb;">${e.id}: ${e.title}</span>
                    <span class="badge badge-verified">${e.evidence_type}</span>
                </div>
                <div style="font-size: 11px; color: #475569; display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 8px;">
                    <div><strong>Case:</strong> ${e.case_id}</div>
                    <div><strong>Associated Person:</strong> Arjun Sharma</div>
                    <div><strong>Source:</strong> ${e.source}</div>
                    <div><strong>Timestamp:</strong> ${e.acquisition_timestamp}</div>
                    <div><strong>SHA-256 Hash:</strong> <code style="color: #2563eb;">${e.file_hash.substring(0, 16)}...</code></div>
                    <div><strong>Integrity Status:</strong> <span class="badge badge-verified">${e.integrity_status}</span></div>
                </div>
                <p style="font-size: 11px; color: #0f172a;"><strong>Analyst Notes / Description:</strong> ${e.analyst_notes}</p>
                <div style="margin-top: 8px; font-size: 10px; color: #64748b;">
                    <strong>AI Extracted Entities:</strong> ${(e.extracted_entities || []).join(', ')}
                </div>
            </div>

            <!-- BUTTONS REQUIRED BY POINT 22 -->
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 10px;">
                <button class="btn btn-secondary" onclick="alert('Viewing original SHA-256 file payload for ${e.id}...')">📄 View Original</button>
                <button class="btn btn-secondary" onclick="switchTab('graph'); closeEvidenceDetailModal();">🕸️ View Graph Connection</button>
                <button class="btn btn-secondary" onclick="switchTab('timeline'); closeEvidenceDetailModal();">⏱️ View Timeline</button>
                <button class="btn btn-secondary" onclick="alert('Note added to ${e.id} on SHA-256 ledger.')">✏️ Add Note</button>
                <button class="btn" style="background: #16a34a;" onclick="alert('Evidence ${e.id} Marked Verified!')">✅ Mark Verified</button>
                <button class="btn" style="background: #d97706;" onclick="alert('Evidence ${e.id} Flagged for Review!')">⚠️ Mark Needs Review</button>
            </div>
        `;
    } catch (err) {
        console.error(err);
    }
}

function closeEvidenceDetailModal() {
    const modal = document.getElementById('evidence-detail-modal');
    if (modal) modal.style.display = 'none';
}

// 4. EVIDENCE FUSION WORKSPACE & AI LEADS
async function loadFusionData() {
    try {
        const res = await fetch(`/api/fusion?case_id=${currentCaseId}&person_id=${currentPersonId}`);
        const data = await res.json();
        const container = document.getElementById('fusion-chain-container');
        if (!container) return;

        container.innerHTML = `
            <div class="xai-box">
                <div class="xai-title">🧠 EXPLAINABLE AI EVIDENCE CHAIN SYNTHESIS</div>
                <p style="font-size: 11px; color: #475569; margin-bottom: 8px;">${data.explainable_ai.WHAT}</p>
                <div class="xai-grid">
                    <div><strong>WHY FLAGGED:</strong> ${data.explainable_ai.WHY}</div>
                    <div><strong>CONFIDENCE SCORE:</strong> <span style="color: #16a34a; font-weight: bold;">${data.explainable_ai.CONFIDENCE}</span></div>
                </div>
            </div>

            <!-- DEFAULT TREE VISUALIZATION (MASTER PROMPT REQUIREMENT 8) -->
            <h4 style="margin: 16px 0 8px 0; font-size: 13px; color: #0284c7;">Default Investigation Tree Representation:</h4>
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px; font-family: monospace; font-size: 12px; margin-bottom: 16px;">
                <div style="font-weight: 800; color: #2563eb;">ARJUN SHARMA (Primary Subject)</div>
                <div>│</div>
                <div>├── <span style="cursor: pointer; color: #0284c7; font-weight: 700;" onclick="openRelEvidenceModal('rel_1')">ROHAN MEHTA (Business Contact - 27 Calls logged)</span></div>
                <div>│</div>
                <div>├── <span style="cursor: pointer; color: #0284c7; font-weight: 700;" onclick="openRelEvidenceModal('rel_2')">PRIYA JOSHI (Associate - Senior Accountant)</span></div>
                <div>│</div>
                <div>├── <span style="cursor: pointer; color: #0284c7; font-weight: 700;" onclick="openRelEvidenceModal('rel_3')">MH12 AB 4821 (SUV Vehicle - ANPR Match)</span></div>
                <div>│</div>
                <div>├── <span style="cursor: pointer; color: #16a34a; font-weight: 700;" onclick="switchTab('financial')">BANK ACCOUNT (HDFC Acc XXXX 4821)</span></div>
                <div>│</div>
                <div>├── <span style="cursor: pointer; color: #d97706; font-weight: 700;" onclick="switchTab('blockchain')">CRYPTO WALLET (0xDEMO...A721 - Balance 8.42 ETH)</span></div>
                <div>│</div>
                <div>├── <span style="cursor: pointer; color: #db2777; font-weight: 700;" onclick="switchTab('dvr')">LOCATIONS (Synthetic Pune Location A)</span></div>
                <div>│</div>
                <div>└── <span style="cursor: pointer; color: #dc2626; font-weight: 700;" onclick="switchTab('timeline')">INCIDENTS (Cyber Incident #1042)</span></div>
            </div>

            <h4 style="margin: 16px 0 8px 0; font-size: 13px; color: #0284c7;">5 Seeded AI Investigative Leads:</h4>
            ${DATASTORE ? '' : ''}
        `;

        // Render AI leads
        const leadsRes = await fetch('/api/leads');
        const leadsData = await leadsRes.json();
        
        container.innerHTML += leadsData.leads.map(lead => `
            <div style="padding: 12px; background: #ffffff; border: 1px solid #e2e8f0; border-left: 4px solid ${lead.confidence < 0.5 ? '#dc2626' : '#2563eb'}; border-radius: 8px; margin-bottom: 8px; box-shadow: 0 1px 2px rgba(0,0,0,0.04);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 13px; font-weight: 800; color: #0f172a;">${lead.id}: ${lead.title}</span>
                    <span class="badge ${lead.confidence < 0.5 ? 'badge-high' : 'badge-verified'}">Confidence: ${Math.round(lead.confidence * 100)}%</span>
                </div>
                <p style="font-size: 11px; color: #475569; margin: 4px 0;">${lead.summary}</p>
                <div style="font-size: 10px; color: #2563eb; margin: 4px 0;"><strong>Supporting Evidence:</strong> ${(lead.supporting_evidence || []).join(', ')}</div>
                <div style="font-size: 10px; color: #d97706;"><strong>Alternative Explanation:</strong> ${lead.alternative_explanation || 'Business coordination.'}</div>
                <div style="margin-top: 6px; font-size: 10px; color: #64748b; font-weight: 700;">Status: ${lead.status}</div>
            </div>
        `).join('');

    } catch (err) {
        console.error(err);
    }
}

// 5. NETWORK GRAPH — TREE VIEW DEFAULT & LAYOUT SWITCHER
async function loadGraphData() {
    try {
        const res = await fetch(`/api/graph?case_id=${currentCaseId}&person_id=${currentPersonId}`);
        currentGraphData = await res.json();
        renderGraphWithLayout(currentGraphLayout);
    } catch (err) {
        console.error(err);
    }
}

function changeGraphLayout(layoutType) {
    currentGraphLayout = layoutType;
    document.querySelectorAll('.graph-layout-btn').forEach(btn => btn.classList.remove('active'));
    
    const activeBtn = document.getElementById(`btn-layout-${layoutType}`);
    if (activeBtn) activeBtn.classList.add('active');

    renderGraphWithLayout(layoutType);
}

function focusSelectedPerson() {
    if (!currentGraphData) return;
    renderGraphWithLayout(currentGraphLayout, true);
}

function renderGraphWithLayout(layoutType, focusMode = false) {
    if (!currentGraphData) return;
    const container = document.getElementById('graph-canvas');
    if (!container) return;

    let nodesToRender = currentGraphData.nodes;
    let edgesToRender = currentGraphData.edges;

    if (focusMode || currentPersonId) {
        const connectedEdges = currentGraphData.edges.filter(e => e.source === currentPersonId || e.target === currentPersonId);
        const connectedNodeIds = new Set([currentPersonId]);
        connectedEdges.forEach(e => {
            connectedNodeIds.add(e.source);
            connectedNodeIds.add(e.target);
        });
        nodesToRender = currentGraphData.nodes.filter(n => connectedNodeIds.has(n.id));
        edgesToRender = connectedEdges;
    }

    const visNodes = nodesToRender.map(n => ({
        id: n.id,
        label: `${n.label}\n[${n.type}]`,
        shape: getNodeShape(n.type),
        color: getNodeColor(n.type),
        font: { color: '#0f172a', size: 10, strokeWidth: 2, strokeColor: '#ffffff', face: 'Inter' },
        level: n.tree_level !== undefined ? n.tree_level : 2
    }));

    const visEdges = edgesToRender.map(e => ({
        id: e.id,
        from: e.source,
        to: e.target,
        label: e.relation,
        arrows: 'to',
        color: { color: getDomainColor(e.domain) },
        font: { color: '#475569', size: 8, strokeWidth: 2, strokeColor: '#ffffff' },
        length: 50
    }));

    const visData = { nodes: new vis.DataSet(visNodes), edges: new vis.DataSet(visEdges) };

    let layoutConfig = {};
    let physicsConfig = { enabled: true };

    if (layoutType === 'tree-ud') {
        layoutConfig = { hierarchical: { direction: 'UD', sortMethod: 'directed', nodeSpacing: 70, levelSeparation: 80 } };
        physicsConfig = { enabled: false };
    } else if (layoutType === 'radial') {
        layoutConfig = { randomSeed: 42 };
        physicsConfig = { barnesHut: { gravitationalConstant: -1000, centralGravity: 0.5, springLength: 40 } };
    } else if (layoutType === 'hierarchy') {
        layoutConfig = { hierarchical: { direction: 'LR', sortMethod: 'directed', nodeSpacing: 60, levelSeparation: 90 } };
        physicsConfig = { enabled: false };
    } else {
        layoutConfig = { randomSeed: 100 };
        physicsConfig = { barnesHut: { gravitationalConstant: -1500, springLength: 40 } };
    }

    const options = {
        nodes: { borderWidth: 2 },
        layout: layoutConfig,
        physics: physicsConfig,
        interaction: { hover: true, tooltipDelay: 150 }
    };

    if (visNetworkInstance) visNetworkInstance.destroy();
    visNetworkInstance = new vis.Network(container, visData, options);

    visNetworkInstance.on('selectNode', function(params) {
        const nodeId = params.nodes[0];
        openPersonDrawer(nodeId);
    });

    visNetworkInstance.on('selectEdge', function(params) {
        if (params.nodes.length === 0 && params.edges.length > 0) {
            const edgeId = params.edges[0];
            openRelEvidenceModal(edgeId);
        }
    });
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

// 6. COMMUNICATIONS (POPULATED)
async function loadCommunicationsData() {
    try {
        const res = await fetch(`/api/communications?person_id=${currentPersonId}`);
        const data = await res.json();

        document.getElementById('comm-stat-calls').innerText = data.total_calls;
        document.getElementById('comm-stat-msgs').innerText = data.total_messages;
        document.getElementById('comm-stat-contacts').innerText = data.unique_contacts;
        document.getElementById('comm-stat-last').innerText = data.last_contact;

        const tree = document.getElementById('comm-contact-tree');
        if (tree && data.contacts) {
            tree.innerHTML = data.contacts.map(c => `
                <div style="padding: 10px; background: #f8fafc; border: 1px solid #e2e8f0; border-left: 3px solid #0284c7; border-radius: 8px; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="font-size: 12px; color: #0f172a;">${c.name}</strong> (${c.role})
                        <div style="font-size: 10px; color: #0284c7;">📞 ${c.phone}</div>
                    </div>
                    <span class="badge badge-verified">${c.calls} Calls Logged</span>
                </div>
            `).join('');
        }

        const timeline = document.getElementById('comm-rohan-timeline');
        if (timeline && data.rohan_call_timeline) {
            timeline.innerHTML = data.rohan_call_timeline.map(t => `
                <div style="padding: 8px 12px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; margin-bottom: 4px; display: flex; justify-content: space-between; font-size: 11px;">
                    <span>⏱️ <strong>${t.timestamp}</strong></span>
                    <span style="color: ${t.direction === 'Outgoing' ? '#2563eb' : '#16a34a'}; font-weight: 700;">${t.direction} (Duration: ${t.duration})</span>
                    <span class="badge badge-verified" style="cursor: pointer;" onclick="openEvidenceDetailModal('${t.evidence_id}')">Ref: ${t.evidence_id}</span>
                </div>
            `).join('');
        }
    } catch (err) {
        console.error(err);
    }
}

// 7. FINANCIAL INTELLIGENCE & HAWALA ANALYSIS
async function loadFinancialData() {
    try {
        const res = await fetch(`/api/financial?person_id=${currentPersonId}`);
        const data = await res.json();

        const grid = document.getElementById('fin-accounts-grid');
        if (grid && data.accounts) {
            grid.innerHTML = data.accounts.map(a => `
                <div style="padding: 12px; background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px;">
                    <div style="font-size: 12px; font-weight: 800; color: #166534;">${a.bank} (${a.account_number})</div>
                    <div style="font-size: 11px; color: #475569;">Type: ${a.type} | Current Balance: <strong style="color: #16a34a;">${a.balance}</strong></div>
                </div>
            `).join('');
        }

        const hawala = document.getElementById('fin-hawala-box');
        if (hawala && data.hawala_analysis) {
            hawala.innerHTML = `
                <div class="xai-title">⚠️ INFORMAL VALUE TRANSFER INDICATORS (HAWALA ANALYSIS)</div>
                <div style="font-size: 12px; font-weight: 700; color: #0f172a; margin-bottom: 4px;">Assessment: ${data.hawala_analysis.title} (Confidence: ${data.hawala_analysis.confidence})</div>
                <p style="font-size: 11px; color: #475569; margin-bottom: 8px;">${data.hawala_analysis.explanation}</p>
                <div style="font-size: 11px; color: #0284c7; display: flex; flex-direction: column; gap: 4px;">
                    ${data.hawala_analysis.indicators.map(i => `<div>● ${i}</div>`).join('')}
                </div>
            `;
        }

        const txList = document.getElementById('fin-transactions-list');
        if (txList && data.transactions) {
            txList.innerHTML = data.transactions.map(t => `
                <div style="padding: 10px; background: #ffffff; border: 1px solid #e2e8f0; border-left: 3px solid ${t.type === 'Outgoing' ? '#dc2626' : '#16a34a'}; border-radius: 8px; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-size: 12px; font-weight: 800; color: #0f172a;">${t.id}: ${t.amount} (${t.type})</div>
                        <div style="font-size: 11px; color: #475569;">Date: ${t.date} ${t.time} | Related Person: <strong>${t.related_person}</strong> | Account: ${t.account}</div>
                        <div style="font-size: 10px; color: #64748b;">${t.notes}</div>
                    </div>
                    <button class="btn btn-secondary" style="font-size: 10px; padding: 3px 8px;" onclick="openEvidenceDetailModal('${t.evidence_id}')">Ref: ${t.evidence_id}</button>
                </div>
            `).join('');
        }
    } catch (err) {
        console.error(err);
    }
}

// 8. BLOCKCHAIN WORKSPACE
async function loadBlockchainData() {
    try {
        const res = await fetch(`/api/blockchain?person_id=${currentPersonId}`);
        const data = await res.json();

        const summary = document.getElementById('blk-summary');
        if (summary && data.wallet) {
            summary.innerHTML = `
                <div style="font-size: 13px; font-weight: 800; color: #d97706;">Wallet Address: ${data.wallet.address}</div>
                <div style="font-size: 11px; color: #475569; margin-top: 2px;">Balance: <strong>${data.wallet.balance}</strong> | Total Txs: ${data.wallet.total_transactions} (In: ${data.wallet.incoming}, Out: ${data.wallet.outgoing})</div>
                <div style="font-size: 10px; color: #92400e; margin-top: 4px; font-weight: 700;">⚠️ ${data.wallet.disclaimer}</div>
            `;
        }

        const list = document.getElementById('blk-list');
        if (list && data.transactions) {
            list.innerHTML = data.transactions.map(t => `
                <div style="padding: 10px; background: #ffffff; border: 1px solid #e2e8f0; border-left: 3px solid #d97706; border-radius: 8px; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="font-size: 12px; color: #d97706;">${t.id}: ${t.amount} (${t.type})</strong>
                        <div style="font-size: 11px; color: #475569;">Sender: ${t.sender} ➔ Recipient: ${t.recipient}</div>
                        <code style="font-size: 10px; color: #2563eb;">Hash: ${t.hash} | Timestamp: ${t.timestamp}</code>
                    </div>
                </div>
            `).join('');
        }
    } catch (err) {
        console.error(err);
    }
}

// 9. OSINT WORKSPACE
async function loadOSINTData() {
    try {
        const res = await fetch(`/api/osint?person_id=${currentPersonId}`);
        const data = await res.json();

        const list = document.getElementById('osint-list');
        if (list && data.records) {
            list.innerHTML = data.records.map(o => `
                <div style="padding: 10px; background: #ffffff; border: 1px solid #e2e8f0; border-left: 3px solid #7c3aed; border-radius: 8px; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span class="badge badge-verified" style="background: #f3e8ff; color: #6b21a8; border-color: #d8b4fe;">${o.type}</span>
                        <strong style="font-size: 12px; color: #0f172a; margin-left: 6px;">${o.value}</strong>
                        <div style="font-size: 11px; color: #475569; margin-top: 2px;">Source: ${o.source} | Last Observed: ${o.last_observed}</div>
                    </div>
                    <button class="btn btn-secondary" style="font-size: 10px; padding: 3px 8px;" onclick="openEvidenceDetailModal('${o.evidence_id}')">Ref: ${o.evidence_id}</button>
                </div>
            `).join('');
        }
    } catch (err) {
        console.error(err);
    }
}

// 10. CCTV / DVR / NVR FORENSICS (3 SYNTHETIC DEMO VIDEOS)
async function loadDVRData() {
    try {
        const res = await fetch(`/api/dvr?person_id=${currentPersonId}`);
        const data = await res.json();
        
        const videoGrid = document.getElementById('dvr-video-grid-container');
        if (videoGrid && data.dvr_videos) {
            videoGrid.innerHTML = data.dvr_videos.map(v => `
                <div class="dvr-card">
                    <div class="dvr-thumb-wrapper">
                        <img src="${v.video_thumbnail}" class="dvr-thumb-img" alt="CCTV Stream">
                        <div class="dvr-rec-badge">● STREAM | ${v.camera_id}</div>
                        <div class="dvr-play-overlay" onclick="openCCTVVideoModal('${v.camera_id}', '${v.event_title}', '${v.timestamp}', '${v.anpr_license_plate}', '${v.video_thumbnail}', '${v.description.replace(/'/g, "\\'")}')">▶</div>
                    </div>
                    <div class="dvr-info-body">
                        <div style="font-size: 13px; font-weight: 800; color: #0f172a; margin-bottom: 2px;">${v.event_title}</div>
                        <div style="font-size: 10px; color: #2563eb; font-weight: 700; margin-bottom: 4px;">📍 ${v.location}</div>
                        <div style="font-size: 11px; color: #475569; margin-bottom: 6px;"><strong>Identified Subjects:</strong> ${v.suspects_identified.join(', ')}</div>
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span class="synthetic-banner" style="font-size: 9px;">${v.label}</span>
                            <button class="btn btn-secondary" style="font-size: 9px; padding: 2px 6px;" onclick="openEvidenceDetailModal('${v.evidence_id}')">Ref: ${v.evidence_id}</button>
                        </div>
                    </div>
                </div>
            `).join('');
        }
    } catch (err) {
        console.error(err);
    }
}

function openCCTVVideoModal(camId, title, timestamp, anpr, imgUrl, desc) {
    const modal = document.getElementById('cctv-video-modal');
    if (!modal) return;
    document.getElementById('cctv-modal-cam').innerText = camId;
    document.getElementById('cctv-modal-img').src = imgUrl;
    document.getElementById('cctv-modal-desc').innerText = `${title} (${timestamp}) - ${desc}`;
    modal.style.display = 'flex';
}

function closeCCTVVideoModal() {
    const modal = document.getElementById('cctv-video-modal');
    if (modal) modal.style.display = 'none';
}

// 11. TIMELINE & TEMPORAL CORRELATION
async function loadTimelineData() {
    try {
        const res = await fetch(`/api/timeline?case_id=${currentCaseId}`);
        const data = await res.json();

        const box = document.getElementById('temporal-assessment-box');
        if (box && data.temporal_assessment) {
            box.innerHTML = `
                <div class="xai-title">⏱️ TEMPORAL CORRELATION ASSESSMENT</div>
                <div style="font-size: 12px; font-weight: 700; color: #0f172a;">${data.temporal_assessment}</div>
            `;
        }

        const container = document.getElementById('timeline-container');
        if (container && data.events) {
            container.innerHTML = data.events.map(ev => `
                <div class="timeline-item" style="cursor: pointer;" onclick="openEvidenceDetailModal('${ev.evidence_id}')">
                    <div style="font-size: 10px; color: #2563eb; font-weight: 700;">[${ev.domain}] ${ev.timestamp}</div>
                    <div style="font-size: 12px; font-weight: 700; color: #0f172a; margin: 2px 0;">${ev.title}</div>
                    <div style="font-size: 11px; color: #475569;">${ev.details}</div>
                </div>
            `).join('');
        }
    } catch (err) {
        console.error(err);
    }
}

// 12. ANALYTICS
async function loadAnalyticsData() {
    try {
        const res = await fetch('/api/analytics');
        const data = await res.json();
        const tbody = document.getElementById('analytics-tbody');
        if (tbody && data.influential_entities) {
            tbody.innerHTML = data.influential_entities.map(e => `
                <tr>
                    <td><strong>${e.label}</strong></td>
                    <td>${e.type}</td>
                    <td>${e.degree_centrality}</td>
                    <td>${e.betweenness_centrality}</td>
                    <td>${e.pagerank}</td>
                    <td><span class="badge badge-verified">${e.assessment}</span></td>
                </tr>
            `).join('');
        }
    } catch (err) {
        console.error(err);
    }
}

// 13. AUDIT
async function loadAuditData() {
    try {
        const res = await fetch('/api/audit');
        const data = await res.json();

        const tbody = document.getElementById('audit-tbody');
        if (tbody && data.audit_events) {
            tbody.innerHTML = data.audit_events.map(b => `
                <tr>
                    <td><strong>${b.timestamp}</strong></td>
                    <td>${b.actor}</td>
                    <td><span class="badge badge-verified">${b.action_type}</span></td>
                    <td>${b.object}</td>
                    <td><span class="badge badge-verified" style="background: #f0fdf4; color: #166534;">${b.result}</span></td>
                </tr>
            `).join('');
        }
    } catch (err) {
        console.error(err);
    }
}

// 14. REPORTS
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

// RIGHT-SIDE SLIDING PERSON DETAIL DRAWER
async function openPersonDrawer(personId) {
    currentPersonDrawerId = personId;
    const drawer = document.getElementById('person-detail-drawer');
    if (drawer) drawer.classList.add('open');
    switchDrawerTab('overview');
}

function closePersonDrawer() {
    const drawer = document.getElementById('person-detail-drawer');
    if (drawer) drawer.classList.remove('open');
}

async function switchDrawerTab(tabName) {
    currentDrawerTab = tabName;
    document.querySelectorAll('.drawer-tab-btn').forEach(btn => btn.classList.remove('active'));
    
    const content = document.getElementById('drawer-content-area');
    if (!content || !currentPersonDrawerId) return;

    try {
        const res = await fetch(`/api/persons/${currentPersonDrawerId}`);
        const data = await res.json();
        const p = data.person;

        if (tabName === 'overview') {
            content.innerHTML = `
                <div class="suspect-card">
                    <img src="${p.photo_url || 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=300'}" class="suspect-avatar">
                    <div>
                        <div style="font-size: 15px; font-weight: 800; color: #0f172a;">${p.name}</div>
                        <div style="font-size: 11px; color: #2563eb; font-weight: 700;">Role: ${p.role}</div>
                        <div style="font-size: 11px; color: #475569; margin-top: 2px;">Age: ${p.age || 34} | Location: ${p.city || 'Pune'}</div>
                    </div>
                </div>

                <div style="font-size: 11px; color: #475569; margin: 12px 0;">
                    <div><strong>Phone:</strong> ${p.phone}</div>
                    <div><strong>Email:</strong> ${p.email}</div>
                    <div><strong>Vehicle:</strong> ${p.vehicle || 'N/A'}</div>
                    <div><strong>Wallet:</strong> ${p.wallet_address || 'N/A'}</div>
                    <div><strong>Notes:</strong> ${p.notes}</div>
                </div>

                <div style="font-size: 11px; color: #2563eb; font-weight: 700; margin: 10px 0 4px 0;">Connected Intelligence Summary:</div>
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px; font-size: 11px; margin-bottom: 12px;">
                    <div>Communications: <strong>${data.connected_counts.communications}</strong></div>
                    <div>Financial Events: <strong>${data.connected_counts.financial}</strong></div>
                    <div>OSINT Records: <strong>${data.connected_counts.osint}</strong></div>
                    <div>Blockchain Txs: <strong>${data.connected_counts.blockchain}</strong></div>
                    <div>CCTV References: <strong>${data.connected_counts.cctv}</strong></div>
                </div>

                <h4 style="font-size: 12px; color: #2563eb; margin: 14px 0 6px 0;">Connected Relationships (${data.relationships.length}):</h4>
                ${data.relationships.map(r => `
                    <div style="padding: 8px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; margin-bottom: 4px; font-size: 11px;">
                        <span style="color: #2563eb;">[${r.domain}] ${r.relation}</span>: ${r.source} ➔ ${r.target}
                    </div>
                `).join('')}
            `;
        } else if (tabName === 'evidence') {
            content.innerHTML = `
                <h4 style="font-size: 12px; color: #2563eb; margin-bottom: 8px;">Associated Evidence Items (${data.evidence_items.length}):</h4>
                ${data.evidence_items.map(e => `
                    <div style="padding: 10px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; margin-bottom: 6px; font-size: 11px; cursor: pointer;" onclick="openEvidenceDetailModal('${e.id}')">
                        <div style="font-weight: 700; color: #0f172a;">${e.id}: ${e.title}</div>
                        <div style="color: #64748b; margin-top: 2px;">Type: ${e.evidence_type} | Source: ${e.source}</div>
                        <span class="badge badge-verified" style="margin-top: 4px;">Hash Verified</span>
                    </div>
                `).join('')}
            `;
        } else {
            content.innerHTML = `<div style="font-size: 12px; color: #64748b; padding: 12px;">Displaying ${tabName.toUpperCase()} records scoped to ${p.name}...</div>`;
        }
    } catch (err) {
        console.error(err);
    }
}

// RELATIONSHIP EVIDENCE DRAWER MODAL
async function openRelEvidenceModal(relId) {
    const modal = document.getElementById('rel-evidence-modal');
    if (!modal) return;
    modal.style.display = 'flex';

    try {
        const res = await fetch(`/api/relationships/${relId}/evidence`);
        const data = await res.json();
        const r = data.relationship;

        document.getElementById('rel-modal-body').innerHTML = `
            <div style="padding: 12px; background: #f0f9ff; border-radius: 8px; margin-bottom: 12px; border: 1px solid #bae6fd;">
                <div style="font-size: 13px; font-weight: 800; color: #0284c7;">Relationship: ${r.relation}</div>
                <div style="font-size: 12px; color: #0f172a; margin: 4px 0;"><strong>${r.source}</strong> ➔ <strong>${r.target}</strong></div>
                <div style="font-size: 11px; color: #475569; margin-top: 4px;"><strong>Temporal Correlation:</strong> ${r.temporal_correlation || '3 events within 42 minutes'}</div>
                <div style="font-size: 11px; color: #16a34a; margin-top: 2px;"><strong>Confidence:</strong> ${Math.round(r.confidence * 100)}%</div>
                <p style="font-size: 11px; color: #0f172a; margin-top: 6px;"><strong>Explanation:</strong> ${r.explanation || 'Repeated communication and shared temporal activity.'}</p>
                <p style="font-size: 11px; color: #d97706; margin-top: 2px;"><strong>Alternative Explanation:</strong> ${r.alt_explanation || 'Business coordination may explain activity.'}</p>
            </div>

            <h4 style="font-size: 12px; color: #2563eb; margin-bottom: 8px;">Supporting Evidence References (${data.supporting_evidence.length}):</h4>
            ${data.supporting_evidence.map(e => `
                <div style="padding: 8px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; margin-bottom: 6px; font-size: 11px; cursor: pointer;" onclick="openEvidenceDetailModal('${e.id}')">
                    <strong style="color: #2563eb;">${e.id}</strong>: ${e.title}
                </div>
            `).join('')}

            <div style="display: flex; justify-content: flex-end; margin-top: 14px;">
                <button class="btn" onclick="switchTab('communications'); closeRelEvidenceModal();">VIEW COMMUNICATION LOGS</button>
            </div>
        `;
    } catch (err) {
        console.error(err);
    }
}

function closeRelEvidenceModal() {
    const modal = document.getElementById('rel-evidence-modal');
    if (modal) modal.style.display = 'none';
}

// MULTI-STEP ADD CASE WIZARD HANDLERS
function openAddCaseWizard() {
    const modal = document.getElementById('add-case-wizard-modal');
    if (modal) modal.style.display = 'flex';
    goToWizardStep(1);
}

function closeAddCaseWizard() {
    const modal = document.getElementById('add-case-wizard-modal');
    if (modal) modal.style.display = 'none';
}

function goToWizardStep(step) {
    document.querySelectorAll('.wizard-step-item').forEach(el => el.classList.remove('active'));
    document.getElementById(`wiz-step-${step}`).classList.add('active');

    document.getElementById('wizard-panel-1').style.display = step === 1 ? 'block' : 'none';
    document.getElementById('wizard-panel-2').style.display = step === 2 ? 'block' : 'none';
    document.getElementById('wizard-panel-3').style.display = step === 3 ? 'block' : 'none';
}

async function submitWizardForm(e) {
    e.preventDefault();
    const title = document.getElementById('wiz-case-title').value.trim();
    const type = document.getElementById('wiz-case-type').value;
    const priority = document.getElementById('wiz-case-priority').value;
    const investigator = document.getElementById('wiz-case-investigator').value.trim();
    const desc = document.getElementById('wiz-case-desc').value.trim();

    const p_name = document.getElementById('wiz-p-name').value.trim();
    const p_alias = document.getElementById('wiz-p-alias').value.trim();
    const p_phone = document.getElementById('wiz-p-phone').value.trim();
    const p_email = document.getElementById('wiz-p-email').value.trim();
    const p_city = document.getElementById('wiz-p-city').value.trim();

    const primary_suspect = {
        id: `person_${p_name.toLowerCase().replace(/\s+/g, '_')}`,
        name: p_name || 'Primary Subject',
        alias: p_alias,
        role: 'Primary Subject',
        relationship_to_primary: 'Self',
        age: 34,
        gender: 'Male',
        photo_url: 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=300',
        phone: p_phone,
        email: p_email,
        city: p_city,
        occupation: 'Subject',
        organization: 'Under Investigation',
        vehicle: '',
        social_usernames: {},
        wallet_address: '',
        notes: desc,
        risk_score: 85,
        evidence_count: 5
    };

    const sec_name = document.getElementById('wiz-sec-name').value.trim();
    const sec_role = document.getElementById('wiz-sec-role').value;
    const sec_phone = document.getElementById('wiz-sec-phone').value.trim();

    const secondary_suspects = [];
    if (sec_name) {
        secondary_suspects.push({
            id: `person_${sec_name.toLowerCase().replace(/\s+/g, '_')}`,
            name: sec_name,
            alias: sec_name,
            role: sec_role,
            relationship_to_primary: 'Associate',
            age: 30,
            photo_url: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=300',
            phone: sec_phone,
            email: '',
            city: 'Pune',
            occupation: 'Associate',
            organization: '',
            vehicle: '',
            social_usernames: {},
            wallet_address: '',
            notes: '',
            risk_score: 70,
            evidence_count: 3
        });
    }

    try {
        const res = await fetch('/api/cases', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                title,
                description: desc,
                investigation_type: type,
                priority,
                lead_investigator: investigator,
                primary_suspect,
                secondary_suspects
            })
        });
        const data = await res.json();
        if (data.success) {
            alert(`✅ Case ${data.case.id} Created Successfully!\nPrimary Subject: ${p_name}\nLogged on SHA-256 Audit Ledger.`);
            closeAddCaseWizard();
            loadInvestigationsData();
            loadOverviewData();
        }
    } catch (err) {
        console.error(err);
    }
}

// GLOBAL SEARCH
function initGlobalSearch() {
    const input = document.getElementById('global-search-input');
    if (!input) return;

    input.addEventListener('keypress', async (e) => {
        if (e.key === 'Enter') {
            const query = input.value.trim();
            if (!query) return;
            const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
            const data = await res.json();
            alert(`🔍 Global Search Results for "${query}":\nCases Found: ${data.matched_cases.length}\nEntities Found: ${data.matched_nodes.length}\nEvidence Items: ${data.matched_evidence.length}\nRelationships: ${data.matched_relationships.length}`);
        }
    });
}
