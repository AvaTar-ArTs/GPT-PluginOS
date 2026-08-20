const state = { providers: [], capabilities: [], policies: [], checkpoints: [] };

const $ = (sel, root=document) => root.querySelector(sel);
const $$ = (sel, root=document) => [...root.querySelectorAll(sel)];

async function loadJSON(path){
  const res = await fetch(path, {cache:'no-store'});
  if(!res.ok) throw new Error(`${path}: ${res.status}`);
  return res.json();
}

function healthScore(status){ return status === 'healthy' ? 5 : status === 'degraded' ? 2 : 0; }
function costScore(cost){ return Math.max(0, 5 - Number(cost || 0)); }
function latencyScore(latency){ return Number(latency || 0); }
function normalizeQuality(q){ return Math.max(0, Math.min(5, Number(q || 0) / 2)); }

function eligibleProviders(capabilityId, policy){
  return state.providers.filter(p => {
    if(!p.capabilities.includes(capabilityId)) return false;
    if(policy.constraints?.localOnly && !['local','first_party'].includes(p.kind)) return false;
    if(policy.constraints?.maxCost != null && p.cost > policy.constraints.maxCost) return false;
    if(policy.constraints?.excludeDegraded && p.status !== 'healthy') return false;
    return true;
  });
}

function scoreProvider(provider, policy){
  const w = policy.weights;
  const components = {
    quality: normalizeQuality(provider.quality),
    privacy: Number(provider.privacy || 0),
    latency: latencyScore(provider.latency),
    cost: costScore(provider.cost),
    health: healthScore(provider.status)
  };
  const score = Object.entries(w).reduce((sum,[key,weight]) => sum + (components[key] || 0) * weight, 0);
  return { score, components };
}

function computeRoute(){
  const capId = $('#capability-select').value;
  const policy = state.policies.find(p => p.id === $('#policy-select').value);
  const ranked = eligibleProviders(capId, policy)
    .map(p => ({...p, ...scoreProvider(p, policy)}))
    .sort((a,b) => b.score - a.score || b.quality - a.quality || a.id.localeCompare(b.id));
  renderRoute(capId, policy, ranked);
}

function renderRoute(capId, policy, ranked){
  $('#route-count').textContent = `${ranked.length} eligible`;
  $('#route-results').innerHTML = ranked.length ? ranked.map((p,i)=>`
    <div class="route-row ${i===0?'winner':''}">
      <div class="rank-bubble">${i+1}</div>
      <div><strong>${p.name}</strong><div class="route-meta">${p.kind} · ${p.category} · ${p.status} · risk ${p.risk}</div></div>
      <div class="route-score">${p.score.toFixed(2)}</div>
    </div>`).join('') : `<div class="callout">No provider satisfies the current constraints. A real runtime should return a structured no-route diagnostic rather than silently widening policy.</div>`;
  const winner = ranked[0];
  const lines = [
    `capability: ${capId}`,
    `policy: ${policy.id}`,
    `eligible_providers: ${ranked.length}`,
    `constraints: ${JSON.stringify(policy.constraints || {})}`,
    `weights: ${JSON.stringify(policy.weights)}`,
    ''
  ];
  if(winner){
    lines.push(`selected: ${winner.id}`);
    lines.push(`score: ${winner.score.toFixed(3)}`);
    lines.push(`quality_component: ${winner.components.quality.toFixed(2)}`);
    lines.push(`privacy_component: ${winner.components.privacy.toFixed(2)}`);
    lines.push(`latency_component: ${winner.components.latency.toFixed(2)}`);
    lines.push(`cost_component: ${winner.components.cost.toFixed(2)}`);
    lines.push(`health_component: ${winner.components.health.toFixed(2)}`);
    lines.push('');
    lines.push('authorization: NOT IMPLIED BY SELECTION');
    lines.push(`required_action_class: ${winner.risk}`);
  } else {
    lines.push('selected: null');
    lines.push('diagnostic: no eligible provider under current policy');
  }
  $('#route-explain').textContent = lines.join('\n');
}

function renderCapabilities(){
  $('#capability-select').innerHTML = state.capabilities.map(c => `<option value="${c.id}">${c.label} · ${c.id}</option>`).join('');
  $('#policy-select').innerHTML = state.policies.map(p => `<option value="${p.id}">${p.label}</option>`).join('');
  $('#policy-select').addEventListener('change', updatePolicyCopy);
  updatePolicyCopy();
}
function updatePolicyCopy(){
  const policy = state.policies.find(p => p.id === $('#policy-select').value);
  $('#policy-copy').textContent = policy?.description || '';
}

function renderProviderFilters(){
  const cats = ['all', ...new Set(state.providers.map(p=>p.category))];
  $('#provider-filters').innerHTML = cats.map((c,i)=>`<button class="filter-chip ${i===0?'active':''}" data-filter="${c}">${c}</button>`).join('');
  $$('.filter-chip').forEach(btn => btn.addEventListener('click',()=>{
    $$('.filter-chip').forEach(b=>b.classList.remove('active')); btn.classList.add('active'); renderProviders();
  }));
}

function renderProviders(){
  const q = $('#provider-search').value.trim().toLowerCase();
  const filter = $('.filter-chip.active')?.dataset.filter || 'all';
  const rows = state.providers.filter(p => {
    const matchesFilter = filter === 'all' || p.category === filter;
    const haystack = [p.name,p.id,p.kind,p.category,p.status,p.risk,...p.capabilities].join(' ').toLowerCase();
    return matchesFilter && (!q || haystack.includes(q));
  });
  $('#provider-grid').innerHTML = rows.map(p=>`
    <article class="provider-card">
      <div class="panel-head"><div><h4>${p.name}</h4><div class="route-meta">${p.id} · ${p.kind}</div></div><span class="health ${p.status}">${p.status}</span></div>
      <div class="route-meta">quality ${p.quality} · cost ${p.cost}/4 · privacy ${p.privacy}/5 · latency ${p.latency}/5</div>
      <div class="cap-list">${p.capabilities.map(c=>`<span class="mini-cap">${c}</span>`).join('')}</div>
    </article>`).join('');
}

function evaluateGate(){
  const risk = $('#risk-select').value;
  const approved = $('#human-approved').checked;
  const provenance = $('#provenance-required').checked;
  const explicit = new Set(['publication','deployment','financial','destructive_write']);
  const review = new Set(['code_change']);
  let allow = true, reason = 'Allowed under default demo policy with audit logging.';
  if(explicit.has(risk) && !approved){ allow = false; reason = 'Blocked: this action class requires explicit human approval.'; }
  if(review.has(risk) && !approved){ allow = false; reason = 'Blocked in this prototype: code changes require review/approval before execution.'; }
  if(!provenance && risk !== 'read_only'){ allow = false; reason = 'Blocked: write-sensitive actions require a provenance record in this policy preset.'; }
  const out = $('#gate-output'); out.classList.remove('allow','block'); out.classList.add(allow?'allow':'block');
  out.innerHTML = `<div class="eyebrow">Decision</div><div class="gate-symbol">${allow?'✓':'×'}</div><h3>${allow?'Gate open':'Gate closed'}</h3><p>${reason}</p><div class="route-meta">action class: ${risk}</div>`;
}

function provenanceRecord(){
  const record = {
    schema: 'pluginos.provenance.demo.v1',
    observed_at: new Date().toISOString(),
    intent: $('#prov-intent').value,
    capability: $('#prov-cap').value,
    provider: $('#prov-provider').value,
    policy: $('#prov-policy').value,
    authorization: { status: 'illustrative', note: 'Provider selection does not imply authorization.' },
    input: { asset: $('#prov-input').value },
    output: { asset: $('#prov-output').value },
    source: { surface: 'PluginOS Studio', mode: 'demo' },
    lineage: [$('#prov-input').value, $('#prov-output').value]
  };
  $('#prov-json').textContent = JSON.stringify(record,null,2);
  return record;
}

function renderCheckpoints(){
  $('#checkpoint-timeline').innerHTML = state.checkpoints.map((c,i)=>`
    <div class="checkpoint-item">
      <div class="checkpoint-spine"><div class="checkpoint-dot">${String(i+1).padStart(2,'0')}</div></div>
      <div class="checkpoint-body">
        <div class="checkpoint-stage">${c.stage}</div><h4>${c.title}</h4><p>${c.summary}</p>
        <div class="artifact-tags">${c.artifacts.map(a=>`<span>${a}</span>`).join('')}</div>
        <p class="route-meta"><strong>Next:</strong> ${c.next}</p>
      </div>
    </div>`).join('');
}

function switchView(view){
  $$('.studio-nav-btn').forEach(b=>b.classList.toggle('active', b.dataset.view===view));
  $$('.studio-view').forEach(p=>p.classList.toggle('active', p.dataset.viewPanel===view));
  const titles = {route:'Route Simulator',registry:'Provider Registry',governance:'Governance Lab',provenance:'Provenance Builder',checkpoints:'Evolution Checkpoints'};
  $('#view-title').textContent = titles[view] || 'PluginOS Studio';
}

async function boot(){
  try{
    const [providers, capabilities, policies, checkpoints] = await Promise.all([
      loadJSON('data/providers.json'), loadJSON('data/capabilities.json'), loadJSON('data/policies.json'), loadJSON('data/checkpoints.json')
    ]);
    state.providers = providers.providers; state.capabilities = capabilities.capabilities; state.policies = policies.policies; state.checkpoints = checkpoints.checkpoints;
    renderCapabilities(); renderProviderFilters(); renderProviders(); renderCheckpoints(); provenanceRecord(); computeRoute();
    $('#dataset-status').textContent = `${state.providers.length} providers · ${state.capabilities.length} capabilities · ${state.policies.length} policies`;
  } catch(err){
    $('#dataset-status').textContent = 'Dataset load failed';
    $('#route-explain').textContent = `${err}\n\nServe the site over HTTP, e.g. python -m http.server 8080 --directory site`;
  }
}

$$('.studio-nav-btn').forEach(b=>b.addEventListener('click',()=>switchView(b.dataset.view)));
$('#route-btn').addEventListener('click',computeRoute);
$('#provider-search').addEventListener('input',renderProviders);
$('#gate-btn').addEventListener('click',evaluateGate);
$('#prov-btn').addEventListener('click',provenanceRecord);
$('#copy-prov').addEventListener('click',async()=>{ try{ await navigator.clipboard.writeText($('#prov-json').textContent); $('#copy-prov').textContent='Copied'; setTimeout(()=>$('#copy-prov').textContent='Copy',1200); }catch{} });

boot();
