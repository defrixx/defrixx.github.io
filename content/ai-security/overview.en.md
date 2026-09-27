# Choose an AI Security Document

Start with the question you need to answer. These documents distinguish AI features within a product, control over agent actions, and the use of AI in engineering work.

| Document | Main question | Coverage |
| --- | --- | --- |
| [Securing AI](securing-ai/overview.en.md) | How do I secure an AI feature within a product? | The overall security program: data, models, infrastructure, lifecycle, and control verification |
| [Agentic AI](agentic-ai/playbook.en.md) | How do I control an agent's actions, memory, and permissions? | Action authorization, tools, memory, isolation, approvals, rollback, and emergency shutdown |
| [MCP Security](mcp-security/playbook.en.md) | How do I review tool connections through MCP? | Server registry, protocol capabilities, deployment patterns, authorization, and logging |
| [AI-assisted development](ai-assisted-development/playbook.en.md) | How do I use AI securely during development? | Assistant context, generated changes, dependencies, and checks before merge and release |
| [Security Skills](../ai-automation/security-skills/overview.en.md) | How do I run a specific supporting workflow? | Assistant instructions for development, security review, or preparing a cleaned copy of materials |

## When a task spans several documents

- For an AI feature within a product, start with Securing AI. Add Agentic AI when the model acts through tools, and MCP Security when connections use MCP.
- For a coding agent, start with AI-assisted development. Continue with Agentic AI to review permissions, memory, and the execution environment, and MCP Security to review MCP connections.
- For a specific engineering task, choose Security Skills. Use the relevant playbook for evaluation criteria; the skill instructions help organize the work.

## Where to find the threat taxonomy

The [OWASP LLM Top 10 overview (2025)](owasp-llm-top-10/overview.en.md) explains threat categories and their differences. Use it as shared vocabulary during threat modeling and reviews, then follow the documents above for controls and verification methods.
