---
title: "Choose an AI Security Document"
description: "Start with the question you need to answer. These documents distinguish AI features within a product, control over agent actions, and the use of AI in engineering work."
sidebar:
  order: 5
---
Start with the question you need to answer. These documents distinguish AI features within a product, control over agent actions, and the use of AI in engineering work.

| Document | Main question | Coverage |
| --- | --- | --- |
| [Securing AI](/en/ai-security/securing-ai/overview/) | How do I secure an AI feature within a product? | Data, models, infrastructure, and the AI feature lifecycle, from defining trust boundaries to verifying controls. Helps organize the overall security program and assign implementation responsibilities. |
| [Agentic AI](/en/ai-security/agentic-ai/playbook/) | How do I control an agent's actions, memory, and permissions? | Action authorization, tools, memory, and agent runtime isolation. Covers approval of sensitive operations, rollback, emergency shutdown, and evidence for reviewing agent behavior. |
| [MCP Security](/en/ai-security/mcp-security/playbook/) | How do I review tool connections through MCP? | MCP server inventory, deployment patterns, authorization, and trust boundaries for tools, resources, and prompts. Includes transport validation, server capability changes, logging, and requests for additional user input. |
| [AI-assisted development](/en/ai-security/ai-assisted-development/playbook/) | How do I use AI securely during development? | Assistant context, sensitive data, generated code, dependencies, and coding-agent permissions. Covers independent change verification, skill use, and evidence before merge and release. |
| [Security Skills](/en/ai-automation/security-skills/overview/) | How do I run a specific supporting workflow? | Selection and installation of instructions for development, security review, or preparing a cleaned copy of materials. Each task describes inputs, the expected report, supporting tools, and result limitations. |

## When a task spans several documents

- For an AI feature within a product, start with Securing AI. Add Agentic AI when the model acts through tools, and MCP Security when connections use MCP.
- For a coding agent, start with AI-assisted development. Continue with Agentic AI to review permissions, memory, and the execution environment, and MCP Security to review MCP connections.
- For a specific engineering task, choose Security Skills. Use the relevant playbook for evaluation criteria; the skill instructions help organize the work.

## Where to find the threat taxonomy

The [OWASP LLM Top 10 overview (2026)](/en/ai-security/owasp-llm-top-10/overview/) explains threat categories and their differences. Use it as shared vocabulary during threat modeling and reviews, then follow the documents above for controls and verification methods.
