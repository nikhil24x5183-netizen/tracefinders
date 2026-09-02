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
        'person_arjun_sharma': 'Arjun Sharma',
        'person_rohan_mehta': 'Rohan Mehta',
        'person_priya_joshi': 'Priya Joshi',
        'person_vikram_patil': 'Vikram Patil',
        'person_neha_kulkarni': 'Neha Kulkarni'
    };
    const pName = personNames[personId] || personId;
    document.getElementById('ctx-subject-name').innerText = pName;
    
    updateBreadcrumb();
    refreshActiveView();
}

function updateBreadcrumb() {
    const pName = document.getElementById('ctx-subject-name').innerText.toUpperCase();
    const activeNav = document.querySelector('.nav-item.active');
    const moduleName = activeNav ? activeNav.innerText.trim().toUpperCase() : 'DASHBOARD';
    
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

        const s = data.case_summary;
        document.getElementById('overview-primary-name').innerText = s.primary_subject;
        document.getElementById('stat-sec-count').innerText = s.secondary_subjects_count;
        document.getElementById('stat-entities').innerText = s.entities_count;
        document.getElementById('stat-evidence').innerText = s.evidence_count;
        document.getElementById('stat-relationships').innerText = s.relationships_count;
        document.getElementById('stat-events').innerText = s.temporal_events_count;

        const actList = document.getElementById('activity-feed');
        if (actList) {
            actList.innerHTML = data.recent_activity.map(act => `
                <div style="padding: 8px 0; border-bottom: 1px solid #e2e8f0; display: flex; justify-content: space-between; font-size: 11px;">
                    <span>⚡ <strong style="color: #0f172a;">${act.event}</strong></span>
                    <span style="color: #64748b;">${act.time}</span>
                </div>
            `).join('');
        }

        const leadsPanel = document.getElementById('ai-leads-panel');
        if (leadsPanel) {
            leadsPanel.innerHTML = data.ai_leads.map(lead => `
                <div style="padding: 12px; background: #f0f9ff; border-left: 3px solid #0284c7; border-radius: 8px; margin-bottom: 8px;">
                    <div style="font-size: 12px; font-weight: 800; color: #0369a1;">${lead.title}</div>
                    <p style="font-size: 11px; color: #475569; margin: 4px 0;">${lead.summary}</p>
                    <span class="badge badge-verified">CONFIDENCE: ${lead.confidence * 100}%</span>
                </div>
            `).join('');
        }
    } catch (err) {
        console.error(err);
    }
}

// 2. CASES SECTION
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
                        <span>${c.id}: ${c.title}</span>
                        <span class="badge ${c.priority === 'High' ? 'badge-high' : 'badge-verified'}">${c.priority} Priority</span>
                    </div>

                    <!-- PRIMARY SUBJECT IDENTITY CARD -->
                    <div class="suspect-card" onclick="openPersonDrawer('${primary.id}')" style="cursor: pointer;">
                        <img src="${primary.photo_url || 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=300'}" class="suspect-avatar">
                        <div>
                            <div style="font-size: 14px; font-weight: 800; color: #0f172a;">${primary.name} <span class="badge badge-high" style="font-size: 9px;">Primary Subject</span></div>
                            <div style="font-size: 11px; color: #475569; margin: 2px 0;">Age: <strong>${primary.age || 34}</strong> | Location: <strong>${primary.city || 'Pune'}</strong> | Occupation: <strong>${primary.occupation || 'Consultant'}</strong></div>
                            <div style="font-size: 11px; color: #2563eb;">📞 ${primary.phone} | ✉️ ${primary.email}</div>
                        </div>
                    </div>

                    <!-- SECONDARY SUBJECTS -->
                    ${secondaries.length > 0 ? `
                        <div style="font-size: 10px; font-weight: 800; color: #0284c7; text-transform: uppercase; margin: 10px 0 6px 0;">👥 Secondary Subjects & Persons of Interest (${secondaries.length}):</div>
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
    document.getElementById('ctx-case-id').innerText = caseId;
    document.getElementById('select-change-case').value = caseId;
    changeActivePerson(personId);
    switchTab('fusion');
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

// 3. EVIDENCE FUSION WORKSPACE
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

            <h4 style="margin: 16px 0 8px 0; font-size: 13px; color: #0284c7;">Concise Investigation Chain:</h4>
            ${data.evidence_chain.map(c => `
                <div style="padding: 10px; background: #ffffff; border: 1px solid #e2e8f0; border-left: 3px solid #2563eb; border-radius: 8px; margin-bottom: 6px; box-shadow: 0 1px 2px rgba(0,0,0,0.04);">
                    <div style="font-size: 11px; font-weight: 700; color: #2563eb;">Step ${c.step_index}: [${c.domain}] ${c.title}</div>
                    <div style="font-size: 12px; margin: 2px 0; color: #0f172a;"><strong>${c.from_entity}</strong> ➔ <strong>${c.to_entity}</strong></div>
                    <div style="font-size: 11px; color: #475569;">${c.details}</div>
                    <span class="badge badge-verified" style="margin-top: 4px;">Ref: ${c.evidence_ref}</span>
                </div>
            `).join('')}
        `;
    } catch (err) {
        console.error(err);
    }
}

// 4. NETWORK GRAPH — TREE VIEW DEFAULT & LAYOUT SWITCHER
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

// 7. RIGHT-SIDE SLIDING PERSON DETAIL DRAWER
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
                        <div style="font-size: 11px; color: #2563eb; font-weight: 700;">${p.role}</div>
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
                    <div style="padding: 10px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; margin-bottom: 6px; font-size: 11px;">
                        <div style="font-weight: 700; color: #0f172a;">${e.id}: ${e.title}</div>
                        <div style="color: #64748b; margin-top: 2px;">Type: ${e.evidence_type} | Source: ${e.source}</div>
                        <span class="badge badge-verified" style="margin-top: 4px;">Hash Verified</span>
                    </div>
                `).join('')}
            `;
        } else {
            content.innerHTML = `<div style="font-size: 12px; color: #64748b;">Displaying ${tabName.toUpperCase()} records scoped to ${p.name}...</div>`;
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
                <div style="font-size: 13px; font-weight: 800; color: #0284c7;">[${r.domain}] ${r.relation}</div>
                <div style="font-size: 12px; color: #0f172a; margin: 4px 0;"><strong>${r.source}</strong> ➔ <strong>${r.target}</strong></div>
                <div style="font-size: 11px; color: #475569;">${r.details}</div>
                <div style="font-size: 11px; color: #64748b; margin-top: 6px; display: flex; gap: 14px;">
                    <div>Calls Logged: <strong style="color: #0f172a;">${r.call_count || 14}</strong></div>
                    <div>First Observed: <strong style="color: #0f172a;">${r.first_observed || '04 Aug 2026'}</strong></div>
                    <div>Last Observed: <strong style="color: #0f172a;">${r.last_observed || '17 Aug 2026'}</strong></div>
                </div>
            </div>

            <h4 style="font-size: 12px; color: #2563eb; margin-bottom: 8px;">Supporting Evidence References (${data.supporting_evidence.length}):</h4>
            ${data.supporting_evidence.map(e => `
                <div style="padding: 8px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; margin-bottom: 6px; font-size: 11px;">
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

// 5. COMMUNICATIONS
async function loadCommunicationsData() {
    try {
        const res = await fetch(`/api/communications?person_id=${currentPersonId}`);
        const data = await res.json();

        document.getElementById('comm-stat-calls').innerText = data.total_calls;
        document.getElementById('comm-stat-msgs').innerText = data.total_messages;
        document.getElementById('comm-stat-contacts').innerText = data.unique_contacts;
        document.getElementById('comm-stat-last').innerText = data.last_contact;

        const container = document.getElementById('comm-contact-tree');
        if (container) {
            container.innerHTML = data.communication_edges.map(c => `
                <div style="padding: 10px; background: #ffffff; border: 1px solid #e2e8f0; border-left: 3px solid #0284c7; border-radius: 8px; margin-bottom: 6px; box-shadow: 0 1px 2px rgba(0,0,0,0.04);" onclick="openRelEvidenceModal('${c.id}')">
                    <div style="font-size: 12px; font-weight: 800; color: #0284c7;">📞 ${c.source} ➔ ${c.target}</div>
                    <div style="font-size: 11px; color: #475569; margin-top: 2px;">${c.details}</div>
                    <span class="badge badge-medium" style="margin-top: 4px;">Temporal Relationship Detected</span>
                </div>
            `).join('');
        }
    } catch (err) {
        console.error(err);
    }
}

// 6. FINANCIAL
async function loadFinancialData() {
    try {
        const res = await fetch(`/api/financial?person_id=${currentPersonId}`);
        const data = await res.json();
        const container = document.getElementById('fin-transactions-list');
        if (container) {
            container.innerHTML = data.financial_edges.map(f => `
                <div style="padding: 10px; background: #ffffff; border: 1px solid #e2e8f0; border-left: 3px solid #16a34a; border-radius: 8px; margin-bottom: 6px; box-shadow: 0 1px 2px rgba(0,0,0,0.04);">
                    <div style="font-size: 12px; font-weight: 800; color: #16a34a;">💳 ${f.source} ➔ ${f.target}</div>
                    <div style="font-size: 11px; color: #475569; margin-top: 2px;">${f.details}</div>
                    <span class="badge badge-high" style="margin-top: 4px;">Hawala Cash Transfer Indicator</span>
                </div>
            `).join('');
        }
    } catch (err) {
        console.error(err);
    }
}

// 7. BLOCKCHAIN
async function loadBlockchainData() {
    try {
        const res = await fetch(`/api/blockchain?person_id=${currentPersonId}`);
        const data = await res.json();
        const container = document.getElementById('blk-list');
        if (container) {
            container.innerHTML = data.blockchain_edges.map(b => `
                <div style="padding: 10px; background: #ffffff; border: 1px solid #e2e8f0; border-left: 3px solid #d97706; border-radius: 8px; margin-bottom: 6px; box-shadow: 0 1px 2px rgba(0,0,0,0.04);">
                    <div style="font-size: 12px; font-weight: 800; color: #d97706;">⛓️ ${b.source} ➔ ${b.target}</div>
                    <div style="font-size: 11px; color: #475569; margin-top: 2px;">${b.details}</div>
                </div>
            `).join('');
        }
    } catch (err) {
        console.error(err);
    }
}

// 8. OSINT
async function loadOSINTData() {
    try {
        const res = await fetch(`/api/osint?person_id=${currentPersonId}`);
        const data = await res.json();
        const container = document.getElementById('osint-list');
        if (container) {
            container.innerHTML = data.osint_edges.map(o => `
                <div style="padding: 10px; background: #ffffff; border: 1px solid #e2e8f0; border-left: 3px solid #7c3aed; border-radius: 8px; margin-bottom: 6px; box-shadow: 0 1px 2px rgba(0,0,0,0.04);">
                    <div style="font-size: 12px; font-weight: 800; color: #7c3aed;">🌐 ${o.source} ➔ ${o.target}</div>
                    <div style="font-size: 11px; color: #475569; margin-top: 2px;">${o.details}</div>
                </div>
            `).join('');
        }
    } catch (err) {
        console.error(err);
    }
}

// 9. CCTV / DVR / NVR (3 SYNTHETIC DEMO VIDEOS)
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
                        <span class="synthetic-banner" style="font-size: 9px;">${v.label}</span>
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

// 10. TIMELINE
async function loadTimelineData() {
    try {
        const res = await fetch(`/api/timeline?case_id=${currentCaseId}`);
        const data = await res.json();
        const container = document.getElementById('timeline-container');
        if (!container) return;

        container.innerHTML = data.events.map(ev => `
            <div class="timeline-item">
                <div style="font-size: 10px; color: #2563eb; font-weight: 700;">[${ev.domain}] ${ev.timestamp}</div>
                <div style="font-size: 12px; font-weight: 700; color: #0f172a; margin: 2px 0;">${ev.title}</div>
                <div style="font-size: 11px; color: #475569;">${ev.details}</div>
            </div>
        `).join('');
    } catch (err) {
        console.error(err);
    }
}

// 11. EVIDENCE
async function loadEvidenceData() {
    try {
        const res = await fetch(`/api/evidence?case_id=${currentCaseId}`);
        const data = await res.json();
        const tbody = document.getElementById('evidence-tbody');
        if (!tbody) return;

        tbody.innerHTML = data.evidence_items.map(e => `
            <tr>
                <td><strong>${e.id}</strong></td>
                <td><span class="badge badge-verified">${e.evidence_type}</span></td>
                <td>${e.title}</td>
                <td>${e.source}</td>
                <td><code style="font-size: 10px; color: #2563eb;">${e.file_hash.substring(0, 14)}...</code></td>
                <td><span class="badge badge-verified">${e.integrity_status}</span></td>
                <td>${e.provenance}</td>
            </tr>
        `).join('');
    } catch (err) {
        console.error(err);
    }
}

// 12. ANALYTICS
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
        if (tbody) {
            tbody.innerHTML = data.blockchain_audit.map(b => `
                <tr>
                    <td>#${b.index}</td>
                    <td>${b.timestamp}</td>
                    <td><strong>${b.action_type}</strong></td>
                    <td>${b.actor}</td>
                    <td><code style="font-size: 10px; color: #2563eb;">${b.block_hash.substring(0, 14)}...</code></td>
                    <td><button class="btn btn-secondary" style="padding: 2px 6px; font-size: 10px;" onclick="simulateBlockTamper(${b.index})">Corrupt Payload</button></td>
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
            body: JSON.stringify({ block_index: blockIndex, field_to_tamper: 'title', tampered_value: '[TAMPERED]' })
        });
        const data = await res.json();
        alert(`🚨 TAMPER SIMULATION EXECUTED ON BLOCK #${blockIndex}!\nAudit Status: ${data.audit_verification.is_valid ? 'VALID' : 'FAILED - TAMPER DETECTED'}`);
        loadAuditData();
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
            alert(`🔍 Search Results for "${query}":\nEntities Found: ${data.matched_nodes.length}\nEvidence Items: ${data.matched_evidence.length}\nRelationships: ${data.matched_relationships.length}`);
        }
    });
}
