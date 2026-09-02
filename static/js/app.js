// TRACE FINDERS Intelligence Workstation Application Controller
let currentCaseId = 'TRX-2026-017';
let currentPersonId = 'P-001';
let currentGraphLayout = 'tree-ud';
let currentPersonDrawerId = null;
let currentDrawerTab = 'overview';
let visNetworkInstance = null;
let currentGraphData = null;
let allCameraInventoryData = [];
let currentDVRVideos = [];
let currentSelectedDVR = null;

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

function toggleTheme() {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    const btn = document.getElementById('theme-toggle-btn');
    if (btn) btn.innerText = isDark ? '☀️ Light Mode' : '🌙 Dark Mode';
    if (currentGraphData) renderGraphWithLayout(currentGraphLayout);
}

function toggleSidebar() {
    const sidebar = document.getElementById('app-sidebar');
    if (sidebar) sidebar.classList.toggle('collapsed');
}

function changeActivePerson(personId) {
    currentPersonId = personId;
    
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
                <div style="padding: 12px 0; border-bottom: 1px solid var(--border-color); display: flex; justify-content: space-between; font-size: 13px;">
                    <span>⚡ <strong style="color: var(--text-main);">[${act.time}]</strong> ${act.event}</span>
                    <span class="badge badge-verified">${act.domain}</span>
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
                <div class="card" style="border-left: 4px solid var(--accent-blue);">
                    <div class="card-title">
                        <span>${c.id}: ${c.title} (${c.location})</span>
                        <span class="badge badge-verified">${c.status}</span>
                    </div>

                    <div class="suspect-card" onclick="openPersonDrawer('${primary.id}')" style="cursor: pointer;">
                        <img src="${primary.photo_url}" class="suspect-avatar">
                        <div>
                            <div style="font-size: 16px; font-weight: 800; color: var(--text-main);">${primary.name} <span class="badge badge-high" style="font-size: 10px;">Primary Subject</span></div>
                            <div style="font-size: 13px; color: var(--text-muted); margin: 4px 0;">Age: <strong>${primary.age}</strong> | City: <strong>${primary.city}</strong> | Occupation: <strong>${primary.occupation}</strong></div>
                            <div style="font-size: 13px; color: var(--accent-blue);">📞 ${primary.phone} | ✉️ ${primary.email}</div>
                        </div>
                    </div>

                    <div style="font-size: 12px; font-weight: 800; color: var(--accent-blue); text-transform: uppercase; margin: 12px 0 8px 0;">👥 Connected Subjects & Associates (${secondaries.length}):</div>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 10px; margin-bottom: 12px;">
                        ${secondaries.map(sec => `
                            <div style="padding: 10px; background: var(--bg-card-hover); border: 1px solid var(--border-color); border-radius: 8px; display: flex; gap: 10px; align-items: center; cursor: pointer;" onclick="changeActivePerson('${sec.id}')">
                                <img src="${sec.photo_url}" style="width: 44px; height: 44px; border-radius: 50%; object-fit: cover;">
                                <div>
                                    <div style="font-size: 13px; font-weight: 700; color: var(--text-main);">${sec.name}</div>
                                    <div style="font-size: 11px; color: var(--accent-blue);">${sec.role}</div>
                                </div>
                            </div>
                        `).join('')}
                    </div>

                    <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 12px;">${c.description}</p>
                </div>
            `;
        }).join('');
    } catch (err) {
        console.error(err);
    }
}

// 3. PERSON PROFILE VIEW
async function loadPersonsViewData() {
    const container = document.getElementById('person-profile-card-container');
    if (!container) return;

    try {
        const res = await fetch(`/api/persons/${currentPersonId}`);
        const data = await res.json();
        const p = data.person;

        container.innerHTML = `
            <div class="card">
                <div style="display: flex; gap: 24px; border-bottom: 1px solid var(--border-color); padding-bottom: 20px; margin-bottom: 20px;">
                    <img src="${p.photo_url}" style="width: 100px; height: 100px; border-radius: 14px; object-fit: cover; border: 3px solid var(--accent-blue);">
                    <div>
                        <div style="font-size: 24px; font-weight: 800; color: var(--text-main);">${p.name}</div>
                        <div style="font-size: 15px; font-weight: 700; color: var(--accent-blue); margin: 4px 0;">Role: ${p.role} (ID: ${p.id})</div>
                        <div style="font-size: 13px; color: var(--text-muted); display: flex; gap: 20px; margin-top: 8px;">
                            <div>Case: <strong style="color: var(--text-main);">${currentCaseId}</strong></div>
                            <div>Status: <span class="badge badge-high">${p.status}</span></div>
                            <div>Last Updated: <strong style="color: var(--text-main);">${p.last_updated}</strong></div>
                        </div>
                    </div>
                </div>

                <h4 style="font-size: 15px; color: var(--accent-blue); margin-bottom: 12px;">STRUCTURED IDENTIFIERS (Click identifier to navigate):</h4>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-bottom: 24px; font-size: 13px;">
                    <div style="padding: 12px; background: var(--bg-card-hover); border: 1px solid var(--border-color); border-radius: 8px;">
                        <div style="font-size: 11px; color: var(--text-muted); font-weight: 800;">FULL NAME</div>
                        <div style="font-weight: 700; color: var(--text-main); font-size: 14px;">${p.name}</div>
                    </div>
                    <div style="padding: 12px; background: var(--bg-card-hover); border: 1px solid var(--border-color); border-radius: 8px;">
                        <div style="font-size: 11px; color: var(--text-muted); font-weight: 800;">KNOWN ALIASES</div>
                        <div style="font-weight: 700; color: var(--accent-blue); font-size: 14px;">${p.alias}</div>
                    </div>
                    <div style="padding: 12px; background: var(--bg-card-hover); border: 1px solid var(--border-color); border-radius: 8px;">
                        <div style="font-size: 11px; color: var(--text-muted); font-weight: 800;">AGE & GENDER</div>
                        <div style="font-weight: 700; color: var(--text-main); font-size: 14px;">${p.age} (${p.gender})</div>
                    </div>
                    <div style="padding: 12px; background: var(--bg-card-hover); border: 1px solid var(--border-color); border-radius: 8px;">
                        <div style="font-size: 11px; color: var(--text-muted); font-weight: 800;">OCCUPATION</div>
                        <div style="font-weight: 700; color: var(--text-main); font-size: 14px;">${p.occupation}</div>
                    </div>
                    <div style="padding: 12px; background: var(--bg-card-hover); border: 1px solid var(--border-color); border-radius: 8px;">
                        <div style="font-size: 11px; color: var(--text-muted); font-weight: 800;">ORGANIZATION</div>
                        <div style="font-weight: 700; color: var(--text-main); font-size: 14px;">${p.organization}</div>
                    </div>
                    <div style="padding: 12px; background: var(--bg-card-hover); border: 1px solid var(--border-color); border-radius: 8px; cursor: pointer;" onclick="switchTab('communications')">
                        <div style="font-size: 11px; color: var(--text-muted); font-weight: 800;">PHONE ➔ COMMUNICATION ANALYSIS</div>
                        <div style="font-weight: 700; color: var(--accent-blue); font-size: 14px;">📞 ${p.phone}</div>
                    </div>
                    <div style="padding: 12px; background: var(--bg-card-hover); border: 1px solid var(--border-color); border-radius: 8px;">
                        <div style="font-size: 11px; color: var(--text-muted); font-weight: 800;">EMAIL</div>
                        <div style="font-weight: 700; color: var(--text-main); font-size: 14px;">✉️ ${p.email}</div>
                    </div>
                    <div style="padding: 12px; background: var(--bg-card-hover); border: 1px solid var(--border-color); border-radius: 8px; cursor: pointer;" onclick="switchTab('dvr')">
                        <div style="font-size: 11px; color: var(--text-muted); font-weight: 800;">VEHICLE ➔ VEHICLE INTELLIGENCE</div>
                        <div style="font-weight: 700; color: var(--accent-blue); font-size: 14px;">🚘 ${p.vehicle}</div>
                    </div>
                    <div style="padding: 12px; background: var(--bg-card-hover); border: 1px solid var(--border-color); border-radius: 8px; cursor: pointer;" onclick="switchTab('osint')">
                        <div style="font-size: 11px; color: var(--text-muted); font-weight: 800;">PUBLIC USERNAME ➔ PUBLIC-SOURCE INTEL</div>
                        <div style="font-weight: 700; color: var(--accent-blue); font-size: 14px;">🌐 ${p.social_usernames ? p.social_usernames.twitter || '@user' : '@user'}</div>
                    </div>
                    <div style="padding: 12px; background: var(--bg-card-hover); border: 1px solid var(--border-color); border-radius: 8px; cursor: pointer;" onclick="switchTab('blockchain')">
                        <div style="font-size: 11px; color: var(--text-muted); font-weight: 800;">WALLET ➔ BLOCKCHAIN ANALYSIS</div>
                        <div style="font-weight: 700; color: var(--accent-blue); font-size: 14px;">⛓️ ${p.wallet_address}</div>
                    </div>
                </div>
            </div>
        `;
    } catch (err) {
        console.error(err);
    }
}

// 5. LINK ANALYSIS KNOWLEDGE GRAPH
async function loadGraphData() {
    try {
        const res = await fetch(`/api/graph?case_id=${currentCaseId}&person_id=${currentPersonId}`);
        currentGraphData = await res.json();
        
        if (currentGraphData.header_stats) {
            const hs = currentGraphData.header_stats;
            document.getElementById('graph-header-subject').innerText = hs.subject_name.toUpperCase();
            document.getElementById('graph-header-entities').innerText = hs.entities_count;
            document.getElementById('graph-header-rels').innerText = hs.relationships_count;
            document.getElementById('graph-header-links').innerText = hs.evidence_links_count;
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
    if (visNetworkInstance && currentPersonId) {
        visNetworkInstance.focus(currentPersonId, { scale: 1.2, animation: { duration: 500 } });
    } else {
        renderGraphWithLayout(currentGraphLayout);
    }
}

function zoomGraphIn() {
    if (visNetworkInstance) {
        const currentScale = visNetworkInstance.getScale();
        visNetworkInstance.moveTo({ scale: currentScale * 1.25, animation: { duration: 300 } });
    }
}

function zoomGraphOut() {
    if (visNetworkInstance) {
        const currentScale = visNetworkInstance.getScale();
        visNetworkInstance.moveTo({ scale: currentScale * 0.75, animation: { duration: 300 } });
    }
}

function fitGraphToScreen() {
    if (visNetworkInstance) {
        visNetworkInstance.fit({ animation: { duration: 400 } });
    }
}

function resetGraphLayout() {
    renderGraphWithLayout(currentGraphLayout);
}

function renderGraphWithLayout(layoutType) {
    if (!currentGraphData) return;
    const container = document.getElementById('graph-canvas');
    if (!container) return;

    const isDark = document.body.classList.contains('dark-mode');

    const visNodes = currentGraphData.nodes.map(n => {
        let nodeColor = { background: '#2563eb', border: '#1d4ed8' };
        if (n.id === currentPersonId) {
            nodeColor = { background: '#dc2626', border: '#b91c1c' };
        } else if (n.type === 'PHONE') {
            nodeColor = { background: '#0284c7', border: '#0369a1' };
        } else if (n.type === 'VEHICLE') {
            nodeColor = { background: '#d97706', border: '#b45309' };
        } else if (n.type === 'BANK_ACCOUNT') {
            nodeColor = { background: '#16a34a', border: '#15803d' };
        } else if (n.type === 'WALLET') {
            nodeColor = { background: '#7c3aed', border: '#6d28d9' };
        } else if (n.type === 'ORGANIZATION') {
            nodeColor = { background: '#475569', border: '#334155' };
        }

        return {
            id: n.id,
            label: `${n.label}\n[${n.type}]`,
            shape: n.type === 'PERSON' ? 'dot' : 'square',
            color: nodeColor,
            font: { color: isDark ? '#f8fafc' : '#0f172a', size: 13, strokeWidth: 2, strokeColor: isDark ? '#0b0f19' : '#ffffff', face: 'Inter' },
            level: n.tree_level !== undefined ? n.tree_level : 1,
            nodeType: n.type,
            personId: n.personId
        };
    });

    const visEdges = currentGraphData.edges.map(e => ({
        id: e.id,
        from: e.source,
        to: e.target,
        label: e.relation,
        arrows: 'to',
        color: { color: isDark ? '#60a5fa' : '#2563eb' },
        font: { color: isDark ? '#94a3b8' : '#475569', size: 11, strokeWidth: 2, strokeColor: isDark ? '#0b0f19' : '#ffffff' },
        length: 100,
        evidenceId: e.evidence_id
    }));

    const visData = { nodes: new vis.DataSet(visNodes), edges: new vis.DataSet(visEdges) };

    let layoutConfig = {};
    let physicsConfig = { enabled: false };

    if (layoutType === 'tree-ud') {
        layoutConfig = { hierarchical: { direction: 'UD', sortMethod: 'directed', nodeSpacing: 100, levelSeparation: 110 } };
        physicsConfig = { enabled: false };
    } else if (layoutType === 'hierarchy') {
        layoutConfig = { hierarchical: { direction: 'LR', sortMethod: 'directed', nodeSpacing: 100, levelSeparation: 120 } };
        physicsConfig = { enabled: false };
    } else if (layoutType === 'compact') {
        layoutConfig = { randomSeed: 42 };
        physicsConfig = { barnesHut: { gravitationalConstant: -1000, springLength: 50 } };
    } else {
        layoutConfig = { randomSeed: 42 };
        physicsConfig = { barnesHut: { gravitationalConstant: -1600, springLength: 70 } };
    }

    const options = {
        nodes: { borderWidth: 2 },
        layout: layoutConfig,
        physics: physicsConfig,
        interaction: {
            dragNodes: true,
            dragView: true,
            zoomView: true,
            hover: true,
            multiselect: true,
            selectable: true,
            hoverConnectedEdges: true,
            keyboard: { enabled: true, bindToWindow: false }
        }
    };

    if (visNetworkInstance) visNetworkInstance.destroy();
    visNetworkInstance = new vis.Network(container, visData, options);

    visNetworkInstance.on('selectNode', function(params) {
        const nodeId = params.nodes[0];
        const selectedNode = currentGraphData.nodes.find(n => n.id === nodeId);
        if (!selectedNode) return;

        if (selectedNode.type === 'PERSON') {
            openPersonDrawer(nodeId);
        } else if (selectedNode.type === 'PHONE') {
            switchTab('communications');
        } else if (selectedNode.type === 'VEHICLE') {
            switchTab('dvr');
        } else if (selectedNode.type === 'BANK_ACCOUNT') {
            switchTab('financial');
        } else if (selectedNode.type === 'WALLET') {
            switchTab('blockchain');
        } else if (selectedNode.type === 'ORGANIZATION') {
            switchTab('osint');
        } else if (selectedNode.type === 'EVIDENCE') {
            openEvidenceDetailModal(nodeId.replace('EVIDENCE-', ''));
        }
    });

    visNetworkInstance.on('doubleClick', function(params) {
        if (params.nodes.length > 0) {
            const nodeId = params.nodes[0];
            visNetworkInstance.focus(nodeId, { scale: 1.4, animation: { duration: 400 } });
        }
    });

    visNetworkInstance.on('selectEdge', function(params) {
        if (params.edges.length > 0 && params.nodes.length === 0) {
            const edgeId = params.edges[0];
            openRelEvidenceModal(edgeId);
        }
    });
}

// 10. CCTV / DVR FORENSICS WORKSPACE
async function loadDVRData() {
    try {
        const res = await fetch(`/api/dvr?person_id=${currentPersonId}`);
        const data = await res.json();
        
        allCameraInventoryData = data.camera_inventory || [];
        currentDVRVideos = data.dvr_videos || [];

        const selectP = document.getElementById('select-change-person');
        const pName = selectP ? selectP.options[selectP.selectedIndex].text.split('(')[0].replace(/^[🔴🔵🟢🟡🟣⚠️]\s*/, '').trim() : 'Arjun Sharma';
        
        document.getElementById('dvr-header-subject').innerText = pName.toUpperCase();
        document.getElementById('dvr-person-clips-title').innerText = pName;

        renderCameraInventoryGrid(allCameraInventoryData);
        renderAllCameraEventsTable(data.all_camera_events || []);
        renderDVRVideoGrid(currentDVRVideos);

        if (currentDVRVideos.length > 0) {
            selectDVRVideo(currentDVRVideos[0]);
        } else {
            document.getElementById('dvr-selected-details-panel').innerHTML = `<div style="padding: 10px; color: var(--text-muted);">No associated surveillance events for ${pName} on selected camera.</div>`;
        }

        const camList = document.getElementById('dvr-camera-list');
        if (camList && allCameraInventoryData) {
            camList.innerHTML = allCameraInventoryData.map(c => `
                <div style="padding: 6px 10px; background: var(--bg-card-hover); border: 1px solid var(--border-color); border-radius: 6px; margin-bottom: 6px; cursor: pointer;" onclick="openCameraDetailModal('${c.id}')">
                    <strong style="color: var(--accent-blue);">${c.id}</strong>: ${c.name} (${c.location})
                </div>
            `).join('');
        }

    } catch (err) {
        console.error(err);
    }
}

function renderCameraInventoryGrid(cameras) {
    const grid = document.getElementById('camera-inventory-grid-container');
    if (!grid) return;

    if (cameras.length === 0) {
        grid.innerHTML = `<div style="padding: 16px; color: var(--text-muted); grid-column: 1/-1;">No cameras found matching search or filter parameters.</div>`;
        return;
    }

    grid.innerHTML = cameras.map(c => `
        <div class="camera-card-full">
            <div class="camera-card-thumb">
                <img src="${c.image_url}" alt="${c.name} Stream">
                <div style="position: absolute; top: 8px; left: 8px; background: rgba(0,0,0,0.8); color: #fff; padding: 3px 8px; border-radius: 4px; font-family: monospace; font-size: 11px; font-weight: 800;">● ${c.id}</div>
                <div style="position: absolute; top: 8px; right: 8px; background: ${c.status === 'Active Recording' ? 'rgba(22,163,74,0.9)' : 'rgba(217,119,6,0.9)'}; color: #fff; padding: 3px 8px; border-radius: 4px; font-size: 10px; font-weight: 800;">● ${c.status.toUpperCase()}</div>
                <div style="position: absolute; bottom: 8px; left: 8px; background: rgba(0,0,0,0.75); color: #fff; padding: 2px 6px; border-radius: 4px; font-size: 10px;">${c.location}</div>
            </div>
            <div style="padding: 14px; flex: 1; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="font-size: 14px; font-weight: 800; color: var(--text-main); margin-bottom: 4px;">${c.name}</div>
                    <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 8px;">
                        <div>📍 Location: <strong>${c.location}</strong></div>
                        <div>⏱️ Window: <strong>${c.recording_window}</strong> (${c.date})</div>
                        <div>🕒 Last Event: <strong style="color: var(--accent-blue);">${c.last_event_time}</strong></div>
                    </div>
                    <div style="display: flex; gap: 12px; background: var(--bg-card-hover); padding: 8px 12px; border-radius: 6px; border: 1px solid var(--border-color); font-size: 11px; margin-bottom: 12px;">
                        <div>EVENTS: <strong style="color: var(--accent-blue); font-size: 13px;">${c.events_count}</strong></div>
                        <div>EVIDENCE: <strong style="color: var(--status-green); font-size: 13px;">${c.evidence_links}</strong></div>
                        <div>PERSONS: <strong style="color: var(--text-main); font-size: 13px;">${c.associated_persons_count}</strong></div>
                    </div>
                </div>
                <button class="btn" style="width: 100%; font-size: 12px; padding: 8px;" onclick="openCameraDetailModal('${c.id}')">🔍 OPEN CAMERA</button>
            </div>
        </div>
    `).join('');
}

function filterCameraGrid() {
    const searchVal = (document.getElementById('camera-search-input')?.value || '').toLowerCase();
    const statusVal = document.getElementById('cam-filter-status')?.value || 'ALL';
    const locVal = document.getElementById('cam-filter-location')?.value || 'ALL';
    const typeVal = document.getElementById('cam-filter-type')?.value || 'ALL';

    let filtered = allCameraInventoryData;

    if (searchVal) {
        filtered = filtered.filter(c => c.id.toLowerCase().includes(searchVal) || c.name.toLowerCase().includes(searchVal) || c.location.toLowerCase().includes(searchVal));
    }
    if (statusVal !== 'ALL') {
        filtered = filtered.filter(c => c.status === statusVal);
    }
    if (locVal !== 'ALL') {
        filtered = filtered.filter(c => c.location.toLowerCase().includes(locVal.toLowerCase()));
    }
    if (typeVal !== 'ALL') {
        filtered = filtered.filter(c => c.camera_type.toLowerCase().includes(typeVal.toLowerCase()));
    }

    renderCameraInventoryGrid(filtered);
}

function renderAllCameraEventsTable(events) {
    const tbody = document.getElementById('all-camera-events-tbody');
    if (!tbody) return;

    tbody.innerHTML = events.map(e => `
        <tr>
            <td><strong style="color: var(--accent-blue); font-family: monospace;">${e.time}</strong></td>
            <td><span class="badge badge-verified">${e.camera_id}</span></td>
            <td><strong>${e.event}</strong></td>
            <td>${e.person}</td>
            <td>${e.location}</td>
            <td><button class="btn btn-secondary" style="font-size: 10px; padding: 2px 6px;" onclick="openEvidenceDetailModal('${e.evidence_id}')">Ref: ${e.evidence_id}</button></td>
            <td><span class="badge ${e.status === 'Verified' ? 'badge-verified' : 'badge-medium'}">${e.status}</span></td>
        </tr>
    `).join('');
}

function openCameraDetailModal(camId) {
    const modal = document.getElementById('camera-detail-modal');
    if (!modal) return;

    const cam = allCameraInventoryData.find(c => c.id === camId) || allCameraInventoryData[0];
    if (!cam) return;

    document.getElementById('cam-modal-id').innerText = cam.id;
    document.getElementById('cam-modal-name').innerText = `${cam.name} (${cam.location})`;

    document.getElementById('cam-modal-body').innerHTML = `
        <div style="display: grid; grid-template-columns: 1.2fr 1fr; gap: 20px; margin-bottom: 20px;">
            <div style="background: #000; border-radius: 12px; overflow: hidden; aspect-ratio: 16/9; position: relative;">
                <img src="${cam.image_url}" style="width: 100%; height: 100%; object-fit: cover;">
                <div style="position: absolute; top: 10px; left: 10px; background: rgba(0,0,0,0.8); color: #10b981; padding: 4px 8px; border-radius: 4px; font-family: monospace; font-size: 11px;">● LIVE STREAM | ${cam.id} | ${cam.date}</div>
            </div>
            
            <div style="background: var(--bg-card-hover); border: 1px solid var(--border-color); border-radius: 12px; padding: 16px; font-size: 13px; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="font-size: 12px; font-weight: 800; color: var(--accent-blue); margin-bottom: 8px;">CAMERA METADATA SPECIFICATIONS</div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
                        <div>Status: <span class="badge ${cam.status === 'Active Recording' ? 'badge-verified' : 'badge-medium'}">${cam.status}</span></div>
                        <div>Resolution: <strong>${cam.resolution}</strong></div>
                        <div>Camera Type: <strong>${cam.camera_type}</strong></div>
                        <div>Source: <strong>${cam.source}</strong></div>
                        <div>Storage NVR: <strong>${cam.storage}</strong></div>
                        <div>Retention: <strong>${cam.retention}</strong></div>
                        <div>Window: <strong>${cam.recording_window}</strong></div>
                        <div>Last Activity: <strong style="color: var(--accent-blue);">${cam.last_event_time}</strong></div>
                    </div>
                </div>

                <div style="display: flex; gap: 12px; background: var(--bg-card); padding: 10px; border-radius: 8px; border: 1px solid var(--border-color); margin-top: 12px;">
                    <div>TOTAL EVENTS: <strong style="font-size: 14px; color: var(--accent-blue);">${cam.events_count}</strong></div>
                    <div>EVIDENCE LINKS: <strong style="font-size: 14px; color: var(--status-green);">${cam.evidence_links}</strong></div>
                    <div>PERSONS: <strong style="font-size: 14px; color: var(--text-main);">${cam.associated_persons_count}</strong></div>
                </div>
            </div>
        </div>

        <h4 style="font-size: 15px; color: var(--accent-blue); margin-bottom: 10px;">⏱️ 24-HOUR RECORDING EVENT MARKER TIMELINE (18 AUG 2026):</h4>
        <div style="background: var(--bg-card-hover); padding: 16px; border-radius: 10px; border: 1px solid var(--border-color); margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; font-size: 11px; color: var(--text-muted); font-weight: 800; font-family: monospace; margin-bottom: 8px;">
                <span>00:00 IST</span><span>06:00 IST</span><span>12:00 IST</span><span>18:00 IST</span><span>23:59 IST</span>
            </div>
            <div style="height: 8px; background: var(--border-color); border-radius: 4px; position: relative; margin-bottom: 16px;">
                <div style="position: absolute; left: 34%; top: -4px; width: 16px; height: 16px; border-radius: 50%; background: var(--accent-blue); cursor: pointer;" title="08:14 Person Detection"></div>
                <div style="position: absolute; left: 52%; top: -4px; width: 16px; height: 16px; border-radius: 50%; background: var(--accent-blue); cursor: pointer;" title="12:43 Vehicle Detection"></div>
                <div style="position: absolute; left: 77%; top: -4px; width: 16px; height: 16px; border-radius: 50%; background: var(--status-red); cursor: pointer;" title="18:32 Person Entry"></div>
                <div style="position: absolute; left: 83%; top: -4px; width: 16px; height: 16px; border-radius: 50%; background: var(--status-red); cursor: pointer;" title="20:01 Meeting Event"></div>
                <div style="position: absolute; left: 85%; top: -4px; width: 16px; height: 16px; border-radius: 50%; background: var(--status-red); cursor: pointer;" title="20:26 Vehicle Departure"></div>
            </div>
            <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                <button class="btn btn-secondary" style="font-size: 11px; padding: 4px 10px;" onclick="openEvidenceDetailModal('EV-CCTV-031')">⏱️ 08:14 Person Detection</button>
                <button class="btn btn-secondary" style="font-size: 11px; padding: 4px 10px;" onclick="openEvidenceDetailModal('EV-CCTV-031')">⏱️ 12:43 Vehicle Detection</button>
                <button class="btn btn-secondary" style="font-size: 11px; padding: 4px 10px;" onclick="openEvidenceDetailModal('EV-CCTV-031')">⏱️ 18:32 Person Entry</button>
                <button class="btn btn-secondary" style="font-size: 11px; padding: 4px 10px;" onclick="openEvidenceDetailModal('EV-CCTV-031')">⏱️ 20:01 Meeting Event</button>
                <button class="btn btn-secondary" style="font-size: 11px; padding: 4px 10px;" onclick="openEvidenceDetailModal('EV-CCTV-033')">⏱️ 20:26 Vehicle Departure</button>
            </div>
        </div>

        <div style="display: flex; gap: 10px; justify-content: flex-end;">
            <button class="btn btn-secondary" onclick="alert('Viewing full raw stream playback for ${cam.id}...')">▶ VIEW RECORDINGS</button>
            <button class="btn btn-secondary" onclick="alert('Filtering all events for ${cam.id}...')">📋 VIEW EVENTS</button>
            <button class="btn btn-secondary" onclick="openEvidenceDetailModal('EV-CCTV-031'); closeCameraDetailModal();">📄 VIEW EVIDENCE</button>
            <button class="btn" onclick="switchTab('timeline'); closeCameraDetailModal();">⏱️ VIEW TIMELINE</button>
        </div>
    `;

    modal.style.display = 'flex';
}

function closeCameraDetailModal() {
    const modal = document.getElementById('camera-detail-modal');
    if (modal) modal.style.display = 'none';
}

function renderDVRVideoGrid(videos) {
    const videoGrid = document.getElementById('dvr-video-grid-container');
    if (!videoGrid) return;

    if (videos.length === 0) {
        const selectP = document.getElementById('select-change-person');
        const pName = selectP ? selectP.options[selectP.selectedIndex].text.split('(')[0].replace(/^[🔴🔵🟢🟡🟣⚠️]\s*/, '').trim() : 'selected person';
        videoGrid.innerHTML = `<div style="font-size: 13px; color: var(--text-muted); padding: 16px; grid-column: span 3; background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 10px;">No associated surveillance clips logged for ${pName} on this camera. (Full camera inventory remains active above).</div>`;
        return;
    }

    videoGrid.innerHTML = videos.map((v, idx) => `
        <div class="dvr-card-compact ${currentSelectedDVR && currentSelectedDVR.id === v.id ? 'selected' : ''}" onclick="selectDVRVideoByIdx(${idx})">
            <div class="dvr-card-thumb">
                <img src="${v.video_thumbnail}" alt="CCTV Thumbnail">
                <div style="position: absolute; top: 6px; left: 6px; background: rgba(0,0,0,0.75); color: #fff; padding: 2px 6px; border-radius: 4px; font-size: 10px; font-family: monospace;">● ${v.camera_id}</div>
                <div style="position: absolute; bottom: 6px; right: 6px; background: rgba(37,99,235,0.9); color: #fff; padding: 2px 6px; border-radius: 4px; font-size: 10px; font-weight: 700;">${v.timestamp.split(' ')[2] || ''}</div>
            </div>
            <div style="padding: 10px;">
                <div style="font-size: 13px; font-weight: 800; color: var(--text-main);">${v.event_title}</div>
                <div style="font-size: 11px; color: var(--accent-blue); font-weight: 700; margin: 2px 0;">📍 ${v.location}</div>
                <div style="font-size: 11px; color: var(--text-muted); display: flex; justify-content: space-between; align-items: center; margin-top: 4px;">
                    <span>Ref: <strong style="color: var(--text-main);">${v.evidence_id}</strong></span>
                    <span class="badge ${v.status === 'VERIFIED' ? 'badge-verified' : 'badge-medium'}">${v.status}</span>
                </div>
            </div>
        </div>
    `).join('');
}

function selectDVRVideoByIdx(idx) {
    if (currentDVRVideos[idx]) selectDVRVideo(currentDVRVideos[idx]);
}

function selectDVRVideo(v) {
    currentSelectedDVR = v;

    document.getElementById('dvr-selected-id').innerText = v.evidence_id;
    document.getElementById('dvr-main-img').src = v.video_thumbnail;
    document.getElementById('dvr-overlay-cam').innerText = v.camera_id;
    document.getElementById('dvr-overlay-time').innerText = v.timestamp;

    const detailsPanel = document.getElementById('dvr-selected-details-panel');
    if (detailsPanel) {
        detailsPanel.innerHTML = `
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 8px;">
                <div>Event: <strong style="color: var(--text-main);">${v.event_title}</strong></div>
                <div>Camera: <strong style="color: var(--accent-blue);">${v.camera_name}</strong></div>
                <div>Timestamp: <strong>${v.timestamp}</strong></div>
                <div>Location: <strong>${v.location}</strong></div>
                <div>Persons: <strong style="color: var(--text-main);">${v.suspects_identified.join(', ')}</strong></div>
                <div>Vehicle: <strong style="color: var(--accent-blue);">${v.associated_vehicle}</strong></div>
            </div>
            <div>Description: ${v.description}</div>
        `;
    }

    const linkedBtns = document.getElementById('dvr-linked-evidence-btns');
    if (linkedBtns) {
        linkedBtns.innerHTML = (v.linked_evidence || [v.evidence_id]).map(evId => `
            <button class="btn btn-secondary" style="font-size: 11px; padding: 4px 10px;" onclick="openEvidenceDetailModal('${evId}')">Ref: ${evId}</button>
        `).join('') + `
            <button class="btn" style="font-size: 11px; padding: 4px 10px;" onclick="switchTab('graph')">VIEW GRAPH</button>
        `;
    }

    const relEntities = document.getElementById('dvr-related-entities-list');
    if (relEntities) {
        relEntities.innerHTML = `
            <div style="display: flex; flex-direction: column; gap: 6px;">
                ${v.suspects_identified.map(pName => `
                    <div style="padding: 6px 10px; background: var(--bg-card-hover); border: 1px solid var(--border-color); border-radius: 6px; cursor: pointer;" onclick="switchTab('persons')">
                        👤 PERSON: <strong style="color: var(--accent-blue);">${pName}</strong>
                    </div>
                `).join('')}
                <div style="padding: 6px 10px; background: var(--bg-card-hover); border: 1px solid var(--border-color); border-radius: 6px; cursor: pointer;" onclick="switchTab('dvr')">
                    🚘 VEHICLE: <strong style="color: var(--accent-blue);">${v.associated_vehicle}</strong>
                </div>
                <div style="padding: 6px 10px; background: var(--bg-card-hover); border: 1px solid var(--border-color); border-radius: 6px; cursor: pointer;" onclick="switchTab('communications')">
                    📞 COMMUNICATION: <strong style="color: var(--accent-blue);">${v.comm_ref || 'COM-001'}</strong>
                </div>
                <div style="padding: 6px 10px; background: var(--bg-card-hover); border: 1px solid var(--border-color); border-radius: 6px; cursor: pointer;" onclick="switchTab('financial')">
                    💳 FINANCIAL EVENT: <strong style="color: var(--accent-blue);">${v.fin_ref || 'TXN-88421'}</strong>
                </div>
            </div>
        `;
    }
}

function togglePlay() {
    alert("▶ CCTV Replay initiated for selected surveillance stream segment.");
}

// 6. COMMUNICATION ANALYSIS
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
                <div style="padding: 12px; background: var(--bg-card-hover); border: 1px solid var(--border-color); border-left: 4px solid var(--accent-blue); border-radius: 8px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="font-size: 14px; color: var(--text-main);">${c.name}</strong> (${c.role})
                        <div style="font-size: 12px; color: var(--accent-blue);">📞 ${c.phone}</div>
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

// 7. FINANCIAL INTELLIGENCE LEDGER
async function loadFinancialData() {
    try {
        const res = await fetch(`/api/financial?person_id=${currentPersonId}`);
        const data = await res.json();

        const grid = document.getElementById('fin-accounts-grid');
        if (grid) {
            grid.innerHTML = `
                <div style="padding: 16px; background: var(--bg-card-hover); border: 1px solid var(--border-color); border-radius: 10px;">
                    <div style="font-size: 15px; font-weight: 800; color: var(--status-green);">Account: ${data.account}</div>
                    <div style="font-size: 13px; color: var(--text-muted); margin-top: 4px;">Current Balance: <strong style="color: var(--text-main);">${data.balance}</strong></div>
                </div>
            `;
        }

        const tbody = document.getElementById('fin-transactions-tbody');
        if (tbody && data.transactions) {
            tbody.innerHTML = data.transactions.map(t => `
                <tr>
                    <td>${t.date}</td>
                    <td>${t.time}</td>
                    <td><strong style="color: ${t.direction === 'OUT' ? '#dc2626' : '#16a34a'}; font-size: 14px;">${t.amount}</strong></td>
                    <td><span class="badge ${t.direction === 'OUT' ? 'badge-high' : 'badge-verified'}">${t.direction}</span></td>
                    <td>${t.account}</td>
                    <td><strong>${t.counterparty}</strong></td>
                    <td><code style="color: var(--accent-blue);">${t.reference}</code></td>
                    <td><button class="btn btn-secondary" style="font-size: 11px; padding: 3px 8px;" onclick="openEvidenceDetailModal('${t.evidence_id}')">Ref: ${t.evidence_id}</button></td>
                </tr>
            `).join('');
        }
    } catch (err) {
        console.error(err);
    }
}

// 8. BLOCKCHAIN ANALYSIS
async function loadBlockchainData() {
    try {
        const res = await fetch(`/api/blockchain?person_id=${currentPersonId}`);
        const data = await res.json();

        document.getElementById('blk-person-name').innerText = data.address;

        const summary = document.getElementById('blk-summary');
        if (summary) {
            summary.innerHTML = `
                <div style="font-size: 15px; font-weight: 800; color: var(--status-amber);">Wallet Address: ${data.address} (Ref: ${data.associated_evidence})</div>
                <div style="font-size: 13px; color: var(--text-muted); margin-top: 4px;">Balance: <strong>${data.balance}</strong> | Total Observed Transactions: ${data.incoming + data.outgoing}</div>
            `;
        }

        const tbody = document.getElementById('blk-transactions-tbody');
        if (tbody && data.transactions) {
            tbody.innerHTML = data.transactions.map(t => `
                <tr>
                    <td><code style="color: var(--status-amber);">${t.hash}</code></td>
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

// 9. PUBLIC-SOURCE INTELLIGENCE
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
                <div style="padding: 14px; background: var(--bg-card-hover); border: 1px solid var(--border-color); border-left: 4px solid var(--accent-purple); border-radius: 8px; margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 14px; font-weight: 800; color: var(--text-main);">SOURCE RECORD ${o.id}: ${o.value}</span>
                        <span class="badge badge-verified">Confidence: ${o.confidence}</span>
                    </div>
                    <div style="font-size: 12px; color: var(--text-muted); margin-top: 6px;">Subject: <strong>${o.subject}</strong> | Source: ${o.source} | Observed: ${o.last_observed} | Entity: <strong>${o.entity}</strong> | Location: ${o.location}</div>
                    <button class="btn btn-secondary" style="margin-top: 8px; font-size: 11px; padding: 4px 10px;" onclick="openEvidenceDetailModal('${o.evidence_id}')">View Evidence: ${o.evidence_id}</button>
                </div>
            `).join('');
        }
    } catch (err) {
        console.error(err);
    }
}

// 11. TIMELINE
async function loadTimelineData() {
    try {
        const res = await fetch(`/api/timeline?person_id=${currentPersonId}`);
        const data = await res.json();

        const pRes = await fetch(`/api/persons/${currentPersonId}`);
        const pData = await pRes.json();
        document.getElementById('timeline-person-name').innerText = pData.person.name;

        const container = document.getElementById('timeline-container');
        if (container && data.events) {
            container.innerHTML = data.events.map(ev => `
                <div class="timeline-item" style="cursor: pointer;" onclick="openEvidenceDetailModal('${ev.evidence_id}')">
                    <div style="font-size: 11px; color: var(--accent-blue); font-weight: 700;">[${ev.domain}] ${ev.timestamp}</div>
                    <div style="font-size: 14px; font-weight: 700; color: var(--text-main); margin: 4px 0;">${ev.title}</div>
                    <div style="font-size: 12px; color: var(--text-muted);">Person: <strong>${ev.person}</strong> | Location: ${ev.location} | Details: ${ev.details}</div>
                </div>
            `).join('');
        }
    } catch (err) {
        console.error(err);
    }
}

// 13. ENTITY RESOLUTION INTERFACE
async function loadEntityResolutionData() {
    const container = document.getElementById('entity-resolution-container');
    if (!container) return;

    try {
        const res = await fetch(`/api/persons/P-006`);
        const data = await res.json();
        const cand = data.person;

        container.innerHTML = `
            <div style="padding: 20px; background: var(--bg-card-hover); border: 1px solid var(--border-color); border-radius: 12px; max-width: 650px;">
                <div style="font-size: 16px; font-weight: 800; color: var(--status-amber); margin-bottom: 10px;">POTENTIAL MATCH: ${cand.name} (Candidate ID: ${cand.id})</div>
                <div style="font-size: 13px; color: var(--text-main); margin-bottom: 6px;">Possible match to Primary Subject: <strong>Arjun Sharma (P-001)</strong></div>
                <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 12px;">
                    <div>Signals: <strong>Name similarity</strong>, <strong>Location overlap</strong></div>
                    <div>Match Confidence Score: <span class="badge badge-medium">43%</span></div>
                    <div>Status: <strong style="color: var(--status-amber);">${cand.status}</strong></div>
                </div>
                <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 16px;">${cand.notes}</p>

                <div style="display: flex; gap: 10px;">
                    <button class="btn" style="background: #16a34a;" onclick="actionEntityResolution('CONFIRM')">CONFIRM MATCH</button>
                    <button class="btn" style="background: #dc2626;" onclick="actionEntityResolution('REJECT')">REJECT MATCH</button>
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

// 14. REPORTS (100% PERSON-SCOPED DOSSIER GENERATION)
async function loadReportData() {
    try {
        const res = await fetch(`/api/reports/generate?case_id=${currentCaseId}&person_id=${currentPersonId}`, { method: 'GET' });
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
            <div style="padding: 16px; background: var(--bg-card-hover); border: 1px solid var(--border-color); border-radius: 10px; margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-size: 16px; font-weight: 800; color: var(--accent-blue);">EVIDENCE RECORD ${e.id}</span>
                    <span class="badge badge-verified">${e.evidence_type}</span>
                </div>
                <div style="font-size: 13px; color: var(--text-muted); display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 10px;">
                    <div>CASE: <strong style="color: var(--text-main);">${e.case_id}</strong></div>
                    <div>PERSON ID: <strong style="color: var(--text-main);">${e.personId}</strong></div>
                    <div>SOURCE: <strong>${e.source}</strong></div>
                    <div>ACQUISITION DATE: <strong>${e.acquisition_date}</strong></div>
                    <div>HASH INTEGRITY: <span class="badge badge-verified">SHA-256 Verified</span></div>
                </div>
                <p style="font-size: 13px; color: var(--text-main);"><strong>ANALYTICAL EXTRACTION:</strong> ${e.analyst_notes}</p>
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
                    <div style="font-size: 16px; font-weight: 800; color: var(--text-main);">${p.name}</div>
                    <div style="font-size: 13px; color: var(--accent-blue); font-weight: 700;">Role: ${p.role}</div>
                    <div style="font-size: 12px; color: var(--text-muted); margin-top: 4px;">Age: ${p.age} | City: ${p.city}</div>
                </div>
            </div>

            <div style="font-size: 13px; color: var(--text-muted); margin: 16px 0; display: flex; flex-direction: flex-column; gap: 6px;">
                <div><strong>PHONE:</strong> <span style="color: var(--accent-blue); cursor: pointer;" onclick="changeActivePerson('${p.id}'); switchTab('communications'); closePersonDrawer();">${p.phone}</span></div>
                <div><strong>EMAIL:</strong> ${p.email}</div>
                <div><strong>VEHICLE:</strong> <span style="color: var(--accent-blue); cursor: pointer;" onclick="changeActivePerson('${p.id}'); switchTab('dvr'); closePersonDrawer();">${p.vehicle}</span></div>
                <div><strong>PUBLIC USERNAME:</strong> <span style="color: var(--accent-blue); cursor: pointer;" onclick="changeActivePerson('${p.id}'); switchTab('osint'); closePersonDrawer();">${p.social_usernames ? p.social_usernames.twitter || '@user' : '@user'}</span></div>
                <div><strong>WALLET:</strong> <span style="color: var(--accent-blue); cursor: pointer;" onclick="changeActivePerson('${p.id}'); switchTab('blockchain'); closePersonDrawer();">${p.wallet_address}</span></div>
                <div><strong>NOTES:</strong> ${p.notes}</div>
            </div>
            
            <button class="btn" style="width: 100%; margin-top: 10px;" onclick="changeActivePerson('${p.id}'); closePersonDrawer();">SWITCH WORKSTATION CONTEXT TO ${p.name.toUpperCase()}</button>
        `;
    } catch (err) {
        console.error(err);
    }
}

function openRelEvidenceModal(relId) {
    const modal = document.getElementById('rel-evidence-modal');
    if (modal) modal.style.display = 'flex';
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
