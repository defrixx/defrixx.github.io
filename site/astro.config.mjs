import { defineConfig } from 'astro/config';
import { unified } from '@astrojs/markdown-remark';
import starlight from '@astrojs/starlight';
import rehypeMermaid from './plugins/rehype-mermaid.mjs';
import mermaidIntegration from './plugins/mermaid-integration.mjs';

const repository = process.env.GITHUB_REPOSITORY ?? '';
const configuredBase =
  process.env.PUBLIC_SITE_BASE ??
  (repository.endsWith('/defrixx.github.io') ? '' : '/Product-security-playbook');

export default defineConfig({
  site: 'https://defrixx.github.io',
  ...(configuredBase ? { base: configuredBase } : {}),
  markdown: {
    processor: unified({ rehypePlugins: [rehypeMermaid] }),
  },
  integrations: [
    mermaidIntegration(),
    starlight({
      disable404Route: true,
      title: 'Product Security Playbook',
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
          href: 'https://github.com/defrixx/Product-security-playbook',
        },
      ],
      customCss: ['./src/styles/custom.css'],
      sidebar: [
        { slug: '', label: 'Главная', translations: { en: 'Home' } },
        {
          label: 'Ревью и управление',
          translations: { en: 'Review and Governance' },
          items: [
            { slug: 'review/overview', label: 'С чего начать', translations: { en: 'Start here' } },
            { slug: 'review/architecture/checklist', label: 'Архитектурное ревью', translations: { en: 'Architecture review' } },
            { slug: 'review/threat-modeling/playbook', label: 'Моделирование угроз', translations: { en: 'Threat modeling' } },
            { slug: 'review/release-governance/playbook', label: 'Управление выпуском', translations: { en: 'Release governance' } },
            { slug: 'review/vulnerability-management/playbook', label: 'Управление уязвимостями', translations: { en: 'Vulnerability management' } },
          ],
        },
        {
          label: 'Безопасность приложений',
          translations: { en: 'Application Security' },
          items: [
            { slug: 'application-security/overview', label: 'С чего начать', translations: { en: 'Start here' } },
            { slug: 'application-security/secure-coding/code-review/playbook', label: 'Ревью кода', translations: { en: 'Code review' } },
            { slug: 'application-security/api/api-security-patterns/playbook', label: 'Безопасность API', translations: { en: 'API security' } },
            { slug: 'application-security/business-logic/business-logic-abuse/playbook', label: 'Бизнес-логика', translations: { en: 'Business logic' } },
            { slug: 'application-security/identity/oidc-oauth/playbook', label: 'OIDC и OAuth', translations: { en: 'OIDC and OAuth' } },
            { slug: 'application-security/web/browser-security/playbook', label: 'Защита в браузере', translations: { en: 'Browser security' } },
            { slug: 'application-security/web/owasp-top-10/playbook', label: 'OWASP Top 10', translations: { en: 'OWASP Top 10' } },
          ],
        },
        {
          label: 'Безопасность платформы',
          translations: { en: 'Platform Security' },
          items: [
            { slug: 'platform-security/overview', label: 'С чего начать', translations: { en: 'Start here' } },
            {
              label: 'Kubernetes',
              items: [
                { slug: 'platform-security/kubernetes/cluster-security-review/playbook', label: 'Ревью кластера', translations: { en: 'Cluster review' } },
                { slug: 'platform-security/kubernetes/pod-security/playbook', label: 'Безопасность Pod', translations: { en: 'Pod security' } },
                { slug: 'platform-security/kubernetes/secrets/playbook', label: 'Секреты Kubernetes', translations: { en: 'Kubernetes secrets' } },
                { slug: 'platform-security/kubernetes/seccomp/checklist', label: 'Проверка seccomp', translations: { en: 'Seccomp checklist' } },
                { slug: 'platform-security/kubernetes/container-escape-capability-abuse/overview', label: 'Выход из контейнера и capabilities', translations: { en: 'Container escape and capabilities' } },
                { slug: 'platform-security/kubernetes/adversarial-validation/playbook', label: 'Проверка защиты от атак', translations: { en: 'Adversarial validation' } },
              ],
            },
            { slug: 'platform-security/secrets/vault/playbook', label: 'Секреты в Vault', translations: { en: 'Secrets in Vault' } },
          ],
        },
        {
          label: 'Цепочка поставки',
          translations: { en: 'Supply Chain' },
          items: [
            { slug: 'supply-chain/overview', label: 'С чего начать', translations: { en: 'Start here' } },
            { slug: 'supply-chain/slsa-provenance/overview', label: 'SLSA и происхождение сборок', translations: { en: 'SLSA and build provenance' } },
            { slug: 'supply-chain/container-image-security/playbook', label: 'Контейнерные образы', translations: { en: 'Container images' } },
          ],
        },
        {
          label: 'Безопасность ИИ',
          translations: { en: 'AI Security' },
          items: [
            { slug: 'ai-security/overview', label: 'С чего начать', translations: { en: 'Start here' } },
            { slug: 'ai-security/securing-ai/overview', label: 'Защита функций ИИ', translations: { en: 'Securing AI features' } },
            { slug: 'ai-security/owasp-llm-top-10/overview', label: 'OWASP LLM Top 10', translations: { en: 'OWASP LLM Top 10' } },
            { slug: 'ai-security/agentic-ai/playbook', label: 'Безопасность агентов', translations: { en: 'Agent security' } },
            { slug: 'ai-security/ai-assisted-development/playbook', label: 'Разработка с ИИ', translations: { en: 'AI-assisted development' } },
            { slug: 'ai-security/mcp-security/playbook', label: 'Безопасность MCP', translations: { en: 'MCP security' } },
          ],
        },
        {
          label: 'Скиллы для задач безопасности',
          translations: { en: 'Security Skills' },
          items: [
            {
              slug: 'ai-automation/security-skills/overview',
              label: 'Обзор и установка',
              translations: { en: 'Overview & installation' },
            },
            { slug: 'ai-automation/security-skills/secure-development/overview' },
            { slug: 'ai-automation/security-skills/security-review/overview' },
            { slug: 'ai-automation/security-skills/sensitive-data-cleanup/overview' },
          ],
        },
        {
          label: 'Справочник',
          translations: { en: 'Reference' },
          items: [
            { slug: 'reference/infrastructure-technologies/infrastructure-technologies', label: 'Инфраструктурные технологии', translations: { en: 'Infrastructure technologies' } },
          ],
        },
      ],
    }),
  ],
});
