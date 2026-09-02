// TRACE-X Intelligence Platform Frontend Application Controller
let selectedPersonFilter = 'ALL';

document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initGlobalSearch();
    loadOverviewData();
});

// Global Person/Suspect Filter Handler
function filterAllModulesByPerson(personId) {
    selectedPersonFilter = personId;
    
    // Update active view
    const activeNav = document.querySelector('.nav-item.active');
    const tabId = activeNav ? activeNav.getAttribute('data-tab') : 'overview';
    switchTab(tabId);
}

// Sidebar Toggle Handler
function toggleSidebar() {
    const sidebar = document.getElementById('app-sidebar');
    if (sidebar) sidebar.classList.toggle('collapsed');
}

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

        container.innerHTML = data.cases.map(c => {
            const primary = c.primary_suspect || {};
            const secondaryList = c.secondary_suspects || [];

            return `
                <div class="card" style="margin-bottom: 20px; border-left: 5px solid ${c.priority === 'HIGH' ? '#dc2626' : '#2563eb'};">
                    <div class="card-title">
                        <span>${c.id}: ${c.title}</span>
                        <span class="badge ${c.priority === 'HIGH' ? 'badge-high' : 'badge-verified'}">${c.priority} PRIORITY</span>
                    </div>

                    <!-- PRIMARY SUSPECT PROFILE CARD WITH INDIAN FACE PHOTO -->
                    <div class="suspect-card" style="background: #f8fafc; border-left: 4px solid #2563eb;">
                        <img src="${primary.avatar_url || 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=300'}" class="suspect-avatar" alt="Primary Suspect">
                        <div>
                            <div style="font-size: 15px; font-weight: 800; color: #0f172a;">${primary.name || c.subject_name} <span class="badge badge-high" style="font-size: 10px;">Primary Suspect</span></div>
                            <div style="font-size: 12px; color: #475569; margin: 2px 0;">Role: <strong>${primary.role || 'Syndicate Lead'}</strong></div>
                            <div style="font-size: 12px; color: #64748b;">📞 Phone: ${primary.phone || 'N/A'} | ✉️ Email: ${primary.email || 'N/A'}</div>
                            <div style="display: flex; gap: 6px; margin-top: 6px; flex-wrap: wrap;">
                                ${Object.entries(primary.social_profiles || {}).map(([platform, handle]) => `
                                    <span class="social-badge">🌐 ${platform.toUpperCase()}: ${handle}</span>
                                `).join('')}
                            </div>
                        </div>
                    </div>

                    <!-- SECONDARY SUSPECTS LIST -->
                    ${secondaryList.length > 0 ? `
                        <div style="margin-top: 10px; margin-bottom: 12px;">
                            <div style="font-size: 11px; font-weight: 800; color: #0284c7; text-transform: uppercase; margin-bottom: 6px;">👥 Secondary Suspects & Co-Conspirators (${secondaryList.length}):</div>
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 10px;">
                                ${secondaryList.map(sec => `
                                    <div style="padding: 10px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; display: flex; gap: 10px; align-items: center;">
                                        <img src="${sec.avatar_url || 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=300'}" style="width: 46px; height: 46px; border-radius: 50%; object-fit: cover;">
                                        <div>
                                            <div style="font-size: 13px; font-weight: 700; color: #0f172a;">${sec.name}</div>
                                            <div style="font-size: 11px; color: #0284c7; font-weight: 600;">${sec.role}</div>
                                            <div style="font-size: 11px; color: #64748b;">${sec.phone || 'N/A'}</div>
                                        </div>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    ` : ''}

                    <p style="font-size: 12px; color: #475569; margin-bottom: 12px;">${c.description}</p>
                    <div style="font-size: 11px; color: #64748b; margin-bottom: 14px; display: flex; gap: 20px; flex-wrap: wrap;">
                        <div>Investigator: <strong style="color: #0f172a;">${c.investigator}</strong></div>
                        <div>Agency: <strong style="color: #0f172a;">${c.agency}</strong></div>
                        <div>Start Date: <strong style="color: #0f172a;">${c.start_date}</strong></div>
                        <div>Status: <strong style="color: #16a34a;">${c.status}</strong></div>
                    </div>
                    <div style="display: flex; gap: 10px;">
                        <button class="btn" onclick="selectActiveCase('${c.id}')">🕸️ Analyze Network Tree Graph</button>
                        <button class="btn btn-secondary" onclick="switchTab('fusion')">🔗 Open Evidence Fusion</button>
                    </div>
                </div>
            `;
        }).join('');
    } catch (err) {
        console.error(err);
    }
}

function selectActiveCase(caseId) {
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
    const priority = document.getElementById('case-input-priority').value;
    const investigator = document.getElementById('case-input-investigator').value.trim();
    const agency = document.getElementById('case-input-agency').value.trim();
    const description = document.getElementById('case-input-desc').value.trim();

    const phone = document.getElementById('case-input-phone').value.trim();
    const email = document.getElementById('case-input-email').value.trim();
    const telegram = document.getElementById('case-input-telegram').value.trim();
    const darkweb = document.getElementById('case-input-darkweb').value.trim();

    const primary_suspect = {
        name: subject_name,
        role: "Primary Suspect",
        avatar_url: "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=300",
        phone: phone,
        email: email,
        social_profiles: {
            telegram: telegram || "@suspect_tg",
            darkweb: darkweb || "dark_alias_01"
        }
    };

    const sec_name = document.getElementById('case-input-sec-name').value.trim();
    const sec_role = document.getElementById('case-input-sec-role').value.trim();
    const sec_phone = document.getElementById('case-input-sec-phone').value.trim();
    const sec_social = document.getElementById('case-input-sec-social').value.trim();

    const secondary_suspects = [];
    if (sec_name) {
        secondary_suspects.push({
            name: sec_name,
            role: sec_role || "Co-Conspirator",
            avatar_url: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=300",
            phone: sec_phone,
            social_profiles: { social: sec_social || "@sec_alias" }
        });
    }

    try {
        const res = await fetch('/api/cases', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, subject_name, investigator, agency, priority, description, primary_suspect, secondary_suspects })
        });
        const data = await res.json();
        if (data.success) {
            alert(`✅ Case Registered Successfully!\n\nCase ID: ${data.case.id}\nPrimary Suspect: ${subject_name}\nSecondary Suspects: ${secondary_suspects.length}\nLogged on Blockchain Evidence Ledger.`);
            closeCreateCaseModal();
            loadInvestigationsData();
            loadOverviewData();
        }
    } catch (err) {
        console.error(err);
        alert('Failed to register case.');
    }
}

// 3. TREE TYPE NETWORK GRAPH WITH COMPACT SHORT LINKS
let visNetworkInstance = null;
let currentGraphData = null;
let currentLayoutType = 'tree-ud'; // 'tree-ud', 'tree-lr', 'force', 'circular'

async function loadGraphData() {
    try {
        const res = await fetch('/api/graph');
        currentGraphData = await res.json();
        renderGraphWithLayout(currentLayoutType);
    } catch (err) {
        console.error('Failed to render graph:', err);
    }
}

function changeGraphLayout(layoutType) {
    currentLayoutType = layoutType;
    document.querySelectorAll('.graph-layout-btn').forEach(btn => btn.classList.remove('active'));
    
    const activeBtn = document.getElementById(`btn-layout-${layoutType}`);
    if (activeBtn) activeBtn.classList.add('active');

    renderGraphWithLayout(layoutType);
}

function renderGraphWithLayout(layoutType) {
    if (!currentGraphData) return;
    const container = document.getElementById('graph-canvas');
    if (!container) return;

    // Filter graph nodes if a specific suspect is selected
    let nodesToRender = currentGraphData.nodes;
    let edgesToRender = currentGraphData.edges;

    if (selectedPersonFilter !== 'ALL') {
        const selectedNode = currentGraphData.nodes.find(n => n.id === selectedPersonFilter);
        if (selectedNode) {
            // Find 1-hop and 2-hop connected nodes
            const connectedEdges = currentGraphData.edges.filter(e => e.source === selectedPersonFilter || e.target === selectedPersonFilter);
            const connectedNodeIds = new Set([selectedPersonFilter]);
            connectedEdges.forEach(e => {
                connectedNodeIds.add(e.source);
                connectedNodeIds.add(e.target);
            });
            nodesToRender = currentGraphData.nodes.filter(n => connectedNodeIds.has(n.id));
            edgesToRender = connectedEdges;
        }
    }

    const visNodes = nodesToRender.map(n => ({
        id: n.id,
        label: `${n.label}\n[${n.type}]`,
        shape: getNodeShape(n.type),
        color: getNodeColor(n.type),
        font: { color: '#0f172a', size: 11, strokeWidth: 2, strokeColor: '#ffffff', face: 'Inter' },
        level: n.tree_level !== undefined ? n.tree_level : 2
    }));

    const visEdges = edgesToRender.map(e => ({
        from: e.source,
        to: e.target,
        label: e.relation,
        arrows: 'to',
        color: { color: getDomainColor(e.domain) },
        font: { color: '#475569', size: 9, strokeWidth: 2, strokeColor: '#ffffff' },
        length: 60 // COMPACT SHORT LINKS
    }));

    const visData = { nodes: new vis.DataSet(visNodes), edges: new vis.DataSet(visEdges) };

    let layoutConfig = {};
    let physicsConfig = { enabled: true };

    if (layoutType === 'tree-ud') {
        // Compact Short-Link Top-Down Tree
        layoutConfig = { hierarchical: { direction: 'UD', sortMethod: 'directed', nodeSpacing: 80, levelSeparation: 90 } };
        physicsConfig = { enabled: false };
    } else if (layoutType === 'tree-lr') {
        // Compact Short-Link Left-Right Tree
        layoutConfig = { hierarchical: { direction: 'LR', sortMethod: 'directed', nodeSpacing: 70, levelSeparation: 110 } };
        physicsConfig = { enabled: false };
    } else if (layoutType === 'circular') {
        layoutConfig = { randomSeed: 42 };
        physicsConfig = { barnesHut: { gravitationalConstant: -1200, centralGravity: 0.4, springLength: 45 } };
    } else {
        // Compact Force-Directed
        layoutConfig = { randomSeed: 100 };
        physicsConfig = { barnesHut: { gravitationalConstant: -1800, springLength: 45 } };
    }

    const options = {
        nodes: { borderWidth: 2 },
        layout: layoutConfig,
        physics: physicsConfig,
        interaction: { hover: true, tooltipDelay: 200 }
    };

    if (visNetworkInstance) visNetworkInstance.destroy();
    visNetworkInstance = new vis.Network(container, visData, options);

    visNetworkInstance.on('selectNode', function(params) {
        const nodeId = params.nodes[0];
        const entity = currentGraphData.nodes.find(n => n.id === nodeId);
        if (entity) showEntityDrawer(entity);
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

function showEntityDrawer(entity) {
    const drawer = document.getElementById('entity-drawer');
    if (!drawer) return;
    drawer.style.display = 'block';
    document.getElementById('drawer-entity-name').innerText = entity.label;
    document.getElementById('drawer-entity-type').innerText = entity.type;
    document.getElementById('drawer-entity-risk').innerText = `${entity.risk_score}/100`;
    document.getElementById('drawer-entity-status').innerText = entity.status;
    document.getElementById('drawer-entity-details').innerText = entity.details;

    const avatarEl = document.getElementById('drawer-entity-avatar');
    if (avatarEl) {
        if (entity.avatar) {
            avatarEl.src = entity.avatar;
            avatarEl.style.display = 'block';
        } else {
            avatarEl.style.display = 'none';
        }
    }
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

        let items = data.evidence_items;
        if (selectedPersonFilter !== 'ALL') {
            items = items.filter(e => e.person_id === selectedPersonFilter || e.case_id === 'TRACE-2026-017');
        }

        tbody.innerHTML = items.map(e => `
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
            let edges = data.communication_edges;
            if (selectedPersonFilter !== 'ALL') {
                const pName = selectedPersonFilter.replace('person_', '').replace('_', ' ');
                edges = edges.filter(c => c.source.toLowerCase().includes(pName) || c.target.toLowerCase().includes(pName) || c.details.toLowerCase().includes(pName));
            }

            container.innerHTML = edges.map(c => `
                <div style="padding: 14px; background: #ffffff; border: 1px solid #e2e8f0; border-left: 4px solid #0284c7; border-radius: 10px; margin-bottom: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">
                    <div style="font-weight: 800; color: #0284c7; font-size: 14px;">📞 ${c.source} ➔ ${c.target}</div>
                    <div style="font-size: 12px; color: #334155; margin-top: 4px; font-weight: 500;">${c.details}</div>
                    <div style="display: flex; gap: 8px; align-items: center; margin-top: 6px;">
                        <span class="badge badge-high">PRE-INCIDENT CALL BURST</span>
                        <span style="font-size: 11px; color: #64748b;">Confidence: ${c.confidence * 100}%</span>
                    </div>
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
            let edges = data.financial_edges;
            if (selectedPersonFilter !== 'ALL') {
                const pName = selectedPersonFilter.replace('person_', '').replace('_', ' ');
                edges = edges.filter(f => f.source.toLowerCase().includes(pName) || f.target.toLowerCase().includes(pName) || f.details.toLowerCase().includes(pName));
            }

            container.innerHTML = edges.map(f => `
                <div style="padding: 14px; background: #ffffff; border: 1px solid #e2e8f0; border-left: 4px solid #16a34a; border-radius: 10px; margin-bottom: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">
                    <div style="font-weight: 800; color: #16a34a; font-size: 14px;">💳 ${f.source} ➔ ${f.target}</div>
                    <div style="font-size: 12px; color: #334155; margin-top: 4px; font-weight: 500;">${f.details}</div>
                    <span class="badge badge-high" style="margin-top: 6px;">HAWALA INDICATOR: Rapid Cash Layering</span>
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
                <div style="padding: 14px; background: #ffffff; border: 1px solid #e2e8f0; border-left: 4px solid #d97706; border-radius: 10px; margin-bottom: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">
                    <div style="font-weight: 800; color: #d97706; font-size: 14px;">⛓️ ${b.source} ➔ ${b.target}</div>
                    <div style="font-size: 12px; color: #334155; margin-top: 4px; font-weight: 500;">${b.details}</div>
                </div>
            `).join('');
        }
    } catch (err) {
        console.error(err);
    }
}

// 9. OSINT Workspace & Suspect Dossiers Loader
async function loadOSINTData() {
    try {
        const resCases = await fetch('/api/cases');
        const dataCases = await resCases.json();
        
        const suspectContainer = document.getElementById('osint-suspects-container');
        if (suspectContainer && dataCases.cases.length > 0) {
            const currentCase = dataCases.cases[0];
            const primary = currentCase.primary_suspect || {};
            const secondaries = currentCase.secondary_suspects || [];

            suspectContainer.innerHTML = `
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px;">
                    <!-- PRIMARY SUSPECT WITH INDIAN FACE PHOTO -->
                    <div class="suspect-card" style="border-left: 5px solid #dc2626;">
                        <img src="${primary.avatar_url || 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=300'}" class="suspect-avatar">
                        <div>
                            <div style="font-size: 15px; font-weight: 800; color: #0f172a;">${primary.name || 'Rahul Sharma'} <span class="badge badge-high" style="font-size: 10px;">Primary Suspect</span></div>
                            <div style="font-size: 12px; color: #0284c7; font-weight: 700; margin: 2px 0;">${primary.role || 'Syndicate Lead'}</div>
                            <div style="font-size: 12px; color: #475569;">📞 ${primary.phone || 'N/A'} | ✉️ ${primary.email || 'N/A'}</div>
                            <div style="display: flex; gap: 6px; margin-top: 8px; flex-wrap: wrap;">
                                ${Object.entries(primary.social_profiles || {}).map(([p, h]) => `<span class="social-badge">🌐 ${p.toUpperCase()}: ${h}</span>`).join('')}
                            </div>
                        </div>
                    </div>

                    <!-- SECONDARY SUSPECTS -->
                    ${secondaries.map(sec => `
                        <div class="suspect-card" style="border-left: 5px solid #0284c7;">
                            <img src="${sec.avatar_url || 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=300'}" class="suspect-avatar" style="border-color: #0284c7;">
                            <div>
                                <div style="font-size: 15px; font-weight: 800; color: #0f172a;">${sec.name} <span class="badge badge-verified" style="font-size: 10px;">Secondary Suspect</span></div>
                                <div style="font-size: 12px; color: #0284c7; font-weight: 700; margin: 2px 0;">${sec.role}</div>
                                <div style="font-size: 12px; color: #475569;">📞 ${sec.phone || 'N/A'} | ✉️ ${sec.email || 'N/A'}</div>
                                <div style="display: flex; gap: 6px; margin-top: 8px; flex-wrap: wrap;">
                                    ${Object.entries(sec.social_profiles || {}).map(([p, h]) => `<span class="social-badge">🌐 ${p.toUpperCase()}: ${h}</span>`).join('')}
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            `;
        }

        const resOsint = await fetch('/api/osint');
        const dataOsint = await resOsint.json();
        const container = document.getElementById('osint-list');
        if (container) {
            container.innerHTML = dataOsint.osint_edges.map(o => `
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

// 10. DVR/NVR Forensics Loader with Realistic Surveillance Video Cards
async function loadDVRData() {
    try {
        const res = await fetch('/api/dvr');
        const data = await res.json();
        
        const videoGrid = document.getElementById('dvr-video-grid-container');
        if (videoGrid && data.dvr_videos) {
            videoGrid.innerHTML = data.dvr_videos.map(v => `
                <div class="dvr-card">
                    <div class="dvr-thumb-wrapper">
                        <img src="${v.video_thumbnail}" class="dvr-thumb-img" alt="CCTV Stream">
                        <div class="dvr-rec-badge">● LIVE STREAM | ${v.camera_id}</div>
                        <div class="dvr-play-overlay" onclick="openCCTVVideoModal('${v.camera_id}', '${v.event_title}', '${v.timestamp}', '${v.anpr_license_plate}', '${v.video_thumbnail}', '${v.description.replace(/'/g, "\\'")}')">▶</div>
                    </div>
                    <div class="dvr-info-body">
                        <div style="font-size: 14px; font-weight: 800; color: #0f172a; margin-bottom: 4px;">${v.event_title}</div>
                        <div style="font-size: 11px; color: #2563eb; font-weight: 700; margin-bottom: 6px;">📍 ${v.location}</div>
                        <div style="font-size: 12px; color: #475569; margin-bottom: 8px;"><strong>Identified Indian Suspects:</strong> ${v.suspects_identified.join(', ')}</div>
                        <div style="display: flex; justify-content: space-between; align-items: center; font-size: 11px; font-family: monospace;">
                            <span style="background: #f1f5f9; padding: 2px 6px; border-radius: 4px;">⏱️ ${v.timestamp}</span>
                            <span class="badge badge-verified">ANPR: ${v.anpr_license_plate}</span>
                        </div>
                    </div>
                </div>
            `).join('');
        }

        const container = document.getElementById('dvr-list');
        if (container) {
            container.innerHTML = data.dvr_edges.map(d => `
                <div style="padding: 12px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; margin-bottom: 8px; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">
                    <div style="font-weight: 700; color: #db2777; font-size: 13px;">📹 ${d.source} ➔ ${d.target}</div>
                    <div style="font-size: 12px; color: #475569; margin-top: 4px;">${d.details}</div>
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
    document.getElementById('cctv-modal-title').innerText = title;
    document.getElementById('cctv-modal-timestamp').innerText = timestamp;
    document.getElementById('cctv-modal-anpr').innerText = `ANPR: ${anpr}`;
    document.getElementById('cctv-modal-img').src = imgUrl;
    document.getElementById('cctv-modal-desc').innerText = desc;
    modal.style.display = 'flex';
}

function closeCCTVVideoModal() {
    const modal = document.getElementById('cctv-video-modal');
    if (modal) modal.style.display = 'none';
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
