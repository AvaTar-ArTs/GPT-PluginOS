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
