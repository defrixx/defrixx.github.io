import { h } from 'hastscript';
import { visit } from 'unist-util-visit';

function textFrom(node) {
  if (!node || !Array.isArray(node.children)) return '';
  return node.children
    .filter((child) => child.type === 'text')
    .map((child) => child.value)
    .join('');
}

export default function rehypeMermaid() {
  return (tree) => {
    visit(tree, 'element', (node, index, parent) => {
      if (!parent || index === undefined || node.tagName !== 'pre') return;

      const code = node.children?.[0];
      if (
        !code ||
        code.type !== 'element' ||
        code.tagName !== 'code' ||
        !Array.isArray(code.properties?.className) ||
        !code.properties.className.includes('language-mermaid')
      ) {
        return;
      }

      parent.children[index] = h(
        'div',
        {
          class: 'mermaid',
          'data-mermaid-source': 'fenced-code',
        },
        textFrom(code)
      );
    });
  };
}

