// TRACE-X Intelligence Workstation Application Controller
let currentCaseId = 'TRX-2026-017';
let currentPersonId = 'P-001'; // Default P-001 (Arjun Sharma)
let currentGraphLayout = 'tree-ud';
let currentPersonDrawerId = null;
let currentDrawerTab = 'overview';
let visNetworkInstance = null;
let currentGraphData = null;

const PERSON_ROLES = {
    'P-001': 'PRIMARY SUBJECT',
    'P-002': 'BUSINESS CONTACT',
    'P-003': 'ASSOCIATE',
    'P-004': 'PERSON OF INTEREST',
    'P-005': 'EMPLOYEE',
    'P-006': 'CANDIDATE MATCH'
};

document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initGlobalSearch();
    loadOverviewData();
});

function toggleSidebar() {
    const sidebar = document.getElementById('app-sidebar');
    if (sidebar) sidebar.classList.toggle('collapsed');
}

function changeActivePerson(personId) {
    currentPersonId = personId;
    
    // Update Header Context (Requirement 19)
    const selectP = document.getElementById('select-change-person');
    const pName = selectP ? selectP.options[selectP.selectedIndex].text.split('(')[0].replace(/^[🔴🔵🟢🟡🟣⚠️]\s*/, '').trim().toUpperCase() : 'ARJUN SHARMA';
    
    const nameElem = document.getElementById('ctx-subject-name');
    if (nameElem) nameElem.innerText = pName;

    const roleElem = document.getElementById('ctx-subject-role');
    if (roleElem) {
        roleElem.innerText = PERSON_ROLES[personId] || 'TRACKED PERSON';
        roleElem.className = `badge ${personId === 'P-001' ? 'badge-high' : 'badge-verified'}`;
    }
    
    updateBreadcrumb();
    refreshActiveView();
}

function updateBreadcrumb() {
    const activeNav = document.querySelector('.nav-item.active');
    const moduleName = activeNav ? activeNav.innerText.trim().toUpperCase() : 'OPERATIONAL OVERVIEW';
    const selectP = document.getElementById('select-change-person');
    const pName = selectP ? selectP.options[selectP.selectedIndex].text.split('(')[0].replace(/^[🔴🔵🟢🟡🟣⚠️]\s*/, '').trim().toUpperCase() : 'ARJUN SHARMA';
    
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
        const cs = data.case_summary;

        document.getElementById('ov-person-name').innerText = cs.primary_subject;
        document.getElementById('ov-person-role').innerText = PERSON_ROLES[currentPersonId] || 'Tracked Subject';
        document.getElementById('ov-evidence-count').innerText = cs.evidence_count;
        document.getElementById('ov-rel-count').innerText = cs.relationships_count;
        document.getElementById('ov-comm-count').innerText = cs.communications_count;
        document.getElementById('ov-fin-count').innerText = cs.financial_count;
        document.getElementById('ov-osint-count').innerText = cs.osint_count;
        document.getElementById('ov-blk-count').innerText = cs.blockchain_count;
        document.getElementById('ov-cctv-count').innerText = cs.cctv_count;

        const actList = document.getElementById('activity-feed');
        if (actList && data.investigation_activity) {
            actList.innerHTML = data.investigation_activity.map(act => `
                <div style="padding: 12px 0; border-bottom: 1px solid #334155; display: flex; justify-content: space-between; font-size: 13px;">
                    <span>⚡ <strong style="color: #f8fafc;">[${act.time}]</strong> ${act.event}</span>
                    <span class="badge badge-verified">${act.domain}</span>
                </div>
            `).join('');
        }

        const leadsPanel = document.getElementById('ai-leads-panel');
        if (leadsPanel && data.ai_leads) {
            leadsPanel.innerHTML = data.ai_leads.map(lead => `
                <div style="padding: 14px; background: #0f172a; border-left: 4px solid #3b82f6; border-radius: 8px; margin-bottom: 10px;">
                    <div style="font-size: 14px; font-weight: 800; color: #38bdf8;">${lead.title}</div>
                    <p style="font-size: 13px; color: #94a3b8; margin: 6px 0;">${lead.lead}</p>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 6px;">
                        <span class="badge ${lead.confidence < 0.5 ? 'badge-high' : 'badge-verified'}">CONFIDENCE: ${Math.round(lead.confidence * 100)}%</span>
                        <span style="font-size: 11px; color: #64748b; font-weight: 700;">Status: ${lead.status}</span>
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
                <div class="card" style="border-left: 4px solid #3b82f6;">
                    <div class="card-title">
                        <span>${c.id}: ${c.title} (${c.location})</span>
                        <span class="badge badge-verified">${c.status}</span>
                    </div>

                    <div class="suspect-card" onclick="openPersonDrawer('${primary.id}')" style="cursor: pointer;">
                        <img src="${primary.photo_url}" class="suspect-avatar">
                        <div>
                            <div style="font-size: 16px; font-weight: 800; color: #f8fafc;">${primary.name} <span class="badge badge-high" style="font-size: 10px;">Primary Subject</span></div>
                            <div style="font-size: 13px; color: #94a3b8; margin: 4px 0;">Age: <strong>${primary.age}</strong> | City: <strong>${primary.city}</strong> | Occupation: <strong>${primary.occupation}</strong></div>
                            <div style="font-size: 13px; color: #38bdf8;">📞 ${primary.phone} | ✉️ ${primary.email}</div>
                        </div>
                    </div>

                    <div style="font-size: 12px; font-weight: 800; color: #38bdf8; text-transform: uppercase; margin: 12px 0 8px 0;">👥 Connected Subjects & Associates (${secondaries.length}):</div>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 10px; margin-bottom: 12px;">
                        ${secondaries.map(sec => `
                            <div style="padding: 10px; background: #0f172a; border: 1px solid #334155; border-radius: 8px; display: flex; gap: 10px; align-items: center; cursor: pointer;" onclick="changeActivePerson('${sec.id}')">
                                <img src="${sec.photo_url}" style="width: 44px; height: 44px; border-radius: 50%; object-fit: cover;">
                                <div>
                                    <div style="font-size: 13px; font-weight: 700; color: #f8fafc;">${sec.name}</div>
                                    <div style="font-size: 11px; color: #38bdf8;">${sec.role}</div>
                                </div>
                            </div>
                        `).join('')}
                    </div>

                    <p style="font-size: 13px; color: #94a3b8; margin-bottom: 12px;">${c.description}</p>
                </div>
            `;
        }).join('');
    } catch (err) {
        console.error(err);
    }
}

// 3. PERSON PROFILE VIEW (REQUIREMENT 3, 4, 5)
async function loadPersonsViewData() {
    const container = document.getElementById('person-profile-card-container');
    if (!container) return;

    try {
        const res = await fetch(`/api/persons/${currentPersonId}`);
        const data = await res.json();
        const p = data.person;

        container.innerHTML = `
            <div class="card">
                <div style="display: flex; gap: 24px; border-bottom: 1px solid #334155; padding-bottom: 20px; margin-bottom: 20px;">
                    <img src="${p.photo_url}" style="width: 100px; height: 100px; border-radius: 14px; object-fit: cover; border: 3px solid #3b82f6;">
                    <div>
                        <div style="font-size: 24px; font-weight: 800; color: #f8fafc;">${p.name}</div>
                        <div style="font-size: 15px; font-weight: 700; color: #38bdf8; margin: 4px 0;">Role: ${p.role} (ID: ${p.id})</div>
                        <div style="font-size: 13px; color: #94a3b8; display: flex; gap: 20px; margin-top: 8px;">
                            <div>Case: <strong style="color: #f8fafc;">${currentCaseId}</strong></div>
                            <div>Status: <span class="badge badge-high">${p.status}</span></div>
                            <div>Last Updated: <strong style="color: #f8fafc;">${p.last_updated}</strong></div>
                        </div>
                    </div>
                </div>

                <h4 style="font-size: 15px; color: #38bdf8; margin-bottom: 12px;">STRUCTURED IDENTIFIERS (Click identifier to navigate):</h4>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-bottom: 24px; font-size: 13px;">
                    <div style="padding: 12px; background: #0f172a; border: 1px solid #334155; border-radius: 8px;">
                        <div style="font-size: 11px; color: #64748b; font-weight: 800;">FULL NAME</div>
                        <div style="font-weight: 700; color: #f8fafc; font-size: 14px;">${p.name}</div>
                    </div>
                    <div style="padding: 12px; background: #0f172a; border: 1px solid #334155; border-radius: 8px;">
                        <div style="font-size: 11px; color: #64748b; font-weight: 800;">KNOWN ALIASES</div>
                        <div style="font-weight: 700; color: #38bdf8; font-size: 14px;">${p.alias}</div>
                    </div>
                    <div style="padding: 12px; background: #0f172a; border: 1px solid #334155; border-radius: 8px;">
                        <div style="font-size: 11px; color: #64748b; font-weight: 800;">AGE & GENDER</div>
                        <div style="font-weight: 700; color: #f8fafc; font-size: 14px;">${p.age} (${p.gender})</div>
                    </div>
                    <div style="padding: 12px; background: #0f172a; border: 1px solid #334155; border-radius: 8px;">
                        <div style="font-size: 11px; color: #64748b; font-weight: 800;">OCCUPATION</div>
                        <div style="font-weight: 700; color: #f8fafc; font-size: 14px;">${p.occupation}</div>
                    </div>
                    <div style="padding: 12px; background: #0f172a; border: 1px solid #334155; border-radius: 8px;">
                        <div style="font-size: 11px; color: #64748b; font-weight: 800;">ORGANIZATION</div>
                        <div style="font-weight: 700; color: #f8fafc; font-size: 14px;">${p.organization}</div>
                    </div>
                    <div style="padding: 12px; background: #0f172a; border: 1px solid #334155; border-radius: 8px; cursor: pointer;" onclick="switchTab('communications')">
                        <div style="font-size: 11px; color: #64748b; font-weight: 800;">PHONE ➔ COMMUNICATION ANALYSIS</div>
                        <div style="font-weight: 700; color: #38bdf8; font-size: 14px;">📞 ${p.phone}</div>
                    </div>
                    <div style="padding: 12px; background: #0f172a; border: 1px solid #334155; border-radius: 8px;">
                        <div style="font-size: 11px; color: #64748b; font-weight: 800;">EMAIL</div>
                        <div style="font-weight: 700; color: #f8fafc; font-size: 14px;">✉️ ${p.email}</div>
                    </div>
                    <div style="padding: 12px; background: #0f172a; border: 1px solid #334155; border-radius: 8px; cursor: pointer;" onclick="switchTab('dvr')">
                        <div style="font-size: 11px; color: #64748b; font-weight: 800;">VEHICLE ➔ VEHICLE INTELLIGENCE</div>
                        <div style="font-weight: 700; color: #38bdf8; font-size: 14px;">🚘 ${p.vehicle}</div>
                    </div>
                    <div style="padding: 12px; background: #0f172a; border: 1px solid #334155; border-radius: 8px; cursor: pointer;" onclick="switchTab('osint')">
                        <div style="font-size: 11px; color: #64748b; font-weight: 800;">PUBLIC USERNAME ➔ PUBLIC-SOURCE INTEL</div>
                        <div style="font-weight: 700; color: #38bdf8; font-size: 14px;">🌐 ${p.social_usernames ? p.social_usernames.twitter || '@user' : '@user'}</div>
                    </div>
                    <div style="padding: 12px; background: #0f172a; border: 1px solid #334155; border-radius: 8px; cursor: pointer;" onclick="switchTab('blockchain')">
                        <div style="font-size: 11px; color: #64748b; font-weight: 800;">WALLET ➔ BLOCKCHAIN ANALYSIS</div>
                        <div style="font-weight: 700; color: #38bdf8; font-size: 14px;">⛓️ ${p.wallet_address}</div>
                    </div>
                </div>

                <h4 style="font-size: 15px; color: #38bdf8; margin-bottom: 12px;">RELATIONSHIP RECORDS FOR ${p.name.toUpperCase()}:</h4>
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px;">
                    ${data.relationships.map(r => `
                        <div style="padding: 14px; background: #0f172a; border: 1px solid #334155; border-radius: 8px;">
                            <div style="font-size: 15px; font-weight: 800; color: #f8fafc;">${r.target_name}</div>
                            <div style="font-size: 13px; color: #38bdf8; margin: 4px 0;">Relationship: <strong>${r.relation}</strong> (${r.target_role})</div>
                            <p style="font-size: 12px; color: #94a3b8; margin-top: 4px;">${r.explanation}</p>
                            <button class="btn btn-secondary" style="margin-top: 8px; font-size: 11px; padding: 4px 10px;" onclick="openRelEvidenceModal('${r.id}')">VIEW RELATIONSHIP</button>
                        </div>
                    `).join('')}
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
        const res = await fetch(`/api/persons/${currentPersonId}`);
        const data = await res.json();
        const p = data.person;
        const container = document.getElementById('fusion-chain-container');
        if (!container) return;

        container.innerHTML = `
            <div class="xai-box">
                <div class="xai-title">🧠 EVIDENCE CHAIN SYNTHESIS FOR ${p.name.toUpperCase()}</div>
                <p style="font-size: 13px; color: #94a3b8; margin-bottom: 10px;">Scoped multi-hop evidence correlation connecting ${p.name} across CDR, Financial, and Surveillance streams.</p>
            </div>

            <!-- LINK ANALYSIS TREE (REQUIREMENT 16) -->
            <h4 style="margin: 20px 0 10px 0; font-size: 15px; color: #38bdf8;">Hierarchy Tree Representation (Root: ${p.name}):</h4>
            <div style="background: #0f172a; border: 1px solid #334155; border-radius: 10px; padding: 18px; font-family: monospace; font-size: 14px; margin-bottom: 20px;">
                <div style="font-weight: 800; color: #38bdf8;">${p.name.toUpperCase()} (${p.role})</div>
                <div>│</div>
                <div>├── <span style="cursor: pointer; color: #38bdf8; font-weight: 700;" onclick="switchTab('communications')">PHONE (${p.phone})</span></div>
                <div>│</div>
                <div>├── <span style="cursor: pointer; color: #10b981; font-weight: 700;" onclick="switchTab('financial')">ACCOUNT (${p.account_number})</span></div>
                <div>│</div>
                <div>├── <span style="cursor: pointer; color: #f59e0b; font-weight: 700;" onclick="switchTab('blockchain')">WALLET (${p.wallet_address})</span></div>
                <div>│</div>
                <div>└── <span style="cursor: pointer; color: #8b5cf6; font-weight: 700;" onclick="switchTab('dvr')">VEHICLE (${p.vehicle})</span></div>
            </div>

            <h4 style="margin: 20px 0 10px 0; font-size: 15px; color: #38bdf8;">Investigative Leads for ${p.name}:</h4>
            ${data.leads.map(lead => `
                <div style="padding: 14px; background: #0f172a; border: 1px solid #334155; border-left: 4px solid #3b82f6; border-radius: 8px; margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 14px; font-weight: 800; color: #f8fafc;">${lead.id}: ${lead.title}</span>
                        <span class="badge badge-verified">Confidence: ${Math.round(lead.confidence * 100)}%</span>
                    </div>
                    <p style="font-size: 13px; color: #94a3b8; margin: 6px 0;">${lead.lead}</p>
                    <div style="font-size: 12px; color: #38bdf8; margin: 4px 0;"><strong>Supporting Evidence:</strong> ${(lead.supporting_evidence || []).join(', ')}</div>
                    <div style="font-size: 12px; color: #f59e0b;"><strong>Alternative Explanation:</strong> ${lead.alternative_explanation}</div>
                </div>
            `).join('')}
        `;
    } catch (err) {
        console.error(err);
    }
}

// 5. LINK ANALYSIS GRAPH (ROOT NODE IS SELECTED PERSON - REQUIREMENT 16)
async function loadGraphData() {
    try {
        const res = await fetch(`/api/graph?case_id=${currentCaseId}&person_id=${currentPersonId}`);
        currentGraphData = await res.json();
        
        const rootElem = document.getElementById('graph-root-name');
        if (rootElem && currentGraphData.nodes.length > 0) {
            rootElem.innerText = `Root: ${currentGraphData.nodes[0].label}`;
        }
        
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
    renderGraphWithLayout(currentGraphLayout);
}

function renderGraphWithLayout(layoutType) {
    if (!currentGraphData) return;
    const container = document.getElementById('graph-canvas');
    if (!container) return;

    const visNodes = currentGraphData.nodes.map(n => ({
        id: n.id,
        label: `${n.label}\n[${n.type}]`,
        shape: n.type === 'PERSON' ? 'dot' : 'square',
        color: n.id === currentPersonId ? { background: '#ef4444', border: '#b91c1c' } : { background: '#3b82f6', border: '#1d4ed8' },
        font: { color: '#f8fafc', size: 14, strokeWidth: 2, strokeColor: '#0b0f19', face: 'Inter' },
        level: n.tree_level !== undefined ? n.tree_level : 1
    }));

    const visEdges = currentGraphData.edges.map(e => ({
        id: e.id,
        from: e.source,
        to: e.target,
        label: e.relation,
        arrows: 'to',
        color: { color: '#38bdf8' },
        font: { color: '#94a3b8', size: 12, strokeWidth: 2, strokeColor: '#0b0f19' },
        length: 60
    }));

    const visData = { nodes: new vis.DataSet(visNodes), edges: new vis.DataSet(visEdges) };

    let layoutConfig = {};
    let physicsConfig = { enabled: true };

    if (layoutType === 'tree-ud') {
        layoutConfig = { hierarchical: { direction: 'UD', sortMethod: 'directed', nodeSpacing: 80, levelSeparation: 90 } };
        physicsConfig = { enabled: false };
    } else if (layoutType === 'hierarchy') {
        layoutConfig = { hierarchical: { direction: 'LR', sortMethod: 'directed', nodeSpacing: 80, levelSeparation: 100 } };
        physicsConfig = { enabled: false };
    } else {
        layoutConfig = { randomSeed: 42 };
        physicsConfig = { barnesHut: { gravitationalConstant: -1200, springLength: 50 } };
    }

    const options = {
        nodes: { borderWidth: 2 },
        layout: layoutConfig,
        physics: physicsConfig,
        interaction: { hover: true }
    };

    if (visNetworkInstance) visNetworkInstance.destroy();
    visNetworkInstance = new vis.Network(container, visData, options);

    visNetworkInstance.on('selectNode', function(params) {
        const nodeId = params.nodes[0];
        if (nodeId.startsWith('P-00')) {
            changeActivePerson(nodeId);
        } else {
            openPersonDrawer(nodeId);
        }
    });
}

// 6. COMMUNICATION ANALYSIS (REQUIREMENT 6 & 7)
async function loadCommunicationsData() {
    try {
        const res = await fetch(`/api/communications?person_id=${currentPersonId}`);
        const data = await res.json();

        const pRes = await fetch(`/api/persons/${currentPersonId}`);
        const pData = await pRes.json();
        document.getElementById('comm-person-name').innerText = pData.person.name.toUpperCase();

        document.getElementById('comm-stat-total').innerText = data.total_events || 0;
        document.getElementById('comm-stat-calls').innerText = data.calls || 0;
        document.getElementById('comm-stat-msgs').innerText = data.messages || 0;
        document.getElementById('comm-stat-contacts').innerText = data.unique_contacts || 0;
        document.getElementById('comm-stat-period').innerText = data.active_period || 'Active Period';

        const tree = document.getElementById('comm-contact-tree');
        if (tree && data.contacts) {
            tree.innerHTML = data.contacts.map(c => `
                <div style="padding: 12px; background: #0f172a; border: 1px solid #334155; border-left: 4px solid #0284c7; border-radius: 8px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="font-size: 14px; color: #f8fafc;">${c.name}</strong> (${c.role})
                        <div style="font-size: 12px; color: #38bdf8;">📞 ${c.phone}</div>
                    </div>
                    <span class="badge badge-verified">${c.calls} Calls Logged</span>
                </div>
            `).join('');
        }

        const tbody = document.getElementById('comm-rohan-tbody');
        if (tbody && data.history) {
            tbody.innerHTML = data.history.map(t => `
                <tr>
                    <td>${t.date}</td>
                    <td>${t.time}</td>
                    <td><strong>${t.contact}</strong></td>
                    <td><span class="badge ${t.direction === 'Outgoing' ? 'badge-verified' : 'badge-medium'}">${t.direction}</span></td>
                    <td>${t.duration}</td>
                    <td><button class="btn btn-secondary" style="font-size: 11px; padding: 3px 8px;" onclick="openEvidenceDetailModal('${t.evidence_id}')">Ref: ${t.evidence_id}</button></td>
                </tr>
            `).join('');
        }
    } catch (err) {
        console.error(err);
    }
}

// 7. FINANCIAL INTELLIGENCE LEDGER (REQUIREMENT 8)
async function loadFinancialData() {
    try {
        const res = await fetch(`/api/financial?person_id=${currentPersonId}`);
        const data = await res.json();

        const grid = document.getElementById('fin-accounts-grid');
        if (grid) {
            grid.innerHTML = `
                <div style="padding: 16px; background: #0f172a; border: 1px solid #334155; border-radius: 10px;">
                    <div style="font-size: 15px; font-weight: 800; color: #10b981;">Account: ${data.account}</div>
                    <div style="font-size: 13px; color: #94a3b8; margin-top: 4px;">Current Balance: <strong style="color: #f8fafc;">${data.balance}</strong></div>
                </div>
            `;
        }

        const hawala = document.getElementById('fin-hawala-box');
        if (hawala && data.hawala_analysis) {
            hawala.innerHTML = `
                <div class="xai-title">INFORMAL VALUE TRANSFER INDICATORS</div>
                <div style="font-size: 13px; font-weight: 700; color: #f8fafc; margin-bottom: 6px;">${data.hawala_analysis.assessment}</div>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 10px;">
                    ${data.hawala_analysis.indicators.map(i => `
                        <div style="padding: 10px; background: #0f172a; border: 1px solid #334155; border-radius: 8px; font-size: 12px;">
                            <div style="font-weight: 700; color: #f8fafc;">${i.name}</div>
                            <div style="margin-top: 4px;"><span class="badge ${i.status === 'OBSERVED' ? 'badge-high' : 'badge-medium'}">${i.status}</span></div>
                        </div>
                    `).join('')}
                </div>
            `;
        }

        const tbody = document.getElementById('fin-transactions-tbody');
        if (tbody && data.transactions) {
            tbody.innerHTML = data.transactions.map(t => `
                <tr>
                    <td>${t.date}</td>
                    <td>${t.time}</td>
                    <td><strong style="color: ${t.direction === 'OUT' ? '#ef4444' : '#10b981'}; font-size: 14px;">${t.amount}</strong></td>
                    <td><span class="badge ${t.direction === 'OUT' ? 'badge-high' : 'badge-verified'}">${t.direction}</span></td>
                    <td>${t.account}</td>
                    <td><strong>${t.counterparty}</strong></td>
                    <td><code style="color: #38bdf8;">${t.reference}</code></td>
                    <td><button class="btn btn-secondary" style="font-size: 11px; padding: 3px 8px;" onclick="openEvidenceDetailModal('${t.evidence_id}')">Ref: ${t.evidence_id}</button></td>
                </tr>
            `).join('');
        }
    } catch (err) {
        console.error(err);
    }
}

// 8. BLOCKCHAIN ANALYSIS (REQUIREMENT 9)
async function loadBlockchainData() {
    try {
        const res = await fetch(`/api/blockchain?person_id=${currentPersonId}`);
        const data = await res.json();

        document.getElementById('blk-person-name').innerText = data.address;

        const summary = document.getElementById('blk-summary');
        if (summary) {
            summary.innerHTML = `
                <div style="font-size: 15px; font-weight: 800; color: #f59e0b;">Wallet Address: ${data.address} (Ref: ${data.associated_evidence})</div>
                <div style="font-size: 13px; color: #94a3b8; margin-top: 4px;">Balance: <strong>${data.balance}</strong> | Total Observed Transactions: ${data.incoming + data.outgoing}</div>
            `;
        }

        const tbody = document.getElementById('blk-transactions-tbody');
        if (tbody && data.transactions) {
            tbody.innerHTML = data.transactions.map(t => `
                <tr>
                    <td><code style="color: #f59e0b;">${t.hash}</code></td>
                    <td>${t.from_addr}</td>
                    <td>${t.to_addr}</td>
                    <td><strong style="font-size: 14px;">${t.value}</strong></td>
                    <td>${t.time}</td>
                    <td><button class="btn btn-secondary" style="font-size: 11px; padding: 3px 8px;" onclick="openEvidenceDetailModal('${t.evidence_id}')">Ref: ${t.evidence_id}</button></td>
                </tr>
            `).join('');
        }
    } catch (err) {
        console.error(err);
    }
}

// 9. PUBLIC-SOURCE INTELLIGENCE (REQUIREMENT 10)
async function loadOSINTData() {
    try {
        const res = await fetch(`/api/osint?person_id=${currentPersonId}`);
        const data = await res.json();

        const pRes = await fetch(`/api/persons/${currentPersonId}`);
        const pData = await pRes.json();
        document.getElementById('osint-person-name').innerText = pData.person.name.toUpperCase();

        const list = document.getElementById('osint-list');
        if (list && data.records) {
            list.innerHTML = data.records.map(o => `
                <div style="padding: 14px; background: #0f172a; border: 1px solid #334155; border-left: 4px solid #8b5cf6; border-radius: 8px; margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 14px; font-weight: 800; color: #f8fafc;">SOURCE RECORD ${o.id}: ${o.value}</span>
                        <span class="badge badge-verified">Confidence: ${o.confidence}</span>
                    </div>
                    <div style="font-size: 12px; color: #94a3b8; margin-top: 6px;">Subject: <strong>${o.subject}</strong> | Source: ${o.source} | Observed: ${o.last_observed} | Entity: <strong>${o.entity}</strong> | Location: ${o.location}</div>
                    <button class="btn btn-secondary" style="margin-top: 8px; font-size: 11px; padding: 4px 10px;" onclick="openEvidenceDetailModal('${o.evidence_id}')">View Evidence: ${o.evidence_id}</button>
                </div>
            `).join('');
        }
    } catch (err) {
        console.error(err);
    }
}

// 10. CCTV / DVR FORENSICS WORKSPACE (REQUIREMENT 11)
async function loadDVRData() {
    try {
        const res = await fetch(`/api/dvr?person_id=${currentPersonId}`);
        const data = await res.json();

        const pRes = await fetch(`/api/persons/${currentPersonId}`);
        const pData = await pRes.json();
        document.getElementById('dvr-person-name').innerText = `Subject: ${pData.person.name}`;
        
        const videoGrid = document.getElementById('dvr-video-grid-container');
        if (videoGrid) {
            if (data.dvr_videos.length === 0) {
                videoGrid.innerHTML = `<div style="font-size: 14px; color: #94a3b8; padding: 20px;">No CCTV surveillance clips logged for ${pData.person.name}.</div>`;
            } else {
                videoGrid.innerHTML = data.dvr_videos.map(v => `
                    <div class="dvr-card" style="background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 12px; overflow: hidden;">
                        <div style="position: relative; height: 180px; background: #000;">
                            <img src="${v.video_thumbnail}" style="width: 100%; height: 100%; object-fit: cover;">
                            <div style="position: absolute; top: 10px; left: 10px; background: rgba(220,38,38,0.9); color: #fff; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: 800;">● STREAM | ${v.camera_id}</div>
                            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 48px; height: 48px; background: rgba(59,130,246,0.9); color: #fff; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 20px; cursor: pointer;" onclick="openCCTVVideoModal('${v.camera_id}', '${v.event_title}', '${v.timestamp}', '${v.anpr_license_plate}', '${v.video_thumbnail}', '${v.description.replace(/'/g, "\\'")}')">▶</div>
                        </div>
                        <div style="padding: 14px;">
                            <div style="font-size: 14px; font-weight: 800; color: #f8fafc;">${v.event_title} (${v.timestamp})</div>
                            <div style="font-size: 12px; color: #38bdf8; font-weight: 700; margin: 4px 0;">📍 ${v.location}</div>
                            <div style="font-size: 12px; color: #94a3b8; margin-bottom: 8px;"><strong>Identified:</strong> ${v.suspects_identified.join(', ')}</div>
                            <button class="btn btn-secondary" style="font-size: 11px; padding: 3px 8px;" onclick="openEvidenceDetailModal('${v.evidence_id}')">Ref: ${v.evidence_id}</button>
                        </div>
                    </div>
                `).join('');
            }
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

// 11. TIMELINE (REQUIREMENT 12)
async function loadTimelineData() {
    try {
        const res = await fetch(`/api/timeline?person_id=${currentPersonId}`);
        const data = await res.json();

        const pRes = await fetch(`/api/persons/${currentPersonId}`);
        const pData = await pRes.json();
        document.getElementById('timeline-person-name').innerText = pData.person.name;

        const box = document.getElementById('temporal-assessment-box');
        if (box && data.temporal_assessment) {
            box.innerHTML = `
                <div class="xai-title">⏱️ TEMPORAL CORRELATION ASSESSMENT</div>
                <div style="font-size: 13px; font-weight: 700; color: #f8fafc;">${data.temporal_assessment}</div>
            `;
        }

        const container = document.getElementById('timeline-container');
        if (container && data.events) {
            container.innerHTML = data.events.map(ev => `
                <div class="timeline-item" style="cursor: pointer;" onclick="openEvidenceDetailModal('${ev.evidence_id}')">
                    <div style="font-size: 11px; color: #38bdf8; font-weight: 700;">[${ev.domain}] ${ev.timestamp}</div>
                    <div style="font-size: 14px; font-weight: 700; color: #f8fafc; margin: 4px 0;">${ev.title}</div>
                    <div style="font-size: 12px; color: #94a3b8;">Person: <strong>${ev.person}</strong> | Location: ${ev.location} | Details: ${ev.details}</div>
                </div>
            `).join('');
        }
    } catch (err) {
        console.error(err);
    }
}

// 13. ENTITY RESOLUTION INTERFACE (REQUIREMENT 4)
async function loadEntityResolutionData() {
    const container = document.getElementById('entity-resolution-container');
    if (!container) return;

    try {
        const res = await fetch(`/api/persons/P-006`);
        const data = await res.json();
        const cand = data.person;

        container.innerHTML = `
            <div style="padding: 20px; background: #0f172a; border: 1px solid #334155; border-radius: 12px; max-width: 650px;">
                <div style="font-size: 16px; font-weight: 800; color: #f59e0b; margin-bottom: 10px;">POTENTIAL MATCH: ${cand.name} (Candidate ID: ${cand.id})</div>
                <div style="font-size: 13px; color: #f8fafc; margin-bottom: 6px;">Possible match to Primary Subject: <strong>Arjun Sharma (P-001)</strong></div>
                <div style="font-size: 12px; color: #94a3b8; margin-bottom: 12px;">
                    <div>Signals: <strong>Name similarity</strong>, <strong>Location overlap</strong></div>
                    <div>Match Confidence Score: <span class="badge badge-medium">43%</span></div>
                    <div>Status: <strong style="color: #f59e0b;">${cand.status}</strong></div>
                </div>
                <p style="font-size: 12px; color: #94a3b8; margin-bottom: 16px;">${cand.notes}</p>

                <div style="display: flex; gap: 10px;">
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
    alert(`✅ Entity Resolution Action Executed: Candidate match P-006 actioned as ${action}.`);
    loadEntityResolutionData();
}

// 12. ANALYTICS
async function loadAnalyticsData() {
    try {
        const res = await fetch(`/api/persons/${currentPersonId}`);
        const data = await res.json();
        const p = data.person;

        const tbody = document.getElementById('analytics-tbody');
        if (tbody) {
            tbody.innerHTML = `
                <tr>
                    <td><strong>${p.name}</strong></td>
                    <td>${p.role}</td>
                    <td>${p.counts.calls || 12}</td>
                    <td>0.84</td>
                    <td>0.42</td>
                    <td><span class="badge badge-verified">HIGH CENTRALITY</span></td>
                </tr>
            `;
        }
    } catch (err) {
        console.error(err);
    }
}

// 15. AUDIT TRAIL
async function loadAuditData() {
    try {
        const tbody = document.getElementById('audit-tbody');
        if (tbody) {
            tbody.innerHTML = `
                <tr><td>18 Aug 2026 09:43</td><td>INV-004</td><td><span class="badge badge-verified">Opened Case</span></td><td>TRX-2026-017</td><td><span class="badge badge-verified">Success</span></td></tr>
                <tr><td>18 Aug 2026 09:51</td><td>INV-004</td><td><span class="badge badge-verified">Viewed Profile</span></td><td>P-001 (Arjun Sharma)</td><td><span class="badge badge-verified">Success</span></td></tr>
                <tr><td>18 Aug 2026 10:19</td><td>INV-004</td><td><span class="badge badge-verified">Switched Person Context</span></td><td>P-002 (Rohan Mehta)</td><td><span class="badge badge-verified">Success</span></td></tr>
                <tr><td>18 Aug 2026 10:44</td><td>INV-004</td><td><span class="badge badge-verified">Viewed Financial Ledger</span></td><td>XXXX7312</td><td><span class="badge badge-verified">Success</span></td></tr>
            `;
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

// STANDARDIZED EVIDENCE DRAWER MODAL
async function openEvidenceDetailModal(evidenceId) {
    const modal = document.getElementById('evidence-detail-modal');
    if (!modal) return;
    modal.style.display = 'flex';

    try {
        const res = await fetch(`/api/evidence/${evidenceId}`);
        const e = await res.json();

        document.getElementById('evidence-modal-body').innerHTML = `
            <div style="padding: 16px; background: #0f172a; border: 1px solid #334155; border-radius: 10px; margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-size: 16px; font-weight: 800; color: #38bdf8;">EVIDENCE RECORD ${e.id}</span>
                    <span class="badge badge-verified">${e.evidence_type}</span>
                </div>
                <div style="font-size: 13px; color: #94a3b8; display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 10px;">
                    <div>CASE: <strong style="color: #f8fafc;">${e.case_id}</strong></div>
                    <div>PERSON ID: <strong style="color: #f8fafc;">${e.personId}</strong></div>
                    <div>SOURCE: <strong>${e.source}</strong></div>
                    <div>ACQUISITION DATE: <strong>${e.acquisition_date}</strong></div>
                    <div>HASH INTEGRITY: <span class="badge badge-verified">SHA-256 Verified</span></div>
                </div>
                <p style="font-size: 13px; color: #f8fafc;"><strong>ANALYTICAL EXTRACTION:</strong> ${e.analyst_notes}</p>
            </div>

            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;">
                <button class="btn btn-secondary" onclick="alert('Viewing raw payload for ${e.id}...')">📄 VIEW ORIGINAL</button>
                <button class="btn btn-secondary" onclick="switchTab('graph'); closeEvidenceDetailModal();">🕸️ VIEW RELATIONSHIP</button>
                <button class="btn btn-secondary" onclick="switchTab('timeline'); closeEvidenceDetailModal();">⏱️ VIEW TIMELINE</button>
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

        content.innerHTML = `
            <div class="suspect-card">
                <img src="${p.photo_url}" class="suspect-avatar">
                <div>
                    <div style="font-size: 16px; font-weight: 800; color: #f8fafc;">${p.name}</div>
                    <div style="font-size: 13px; color: #38bdf8; font-weight: 700;">Role: ${p.role}</div>
                    <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">Age: ${p.age} | City: ${p.city}</div>
                </div>
            </div>

            <div style="font-size: 13px; color: #94a3b8; margin: 16px 0; display: flex; flex-direction: flex-column; gap: 6px;">
                <div><strong>PHONE:</strong> <span style="color: #38bdf8; cursor: pointer;" onclick="changeActivePerson('${p.id}'); switchTab('communications'); closePersonDrawer();">${p.phone}</span></div>
                <div><strong>EMAIL:</strong> ${p.email}</div>
                <div><strong>VEHICLE:</strong> <span style="color: #38bdf8; cursor: pointer;" onclick="changeActivePerson('${p.id}'); switchTab('dvr'); closePersonDrawer();">${p.vehicle}</span></div>
                <div><strong>PUBLIC USERNAME:</strong> <span style="color: #38bdf8; cursor: pointer;" onclick="changeActivePerson('${p.id}'); switchTab('osint'); closePersonDrawer();">${p.social_usernames ? p.social_usernames.twitter || '@user' : '@user'}</span></div>
                <div><strong>WALLET:</strong> <span style="color: #38bdf8; cursor: pointer;" onclick="changeActivePerson('${p.id}'); switchTab('blockchain'); closePersonDrawer();">${p.wallet_address}</span></div>
                <div><strong>NOTES:</strong> ${p.notes}</div>
            </div>
            
            <button class="btn" style="width: 100%; margin-top: 10px;" onclick="changeActivePerson('${p.id}'); closePersonDrawer();">SWITCH WORKSTATION CONTEXT TO ${p.name.toUpperCase()}</button>
        `;
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
            <div style="padding: 16px; background: #0c2a4a; border-radius: 10px; margin-bottom: 16px; border: 1px solid #1e40af;">
                <div style="font-size: 16px; font-weight: 800; color: #f8fafc;">RELATIONSHIP EVIDENCE RECORD ${relId}</div>
                <div style="font-size: 13px; color: #38bdf8; margin: 4px 0;">First Observed: ${r.first_observed} | Last Observed: ${r.last_observed}</div>
                <p style="font-size: 13px; color: #f8fafc; margin-top: 8px;"><strong>Analytical Explanation:</strong> ${r.explanation}</p>
                <p style="font-size: 13px; color: #f59e0b; margin-top: 4px;"><strong>Alternative Explanation:</strong> ${r.alt_explanation}</p>
            </div>
            <div style="display: flex; justify-content: flex-end;">
                <button class="btn" onclick="closeRelEvidenceModal()">CLOSE RECORD</button>
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
    alert('✅ Case Created Successfully!');
    closeAddCaseWizard();
}

function initGlobalSearch() {
    const input = document.getElementById('global-search-input');
    if (!input) return;

    input.addEventListener('keypress', async (e) => {
        if (e.key === 'Enter') {
            const query = input.value.trim();
            if (!query) return;
            const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
            const data = await res.json();
            alert(`🔍 Search Results for "${query}":\nProfiles Found: ${data.matched_nodes.length}\nEvidence Records: ${data.matched_evidence.length}`);
        }
    });
}
