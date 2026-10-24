# Agent skills (project)

Cursor loads skills from `.agents/skills/` for everyone who clones this repo. They override global skills with the same name on your machine when you work in this project (see `.cursor/rules/project-agent-skills.mdc`).

| Skill | Role |
| --- | --- |
| `ml-flow` | Orchestrator: understanding → decisions → implement → audit |
| `ml-understanding` | Gate on math/ML understanding before modeling |
| `ml-decision-ledger` | Strict decision log for the university ML project |
| `decision-ledger` | General decision surfacing |
| `implementa` | Parallel implementation of agreed work |
| `ponytail` | Minimal, senior-dev style changes |
| `deep-research`, `find-skills`, `test-driven-development`, … | Shared workflow skills |

Invoke with `/skill-name` in Agent chat or let the agent pick them from context.
