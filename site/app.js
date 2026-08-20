document.addEventListener('click', (event) => {
  const button = event.target.closest('[data-tab]');
  if (!button) return;

  const group = button.dataset.group;
  const target = button.dataset.tab;

  document.querySelectorAll(`[data-group="${group}"]`).forEach((item) => {
    item.classList.toggle('active', item.dataset.tab === target);
  });

  document.querySelectorAll(`[data-panel-group="${group}"]`).forEach((panel) => {
    panel.classList.toggle('active', panel.dataset.panel === target);
  });
});

document.querySelectorAll('[data-year]').forEach((el) => {
  el.textContent = new Date().getFullYear();
});

// Keep the original field-site pages useful as the product grows. New operator
// surfaces are injected into the shared navigation without requiring every
// static page to be rewritten whenever another lab is added.
document.querySelectorAll('.nav-links').forEach((nav) => {
  const links = [...nav.querySelectorAll('a')];
  const hasStudio = links.some((a) => a.getAttribute('href') === 'studio.html');
  const hasRevenue = links.some((a) => a.getAttribute('href') === 'revenue-studio.html');
  const docs = links.find((a) => a.getAttribute('href')?.includes('README.md'));

  const addLink = (href, label) => {
    const a = document.createElement('a');
    a.href = href;
    a.textContent = label;
    if (location.pathname.endsWith(href)) a.classList.add('active');
    if (docs) nav.insertBefore(a, docs); else nav.appendChild(a);
  };

  if (!hasStudio) addLink('studio.html', 'Studio');
  if (!hasRevenue) addLink('revenue-studio.html', 'Revenue Studio');
});
