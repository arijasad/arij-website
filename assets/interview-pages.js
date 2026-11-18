(() => {
  const revealHash = () => {
    let id;
    try { id = decodeURIComponent(window.location.hash.slice(1)); }
    catch (_) { return; }
    const target = document.getElementById(id);
    if (!target) return;
    let details = target.closest('details');
    while (details) {
      details.open = true;
      details = details.parentElement?.closest('details');
    }
  };
  revealHash();
  window.addEventListener('hashchange', revealHash);
  const table = document.querySelector('[data-college-table]');
  if (!table) return;
  const search = document.getElementById('college-search');
  const format = document.getElementById('college-format');
  const papers = document.getElementById('papers-only');
  const reset = document.getElementById('reset-colleges');
  const status = document.getElementById('college-count');
  const empty = document.getElementById('no-colleges');
  const entries = Array.from(document.querySelectorAll('[data-college-entry]'));
  const rows = Array.from(table.querySelectorAll('tbody tr'));
  const compact = document.getElementById('compact-colleges');
  const compactEntries = compact ? Array.from(compact.querySelectorAll('[data-college-entry]')) : [];
  const normalise = value => value.toLowerCase().replace(/[’']/g, '').replace(/&/g, 'and').replace(/[^a-z0-9]+/g, ' ').trim();
  const update = () => {
    const words = normalise(search.value).split(/\s+/).filter(Boolean);
    let count = 0;
    for (const row of entries) {
      const name = normalise(row.dataset.college);
      const visible = words.every(word => name.includes(word)) &&
        (!format.value || row.dataset.format === format.value) &&
        (!papers.checked || row.dataset.papers === 'true');
      row.hidden = !visible;
      if (visible) count++;
    }
    status.textContent = `${count} of ${entries.length} colleges shown`;
    empty.hidden = count !== 0;
    table.hidden = rows.every(row => row.hidden);
    if (compact) compact.hidden = compactEntries.every(row => row.hidden);
  };
  search.addEventListener('input', update);
  format.addEventListener('change', update);
  papers.addEventListener('change', update);
  reset.addEventListener('click', () => {
    search.value = '';
    format.value = '';
    papers.checked = false;
    update();
    search.focus();
  });
  document.getElementById('college-tools').hidden = false;
  update();
})();
