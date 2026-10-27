/* Offline handbook diagram view. Renderer settings are owned by the viewer. */
(() => {
  let pending = null;
  let sequence = 0;
  const theme = () => document.documentElement.dataset.theme === 'dark' ? 'dark' : 'default';

  function size(figure, action) {
    const viewport = figure.querySelector('.diagram-viewport');
    const svg = viewport.querySelector('svg');
    if (!svg) return;
    const natural = svg.viewBox.baseVal.width || 800;
    const current = svg.getBoundingClientRect().width;
    const width = action === 'actual' ? natural
      : action === 'in' ? Math.min(current * 1.25, natural * 4)
      : action === 'out' ? Math.max(current / 1.25, Math.min(natural, 160)) : null;
    svg.style.width = width === null ? `min(100%, ${natural}px)` : `${width}px`;
    viewport.classList.toggle('zoomed', width !== null);
    if (width === null) viewport.scrollTo(0, 0);
  }

  async function renderActive() {
      // One render at a time. Re-read the active chapter and theme after each
      // await, so navigation or theme changes during rendering are not lost.
      while (true) {
        const selectedTheme = theme();
        const figure = [...document.querySelectorAll('.chapter.active .diagram')]
          .find(item => item.dataset.renderTheme !== selectedTheme);
        if (!figure) break;
        const source = figure.querySelector('.language-mermaid').textContent;
        const status = figure.querySelector('.diagram-status');
        const details = figure.querySelector('.diagram-source');
        const viewport = figure.querySelector('.diagram-viewport');
        const controls = figure.querySelector('.diagram-tools');
        const alreadyRendered = figure.dataset.rendered === 'true';
        status.hidden = false;
        status.textContent = 'Rendering diagram…';
        // Measure in a visible, off-screen host independent of chapter layout.
        const host = document.createElement('div');
        host.style.cssText = 'position:fixed;left:-10000px;top:0;width:900px;pointer-events:none';
        host.setAttribute('aria-hidden', 'true');
        document.body.append(host);
        try {
          if (/^\s*---/.test(source) || /%%\s*\{/.test(source)) {
            throw new Error('Diagram configuration is disabled');
          }
          if (!globalThis.mermaid) throw new Error('Renderer unavailable');
          mermaid.initialize({
            startOnLoad: false, securityLevel: 'strict', theme: selectedTheme,
            fontFamily: 'system-ui, sans-serif', htmlLabels: false,
            suppressErrorRendering: true, maxTextSize: 50000, maxEdges: 500,
            flowchart: { htmlLabels: false },
          });
          const { svg } = await mermaid.render(`handbook-diagram-${++sequence}`, source, host);
          viewport.innerHTML = svg;
          // No diagram-provided actions or external media in this reading view.
          viewport.querySelectorAll('a').forEach(link => link.replaceWith(...link.childNodes));
          viewport.querySelectorAll('image,foreignObject,script').forEach(node => node.remove());
          viewport.hidden = false;
          controls.hidden = false;
          status.hidden = true;
          if (!alreadyRendered) details.open = false;
          figure.dataset.rendered = 'true';
          size(figure, 'fit');
        } catch (_) {
          viewport.replaceChildren();
          viewport.hidden = true;
          controls.hidden = true;
          status.textContent = 'Diagram unavailable. Check syntax and supported diagram types; configuration directives are disabled. Source is preserved below.';
          details.open = true;
        } finally {
          figure.dataset.renderTheme = selectedTheme;
          host.remove();
        }
      }
  }

  function refresh() {
    if (!pending) pending = renderActive().finally(() => { pending = null; });
    return pending;
  }

  document.addEventListener('click', event => {
    const button = event.target.closest('[data-diagram-action]');
    if (button) size(button.closest('.diagram'), button.dataset.diagramAction);
  });
  window.handbookDiagrams = { refresh };
})();
