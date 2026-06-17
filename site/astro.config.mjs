import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import rehypeMermaid from './plugins/rehype-mermaid.mjs';
import mermaidIntegration from './plugins/mermaid-integration.mjs';

export default defineConfig({
  site: 'https://defrixx.github.io',
  base: '/Product-security-playbook',
  markdown: {
    rehypePlugins: [rehypeMermaid],
  },
  integrations: [
    mermaidIntegration(),
    starlight({
      title: 'Product Security Playbook',
      description:
        'Practical product security playbooks for architecture review, AppSec, platform security, supply chain, and AI security.',
      defaultLocale: 'ru',
      locales: {
        ru: {
          label: 'Русский',
          lang: 'ru',
        },
        en: {
          label: 'English',
          lang: 'en',
        },
      },
      editLink: {
        baseUrl: 'https://github.com/defrixx/Product-security-playbook/edit/main/',
      },
      social: {
        github: 'https://github.com/defrixx/Product-security-playbook',
      },
      customCss: ['./src/styles/custom.css'],
      sidebar: [
        {
          label: 'Ревью и управление',
          translations: { en: 'Review and Governance' },
          items: [{ autogenerate: { directory: 'review' } }],
        },
        {
          label: 'Application Security',
          items: [{ autogenerate: { directory: 'application-security' } }],
        },
        {
          label: 'Platform Security',
          items: [{ autogenerate: { directory: 'platform-security' } }],
        },
        {
          label: 'Supply Chain',
          items: [{ autogenerate: { directory: 'supply-chain' } }],
        },
        {
          label: 'AI Security',
          items: [{ autogenerate: { directory: 'ai-security' } }],
        },
        {
          label: 'Справочник',
          translations: { en: 'Reference' },
          items: [{ autogenerate: { directory: 'reference' } }],
        },
      ],
    }),
  ],
});
