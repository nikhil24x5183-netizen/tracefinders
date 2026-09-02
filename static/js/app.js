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
    document.getElementById('ctx-case-id').innerText = caseId;
    updateBreadcrumb();
    refreshActiveView();
}

function changeActivePerson(personId) {
    currentPersonId = personId;
    
    const personNames = {
        'person_arjun_sharma': 'ARJUN SHARMA',
        'person_rohan_mehta': 'ROHAN MEHTA',
        'person_priya_joshi': 'PRIYA JOSHI',
        'person_vikram_patil': 'VIKRAM PATIL',
        'person_neha_kulkarni': 'NEHA KULKARNI',
        'person_arjun_s_candidate': 'ARJUN S. (CANDIDATE)'
    };
    const pName = personNames[personId] || personId.toUpperCase();
    document.getElementById('ctx-subject-name').innerText = pName;
    
    updateBreadcrumb();
    refreshActiveView();
}

function updateBreadcrumb() {
    const activeNav = document.querySelector('.nav-item.active');
    const moduleName = activeNav ? activeNav.innerText.trim().toUpperCase() : 'OPERATIONAL OVERVIEW';
    const selectP = document.getElementById('select-change-person');
    const pName = selectP ? selectP.options[selectP.selectedIndex].text.split('(')[0].trim().toUpperCase() : 'ARJUN SHARMA';
    
    document.getElementById('breadcrumb-text').innerText = `CASE MANAGEMENT > ${currentCaseId} > ${pName} > ${moduleName}`;
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
        if (tabId === 'cases') loadInvestigationsData();
        if (tabId === 'persons') loadPersonsViewData();
        if (tabId === 'graph') loadGraphData();
        if (tabId === 'timeline') loadTimelineData();
        if (tabId === 'communications') loadCommunicationsData();
        if (tabId === 'financial') loadFinancialData();
        if (tabId === 'blockchain') loadBlockchainData();
        if (tabId === 'osint') loadOSINTData();
        if (tabId === 'dvr') loadDVRData();
        if (tabId === 'analytics') loadAnalyticsData();
        if (tabId === 'fusion') loadFusionData();
        if (tabId === 'resolution') loadEntityResolutionData();
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

// 1. OPERATIONAL OVERVIEW
async function loadOverviewData() {
    try {
        const res = await fetch(`/api/overview?case_id=${currentCaseId}&person_id=${currentPersonId}`);
        const data = await res.json();

        const actList = document.getElementById('activity-feed');
        if (actList && data.investigation_activity) {
            actList.innerHTML = data.investigation_activity.map(act => `
                <div style="padding: 10px 0; border-bottom: 1px solid #334155; display: flex; justify-content: space-between; font-size: 11px;">
                    <span>⚡ <strong style="color: #f8fafc;">[${act.time}]</strong> ${act.event}</span>
                    <span class="badge badge-verified">${act.domain}</span>
                </div>
            `).join('');
        }

        const leadsPanel = document.getElementById('ai-leads-panel');
        if (leadsPanel && data.ai_leads) {
            leadsPanel.innerHTML = data.ai_leads.map(lead => `
                <div style="padding: 12px; background: #0f172a; border-left: 3px solid #3b82f6; border-radius: 8px; margin-bottom: 8px;">
                    <div style="font-size: 12px; font-weight: 800; color: #38bdf8;">${lead.title}</div>
                    <p style="font-size: 11px; color: #94a3b8; margin: 4px 0;">${lead.lead || lead.summary}</p>
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

// 2. CASE MANAGEMENT SECTION
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
                <div class="card" style="border-left: 4px solid ${c.priority === 'HIGH' ? '#ef4444' : '#3b82f6'};">
                    <div class="card-title">
                        <span>${c.id}: ${c.title} (${c.location})</span>
                        <span class="badge ${c.priority === 'HIGH' ? 'badge-high' : 'badge-verified'}">${c.status}</span>
                    </div>

                    <!-- PRIMARY SUBJECT IDENTITY CARD -->
                    <div class="suspect-card" onclick="openPersonDrawer('${primary.id}')" style="cursor: pointer;">
                        <img src="${primary.photo_url || 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=300'}" class="suspect-avatar">
                        <div>
                            <div style="font-size: 14px; font-weight: 800; color: #f8fafc;">${primary.name} <span class="badge badge-high" style="font-size: 9px;">Primary Subject</span></div>
                            <div style="font-size: 11px; color: #94a3b8; margin: 2px 0;">Age: <strong>${primary.age || 34}</strong> | City: <strong>${primary.city || 'Pune'}</strong> | Occupation: <strong>${primary.occupation || 'Consultant'}</strong></div>
                            <div style="font-size: 11px; color: #38bdf8;">📞 ${primary.phone} | ✉️ ${primary.email}</div>
                        </div>
                    </div>

                    <!-- SECONDARY SUBJECTS / PERSONS OF INTEREST -->
                    ${secondaries.length > 0 ? `
                        <div style="font-size: 10px; font-weight: 800; color: #38bdf8; text-transform: uppercase; margin: 10px 0 6px 0;">👥 Persons of Interest & Associates (${secondaries.length}):</div>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 8px; margin-bottom: 10px;">
                            ${secondaries.map(sec => `
                                <div style="padding: 8px; background: #0f172a; border: 1px solid #334155; border-radius: 8px; display: flex; gap: 8px; align-items: center; cursor: pointer;" onclick="openPersonDrawer('${sec.id}')">
                                    <img src="${sec.photo_url || 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=300'}" style="width: 36px; height: 36px; border-radius: 50%; object-fit: cover;">
                                    <div>
                                        <div style="font-size: 12px; font-weight: 700; color: #f8fafc;">${sec.name}</div>
                                        <div style="font-size: 10px; color: #38bdf8;">${sec.role}</div>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    ` : ''}

                    <div style="display: grid; grid-template-columns: repeat(6, 1fr); gap: 8px; font-size: 11px; color: #94a3b8; margin: 8px 0;">
                        <div>Evidence: <strong>${c.evidence_count || 148}</strong></div>
                        <div>Relationships: <strong>${c.relationships_count || 37}</strong></div>
                        <div>Calls: <strong>${c.communications_count || 421}</strong></div>
                        <div>Financial: <strong>${c.financial_count || 63}</strong></div>
                        <div>OSINT: <strong>${c.osint_count || 42}</strong></div>
                        <div>CCTV: <strong>${c.cctv_count || 9}</strong></div>
                    </div>

                    <p style="font-size: 11px; color: #94a3b8; margin-bottom: 10px;">${c.description}</p>
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

// 3. PERSONS INTELLIGENCE PROFILE VIEW (REQUIREMENT 4 & 5)
async function loadPersonsViewData() {
    const container = document.getElementById('person-profile-card-container');
    if (!container) return;

    try {
        const res = await fetch(`/api/persons/${currentPersonId}`);
        const data = await res.json();
        const p = data.person;

        container.innerHTML = `
            <div class="card">
                <!-- TOP PROFILE SECTION (REQUIREMENT 4) -->
                <div style="display: flex; gap: 20px; border-bottom: 1px solid #334155; padding-bottom: 16px; margin-bottom: 16px;">
                    <img src="${p.photo_url || 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=300'}" style="width: 90px; height: 90px; border-radius: 12px; object-fit: cover; border: 2px solid #3b82f6;">
                    <div>
                        <div style="font-size: 20px; font-weight: 800; color: #f8fafc;">${p.name}</div>
                        <div style="font-size: 13px; font-weight: 700; color: #38bdf8; margin: 2px 0;">${p.role}</div>
                        <div style="font-size: 11px; color: #94a3b8; display: flex; gap: 16px; margin-top: 6px;">
                            <div>Case: <strong style="color: #f8fafc;">${currentCaseId}</strong></div>
                            <div>Status: <span class="badge badge-high">${p.status || 'Under Investigation'}</span></div>
                            <div>Last Updated: <strong style="color: #f8fafc;">${p.last_updated || '18 Aug 2026 21:17'}</strong></div>
                        </div>
                    </div>
                </div>

                <!-- PERSON IDENTIFIER PANEL WITH CLICKABLE LINKS (REQUIREMENT 5) -->
                <h4 style="font-size: 13px; color: #38bdf8; margin-bottom: 10px;">STRUCTURED IDENTIFIERS (Click to navigate):</h4>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 20px; font-size: 12px;">
                    <div style="padding: 10px; background: #0f172a; border: 1px solid #334155; border-radius: 8px;">
                        <div style="font-size: 10px; color: #64748b; font-weight: 800;">FULL NAME</div>
                        <div style="font-weight: 700; color: #f8fafc;">${p.name}</div>
                    </div>
                    <div style="padding: 10px; background: #0f172a; border: 1px solid #334155; border-radius: 8px;">
                        <div style="font-size: 10px; color: #64748b; font-weight: 800;">KNOWN ALIASES</div>
                        <div style="font-weight: 700; color: #38bdf8;">${p.alias}</div>
                    </div>
                    <div style="padding: 10px; background: #0f172a; border: 1px solid #334155; border-radius: 8px;">
                        <div style="font-size: 10px; color: #64748b; font-weight: 800;">AGE & GENDER</div>
                        <div style="font-weight: 700; color: #f8fafc;">${p.age} (${p.gender})</div>
                    </div>
                    <div style="padding: 10px; background: #0f172a; border: 1px solid #334155; border-radius: 8px;">
                        <div style="font-size: 10px; color: #64748b; font-weight: 800;">OCCUPATION</div>
                        <div style="font-weight: 700; color: #f8fafc;">${p.occupation}</div>
                    </div>
                    <div style="padding: 10px; background: #0f172a; border: 1px solid #334155; border-radius: 8px;">
                        <div style="font-size: 10px; color: #64748b; font-weight: 800;">ORGANIZATION</div>
                        <div style="font-weight: 700; color: #f8fafc;">${p.organization}</div>
                    </div>
                    <div style="padding: 10px; background: #0f172a; border: 1px solid #334155; border-radius: 8px; cursor: pointer;" onclick="switchTab('communications')">
                        <div style="font-size: 10px; color: #64748b; font-weight: 800;">PHONE ➔ COMMUNICATION ANALYSIS</div>
                        <div style="font-weight: 700; color: #38bdf8;">📞 ${p.phone}</div>
                    </div>
                    <div style="padding: 10px; background: #0f172a; border: 1px solid #334155; border-radius: 8px;">
                        <div style="font-size: 10px; color: #64748b; font-weight: 800;">EMAIL</div>
                        <div style="font-weight: 700; color: #f8fafc;">✉️ ${p.email}</div>
                    </div>
                    <div style="padding: 10px; background: #0f172a; border: 1px solid #334155; border-radius: 8px; cursor: pointer;" onclick="switchTab('dvr')">
                        <div style="font-size: 10px; color: #64748b; font-weight: 800;">VEHICLE ➔ VEHICLE INTELLIGENCE</div>
                        <div style="font-weight: 700; color: #38bdf8;">🚘 ${p.vehicle || 'MH12 AB 4821'}</div>
                    </div>
                    <div style="padding: 10px; background: #0f172a; border: 1px solid #334155; border-radius: 8px;">
                        <div style="font-size: 10px; color: #64748b; font-weight: 800;">CITY</div>
                        <div style="font-weight: 700; color: #f8fafc;">📍 ${p.city}</div>
                    </div>
                    <div style="padding: 10px; background: #0f172a; border: 1px solid #334155; border-radius: 8px; cursor: pointer;" onclick="switchTab('osint')">
                        <div style="font-size: 10px; color: #64748b; font-weight: 800;">PUBLIC USERNAME ➔ PUBLIC-SOURCE INTEL</div>
                        <div style="font-weight: 700; color: #38bdf8;">🌐 @arjun_s_demo</div>
                    </div>
                    <div style="padding: 10px; background: #0f172a; border: 1px solid #334155; border-radius: 8px; cursor: pointer;" onclick="switchTab('blockchain')">
                        <div style="font-size: 10px; color: #64748b; font-weight: 800;">WALLET ➔ BLOCKCHAIN ANALYSIS</div>
                        <div style="font-weight: 700; color: #38bdf8;">⛓️ ${p.wallet_address || '0xDEMO...A721'}</div>
                    </div>
                </div>

                <!-- RELATIONSHIP INTELLIGENCE PANEL (REQUIREMENT 6) -->
                <h4 style="font-size: 13px; color: #38bdf8; margin-bottom: 10px;">RELATIONSHIP INTELLIGENCE:</h4>
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px;">
                    <div style="padding: 12px; background: #0f172a; border: 1px solid #334155; border-radius: 8px;">
                        <div style="font-size: 14px; font-weight: 800; color: #f8fafc;">ROHAN MEHTA</div>
                        <div style="font-size: 11px; color: #38bdf8;">Relationship: <strong>Business Contact</strong> (Confidence: <strong>82%</strong>)</div>
                        <div style="font-size: 10px; color: #94a3b8; margin: 4px 0;">First Observed: 03 Aug 2026 | Last Observed: 18 Aug 2026</div>
                        <div style="font-size: 10px; color: #94a3b8;">Supporting Evidence: 7 | Communication Events: 27 | Shared Locations: 3 | Shared Organizations: 1</div>
                        <button class="btn btn-secondary" style="margin-top: 8px; font-size: 10px; padding: 3px 8px;" onclick="openRelEvidenceModal('REL-014')">VIEW RELATIONSHIP</button>
                    </div>
                    <div style="padding: 12px; background: #0f172a; border: 1px solid #334155; border-radius: 8px;">
                        <div style="font-size: 14px; font-weight: 800; color: #f8fafc;">PRIYA JOSHI</div>
                        <div style="font-size: 11px; color: #38bdf8;">Relationship: <strong>Associate</strong> (Confidence: <strong>92%</strong>)</div>
                        <div style="font-size: 10px; color: #94a3b8; margin: 4px 0;">First Observed: 10 Aug 2026 | Last Observed: 18 Aug 2026</div>
                        <div style="font-size: 10px; color: #94a3b8;">Supporting Evidence: 5 | Communication Events: 8 | Shared Locations: 2 | Shared Organizations: 1</div>
                        <button class="btn btn-secondary" style="margin-top: 8px; font-size: 10px; padding: 3px 8px;" onclick="openRelEvidenceModal('REL-022')">VIEW RELATIONSHIP</button>
                    </div>
                </div>
            </div>
        `;
    } catch (err) {
        console.error(err);
    }
}

// 4. EVIDENCE ASSOCIATIONS & LEADS
async function loadFusionData() {
    try {
        const res = await fetch(`/api/fusion?case_id=${currentCaseId}&person_id=${currentPersonId}`);
        const data = await res.json();
        const container = document.getElementById('fusion-chain-container');
        if (!container) return;

        container.innerHTML = `
            <div class="xai-box">
                <div class="xai-title">🧠 EXPLAINABLE AI EVIDENCE CHAIN SYNTHESIS</div>
                <p style="font-size: 11px; color: #94a3b8; margin-bottom: 8px;">${data.explainable_ai.WHAT}</p>
                <div class="xai-grid">
                    <div><strong>WHY FLAGGED:</strong> ${data.explainable_ai.WHY}</div>
                    <div><strong>CONFIDENCE SCORE:</strong> <span style="color: #10b981; font-weight: bold;">${data.explainable_ai.CONFIDENCE}</span></div>
                </div>
            </div>

            <!-- LINK ANALYSIS TREE (REQUIREMENT 9 & 10) -->
            <h4 style="margin: 16px 0 8px 0; font-size: 13px; color: #38bdf8;">Default Link Analysis Tree Representation:</h4>
            <div style="background: #0f172a; border: 1px solid #334155; border-radius: 10px; padding: 14px; font-family: monospace; font-size: 12px; margin-bottom: 16px;">
                <div style="font-weight: 800; color: #38bdf8;">ARJUN SHARMA (Primary Subject)</div>
                <div>│</div>
                <div>├── <span style="cursor: pointer; color: #38bdf8; font-weight: 700;" onclick="openRelEvidenceModal('REL-014')">ROHAN MEHTA (Business Contact - 27 Calls logged)</span></div>
                <div>│</div>
                <div>├── <span style="cursor: pointer; color: #38bdf8; font-weight: 700;" onclick="openRelEvidenceModal('REL-022')">PRIYA JOSHI (Associate - Senior Accountant)</span></div>
                <div>│</div>
                <div>├── <span style="cursor: pointer; color: #38bdf8; font-weight: 700;" onclick="openRelEvidenceModal('REL-031')">MH12 AB 4821 (SUV Vehicle - ANPR Match)</span></div>
                <div>│</div>
                <div>├── <span style="cursor: pointer; color: #10b981; font-weight: 700;" onclick="switchTab('financial')">BANK ACCOUNT (XXXX4821)</span></div>
                <div>│</div>
                <div>├── <span style="cursor: pointer; color: #f59e0b; font-weight: 700;" onclick="switchTab('blockchain')">CRYPTO WALLET (0xDEMO...A721 - Balance 8.42 ETH)</span></div>
                <div>│</div>
                <div>├── <span style="cursor: pointer; color: #ec4899; font-weight: 700;" onclick="switchTab('dvr')">LOCATIONS (Synthetic Pune Location A)</span></div>
                <div>│</div>
                <div>└── <span style="cursor: pointer; color: #ef4444; font-weight: 700;" onclick="switchTab('timeline')">INCIDENTS (Cyber Incident #1042)</span></div>
            </div>

            <h4 style="margin: 16px 0 8px 0; font-size: 13px; color: #38bdf8;">Investigative Leads:</h4>
        `;

        const leadsRes = await fetch('/api/leads');
        const leadsData = await leadsRes.json();
        
        container.innerHTML += leadsData.leads.map(lead => `
            <div style="padding: 12px; background: #0f172a; border: 1px solid #334155; border-left: 4px solid ${lead.confidence < 0.5 ? '#ef4444' : '#3b82f6'}; border-radius: 8px; margin-bottom: 8px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 13px; font-weight: 800; color: #f8fafc;">${lead.id}: ${lead.title}</span>
                    <span class="badge ${lead.confidence < 0.5 ? 'badge-high' : 'badge-verified'}">Confidence: ${Math.round(lead.confidence * 100)}%</span>
                </div>
                <p style="font-size: 11px; color: #94a3b8; margin: 4px 0;">${lead.lead || lead.observed_pattern}</p>
                <div style="font-size: 10px; color: #38bdf8; margin: 4px 0;"><strong>Supporting Evidence:</strong> ${(lead.supporting_evidence || []).join(', ')}</div>
                <div style="font-size: 10px; color: #f59e0b;"><strong>Alternative Explanation:</strong> ${lead.alternative_explanation || 'Business coordination.'}</div>
                <div style="margin-top: 6px; font-size: 10px; color: #64748b; font-weight: 700;">Status: ${lead.status}</div>
            </div>
        `).join('');

    } catch (err) {
        console.error(err);
    }
}

// 5. LINK ANALYSIS GRAPH (TREE VIEW DEFAULT & SHORT EDGE LABELS - REQUIREMENT 9 & 10)
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
        font: { color: '#f8fafc', size: 10, strokeWidth: 2, strokeColor: '#0b0f19', face: 'Inter' },
        level: n.tree_level !== undefined ? n.tree_level : 2
    }));

    // SHORT EDGE LABELS REQUIRED BY REQUIREMENT 10
    const visEdges = edgesToRender.map(e => ({
        id: e.id,
        from: e.source,
        to: e.target,
        label: e.relation,
        arrows: 'to',
        color: { color: getDomainColor(e.domain) },
        font: { color: '#94a3b8', size: 8, strokeWidth: 2, strokeColor: '#0b0f19' },
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
    if (type === 'BANK_ACCOUNT') return { background: '#10b981', border: '#047857' };
    if (type === 'CRYPTO_WALLET') return { background: '#f59e0b', border: '#b45309' };
    if (type === 'VEHICLE') return { background: '#8b5cf6', border: '#6d28d9' };
    if (type === 'CAMERA') return { background: '#ec4899', border: '#be185d' };
    return { background: '#3b82f6', border: '#1d4ed8' };
}

function getDomainColor(domain) {
    if (domain === 'COMMUNICATION') return '#0284c7';
    if (domain === 'FINANCIAL') return '#10b981';
    if (domain === 'BLOCKCHAIN') return '#f59e0b';
    if (domain === 'DVR') return '#ec4899';
    if (domain === 'OSINT') return '#8b5cf6';
    return '#64748b';
}

// 6. COMMUNICATION ANALYSIS (REQUIREMENT 11)
async function loadCommunicationsData() {
    try {
        const res = await fetch(`/api/communications?person_id=${currentPersonId}`);
        const data = await res.json();

        document.getElementById('comm-stat-total').innerText = data.total_events || 421;
        document.getElementById('comm-stat-calls').innerText = data.calls || 187;
        document.getElementById('comm-stat-msgs').innerText = data.messages || 234;
        document.getElementById('comm-stat-contacts').innerText = data.unique_contacts || 11;
        document.getElementById('comm-stat-period').innerText = data.active_period || '03 Aug – 18 Aug 2026';

        const tree = document.getElementById('comm-contact-tree');
        if (tree && data.contacts) {
            tree.innerHTML = data.contacts.map(c => `
                <div style="padding: 10px; background: #0f172a; border: 1px solid #334155; border-left: 3px solid #0284c7; border-radius: 8px; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="font-size: 12px; color: #f8fafc;">${c.name}</strong> (${c.role})
                        <div style="font-size: 10px; color: #38bdf8;">📞 ${c.phone}</div>
                    </div>
                    <span class="badge badge-verified">${c.calls} Calls Logged</span>
                </div>
            `).join('');
        }

        const tbody = document.getElementById('comm-rohan-tbody');
        if (tbody && data.rohan_call_timeline) {
            tbody.innerHTML = data.rohan_call_timeline.map(t => `
                <tr>
                    <td>${t.date}</td>
                    <td>${t.time}</td>
                    <td><span class="badge ${t.direction === 'Outgoing' ? 'badge-verified' : 'badge-medium'}">${t.direction}</span></td>
                    <td>${t.duration}</td>
                    <td><button class="btn btn-secondary" style="font-size: 10px; padding: 2px 6px;" onclick="openEvidenceDetailModal('${t.evidence_id}')">Ref: ${t.evidence_id}</button></td>
                </tr>
            `).join('');
        }
    } catch (err) {
        console.error(err);
    }
}

// 7. FINANCIAL INTELLIGENCE LEDGER (REQUIREMENT 12, 13, 14)
async function loadFinancialData() {
    try {
        const res = await fetch(`/api/financial?person_id=${currentPersonId}`);
        const data = await res.json();

        const grid = document.getElementById('fin-accounts-grid');
        if (grid && data.accounts) {
            grid.innerHTML = data.accounts.map(a => `
                <div style="padding: 12px; background: #0f172a; border: 1px solid #334155; border-radius: 8px;">
                    <div style="font-size: 12px; font-weight: 800; color: #10b981;">${a.bank} (${a.account_number})</div>
                    <div style="font-size: 11px; color: #94a3b8;">Type: ${a.type} | Current Balance: <strong style="color: #f8fafc;">${a.balance}</strong></div>
                </div>
            `).join('');
        }

        const hawala = document.getElementById('fin-hawala-box');
        if (hawala && data.hawala_analysis) {
            hawala.innerHTML = `
                <div class="xai-title">INFORMAL VALUE TRANSFER INDICATORS</div>
                <div style="font-size: 12px; font-weight: 700; color: #f8fafc; margin-bottom: 4px;">${data.hawala_analysis.assessment} (${data.hawala_analysis.status})</div>
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-top: 8px;">
                    ${data.hawala_analysis.indicators.map(i => `
                        <div style="padding: 8px; background: #0f172a; border: 1px solid #334155; border-radius: 6px; font-size: 11px;">
                            <div style="font-weight: 700; color: #f8fafc;">${i.name}</div>
                            <div style="margin-top: 2px;"><span class="badge ${i.status === 'OBSERVED' ? 'badge-high' : 'badge-medium'}">STATUS: ${i.status}</span></div>
                            <div style="font-size: 10px; color: #94a3b8; margin-top: 4px;">${i.details}</div>
                        </div>
                    `).join('')}
                </div>
            `;
        }

        const tbody = document.getElementById('fin-transactions-tbody');
        if (tbody && data.transactions) {
            tbody.innerHTML = data.transactions.map(t => `
                <tr style="cursor: pointer;" onclick="openTransactionDetail('${t.reference}')">
                    <td>${t.date}</td>
                    <td>${t.time}</td>
                    <td><strong style="color: ${t.direction === 'OUT' ? '#ef4444' : '#10b981'};">${t.amount}</strong></td>
                    <td><span class="badge ${t.direction === 'OUT' ? 'badge-high' : 'badge-verified'}">${t.direction}</span></td>
                    <td>${t.account}</td>
                    <td><strong>${t.counterparty}</strong></td>
                    <td><code style="color: #38bdf8;">${t.reference}</code></td>
                    <td><button class="btn btn-secondary" style="font-size: 10px; padding: 2px 6px;" onclick="event.stopPropagation(); openEvidenceDetailModal('${t.evidence_id}')">Ref: ${t.evidence_id}</button></td>
                </tr>
            `).join('');
        }
    } catch (err) {
        console.error(err);
    }
}

function openTransactionDetail(refId) {
    alert(`TRANSACTION RECORD ${refId}:\nAmount: ₹48,500\nDate: 18 Aug 2026 20:58\nSource Account: XXXX4821 ➔ Destination: XXXX7312\nAssociated Person: Rohan Mehta\nCommunication Correlation: EV-COM-031\nAnalytic Indicator: Temporal proximity between communication and financial activity.\nConfidence: 71%`);
}

// 8. BLOCKCHAIN ANALYSIS (REQUIREMENT 15)
async function loadBlockchainData() {
    try {
        const res = await fetch(`/api/blockchain?person_id=${currentPersonId}`);
        const data = await res.json();

        const summary = document.getElementById('blk-summary');
        if (summary && data.wallet) {
            summary.innerHTML = `
                <div style="font-size: 13px; font-weight: 800; color: #f59e0b;">Wallet Address: ${data.wallet.address} (Associated Evidence: ${data.wallet.associated_evidence})</div>
                <div style="font-size: 11px; color: #94a3b8; margin-top: 2px;">Balance: <strong>${data.wallet.balance}</strong> | Total Observed: ${data.wallet.total_observed} (Incoming: ${data.wallet.incoming}, Outgoing: ${data.wallet.outgoing})</div>
            `;
        }

        const tbody = document.getElementById('blk-transactions-tbody');
        if (tbody && data.transactions) {
            tbody.innerHTML = data.transactions.map(t => `
                <tr>
                    <td><code style="color: #f59e0b;">${t.hash}</code></td>
                    <td>${t.from_addr}</td>
                    <td>${t.to_addr}</td>
                    <td><strong>${t.value}</strong></td>
                    <td>${t.time}</td>
                    <td><button class="btn btn-secondary" style="font-size: 10px; padding: 2px 6px;" onclick="openEvidenceDetailModal('${t.evidence_id}')">Ref: ${t.evidence_id}</button></td>
                </tr>
            `).join('');
        }
    } catch (err) {
        console.error(err);
    }
}

// 9. PUBLIC-SOURCE INTELLIGENCE (REQUIREMENT 16)
async function loadOSINTData() {
    try {
        const res = await fetch(`/api/osint?person_id=${currentPersonId}`);
        const data = await res.json();

        const list = document.getElementById('osint-list');
        if (list && data.records) {
            list.innerHTML = data.records.map(o => `
                <div style="padding: 12px; background: #0f172a; border: 1px solid #334155; border-left: 3px solid #8b5cf6; border-radius: 8px; margin-bottom: 8px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 13px; font-weight: 800; color: #f8fafc;">SOURCE RECORD ${o.id}: ${o.value}</span>
                        <span class="badge badge-verified">Confidence: ${o.confidence}</span>
                    </div>
                    <div style="font-size: 11px; color: #94a3b8; margin-top: 4px;">Subject: <strong>${o.subject}</strong> | Source: ${o.source} | Observed: ${o.last_observed} | Entity: <strong>${o.entity}</strong> | Location: ${o.location}</div>
                    <button class="btn btn-secondary" style="margin-top: 6px; font-size: 10px; padding: 3px 8px;" onclick="openEvidenceDetailModal('${o.evidence_id}')">View Evidence: ${o.evidence_id}</button>
                </div>
            `).join('');
        }
    } catch (err) {
        console.error(err);
    }
}

// 10. CCTV / DVR FORENSICS WORKSPACE (REQUIREMENT 17 & 18)
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
                        <div style="font-size: 13px; font-weight: 800; color: #f8fafc; margin-bottom: 2px;">${v.event_title} (${v.timestamp})</div>
                        <div style="font-size: 10px; color: #38bdf8; font-weight: 700; margin-bottom: 4px;">📍 ${v.location}</div>
                        <div style="font-size: 11px; color: #94a3b8; margin-bottom: 6px;"><strong>Identified Subjects:</strong> ${v.suspects_identified.join(', ')}</div>
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span class="badge badge-verified" style="font-size: 9px;">${v.label}</span>
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

// 11. TIMELINE & TEMPORAL CORRELATION (REQUIREMENT 19)
async function loadTimelineData() {
    try {
        const res = await fetch(`/api/timeline?case_id=${currentCaseId}`);
        const data = await res.json();

        const box = document.getElementById('temporal-assessment-box');
        if (box && data.temporal_assessment) {
            box.innerHTML = `
                <div class="xai-title">⏱️ TEMPORAL CORRELATION ASSESSMENT</div>
                <div style="font-size: 12px; font-weight: 700; color: #f8fafc;">${data.temporal_assessment}</div>
            `;
        }

        const container = document.getElementById('timeline-container');
        if (container && data.events) {
            container.innerHTML = data.events.map(ev => `
                <div class="timeline-item" style="cursor: pointer;" onclick="openEvidenceDetailModal('${ev.evidence_id}')">
                    <div style="font-size: 10px; color: #38bdf8; font-weight: 700;">[${ev.domain}] ${ev.timestamp}</div>
                    <div style="font-size: 12px; font-weight: 700; color: #f8fafc; margin: 2px 0;">${ev.title}</div>
                    <div style="font-size: 11px; color: #94a3b8;">Person: <strong>${ev.person}</strong> | Location: ${ev.location} | Details: ${ev.details}</div>
                </div>
            `).join('');
        }
    } catch (err) {
        console.error(err);
    }
}

// 13. ENTITY RESOLUTION INTERFACE (REQUIREMENT 25)
async function loadEntityResolutionData() {
    const container = document.getElementById('entity-resolution-container');
    if (!container) return;

    try {
        const res = await fetch(`/api/persons/person_arjun_s_candidate`);
        const data = await res.json();
        const cand = data.person;

        container.innerHTML = `
            <div style="padding: 16px; background: #0f172a; border: 1px solid #334155; border-radius: 10px; max-width: 600px;">
                <div style="font-size: 14px; font-weight: 800; color: #f59e0b; margin-bottom: 8px;">POTENTIAL MATCH: ${cand.name}</div>
                <div style="font-size: 12px; color: #f8fafc; margin-bottom: 4px;">Possible match to Primary Subject: <strong>Arjun Sharma</strong></div>
                <div style="font-size: 11px; color: #94a3b8; margin-bottom: 8px;">
                    <div>Signals: <strong>Name similarity</strong>, <strong>Location overlap</strong>, <strong>Organization overlap</strong></div>
                    <div>Confidence: <span class="badge badge-medium">43%</span></div>
                    <div>Status: <strong style="color: #f59e0b;">${cand.status}</strong></div>
                </div>
                <p style="font-size: 11px; color: #94a3b8; margin-bottom: 12px;">${cand.notes}</p>

                <div style="display: flex; gap: 8px;">
                    <button class="btn" style="background: #10b981;" onclick="actionEntityResolution('CONFIRM')">CONFIRM MATCH</button>
                    <button class="btn" style="background: #ef4444;" onclick="actionEntityResolution('REJECT')">REJECT MATCH</button>
                    <button class="btn btn-secondary" onclick="actionEntityResolution('REVIEW')">MARK FOR REVIEW</button>
                </div>
            </div>
        `;
    } catch (err) {
        console.error(err);
    }
}

async function actionEntityResolution(action) {
    try {
        const res = await fetch('/api/entity-resolution/action', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ candidate_id: 'person_arjun_s_candidate', action: action })
        });
        const data = await res.json();
        alert(`✅ Entity Resolution Action Executed: ${data.message}`);
        loadEntityResolutionData();
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

// 15. AUDIT TRAIL (REQUIREMENT 27)
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
                    <td><span class="badge badge-verified" style="background: #064e3b; color: #6ee7b7;">${b.result}</span></td>
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

// STANDARDIZED EVIDENCE DRAWER MODAL (REQUIREMENT 8)
async function openEvidenceDetailModal(evidenceId) {
    const modal = document.getElementById('evidence-detail-modal');
    if (!modal) return;
    modal.style.display = 'flex';

    try {
        const res = await fetch(`/api/evidence/${evidenceId}`);
        const e = await res.json();

        document.getElementById('evidence-modal-body').innerHTML = `
            <div style="padding: 14px; background: #0f172a; border: 1px solid #334155; border-radius: 10px; margin-bottom: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span style="font-size: 14px; font-weight: 800; color: #38bdf8;">EVIDENCE RECORD ${e.id}</span>
                    <span class="badge badge-verified">${e.evidence_type}</span>
                </div>
                <div style="font-size: 11px; color: #94a3b8; display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 8px;">
                    <div>CASE: <strong style="color: #f8fafc;">${e.case_id}</strong></div>
                    <div>SUBJECT: <strong style="color: #f8fafc;">Arjun Sharma</strong></div>
                    <div>SOURCE: <strong>${e.source}</strong></div>
                    <div>DATE: <strong>${e.acquisition_date || '18 Aug 2026'}</strong></div>
                    <div>TIME: <strong>${e.acquisition_time || '20:02:14'}</strong></div>
                    <div>DURATION / DIRECTION: <strong>${e.duration || '04:21'} (${e.direction || 'Outgoing'})</strong></div>
                    <div>ASSOCIATED PERSON: <strong>Rohan Mehta</strong></div>
                    <div>INTEGRITY: <span class="badge badge-verified">Hash: ${e.file_hash.substring(0, 10)}... (Verified)</span></div>
                </div>
                <p style="font-size: 11px; color: #f8fafc;"><strong>ANALYTIC EXTRACTION:</strong> ${e.analyst_notes}</p>
                <div style="margin-top: 6px; font-size: 10px; color: #38bdf8;">
                    <strong>Extracted Entities:</strong> ${(e.extracted_entities || []).join(', ')} | <strong>Related Events:</strong> ${(e.related_events || []).join(', ')}
                </div>
            </div>

            <!-- BUTTONS REQUIRED BY REQUIREMENT 8 -->
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 10px;">
                <button class="btn btn-secondary" onclick="alert('Viewing original SHA-256 file payload for ${e.id}...')">📄 VIEW ORIGINAL</button>
                <button class="btn btn-secondary" onclick="switchTab('graph'); closeEvidenceDetailModal();">🕸️ VIEW RELATIONSHIP</button>
                <button class="btn btn-secondary" onclick="switchTab('timeline'); closeEvidenceDetailModal();">⏱️ VIEW TIMELINE</button>
                <button class="btn" style="background: #10b981;" onclick="alert('Evidence ${e.id} Marked Verified!')">✅ VERIFY</button>
                <button class="btn" style="background: #f59e0b;" onclick="alert('Evidence ${e.id} Flagged for Review!')">⚠️ FLAG FOR REVIEW</button>
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

        if (tabName === 'overview' || tabName === 'identifiers') {
            content.innerHTML = `
                <div class="suspect-card">
                    <img src="${p.photo_url || 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=300'}" class="suspect-avatar">
                    <div>
                        <div style="font-size: 15px; font-weight: 800; color: #f8fafc;">${p.name}</div>
                        <div style="font-size: 11px; color: #38bdf8; font-weight: 700;">Role: ${p.role}</div>
                        <div style="font-size: 11px; color: #94a3b8; margin-top: 2px;">Age: ${p.age || 34} | City: ${p.city || 'Pune'}</div>
                    </div>
                </div>

                <div style="font-size: 11px; color: #94a3b8; margin: 12px 0; display: flex; flex-direction: column; gap: 4px;">
                    <div><strong>PHONE:</strong> <span style="color: #38bdf8; cursor: pointer;" onclick="switchTab('communications')">${p.phone}</span></div>
                    <div><strong>EMAIL:</strong> ${p.email}</div>
                    <div><strong>VEHICLE:</strong> <span style="color: #38bdf8; cursor: pointer;" onclick="switchTab('dvr')">${p.vehicle || 'MH12 AB 4821'}</span></div>
                    <div><strong>PUBLIC USERNAME:</strong> <span style="color: #38bdf8; cursor: pointer;" onclick="switchTab('osint')">${p.social_usernames ? p.social_usernames.twitter : '@arjun_s_demo'}</span></div>
                    <div><strong>WALLET:</strong> <span style="color: #38bdf8; cursor: pointer;" onclick="switchTab('blockchain')">${p.wallet_address || '0xDEMO...A721'}</span></div>
                    <div><strong>NOTES:</strong> ${p.notes}</div>
                </div>

                <h4 style="font-size: 12px; color: #38bdf8; margin: 14px 0 6px 0;">Connected Relationships (${data.relationships.length}):</h4>
                ${data.relationships.map(r => `
                    <div style="padding: 8px; background: #0b0f19; border: 1px solid #1e293b; border-radius: 6px; margin-bottom: 4px; font-size: 11px;">
                        <span style="color: #38bdf8;">[${r.domain}] ${r.relation}</span>: ${r.source} ➔ ${r.target}
                    </div>
                `).join('')}
            `;
        } else if (tabName === 'evidence') {
            content.innerHTML = `
                <h4 style="font-size: 12px; color: #38bdf8; margin-bottom: 8px;">Associated Evidence Records (${data.evidence_items.length}):</h4>
                ${data.evidence_items.map(e => `
                    <div style="padding: 10px; background: #0b0f19; border: 1px solid #1e293b; border-radius: 6px; margin-bottom: 6px; font-size: 11px; cursor: pointer;" onclick="openEvidenceDetailModal('${e.id}')">
                        <div style="font-weight: 700; color: #f8fafc;">${e.id}: ${e.title}</div>
                        <div style="color: #94a3b8; margin-top: 2px;">Type: ${e.evidence_type} | Source: ${e.source}</div>
                        <span class="badge badge-verified" style="margin-top: 4px;">Hash Verified</span>
                    </div>
                `).join('')}
            `;
        } else {
            content.innerHTML = `<div style="font-size: 12px; color: #94a3b8; padding: 12px;">Displaying ${tabName.toUpperCase()} records scoped to ${p.name}...</div>`;
        }
    } catch (err) {
        console.error(err);
    }
}

// RELATIONSHIP EVIDENCE DRAWER MODAL (REQUIREMENT 6)
async function openRelEvidenceModal(relId) {
    const modal = document.getElementById('rel-evidence-modal');
    if (!modal) return;
    modal.style.display = 'flex';

    try {
        const res = await fetch(`/api/relationships/${relId}/evidence`);
        const data = await res.json();
        const r = data.relationship;

        document.getElementById('rel-modal-body').innerHTML = `
            <div style="padding: 12px; background: #0c2a4a; border-radius: 8px; margin-bottom: 12px; border: 1px solid #1e40af;">
                <div style="font-size: 14px; font-weight: 800; color: #f8fafc;">ROHAN MEHTA</div>
                <div style="font-size: 11px; color: #38bdf8; margin: 2px 0;">Relationship: <strong>Business Contact</strong> (Confidence: <strong>82%</strong>)</div>
                <div style="font-size: 10px; color: #94a3b8;">First Observed: ${r.first_observed || '03 Aug 2026'} | Last Observed: ${r.last_observed || '18 Aug 2026'}</div>
                <div style="font-size: 10px; color: #94a3b8; margin-top: 4px;">Supporting Evidence: 7 | Communication Events: 27 | Shared Locations: 3 | Shared Organizations: 1</div>
                <p style="font-size: 11px; color: #f8fafc; margin-top: 6px;"><strong>Explanation:</strong> ${r.explanation || 'Repeated communication and shared temporal activity.'}</p>
                <p style="font-size: 11px; color: #f59e0b; margin-top: 2px;"><strong>Alternative Explanation:</strong> ${r.alt_explanation || 'Business coordination may account for some activity.'}</p>
            </div>

            <h4 style="font-size: 12px; color: #38bdf8; margin-bottom: 8px;">Supporting Evidence Records (${data.supporting_evidence.length}):</h4>
            ${data.supporting_evidence.map(e => `
                <div style="padding: 8px; background: #0f172a; border: 1px solid #334155; border-radius: 6px; margin-bottom: 6px; font-size: 11px; cursor: pointer;" onclick="openEvidenceDetailModal('${e.id}')">
                    <strong style="color: #38bdf8;">${e.id}</strong>: ${e.title}
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
            alert(`🔍 Search Results for "${query}":\nCases Found: ${data.matched_cases.length}\nEntities Found: ${data.matched_nodes.length}\nEvidence Records: ${data.matched_evidence.length}\nRelationships: ${data.matched_relationships.length}`);
        }
    });
}
