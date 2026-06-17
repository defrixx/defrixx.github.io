export default function mermaidIntegration() {
  return {
    name: 'product-security-playbook-mermaid',
    hooks: {
      'astro:config:setup': ({ injectScript }) => {
        injectScript(
          'page',
          `
          import mermaid from 'mermaid';

          function currentTheme() {
            return document.documentElement.dataset.theme === 'dark' ? 'dark' : 'default';
          }

          async function renderMermaid() {
            const diagrams = Array.from(document.querySelectorAll('.mermaid'));
            if (diagrams.length === 0) return;

            mermaid.initialize({
              startOnLoad: false,
              securityLevel: 'strict',
              theme: currentTheme(),
            });

            await mermaid.run({ nodes: diagrams });
          }

          renderMermaid();

          const observer = new MutationObserver(() => {
            renderMermaid();
          });

          observer.observe(document.documentElement, {
            attributes: true,
            attributeFilter: ['data-theme'],
          });
          `
        );
      },
    },
  };
}

