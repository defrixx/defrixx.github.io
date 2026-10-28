import { defineConfig } from 'astro/config';
import { ExpressiveCodeTheme } from '@expressive-code/core';
import { unified } from '@astrojs/markdown-remark';
import starlight from '@astrojs/starlight';
import rehypeMermaid from './plugins/rehype-mermaid.mjs';
import mermaidIntegration from './plugins/mermaid-integration.mjs';
import thirdPartyNotices from './plugins/third-party-notices.mjs';

const configuredBase = process.env.PUBLIC_SITE_BASE ?? '';

function codeTheme(name, type, bg, fg, accent, muted, border) {
  return new ExpressiveCodeTheme({
    name, type, bg, fg,
    colors: { 'editor.background': bg, 'editor.foreground': fg, 'panel.border': border },
    tokenColors: [
      { scope: ['keyword', 'storage', 'entity.name.function', 'constant', 'support'], settings: { foreground: accent } },
      { scope: ['string'], settings: { foreground: muted } },
      { scope: ['comment'], settings: { foreground: muted, fontStyle: 'italic' } },
    ],
  });
}


export default defineConfig({
  site: 'https://defrixx.github.io',
  ...(configuredBase ? { base: configuredBase } : {}),
  vite: { build: { license: { fileName: 'third-party-licenses.json' } } },
  markdown: {
    processor: unified({ rehypePlugins: [rehypeMermaid] }),
  },
  integrations: [
    mermaidIntegration(),
    starlight({
      disable404Route: true,
      expressiveCode: {
        themes: [
          codeTheme('hub-dark', 'dark', '#202630', '#e2e7ef', '#a3b9ee', '#b1bac9', '#343d4c'),
          codeTheme('hub-light', 'light', '#eceff3', '#202632', '#3659a8', '#576171', '#d5d9e1'),
        ],
        styleOverrides: {
          borderColor: ({ theme }) => theme.colors['panel.border'],
          frames: { editorBackground: ({ theme }) => theme.bg, terminalBackground: ({ theme }) => theme.bg },
        },
      },
      title: 'Product Security Hub',
      description:
        'Practical product security playbooks for architecture review, AppSec, platform security, supply chain, and AI security.',
      defaultLocale: 'en',
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
      social: [
        {
          icon: 'github',
          label: 'GitHub',
          href: 'https://github.com/defrixx/defrixx.github.io',
        },
      ],
      customCss: ['./src/styles/custom.css'],
      components: {
        Header: './src/components/HubHeader.astro',
        PageTitle: './src/components/HubPageTitle.astro',
        Footer: './src/components/HubFooter.astro',
        MobileMenuFooter: './src/components/HubMobileMenuFooter.astro',
      },
      sidebar: [
        { slug: 'hub/tasks/overview', label: 'Сценарии', translations: { en: 'Scenarios' } },
        { slug: 'hub/knowledge/overview', label: 'Библиотека', translations: { en: 'Library' } },
        {
          label: 'Ревью и управление',
          translations: { en: 'Review and Governance' },
          collapsed: true,
          items: [
            { slug: 'review/overview', label: 'Обзор', translations: { en: 'Overview' }, attrs: { class: 'section-guide' } },
            { slug: 'review/architecture/checklist', label: 'Архитектурное ревью', translations: { en: 'Architecture review' } },
            { slug: 'review/threat-modeling/playbook', label: 'Моделирование угроз', translations: { en: 'Threat modeling' } },
            { slug: 'review/release-governance/playbook', label: 'Управление выпуском', translations: { en: 'Release governance' } },
            { slug: 'review/vulnerability-management/playbook', label: 'Управление уязвимостями', translations: { en: 'Vulnerability management' } },
          ],
        },
        {
          label: 'Безопасность приложений',
          translations: { en: 'Application Security' },
          collapsed: true,
          items: [
            { slug: 'application-security/overview', label: 'Обзор', translations: { en: 'Overview' }, attrs: { class: 'section-guide' } },
            {
              label: 'Код, API и доступ',
              translations: { en: 'Code, APIs, and access control' },
              collapsed: true,
              items: [
                { slug: 'application-security/secure-coding/code-review/playbook', label: 'Ревью кода', translations: { en: 'Code review' }, attrs: { class: 'sidebar-topic' } },
                { slug: 'application-security/api/api-security-patterns/playbook', label: 'Безопасность API', translations: { en: 'API security' } },
                { slug: 'application-security/business-logic/business-logic-abuse/playbook', label: 'Бизнес-логика', translations: { en: 'Business logic' } },
                { slug: 'application-security/identity/oidc-oauth/playbook', label: 'OIDC и OAuth', translations: { en: 'OIDC and OAuth' } },
              ],
            },
            {
              label: 'Веб и браузер',
              translations: { en: 'Web and browser' },
              collapsed: true,
              items: [
                { slug: 'application-security/web/browser-security/playbook', label: 'Защита в браузере', translations: { en: 'Browser security' }, attrs: { class: 'sidebar-topic' } },
                { slug: 'application-security/web/owasp-top-10/playbook', label: 'OWASP Top 10', translations: { en: 'OWASP Top 10' } },
              ],
            },
          ],
        },
        {
          label: 'Безопасность платформы',
          translations: { en: 'Platform Security' },
          collapsed: true,
          items: [
            { slug: 'platform-security/overview', label: 'Обзор', translations: { en: 'Overview' }, attrs: { class: 'section-guide' } },
            { slug: 'platform-security/cloud-iam-workload-identity/playbook', label: 'Cloud IAM и доступ Workload', translations: { en: 'Cloud IAM and workload access' } },
            {
              label: 'Kubernetes',
              collapsed: true,
              items: [
                { slug: 'platform-security/kubernetes/cluster-security-review/playbook', label: 'Ревью кластера', translations: { en: 'Cluster review' }, attrs: { class: 'sidebar-topic' } },
                { slug: 'platform-security/kubernetes/pod-security/playbook', label: 'Безопасность Pod', translations: { en: 'Pod security' } },
                { slug: 'platform-security/kubernetes/secrets/playbook', label: 'Секреты Kubernetes', translations: { en: 'Kubernetes secrets' } },
                { slug: 'platform-security/kubernetes/seccomp/checklist', label: 'Проверка seccomp', translations: { en: 'Seccomp checklist' } },
                { slug: 'platform-security/kubernetes/container-escape-capability-abuse/overview', label: 'Выход из контейнера и capabilities', translations: { en: 'Container escape and capabilities' } },
                { slug: 'platform-security/kubernetes/adversarial-validation/playbook', label: 'Проверка защиты от атак', translations: { en: 'Adversarial validation' } },
              ],
            },
            {
              label: 'Управление секретами',
              translations: { en: 'Secrets management' },
              collapsed: true,
              items: [
                { slug: 'platform-security/secrets/vault/playbook', label: 'Секреты в Vault', translations: { en: 'Secrets in Vault' }, attrs: { class: 'sidebar-topic' } },
              ],
            },
          ],
        },
        {
          label: 'Цепочка поставки',
          translations: { en: 'Supply Chain' },
          collapsed: true,
          items: [
            { slug: 'supply-chain/overview', label: 'Обзор', translations: { en: 'Overview' }, attrs: { class: 'section-guide' } },
            { slug: 'supply-chain/ci-cd-security/playbook', label: 'Безопасность CI/CD', translations: { en: 'CI/CD security' } },
            { slug: 'supply-chain/slsa-provenance/overview', label: 'SLSA и происхождение сборок', translations: { en: 'SLSA and build provenance' } },
            { slug: 'supply-chain/container-image-security/playbook', label: 'Контейнерные образы', translations: { en: 'Container images' } },
          ],
        },
        {
          label: 'Безопасность ИИ',
          translations: { en: 'AI Security' },
          collapsed: true,
          items: [
            { slug: 'ai-security/overview', label: 'Обзор', translations: { en: 'Overview' }, attrs: { class: 'section-guide' } },
            {
              label: 'Защита ИИ и типовые угрозы',
              translations: { en: 'AI features and threats' },
              collapsed: true,
              items: [
                { slug: 'ai-security/securing-ai/overview', label: 'Защита функций ИИ', translations: { en: 'Securing AI features' }, attrs: { class: 'sidebar-topic' } },
                { slug: 'ai-security/owasp-llm-top-10/overview', label: 'OWASP LLM Top 10 (2026)', translations: { en: 'OWASP LLM Top 10 (2026)' } },
              ],
            },
            {
              label: 'Агенты и интеграции',
              translations: { en: 'Agents and integrations' },
              collapsed: true,
              items: [
                { slug: 'ai-security/agentic-ai/playbook', label: 'Безопасность агентов', translations: { en: 'Agent security' }, attrs: { class: 'sidebar-topic' } },
                { slug: 'ai-security/mcp-security/playbook', label: 'Безопасность MCP', translations: { en: 'MCP security' } },
              ],
            },
            {
              label: 'Разработка с ИИ',
              translations: { en: 'AI-assisted development' },
              collapsed: true,
              items: [
                { slug: 'ai-security/ai-assisted-development/playbook', label: 'Разработка с ИИ', translations: { en: 'AI-assisted development' }, attrs: { class: 'sidebar-topic' } },
              ],
            },
          ],
        },
        {
          label: 'Скиллы и инструменты',
          translations: { en: 'Skills and Tools' },
          collapsed: true,
          items: [
            {
              slug: 'ai-automation/security-skills/overview',
              label: 'Обзор и установка',
              translations: { en: 'Overview & installation' },
              attrs: { class: 'section-guide' },
            },
            {
              label: 'Скиллы',
              translations: { en: 'Skills' },
              collapsed: true,
              items: [
                { slug: 'ai-automation/security-skills/secure-development/overview', attrs: { class: 'sidebar-topic' } },
                { slug: 'ai-automation/security-skills/security-review/overview' },
                { slug: 'ai-automation/security-skills/sensitive-data-cleanup/overview' },
                { slug: 'ai-automation/security-skills/security-report-triage/overview' },
                { slug: 'ai-automation/security-skills/security-fix-verification/overview' },
              ],
            },
            {
              label: 'Совместная работа скиллов',
              translations: { en: 'Combined workflow' },
              collapsed: true,
              items: [
                { slug: 'ai-automation/security-skills/workflow/overview', attrs: { class: 'sidebar-topic' } },
              ],
            },
            {
              label: 'Инструменты',
              translations: { en: 'Tools' },
              collapsed: true,
              items: [
                { slug: 'ai-automation/prompt-integrity/overview', attrs: { class: 'sidebar-topic' } },
                { slug: 'ai-automation/model-security-eval/overview', attrs: { class: 'sidebar-topic' } },
                { slug: 'ai-automation/prompt-guard/overview', attrs: { class: 'sidebar-topic' } },
              ],
            },
          ],
        },
        {
          label: 'Справочник',
          translations: { en: 'Reference' },
          collapsed: true,
          items: [
            { slug: 'reference/infrastructure-technologies/infrastructure-technologies', label: 'Инфраструктурные технологии', translations: { en: 'Infrastructure technologies' } },
            { slug: 'reference/security-policy-examples/overview', label: 'Примеры политик безопасности', translations: { en: 'Security policy examples' } },
          ],
        },
      ],
    }),
    thirdPartyNotices(),
  ],
});
