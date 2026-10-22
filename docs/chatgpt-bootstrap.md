# Source-controlled ChatGPT Instructions lifecycle (candidate)

One versioned [base and maintenance implementation](../packages/development-governance/tools/chatgpt/README.md)
ships as optional files in the Development Governance flow. Consumers invoke it
from their existing pinned VibeVM slot; there is no copied generator or per-project
export procedure. VibeVM owns dependency resolution and materialization.

Each consumer reviews its small binding plus **custom Markdown**, then checks in
one complete generated Instructions file. Shared Governance's
canonical desired state is [chatgpt/instructions.md](../chatgpt/instructions.md),
with [custom.md](../chatgpt/custom.md) and [binding.json](../chatgpt/binding.json).
The generated source is not proof of installed ChatGPT settings.

The package interface documents check/update, exact owner-export comparison,
optional selected Sources snapshots, content-based stale detection, update, no-op,
unsupported formats and authority limits. The producer convenience entry
`python scripts/project-chatgpt.py` delegates to that same canonical code.

[Task 32 Step 5](task-32/step-5/README.md) records the admitted candidate,
semantic coverage, real exported/installed consumer fixtures and owner handoff.
The independently accepted source for this effort remains frozen separately;
new package and generated content are proposals until accepted. Existing
protocols and topic adoptions are unchanged. A stable navigation URL never
establishes acceptance: each effort must independently establish its exact
accepted revision. An unrelated accepted commit does not change effective Instructions.
Exact accepted-source identities belong to invocation evidence, not a circular
containing-commit pin. There is no ChatGPT projection receipt or ownership gate;
adopting consumers remove their old receipt in the same reviewed adoption PR.
Native VibeVM slot receipts remain intact. Status schema 4 distinguishes content
changes from NO_OP and keeps application conditional on Task scope; generation
alone requires no live Settings action.

The prior [Step 4](task-32/step-4/README.md) schema-1 prototype and its limitations
remain historical at its exact result commit. Its old reproduction commands
need that commit's tool/template; they do not define the new lifecycle interface.

No live ChatGPT Instructions/Sources edits, consumer migration or public package
publication occur here. Real loading, role adherence, spontaneous review depth,
Sources addressability/freshness and repeated model reliability remain unqualified.
