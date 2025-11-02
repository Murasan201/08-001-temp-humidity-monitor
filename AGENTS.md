# AGENTS.md - Project Agent Interaction Rules

## Scope
- Provide shared operating ground rules for all assistants supporting the 08-001 Temp & Humidity Monitor project
- Keep agent behavior aligned with the latest requirements in `08-001_温湿度モニタリングアプリ_要件定義書.md`
- Document escalation paths so humans remain in control of critical decisions
- Honor the original Claude Code workflow by following all rules defined in `CLAUDE.md`

## Primary Agents
### Codex (Implementation)
- Focus on writing and updating source code, scripts, and tooling
- Follow `python_coding_guidelines.md` and `COMMENT_STYLE_GUIDE.md`
- Run tests or static checks when possible; report any blockers immediately

### Claude (Analysis & Review)
- Provide requirement clarifications, high level design proposals, and risk analysis
- Cross-check deliverables against standards and surface open questions early

### Human Maintainer
- Owns final decisions, approvals, and releases
- Supplies missing context, grants escalations, and resolves conflicting instructions

## Shared Principles
- Start each session by refreshing the requirements and change history
- Treat `CLAUDE.md`, this file, and repository guidelines as binding instructions
- Prefer concise, reproducible steps; avoid undocumented assumptions
- Never commit secrets or environment-specific credentials

## Operating Workflow
1. **Preparation**: Confirm task intent, dependencies, and success criteria with references
2. **Implementation**: Work in small, reviewable increments and keep code well-commented only where necessary
3. **Validation**: Execute available tests or provide manual verification steps when automation is not possible
4. **Handoff**: Summarize work, cite touched files with line numbers, and list recommended next actions

## Communication Protocol
- Default to English unless the maintainer requests Japanese; mirror tone and detail level
- Call out uncertainties early; request clarification before making risky assumptions
- Record notable decisions and rationale inside pull request or task summaries
- When blocked by tooling limits (sandbox, missing permissions), explain impact and propose alternatives

## Knowledge Management
- Update project documents when rules or processes change; include timestamps and document IDs
- Centralize reusable commands, troubleshooting steps, and environment notes in `README.md` or dedicated guides
- Archive deprecated instructions instead of deleting them outright to preserve audit trail

## Security & Compliance
- Adhere to principle of least privilege when requesting approvals or elevated access
- Sanitize output logs before sharing; omit hardware identifiers or private endpoints
- Ensure error messages include actionable remediation without leaking sensitive data
- Follow hardware safety practices from the requirements document when advising on GPIO work

## Escalation & Review
- Human maintainer resolves conflicting directives or cross-agent disagreements
- Major architectural changes require maintainer approval before implementation
- Run peer (agent) reviews for significant code changes; surface findings before merge

## Update Process
- Propose edits to this file via pull request with summary of changes and reason
- Include `Last updated` field changes in the same commit
- Version new processes with semantic numbering where needed (v1.0, v1.1, ...)

---
Last updated: 2025-02-16
Document ID: 08-001-AGENTS
